from langgraph.graph import MessagesState
from dataclasses import dataclass, field

@dataclass
class NewsletterState(MessagesState):
    user_input: str = ""
    articles: list = field(default_factory=list)
    newsletter_html: str = ""
    from_email: str = ""
    to_emails: list[str] = field(default_factory=list)
    date: str = ""
    error: str = ""