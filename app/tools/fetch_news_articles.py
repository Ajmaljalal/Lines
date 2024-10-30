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
    day = now.day
    month = now.month
    year = now.year
    date = f"{month}/{day}/{year}"

    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = tavily_client.search(
        query=user_input + "-" + date, 
        search_depth="advanced", 
        max_results=5,
        include_images=True
    )
    return NewsletterState(articles=response['results'])