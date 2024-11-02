from langchain_core.tools import tool
from datetime import datetime

@tool
def get_current_date() -> str:
    """Returns the current date in the format of month/day/year. 
    Always use this date in the search queries to fetch the most relevant articles.
    """
    now = datetime.now()
    day = now.day
    month = now.month
    year = now.year
    return {"date": f"{month}/{day}/{year}"}