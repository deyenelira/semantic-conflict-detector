import csv
from gemini_config import ask
from prompts import PROMPTS

DATASET = "dataset.csv"       
OUTPUT = "answers.csv"

def main():
    with open(DATASET, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        output = csv.DictWriter(f, fieldnames=["id", "prompt", "answer"])
        output.writeheader()
        for i, row in enumerate(rows):
            for name, prompt in PROMPTS.items():
                answer = ask(prompt.format(**row))
                print(f"--- {row.get('id', i)} | {name}\n{answer}\n")
                output.writerow({"id": row.get("id", i), "prompt": name, "answer": answer})
                f.flush() 


if __name__ == "__main__":
    main()