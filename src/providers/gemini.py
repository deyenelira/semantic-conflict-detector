import os
import random
import time
from google import genai
from google.genai import errors
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = "gemini-3.8-flash"

# janela de contexto do modelo (confirmar no model card) menos o espaço reservado para a resposta
MAX_PROMPT_TOKENS = 1_048_576 - 1500

MAX_RETRIES = 5
BASE_DELAY = 1.0
MAX_DELAY = 30.0
RETRYABLE_CODES = {429, 500, 502, 503, 504}

def ask(prompt):
    for attempt in range(MAX_RETRIES + 1):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config={
                    "max_output_tokens": 1500
                }
            )
            return response.text or ""
        except errors.APIError as e:
            if e.code not in RETRYABLE_CODES or attempt == MAX_RETRIES:
                raise
            delay = min(BASE_DELAY * 2 ** attempt, MAX_DELAY)
            delay += random.uniform(0, delay / 2)  # jitter
            print(f"Gemini error {e.code}, retrying in {delay:.1f}s "
                  f"({attempt + 1}/{MAX_RETRIES})")
            time.sleep(delay)
