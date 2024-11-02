from langchain_core.tools import tool
from app.utils.newsletter_state import NewsletterState
from app.utils.email_sender import sendgrid_send_email


@tool 
def send_email(from_email: str, newsletter_html: str, to: list[str], subject: str) -> NewsletterState: 
    """Sends the newsletter html content to the given email addresses

    Args:
        from_email: str (email address of the sender)
        newsletter_html: str (html content of the newsletter)
        to: list[str] (list of email addresses)
        subject: str (subject of the email)
    """
    sendgrid_send_email(to, subject, newsletter_html, from_email)
    return {"status": "Email sent successfully!"}