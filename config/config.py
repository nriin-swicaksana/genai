import os

from dotenv import load_dotenv
load_dotenv()

PORT = int(os.environ.get("PORT", 3000))

LLM_API_BASE_URL = os.getenv("LLM_API_BASE_URL")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_CHAT_MODEL = os.getenv("LLM_CHAT_MODEL")
LLM_STREAMING = os.getenv("LLM_STREAMING", "yes").lower() != "no"

