from langchain_openai import ChatOpenAI
import os

OpenAI_GPT4O = ChatOpenAI(
        model="gpt-4o", 
        api_key=os.getenv("OPENAI_API_KEY"), 
        max_tokens=8192,
        temperature=0.3
    )

