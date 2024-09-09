from groq import Groq
import json
from config.config import LLM_API_BASE_URL, LLM_API_KEY, LLM_CHAT_MODEL

client = Groq(api_key=LLM_API_KEY)  # Initialize Groq client with the API key

def run_conversation(user_prompt):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant providing nutritional advice based on user queries."
        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]
    tools = []  # No tools needed for nutritional queries

    response = client.chat.completions.create(
        model=LLM_CHAT_MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=4096
    )

    response_message = response.choices[0].message
    return response_message.content
