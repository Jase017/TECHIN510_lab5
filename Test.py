import os

import requests
from dotenv import load_dotenv

load_dotenv()

URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
)

data = {
    "contents": [
        {
            "parts": [
                {"text": "Tell me a joke about HTML."}
            ]
        }
    ]
}

res = requests.post(
    URL,
    headers={
        "content-type": "application/json",
    },
    json=data,
    params={"key": os.getenv("GEMINI_API_KEY")}
)
print(res.json())