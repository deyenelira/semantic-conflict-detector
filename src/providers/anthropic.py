import os
import random
import time
import anthropic
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

# o SDK lê ANTHROPIC_API_KEY do ambiente; as tentativas ficam por conta do backoff abaixo
# chaves sem workspace exigem o header anthropic-workspace-id (chaves de um workspace não precisam)
workspace_id = os.getenv("ANTHROPIC_WORKSPACE_ID")
client = Anthropic(
    max_retries=0,
    default_headers={"anthropic-workspace-id": workspace_id} if workspace_id else None,
)

MODEL = "claude-haiku-5-5"

# janela de contexto do modelo (1M tokens) menos o espaço reservado para a resposta
MAX_PROMPT_TOKENS = 1_000_000 - 16_000

# a resposta curta (SIM/NAO) vem depois do raciocínio do modelo, que também conta nesse limite
MAX_OUTPUT_TOKENS = 16_000

MAX_RETRIES = 6
BASE_DELAY = 2.0
MAX_DELAY = 70.0  # o limite de tokens é por minuto: esperar ~1 min libera a cota
RETRYABLE_CODES = {408, 409, 429, 500, 502, 503, 504, 529}


def is_retryable(e):
    if isinstance(e, anthropic.APIConnectionError):  # inclui timeout
        return True
    # 400/401/403/404/413 (prompt inválido ou grande demais) não mudam ao repetir
    return isinstance(e, anthropic.APIStatusError) and e.status_code in RETRYABLE_CODES


def retry_delay(e, attempt):
    delay = min(BASE_DELAY * 2 ** attempt, MAX_DELAY)
    # se a API informa quanto esperar, usa isso como piso
    retry_after = getattr(getattr(e, "response", None), "headers", {}).get("retry-after")
    try:
        delay = max(delay, float(retry_after))
    except (TypeError, ValueError):
        pass
    return delay + random.uniform(0, delay / 2)  # jitter


def ask(prompt):
    for attempt in range(MAX_RETRIES + 1):
        try:
            # sem temperature/top_p (rejeitados por este modelo) e sem thinking (sempre ligado, não pode ser desativado)
            response = client.messages.create(
                model=MODEL,
                max_tokens=MAX_OUTPUT_TOKENS,
                output_config={"effort": "medium"},
                messages=[{"role": "user", "content": prompt}],
            )
            break
        except anthropic.AnthropicError as e:
            if not is_retryable(e) or attempt == MAX_RETRIES:
                raise
            delay = retry_delay(e, attempt)
            code = getattr(e, "status_code", type(e).__name__)
            print(f"Anthropic error {code}, retrying in {delay:.1f}s "
                  f"({attempt + 1}/{MAX_RETRIES})")
            time.sleep(delay)
    # a recusa por segurança volta com HTTP 200; vira erro para ser registrada na coluna status
    if response.stop_reason == "refusal":
        category = response.stop_details.category if response.stop_details else None
        raise RuntimeError(f"refusal (category={category})")
    return "".join(block.text for block in response.content if block.type == "text")
