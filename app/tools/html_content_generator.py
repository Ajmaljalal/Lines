from langchain_core.messages import SystemMessage, HumanMessage
from app.utils.llms import Claude_3_5
from app.utils.newsletter_state import NewsletterState
from langchain_core.tools import tool
from app.agents.prompts import newsletter_html_creation_prompt

@tool
def html_generation(articles: list[dict]) -> NewsletterState: 
    """Generates beautifully styled html content for a newsletter based on the given articles
    Args:
        articles: list[dict] (list of news articles)
    """
    
    sys_msg = SystemMessage(content=newsletter_html_creation_prompt)
    # Convert the list of articles to a string
    articles_str = ', '.join(str(article) for article in articles)
    human_msg = HumanMessage(content='Generate HTML for a newsletter with the following articles: ' + articles_str)
    
    response = Claude_3_5.invoke(
        [
            sys_msg,    
            human_msg
        ]
    )    
    return NewsletterState(newsletter_html=response)