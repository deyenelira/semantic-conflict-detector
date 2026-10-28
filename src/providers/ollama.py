import json
import re
import urllib.request

# API nativa do Ollama: a compatível com OpenAI não permite definir o tamanho do contexto
URL = "http://localhost:11434/api/chat"

MODEL = "codellama:7b-instruct"  # mudar para: "codellama:70b-instruct"

# Por padrão o Ollama usa um contexto pequeno e corta o início de prompts longos sem avisar,
# por isso o tamanho do contexto é definido explicitamente em cada chamada.
NUM_CTX = 32768
# espaço para a resposta, incluindo o raciocínio de modelos como DeepSeek R1 e Qwen3
MAX_OUTPUT_TOKENS = 8192
MAX_PROMPT_TOKENS = NUM_CTX - MAX_OUTPUT_TOKENS


def ask(prompt):
    print("Asking prompt to Ollama...")
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False,
        "options": {
            "num_ctx": NUM_CTX,
            "num_predict": MAX_OUTPUT_TOKENS
        }
    }
    request = urllib.request.Request(URL, data=json.dumps(payload).encode("utf-8"),
                                     headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request) as response:
        body = json.load(response)

    prompt_tokens = body.get("prompt_eval_count", 0)
    if prompt_tokens > MAX_PROMPT_TOKENS:
        print(f"Aviso: o prompt usou {prompt_tokens} tokens (limite {MAX_PROMPT_TOKENS}); "
              f"pode ter sido cortado ou ter sobrado pouco espaço para a resposta.")
    if body.get("done_reason") == "length":
        print(f"Aviso: a resposta atingiu o limite de {MAX_OUTPUT_TOKENS} tokens e foi cortada.")

    content = body.get("message", {}).get("content") or ""
    # remove o raciocínio que alguns modelos devolvem junto da resposta
    return re.sub(r"<think>.*?</think>", "", content, flags=re.S).strip()
