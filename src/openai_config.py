from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1/",
    api_key="ollama123" 
)

MODEL = "codellama:7b-instruct"  # mudar para: "codellama:70b-instruct"

def ask(prompt):
    print("Asking prompt to OpenAI...")
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500
    )
    return response.choices[0].message.content or ""