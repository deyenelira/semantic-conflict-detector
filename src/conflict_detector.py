import csv
from prompts import PROMPTS
from openai_config import ask

DATASET = "dataset.csv"       
OUTPUT = "response.csv"

def main():
    with open(DATASET, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
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