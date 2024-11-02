from datetime import datetime
import os
from langchain_core.messages import SystemMessage, HumanMessage
from app.utils.llms import Claude_3_5
from app.utils.newsletter_state import NewsletterState
from langchain_core.tools import tool
from app.prompts.prompts import newsletter_html_creation_prompt
from tavily import TavilyClient

@tool
def generate_newsletter_based_on_topic_or_inquiry(topic: str) -> NewsletterState:
    """Generates beautifully styled html content for a newsletter/email based on a specific topic provided by the user
    Args:
        topic: str (the topic or subject to generate the newsletter about)
    """
    sys_msg = SystemMessage(content=newsletter_html_creation_prompt)
    
    now = datetime.now()
    formatted_date = now.strftime("%m/%d/%Y")

    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY")) 
    response = tavily_client.search(
        query=f"{topic} -{formatted_date}", 
        search_depth="advanced", 
        max_results=5,
        include_images=True
    )
    articles = response['results']
    
    human_msg = HumanMessage(
        content=f'Generate HTML for a newsletter about the following topic: {topic}\n' + 
        (f'Include these relevant articles: {str(articles)}' if articles else '')
    )
    
    response = Claude_3_5.invoke([sys_msg, human_msg])    
    return NewsletterState(newsletter_html=response)

@tool
def generate_newsletter_based_on_email_content(email_content_text: str) -> NewsletterState:
    """Generates beautifully styled html content for a newsletter based on email content provided by the user
    Args:
        email_content_text: str (the email body text to be transformed into a newsletter)
    """
    sys_msg = SystemMessage(content=newsletter_html_creation_prompt)
    
    # now = datetime.now()
    # formatted_date = now.strftime("%m/%d/%Y")

    # tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY")) 
    # response = tavily_client.search(
    #     query=f"{email_content_text} -{formatted_date}", 
    #     search_depth="advanced", 
    #     max_results=5,
    #     include_images=True
    # )
    # articles = response['results']
    
    human_msg = HumanMessage(
        content=f'Generate HTML for a newsletter based on this email content: {email_content_text}'
    )
    
    response = Claude_3_5.invoke([sys_msg, human_msg])    
    return NewsletterState(newsletter_html=response)
