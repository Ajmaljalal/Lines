import { ChatAnthropic } from "@langchain/anthropic";
import { ChatOpenAI } from "@langchain/openai";
import { BaseChatModel } from "@langchain/core/language_models/chat_models";

export const Anthropic_3_5_Sonnet: BaseChatModel = new ChatAnthropic({
  model: "claude-3-5-sonnet-20241022",
  temperature: 0.3,
  apiKey: process.env.ANTHROPIC_API_KEY,
});

export const OpenAI_GPT_4o: BaseChatModel = new ChatOpenAI({
  model: "gpt-4o",
  temperature: 0.3,
  apiKey: process.env.OPENAI_API_KEY,
});

export const OpenAI_GPT_4o_Mini: BaseChatModel = new ChatOpenAI({
  model: "gpt-4o-mini",
  temperature: 0.3,
});
