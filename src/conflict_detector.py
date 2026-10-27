import argparse
import csv
from pathlib import Path

from src.prompts import PROMPTS
from src.providers import PROVIDERS, get_provider

ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "data" / "dataset.csv"
RESULTS_DIR = ROOT / "results"


def main():
    parser = argparse.ArgumentParser(description="Detecta conflitos semânticos em merges usando LLMs.")
    parser.add_argument("--provider", choices=PROVIDERS, default="groq")
    args = parser.parse_args()

    ask = get_provider(args.provider)
    output_path = RESULTS_DIR / f"{args.provider}_response.csv"
    RESULTS_DIR.mkdir(exist_ok=True)

    with open(DATASET, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        output = csv.DictWriter(f, fieldnames=["id", "prompt", "response"])
        output.writeheader()
        for i, row in enumerate(rows):
            for name, prompt in PROMPTS.items():
                response = ask(prompt.format(**row))
                print(f"--- {row.get('id', i)} | {name}\n{response}\n")
                output.writerow({"id": row.get("id", i), "prompt": name, "response": response})
                f.flush()


if __name__ == "__main__":
    main()
