from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
import os

OpenAI_GPT4O = ChatOpenAI(
        model="gpt-4o", 
        api_key=os.getenv("OPENAI_API_KEY"), 
        max_tokens=8192,
        temperature=0.3
    )

Claude_3_5 = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    max_tokens=8192,
    temperature=0.5
)

