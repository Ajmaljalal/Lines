import { HumanMessage, SystemMessage } from "@langchain/core/messages";
import { Anthropic_3_5_Sonnet, OpenAI_GPT_4o } from "./llms";
import { BaseMessage } from "@langchain/core/messages";
import { StringOutputParser } from "@langchain/core/output_parsers";
import { createInterface } from 'readline';
import { promisify } from 'util';
import { PlannerPrompt } from "./prompts/system_prompts";

// Remove warning logs
process.removeAllListeners("warning");


export enum PlanStatus {
  IN_PROGRESS = "in_progress",
  COMPLETED = "completed",
  NOT_STARTED = "not_started",
}

export const PlanTemplate = {
  "newsletter_plan": {
    "get_topic_step": {
      "required": true,
      "main_topic": "",
      "topic_confirmed_by_user": false,
      "status": PlanStatus.NOT_STARTED,
    },
    "generate_sections_step": {
      "required": true,
      "sections": [],
      "sections_confirmed_by_user": false,
      "status": PlanStatus.NOT_STARTED,
    },
    "draft_newsletter_content_step": {
      "required": true,
      "newsletter_draft": "",
      "newsletter_draft_confirmed_by_user": false,
      "status": PlanStatus.NOT_STARTED,
    },
    "generate_html_content_step": {
      "required": true,
      "html_content": "",
      "html_content_confirmed_by_user": false,
      "status": PlanStatus.NOT_STARTED,
    },
    "modify_newsletter_html_content_step": {
      "final_html_content": "",
      "final_html_content_confirmed_by_user": false,
      "status": PlanStatus.NOT_STARTED,
    },
    "get_recipient_list_step": {
      "required": true,
      "subscriber_list": [],
      "excluded_emails": [],
      "subscriber_list_confirmed_by_user": false,
      "status": PlanStatus.NOT_STARTED,
    },
    "schedule_step": {
      "send_date": "",
      "send_time": "",
      "send_date_confirmed_by_user": false,
      "status": PlanStatus.NOT_STARTED,
    }
  }
}

const readline = createInterface({
  input: process.stdin,
  output: process.stdout
});

const question = (query: string): Promise<string> => {
  return new Promise((resolve) => {
    readline.question(query, resolve);
  });
};

async function processNewsletterPlan(plan: typeof PlanTemplate.newsletter_plan) {
  const llm = Anthropic_3_5_Sonnet;

  while (Object.values(plan).some(step => step.status !== PlanStatus.COMPLETED)) {
    try {
      console.log("\n--- Starting new iteration ---");

      // Get next question from LLM
      console.log("Getting next question from LLM...");
      const nextQuestionResponse = await llm.invoke([
        new SystemMessage("You are a newsletter planning assistant. Review the current plan state and generate the next appropriate question. Focus on incomplete steps."),
        new HumanMessage(`Current plan state: ${JSON.stringify(plan, null, 2)}\n\nWhat should be the next question to ask the user?`)
      ]);

      const nextQuestion = await new StringOutputParser().invoke(nextQuestionResponse);
      console.log("Generated question:", nextQuestion);

      // Ask user the question and get their answer
      const userAnswer = await question(`${nextQuestion}: `);
      console.log("User answer received:", userAnswer);

      if (userAnswer.trim() === '') {
        console.log("No answer provided, please try again.");
        continue;
      }

      // Update plan based on user's answer
      console.log("Requesting plan update from LLM...");
      const updatedPlanResponse = await llm.invoke([
        new SystemMessage(`You are a newsletter planning assistant that MUST respond with valid JSON only.
Your task is to update the newsletter plan based on the user's answer.
IMPORTANT:
1. Return ONLY a valid JSON object matching the exact structure of the current plan.
2. Do NOT include any Markdown syntax, such as code blocks or backticks.
3. Do NOT include any additional text, explanations, or comments.
4. If you are unsure, return the current plan unchanged.`),
        new HumanMessage(`
Current plan: ${JSON.stringify(plan, null, 2)}
Question asked: ${nextQuestion}
User's answer: ${userAnswer}

Return the updated plan as a JSON object. Update the relevant fields and status based on the user's answer.
The response must be valid JSON that matches the exact structure of the current plan.`)
      ]);

      console.log("Received response from LLM");
      let updatedPlanString = await new StringOutputParser().invoke(updatedPlanResponse);
      console.log("\nDebug - Raw LLM Response:", updatedPlanString);

      // Attempt to extract JSON from code block
      const extractedJSON = extractJSON(updatedPlanString);
      if (extractedJSON) {
        updatedPlanString = extractedJSON;
      } else {
        // If no code block is found, proceed with the original string
        updatedPlanString = updatedPlanString.trim();
      }

      let updatedPlan;
      try {
        updatedPlan = JSON.parse(updatedPlanString);
        console.log("Successfully parsed JSON response");
      } catch (parseError) {
        console.error("Failed to parse LLM response as JSON:", parseError);
        console.error("Raw response:", updatedPlanString);
        continue;
      }

      // Validate the structure before updating
      if (!validatePlanStructure(updatedPlan)) {
        console.error("Invalid plan structure received");
        continue;
      }

      // Update the plan
      Object.assign(plan, updatedPlan);
      console.log("\nPlan updated successfully!");
      console.log("Current plan state:", JSON.stringify(plan, null, 2));

    } catch (error) {
      console.error("Error occurred during processing:");
      if (error instanceof Error) {
        console.error("Error message:", error.message);
      } else if (typeof error === 'string') {
        console.error("Error string:", error);
      } else {
        console.error("Unknown error type:", error);
      }
      // Add a small delay before continuing to prevent rapid loops
      await new Promise(resolve => setTimeout(resolve, 1000));
      continue;
    }
  }

  return plan;
}

// Add this helper function to validate the plan structure
function validatePlanStructure(plan: any): boolean {
  const requiredKeys = [
    'get_topic_step',
    'generate_sections_step',
    'draft_newsletter_content_step',
    'generate_html_content_step',
    'modify_newsletter_html_content_step',
    'get_recipient_list_step',
    'schedule_step',
  ];

  for (const key of requiredKeys) {
    if (!plan[key]) {
      console.error(`Missing required key: ${key}`);
      return false;
    }
  }

  return true;
}

async function runNewsletterPlanner() {
  try {
    const plan = structuredClone(PlanTemplate.newsletter_plan);
    const updatedPlan = await processNewsletterPlan(plan);
    console.log("\nFinal Newsletter Plan:", JSON.stringify(updatedPlan, null, 2));
  } catch (error) {
    console.error("Error Happened here:", error);
  } finally {
    readline.close();
  }
}

runNewsletterPlanner();

/**
 * Extracts JSON string from a Markdown code block.
 * @param input - The raw string containing JSON within a code block.
 * @returns The extracted JSON string or null if extraction fails.
 */
function extractJSON(input: string): string | null {
  const codeBlockRegex = /```json\s*([\s\S]*?)```/;
  const match = input.match(codeBlockRegex);
  if (match && match[1]) {
    return match[1].trim();
  }
  return null;
}
