import argparse
import csv
import re
from datetime import datetime
from pathlib import Path

from src.datasets import DATASETS, load
from src.prompts import PROMPTS
from src.providers import PROVIDERS, get_provider

ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "results"

# Estimativa grosseira, igual para todos os modelos: cada prompt tem sempre o mesmo tamanho
# estimado. Se ele é ignorado ou não depende do limite de cada modelo (MAX_PROMPT_TOKENS).
CHARS_PER_TOKEN = 3.5


def estimate_tokens(text):
    return round(len(text) / CHARS_PER_TOKEN)


# "SIM - Condição A: variável" / "NAO" (tolera markdown e variações de acento/pontuação)
RESPONSE_RE = re.compile(
    r"(SIM|N[AÃ]O)\b(?:\s*[-–—:]\s*(?:Condi[cç][aã]o\s*)?\(?([ABC])\)?\b\s*[:\-–—]?\s*(.*))?",
    re.IGNORECASE)

# os prompts pedem a análise em <analise> e a resposta final em <resultado>
RESULT_RE = re.compile(r"<resultado>(.*?)(?:</resultado>|$)", re.IGNORECASE | re.DOTALL)

COLUMNS = ["id", "prompt", "expected answer", "model answer", "violated condition", "state variable", "status"]


def parse_response(response):
    """Extrai (resposta do modelo, condição violada, variável de estado) do bloco <resultado> (ou da primeira linha, se o modelo não usou as tags).

    A resposta do modelo é normalizada para YES/NO, como o `label` do dataset."""
    blocks = RESULT_RE.findall(response)
    if blocks:
        response = blocks[-1]
    lines = response.replace("*", "").strip().splitlines()
    m = RESPONSE_RE.search(lines[0]) if lines else None
    if not m:
        return "", "", ""
    conflict = "YES" if m.group(1).upper() == "SIM" else "NO"
    return conflict, (m.group(2) or "").upper(), (m.group(3) or "").strip()


def main():
    parser = argparse.ArgumentParser(description="Detecta conflitos semânticos em merges usando LLMs.")
    parser.add_argument("--provider", choices=PROVIDERS, default="groq")
    parser.add_argument("--dataset", choices=DATASETS, default="toy")
    args = parser.parse_args()

    provider = get_provider(args.provider)
    max_prompt_tokens = provider.MAX_PROMPT_TOKENS
    # data e hora no nome para que uma execução nunca sobrescreva resultados anteriores
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_path = RESULTS_DIR / f"{args.dataset}_{args.provider}_{timestamp}_response.csv"
    RESULTS_DIR.mkdir(exist_ok=True)

    rows = load(args.dataset)
    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        output = csv.DictWriter(f, fieldnames=COLUMNS)
        output.writeheader()
        for i, row in enumerate(rows):
            for name, prompt in PROMPTS.items():
                text = prompt.format(**row)
                tokens = estimate_tokens(text)
                if tokens > max_prompt_tokens:
                    response, status = "", f"skipped: ~{tokens} tokens > {max_prompt_tokens}"
                else:
                    try:
                        response, status = provider.ask(text), "ok"
                    except Exception as e:
                        # registra a falha e segue para a próxima chamada em vez de interromper a execução
                        response, status = "", f"error: {type(e).__name__}: {e}"
                print(f"--- {row.get('id', i)} | {name} | {status}\n{response}\n")
                conflict, condition, variable = parse_response(response)
                output.writerow({"id": row.get("id", i), "prompt": name,
                                 "expected answer": row.get("label", "").upper(),
                                 "model answer": conflict, "violated condition": condition,
                                 "state variable": variable, "status": status})
                f.flush()


if __name__ == "__main__":
    main()
