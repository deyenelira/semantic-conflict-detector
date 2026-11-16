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

MODEL = "claude-opus-5-5"

# `ask` aceita `cache_prefix` (ver conflict_detector.py --cache)
SUPPORTS_PREFIX_CACHE = True

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


def ask(prompt, cache_prefix=None):
    """Envia o prompt. Com `cache_prefix` (o começo exato do prompt), esse trecho vai em um bloco próprio
    marcado para cache de 1h (a escrita custa 2x, mas o cache sobrevive aos intervalos entre usos do mesmo
    prefixo, que alternam entre 8 prompts). O texto que o modelo recebe é o mesmo, só dividido em dois blocos."""
    content = prompt
    if cache_prefix and prompt.startswith(cache_prefix) and len(prompt) > len(cache_prefix):
        content = [
            {"type": "text", "text": cache_prefix, "cache_control": {"type": "ephemeral", "ttl": "1h"}},
            {"type": "text", "text": prompt[len(cache_prefix):]},
        ]
    for attempt in range(MAX_RETRIES + 1):
        try:
            # sem temperature/top_p (rejeitados por este modelo) e sem thinking (sempre ligado, não pode ser desativado)
            response = client.messages.create(
                model=MODEL,
                max_tokens=MAX_OUTPUT_TOKENS,
                output_config={"effort": "medium"},
                messages=[{"role": "user", "content": content}],
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
    if isinstance(content, list):  # só quando o cache foi pedido: mostra se ele foi lido, escrito ou ignorado
        u = response.usage
        print(f"cache: lido={u.cache_read_input_tokens or 0} escrito={u.cache_creation_input_tokens or 0} "
              f"sem_cache={u.input_tokens}")
    # a recusa por segurança volta com HTTP 200; vira erro para ser registrada na coluna status
    if response.stop_reason == "refusal":
        category = response.stop_details.category if response.stop_details else None
        raise RuntimeError(f"refusal (category={category})")
    return "".join(block.text for block in response.content if block.type == "text")
