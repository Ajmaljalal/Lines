from datetime import datetime
import os
from langchain_core.messages import SystemMessage, HumanMessage
from app.utils.llms import Claude_3_5
from app.utils.newsletter_state import NewsletterState
from langchain_core.tools import tool
from app.agents.prompts import newsletter_html_creation_prompt
from tavily import TavilyClient
@tool
def html_content_generation_based_on_user_provided_string_content(email_content_text: str) -> NewsletterState:
    """Generates beautifully styled html content for a newsletter/email based on the given user provided text content.
    Args:
        email_content_text: str
    """

    sys_msg = SystemMessage(content=newsletter_html_creation_prompt)
    human_msg = HumanMessage(content='Generate HTML for a newsletter/email with the following text content: ' + email_content_text)
    
    response = Claude_3_5.invoke(
        [
            sys_msg,    
            human_msg
        ]
    )    
    return NewsletterState(newsletter_html=response)



def html_content_generation_based_on_internet_search(user_query: str) -> NewsletterState:
    """Generates beautifully styled html content for a newsletter/email based on the user query, 
    it searches the internet for the most relevant articles based on the user query.
    Args:
        user_query: str
    """

    now = datetime.now()
    day = now.day
    month = now.month
    year = now.year
    date = f"{month}/{day}/{year}"

    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))  
    response = tavily_client.search(
        query=user_query + "-" + date, 
        search_depth="advanced", 
        max_results=5,
        include_images=True
    )

    articles = response['results']
    if not articles:
        return NewsletterState(newsletter_html="No articles found")
    
    sys_msg = SystemMessage(content=newsletter_html_creation_prompt)
    
    articles_str = str(articles)
    human_msg = HumanMessage(content='Generate HTML for a newsletter/email with the following articles: ' + articles_str)
    
    response = Claude_3_5.invoke(
        [
            sys_msg,    
            human_msg
        ]
    )    
    return NewsletterState(newsletter_html=response)
