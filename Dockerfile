FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src ./src
COPY data ./data

# Por padrão roda o experimento completo (src.experiment) e grava em results/experiment.
# Uso: docker run --env-file .env -v $(pwd)/results:/app/results <imagem> results/v4 --models claude-haiku-5-5
# Uma execução avulsa: docker run ... --entrypoint python <imagem> -m src.conflict_detector --provider anthropic
ENTRYPOINT ["python", "-m", "src.experiment"]
CMD ["results/experiment"]
