# Execução

## Setup local do Code Llama

## Instale usando a linha de comando no Ubuntu

```
sudo snap install ollama
```

## Baixe e execute o modelo

```
ollama run codellama:7b-instruct
```

## Caso queira validar se está tudo funcionando, execute o código abaixo no seu terminal

```
curl http://localhost:11434/api/generate -d '{
  "model": "codellama:7b-instruct",
  "prompt": "Escreva um Hello World em Python.",
  "stream": false
}'
```

# Setup do projeto Python

## Criacao de ambiente virtual
```
python3 -m venv venv 
source venv/bin/activate
```

## Instalando dependencias
```
pip install -r requirements.txt
```

## Variaveis de ambiente

É necessário criar um arquivo .env com as variáveis de ambiente relacionadas às API KEYS dos modelos utilizados

## Execucao

```
python3 conflict_detector.py
```

## Saída

Os resultados serão armazenados no arquivo response.csv


