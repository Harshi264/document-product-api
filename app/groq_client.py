import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"

async def analyze_text(text: str):
    response = openai.ChatCompletion.create(
        model="mixtral-8x7b-32768",
        messages=[
            {"role": "system", "content": "Summarize the following text"},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message["content"]
