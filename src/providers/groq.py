import os
import random
import re
import time
import groq
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
    max_retries=0  # as tentativas ficam por conta do backoff abaixo
)

MODEL = "openai/gpt-oss-120b"

# limite de tokens por minuto do plano gratuito (8.000), que conta prompt + resposta reservada; prompts
# maiores nunca passam, então são pulados (a janela de contexto do modelo seria 131.072 tokens)
TOKENS_PER_MINUTE = 8_000
MAX_OUTPUT_TOKENS = 2048
MAX_PROMPT_TOKENS = TOKENS_PER_MINUTE - MAX_OUTPUT_TOKENS

MAX_RETRIES = 6
BASE_DELAY = 2.0
MAX_DELAY = 70.0  # o limite de tokens é por minuto: esperar ~1 min libera a cota
RETRYABLE_CODES = {408, 429, 500, 502, 503, 504}

# mensagem do Groq: "... Limit 8000, Requested 18197, ..."
LIMIT_RE = re.compile(r"Limit (\d+), Requested (\d+)")


def is_retryable(e):
    if isinstance(e, groq.APIConnectionError):  # inclui timeout
        return True
    if not isinstance(e, groq.APIStatusError):
        return False
    # um único prompt maior que o limite por minuto nunca passa, esperar não adianta
    m = LIMIT_RE.search(str(e))
    if m and int(m.group(2)) > int(m.group(1)):
        return False
    return e.status_code in RETRYABLE_CODES or e.status_code == 413


def retry_delay(e, attempt):
    delay = min(BASE_DELAY * 2 ** attempt, MAX_DELAY)
    # se o Groq informa quanto esperar, usa isso como piso
    retry_after = getattr(getattr(e, "response", None), "headers", {}).get("retry-after")
    try:
        delay = max(delay, float(retry_after))
    except (TypeError, ValueError):
        pass
    return delay + random.uniform(0, delay / 2)  # jitter


def ask(prompt):
    for attempt in range(MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=1,
                max_completion_tokens=MAX_OUTPUT_TOKENS,
                top_p=1,
                reasoning_effort="medium"
            )
            return response.choices[0].message.content or ""
        except groq.GroqError as e:
            if not is_retryable(e) or attempt == MAX_RETRIES:
                raise
            delay = retry_delay(e, attempt)
            code = getattr(e, "status_code", type(e).__name__)
            print(f"Groq error {code}, retrying in {delay:.1f}s "
                  f"({attempt + 1}/{MAX_RETRIES})")
            time.sleep(delay)
