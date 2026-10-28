import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = "openai/gpt-oss-120b"

# janela de contexto do modelo (131.072 tokens) menos o espaço reservado para a resposta
MAX_PROMPT_TOKENS = 131_072 - 2048

def ask(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=1,
        max_completion_tokens=2048,
        top_p=1,
        reasoning_effort="medium"
    )
    return response.choices[0].message.content or ""
