from langchain_core.messages import SystemMessage, HumanMessage
from app.utils.llms import Claude_3_5
from app.utils.newsletter_state import NewsletterState
from langchain_core.tools import tool
from app.agents.prompts import newsletter_html_updates_prompt

@tool
def html_content_updates(newsletter_html: str, requested_changes: str) -> NewsletterState: 
    """Updates the newsletter html content with the requested changes
    Args:
        newsletter_html: str (newsletter html content)
        requested_changes: str (requested changes)
    """
    
    sys_msg = SystemMessage(content=newsletter_html_updates_prompt)
    human_msg = HumanMessage(content=f'Update the following [newsletter_html_content] with the [requested_changes]. newsletter_html_content: {newsletter_html} \n, requested_changes: {requested_changes}')
    
    response = Claude_3_5.invoke(
        [
            sys_msg,    
            human_msg
        ]
    )    
    return NewsletterState(newsletter_html=response)