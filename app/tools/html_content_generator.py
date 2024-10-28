from langchain_core.messages import SystemMessage, HumanMessage
from app.utils.llms import Claude_3_5
from app.utils.newsletter_state import NewsletterState
from langchain_core.tools import tool
from app.agents.prompts import newsletter_html_creation_prompt

@tool
def html_content_generation(articles: list[dict] | None = None, textStringOfTheEmailOrNewsletterBody: str | None = None) -> NewsletterState:
    """Generates beautifully styled html content for a newsletter based on the given articles or topic as a text string
    Args:
        articles: list[dict] (list of news articles) or None
        textStringOfTheEmailOrNewsletterBody: str (a text string of the newsletter or email body) or None
    """
    
    sys_msg = SystemMessage(content=newsletter_html_creation_prompt)
    
    if articles:
        articles_str = str(articles)
        human_msg = HumanMessage(content='Generate HTML for a newsletter with the following articles: ' + articles_str)
    else:
        human_msg = HumanMessage(content='Generate HTML for a newsletter about the following topic: ' + textStringOfTheEmailOrNewsletterBody)
    
    response = Claude_3_5.invoke(
        [
            sys_msg,    
            human_msg
        ]
    )    
    return NewsletterState(newsletter_html=response)
