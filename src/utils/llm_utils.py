import json
import requests
from config.config import LLM_API_BASE_URL, LLM_API_KEY, LLM_CHAT_MODEL

def parse_line(line):
    if not line.startswith("data: "):
        return None
    
    try:
        parsed_data = json.loads(line[len("data: "):])
        choices = parsed_data.get("choices", [])
        if choices:
            return choices[0].get("delta", {}).get("content")
    except json.JSONDecodeError:
        return None

    return None

def chat(messages, handler):
    url = f"{LLM_API_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": messages,
        "model": LLM_CHAT_MODEL,
        "max_tokens": 400,
        "temperature": 0.5,
        "top_p": 0.9,
        #"top_k": 0.9,  #top_k parameters cannot be used if you use the Groq API, as it does not support these sampling techniques for controlling output generation.
        "stream": True
    }

    response = requests.post(url, headers=headers, json=data, stream=True)
    response.raise_for_status()

    answer = ""
    buffer = ""
    
    for line in response.iter_lines(decode_unicode=True):
        line = buffer + line if line else ""
        
        if line.startswith(":") or line == "data: [DONE]":
            buffer = ""
            continue
        
        partial = parse_line(line)
        if partial:
            answer += partial
            if handler:
                handler(partial)
        else:
            buffer = line
    
    return answer
