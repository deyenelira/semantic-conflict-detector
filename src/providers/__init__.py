import importlib

from dotenv import load_dotenv

load_dotenv()

PROVIDERS = ("gemini", "groq", "ollama")


def get_provider(name):
    """Carrega sob demanda o módulo do provedor e devolve sua função `ask`."""
    if name not in PROVIDERS:
        raise ValueError(f"Provedor inválido: {name!r}. Opções: {', '.join(PROVIDERS)}")
    return importlib.import_module(f"{__name__}.{name}").ask
