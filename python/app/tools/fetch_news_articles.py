from datetime import datetime
from langchain_core.tools import tool
from tavily import TavilyClient
import os
from app.utils.newsletter_state import NewsletterState
@tool 
def fetch_news_articles(user_input: str) -> NewsletterState:
    """Fetches news articles based on the user input and date
    Args:
        user_input: str
        date: str (format: month/day/year)
    """

    now = datetime.now()
    formatted_date = now.strftime("%m/%d/%Y")

    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = tavily_client.search(
        query=user_input + "-" + formatted_date, 
        search_depth="advanced", 
        max_results=5,
        include_images=True
    )
    return NewsletterState(articles=response['results'])