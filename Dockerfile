FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src ./src
COPY data ./data

# Uso: docker run --env-file .env -v $(pwd)/results:/app/results <imagem> --provider anthropic
ENTRYPOINT ["python", "-m", "src.conflict_detector"]
CMD ["--provider", "anthropic"]
