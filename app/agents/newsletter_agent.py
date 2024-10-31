import logging
from langgraph.graph import StateGraph, START
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import ToolNode, tools_condition

from app.prompts.prompts import newsletter_agent_system_prompt
# from app.tools.fetch_news_articles import fetch_news_articles
from app.tools.html_content_generator import generate_newsletter_based_on_email_content, generate_newsletter_based_on_topic_or_inquiry
from app.tools.html_content_updates import html_content_updates
from app.tools.send_email import send_email
from app.utils.llms import OpenAI_GPT4O
from app.utils.newsletter_state import NewsletterState

from langgraph.checkpoint.memory import MemorySaver

# from langchain_anthropic import ChatAnthropic


# Set specific loggers to ERROR/CRITICAL
# loggers = [
#     'httpx',
#     'httpcore',
#     'werkzeug',
#     'openai',
#     'python_http_client',
#     'flask',
#     'urllib3'
# ]

# for logger_name in loggers:
#     logger = logging.getLogger(logger_name)
#     logger.setLevel(logging.ERROR) 


# Create LLM and bind tools
llm_with_tools = OpenAI_GPT4O.bind_tools([generate_newsletter_based_on_topic_or_inquiry, generate_newsletter_based_on_email_content, html_content_updates, send_email])

# System message
sys_msg = SystemMessage(content=newsletter_agent_system_prompt)

# Node definition
def assistant(state: NewsletterState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

# Create the graph
workflow = StateGraph(NewsletterState)

# Add nodes
workflow.add_node("assistant", assistant)
workflow.add_node("tools", ToolNode([generate_newsletter_based_on_topic_or_inquiry, generate_newsletter_based_on_email_content, html_content_updates, send_email]))

# Add edges
workflow.add_edge(START, "assistant")
workflow.add_conditional_edges(
    "assistant",
    tools_condition,
)
workflow.add_edge("tools", "assistant")

memory = MemorySaver()

# Compile the graph
newsletter_creator_agent = workflow.compile(checkpointer=memory)

# Run the newsletter creator agent
def run_newsletter_creator(user_input, thread_id):
    config = {"configurable": {"thread_id": thread_id}, 
              "recursion_limit": 100}
    messages = [HumanMessage(content=user_input)]
    
    try:
        result = newsletter_creator_agent.invoke({"messages": messages, "user_input": user_input}, config)
        for m in result.get("messages", []):
            m.pretty_print()

        return result.get("messages", [])
    except Exception as e:
        logging.error(f"Exception during run_newsletter_creator: {str(e)}")
        raise
