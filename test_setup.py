from openrouter import OpenRouter
import os
from dotenv import load_dotenv

load_dotenv()

with OpenRouter(
    api_key=os.getenv("OPENROUTER_API_KEY", ""),
) as open_router:
    res = open_router.chat.send(
        messages=[
            {"content": "What is the capital of France?", "role": "user"},
        ],
        stream=False,
        model=os.getenv("MODEL", ""),
    )
    print(res.choices[0].message.content)