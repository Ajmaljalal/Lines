import logging
import os
from flask import request
from langgraph.graph import StateGraph, MessagesState, START
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode, tools_condition
from .prompts import get_newsletter_creation_prompt
from langgraph.checkpoint.memory import MemorySaver
from tavily import TavilyClient
from datetime import datetime
from dataclasses import dataclass, field

llm = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"), verbose=False)


# logging.basicConfig(level=logging.DEBUG)

# Define our state
@dataclass
class NewsletterState(MessagesState):
    user_input: str = ""
    articles: list = field(default_factory=list)
    newsletter_html: str = ""
    email: str = ""
    date: str = ""
    error: str = ""

# Tool definitions

@tool
def get_current_date() -> NewsletterState:
    """Returns the current date in the format of month/day/year. 
    Always use this date in the search queries to fetch the most relevant articles.
    """
    now = datetime.now()
    day = now.day
    month = now.month
    year = now.year
    return {"date": f"{month}/{day}/{year}"}

@tool
def fetch_news_articles(user_input: str, date: str) -> NewsletterState:
    """Fetches news articles based on the user input and date"""
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = tavily_client.search(query=user_input + "-" + date, search_depth="advanced", max_results=5)
    return {"articles": response['results']}

@tool
def html_generation(state: NewsletterState) -> NewsletterState:
    """Generates styled newsletter html content based on the given articles"""
    # Use OpenAI's API to generate HTML
    sys_prompt = f"""
    - You are a HTML generator for newsletters. 
    - Make it visually appealing and well-structured.
    - You generate the newsletter using table tag and style it with inline styling, Do NOT use css classes or ids for styling,
    - Only return the html, noting else. 
    """

    sys_msg = SystemMessage(content=sys_prompt)
    # Convert the list of articles to a string
    articles_str = ', '.join(str(article) for article in state["articles"])
    human_msg = HumanMessage(content='Generate HTML for a newsletter with the following articles: ' + articles_str)
    
    response = llm.invoke(
        [
            sys_msg,
            human_msg
        ]
    )    
    return {"newsletter_html": response, "iteration": state.get("iteration", 0) + 1}

# @tool
# def validate_html_newsletter_format(state: NewsletterState) -> NewsletterState:
#     """Checks if the HTML is valid newsletter HTML with the correct table tags and styling, removing any extra text before and after the <table> tags."""
#     html = state["newsletter_html"]

#     # Find the start and end of the <table> tags
#     table_start = html.find("<table")
#     table_end = html.rfind("</table>") + len("</table>")

#     if table_start != -1 and table_end != -1:
#         # Extract the content within the <table> tags
#         html = html[table_start:table_end]
#     else:
#         state["error"] = "Invalid HTML format: fix the html with the correct table tags and styling."
#         return state
#     return {"newsletter_html": html, "iteration": state.get("iteration", 0) + 1}

# Create LLM and bind tools
llm_with_tools = llm.bind_tools([fetch_news_articles, get_current_date, html_generation])

# System message
system_prompt = get_newsletter_creation_prompt()
sys_msg = SystemMessage(content=system_prompt)

# Node definition
def assistant(state: NewsletterState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

# Create the graph
workflow = StateGraph(NewsletterState)

# Add nodes
workflow.add_node("assistant", assistant)
workflow.add_node("tools", ToolNode([fetch_news_articles, get_current_date, html_generation]))

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

def run_newsletter_creator(user_input, thread_id):
    config = {"configurable": {"thread_id": thread_id}}
    messages = [HumanMessage(content=user_input)]
    
    try:
        result = newsletter_creator_agent.invoke({"messages": messages, "user_input": user_input}, config)
        
        for m in result['messages']:
            m.pretty_print()

        return result.get("messages", [])
    except Exception as e:
        logging.error(f"Exception during run_newsletter_creator: {str(e)}")
        raise
