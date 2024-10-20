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
from typing import Dict, Any
from datetime import datetime


# logging.basicConfig(level=logging.DEBUG)

# Define our state
class NewsletterState(MessagesState):
    user_input: str
    articles: list
    newsletter_content: str
    email: str
    date: str # in the format of month/day/year

# Tool definitions

@tool
def get_current_date():
    """Returns the current date in the format of month/day/year. Always use this date in the search queries to fetch the most relevant articles."""
    now = datetime.now()
    day = now.day
    month = now.month
    year = now.year
    return f"{month}/{day}/{year}"

@tool
def fetch_news_articles(user_input: str, date: str):
    """Fetches news articles based on the user input and date"""
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = tavily_client.search(query=user_input + "-" + date, search_depth="advanced", max_results=2)
    return {"articles": response['results']}

@tool
def generate_newsletter_html_content(articles: list):
    """Generates styled newsletter html content based on the given articles"""
    html_content = """
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            .article {
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 20px;
            }
            .article h2 {
                color: #2c3e50;
                margin-top: 0;
            }
            .article a {
                color: #3498db;
                text-decoration: none;
            }
            .article a:hover {
                text-decoration: underline;
            }
            .article img {
                max-width: 100%;
                height: auto;
                margin: 10px 0;
            }
            .source {
                font-style: italic;
                color: #7f8c8d;
            }
        </style>
    </head>
    <body>
        <h1>Your Personalized Newsletter</h1>
    """
    
    for article in articles:
        html_content += f"""
        <div class="article">
            <h2><a href="{article.get('url', '#')}">{article.get('title', 'No Title')}</a></h2>
            <p>{article.get('content', 'No content available.')}</p>
            {f'<img src="{article["image"]}" alt="{article.get("title", "Article image")}" />' if article.get('image') else ''}
            <p class="source">Source: {article.get('source', 'Unknown')}</p>
        </div>
        """
    
    html_content += "</body></html>"
    return {"newsletter_content": html_content}

# @tool
# def generate_newsletter_content( state: NewsletterState):
#     """
#     Generates newsletter content based on the given articles and style.
#     It will generate html content with the articles that can be rendered in an email
#     It will also include a summary of the articles and a call to action for the user
#     """
#     return {"newsletter_content": "Generated newsletter content"}

# @tool
# def send_newsletter(state: NewsletterState):
#     """Sends the newsletter to the specified email address"""
#     # Placeholder implementation
#     return f"Newsletter sent to {state.email}"

# Create LLM and bind tools
llm = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"), verbose=False)
llm_with_tools = llm.bind_tools([fetch_news_articles, get_current_date, generate_newsletter_html_content])

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
workflow.add_node("tools", ToolNode([fetch_news_articles, get_current_date, generate_newsletter_html_content]))

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
