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
python3 -m src.conflict_detector --provider groq   # ou gemini / ollama
python3 -m src.conflict_detector --provider groq --dataset mergedataset
```

Opções:

- `--dataset`: nome de um diretório em `data/` que tenha um `dataset.csv` (padrão: `toy`).

Prompts maiores que o limite do provedor (`MAX_PROMPT_TOKENS` em `src/providers/<provider>.py`, comparado com uma estimativa do tamanho do prompt) não são enviados ao modelo.

## Datasets

Todo dataset segue a mesma estrutura:

- `data/<dataset>/dataset.csv`, com as colunas:
  - `id`: `<pasta>#<alvo>`, onde `<pasta>` contém o código e `<alvo>` é o nome do método ou campo alvo, sem parâmetros. Uma mesma pasta pode ter mais de um alvo.
  - `target`: assinatura do método ou campo alvo.
  - `label`: `Yes` se há conflito semântico, `No` caso contrário.
  - `left_summary` e `right_summary`: resumo das mudanças de cada lado (podem ser vazios).
- `data/<dataset>/<pasta>/{base,left,right,merge}.<extensão>`: o código de cada versão.

Ao carregar um caso, `{base}` recebe o código completo de BASE e `{left}`, `{right}` e `{merge}` recebem diffs unificados em relação a BASE, o que os prompts informam explicitamente. As demais colunas ficam disponíveis para prompts que as usem (`{target}`, `{left_summary}`, `{right_summary}`).

### toy

3 casos pequenos em Python. Rótulos: `c01` e `c05` com conflito, `n02` sem conflito. Alvos e resumos das mudanças foram escritos manualmente: nesses casos LEFT e RIGHT alteram funções diferentes, então o alvo é a função compartilhada (alterada por LEFT e usada pelo código novo de RIGHT).

### mergedataset

As 71 classes que contêm os 79 alvos usados em Barbosa et al. (2026), *Assessing the Effectiveness of Large Language Models in Detecting Semantic Conflicts*, JSERD. As pastas se chamam `<projeto>__<commit[:8]>__<Classe>`.

- Código: copiado sem alteração das pastas `source/` do branch `master` de [spgroup/mergedataset](https://github.com/spgroup/mergedataset). O único ajuste é o nome do arquivo `rigth.java` do eureka, salvo como `right.java`. O conteúdo foi conferido com os commits dos repositórios originais (merge, pais e merge base).
- Alvos e resumos das mudanças: arquivo de entrada do artigo (`inputs/input-smat.json` do [material suplementar](https://doi.org/10.5281/zenodo.20938400)).
- Rótulos (29 sim / 50 não): os da tese de Léuson Da Silva, `sample-semantic-conflicts.csv`, mantido sem alteração nesta pasta e copiado de [leusonmario/papers](https://github.com/leusonmario/papers/blob/master/2022PHDThesis/results/sample-semantic-conflicts.csv), com duas observações:
  - `ExplodedArchive.getUrl()` (spring-boot) está como `No` na tese, mas o artigo o considera conflito, então aqui está como `Yes`. Com o rótulo da tese seriam 28 sim / 51 não.
  - O alvo `HConnectionManager.operateWithFailover` (hector) aparece na tese como `HconnectionManager`; o rótulo (`No`) foi tirado dessa linha.

## Ollama e prompts longos

O Ollama usa um contexto pequeno por padrão e corta o início de prompts longos sem avisar. Por isso `src/providers/ollama.py` usa a API nativa e define `num_ctx` (32k) e o limite da resposta (8k, para modelos que raciocinam antes de responder, como DeepSeek R1 e Qwen3). Com esses valores, prompts acima de ~24k tokens são ignorados. Se o Ollama informar que um prompt usou mais tokens que o limite, um aviso é exibido.

## Saída

Os resultados serão armazenados em `results/<dataset>_<provider>_<data-hora>_response.csv` (ex.: `toy_groq_20261028-0044_response.csv`), então uma nova execução nunca sobrescreve as anteriores.

Colunas: `id`, `prompt`, `response` e `status`:

- `ok`: o modelo respondeu;
- `skipped: ~<tokens estimados> tokens > <limite>`: o prompt passa do limite do provedor e não foi enviado;
- `error: <erro>`: a chamada falhou (ex.: limite de requisições do provedor). A execução continua com as próximas chamadas.


