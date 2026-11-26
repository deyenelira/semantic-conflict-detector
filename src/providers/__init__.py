import importlib

from dotenv import load_dotenv

load_dotenv()

PROVIDERS = ("anthropic", "gemini", "groq", "ollama")


def get_provider(name, model=None):
    """Carrega sob demanda o módulo do provedor, que expõe `ask`, `MODEL` e `MAX_PROMPT_TOKENS`.

    Com `model`, substitui o `MODEL` padrão do provedor (lido por `ask` a cada chamada)."""
    if name not in PROVIDERS:
        raise ValueError(f"Provedor inválido: {name!r}. Opções: {', '.join(PROVIDERS)}")
    provider = importlib.import_module(f"{__name__}.{name}")
    if model:
        provider.MODEL = model
    return provider
