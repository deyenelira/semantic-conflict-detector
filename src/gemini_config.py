import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = "gemini-3.8-flash"

def ask(prompt):
    answer = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config={
            "max_output_tokens": 1500
        }
    )
    return answer.text or ""
