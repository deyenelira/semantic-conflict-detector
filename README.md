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

Copie `.env.example` para `.env` e preencha as chaves dos provedores que for usar:

- `GROQ_API_KEY`, `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`;
- `ANTHROPIC_WORKSPACE_ID`: só é necessária se a chave da Anthropic não estiver vinculada a um workspace.

O Ollama roda localmente e não precisa de chave.

## Execucao

```
source venv/bin/activate
python3 -m src.conflict_detector --provider groq   # ou anthropic / gemini / ollama
python3 -m src.conflict_detector --provider groq --dataset mergedataset
```

Opções:

- `--provider`: `anthropic`, `gemini`, `groq` ou `ollama` (padrão: `groq`).
- `--dataset`: nome de um diretório em `data/` que tenha um `dataset.csv` (padrão: `toy`).

Cada caso do dataset é enviado uma vez para cada prompt de `src/prompts.py` (8 prompts: 24 chamadas no `toy`, 632 no `mergedataset`). Os prompts combinam zero-shot ou few-shot (6 exemplos) com quatro variantes de contexto: sem target nem resumos (`none`), só resumos (`summaries`), só target (`target`) e ambos (`both`).

## Provedores

O modelo e os limites de cada provedor ficam em `src/providers/<provider>.py` (`MODEL`, `MAX_PROMPT_TOKENS`).

| Provedor | Modelo | Prompts ignorados acima de |
|---|---|---|
| `anthropic` | `claude-fable-5-1` | ~984k tokens (contexto de 1M menos 16k para a resposta) |
| `gemini` | `gemini-3.8-flash` | ~1M tokens (confirmar no model card) |
| `groq` | `openai/gpt-oss-120b` | ~5.950 tokens: o plano gratuito limita a 8.000 tokens por minuto, contando prompt e resposta (2.048) |
| `ollama` | `codellama:7b-instruct` | ~24k tokens (veja abaixo) |

Prompts maiores que o limite do provedor (`MAX_PROMPT_TOKENS`, comparado com uma estimativa do tamanho do prompt) não são enviados ao modelo. Com o plano gratuito do Groq, a maior parte do `mergedataset` é ignorada.

Groq, Gemini e Anthropic repetem a chamada com espera crescente quando a falha é temporária (ex.: limite de requisições, erro do servidor). Na Anthropic, uma recusa do modelo é registrada como erro.

## Datasets

Todo dataset segue a mesma estrutura:

- `data/<dataset>/dataset.csv`, com as colunas:
  - `id`: `<pasta>#<alvo>`, onde `<pasta>` contém o código e `<alvo>` é o nome do método ou campo alvo, sem parâmetros. Uma mesma pasta pode ter mais de um alvo.
  - `target`: assinatura do método ou campo alvo.
  - `label`: `Yes` se há conflito semântico, `No` caso contrário.
  - `left_summary` e `right_summary`: resumo das mudanças de cada lado (podem ser vazios).
- `data/<dataset>/<pasta>/{base,left,right,merge}.<extensão>`: o código de cada versão.

Ao carregar um caso, `{base}` recebe o código completo de BASE e `{left}`, `{right}` e `{merge}` recebem diffs unificados em relação a BASE, o que os prompts informam explicitamente. As demais colunas ficam disponíveis para prompts que as usem (`{target}`, `{left_summary}`, `{right_summary}`).

Os prompts, em `src/prompts.py`, são dois (zero-shot e one-shot), e a resposta final vem no bloco `<resultado>`:

- `zero_shot_guided` e `one_shot_guided`: ambos usam os resumos do dataset (`left_summary`, `right_summary`) e o `target`, o método que sofreu alteração no merge, como foco da análise.

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

Os resultados serão armazenados em `results/<dataset>_<provider>_<data-hora>_response.csv` (ex.: `toy_groq_20261028-004741_response.csv`), então uma nova execução nunca sobrescreve as anteriores.

Colunas (em inglês): `id`, `prompt`, `expected answer` (o `label` do dataset, `YES`/`NO`), `model answer` (`YES`/`NO`, convertido do `SIM`/`NAO` que os prompts pedem), `violated condition` (`A`/`B`/`C`), `state variable` e `status`. As três colunas extraídas da resposta ficam vazias quando o modelo não segue o formato `SIM - Condição A: <variável>` / `NAO`. O `status` pode ser:

- `ok`: o modelo respondeu;
- `skipped: ~<tokens estimados> tokens > <limite>`: o prompt passa do limite do provedor e não foi enviado;
- `error: <erro>`: a chamada falhou (ex.: limite de requisições do provedor). A execução continua com as próximas chamadas.



## Métricas

`src/metrics.py` lê um CSV de resultados e imprime um relatório em Markdown com as métricas por prompt:

```
python3 -m src.metrics results/toy_anthropic_20261102-212945_response.csv
python3 -m src.metrics results/<arquivo>.csv > relatorio.md   # para salvar
```

O relatório traz:

1. resultado geral e a baseline "sempre NO";
2. acurácia, precisão, recall, F1, especificidade, TP/TN/FP/FN e chamadas sem resposta de cada prompt, além da distribuição de respostas YES/NO;
3. efeito de cada fator: zero-shot vs. few-shot e o contexto fornecido (`none`, `summaries`, `target`, `both`), somando os prompts que compartilham o fator;
4. concordância entre os prompts: votos YES por caso, ensemble por voto (YES se ≥k prompts) e concordância par a par;
5. condição violada (A/B/C) nas respostas YES;
6. acertos por projeto (no `toy`, cada caso é um projeto);
7. chamadas sem resposta YES/NO: ignoradas (prompt grande demais), erros, recusas e respostas fora do formato.

As métricas (classe YES = conflito) consideram só as chamadas com resposta YES/NO; as demais são contadas à parte em "Sem resposta", para que prompts ignorados por limite de tamanho não sejam contados como erros do modelo. A exceção é o resultado por projeto, que conta as chamadas sem resposta como incorretas.

### Várias execuções e modelos

`src/reports.py` gera todos os relatórios de um diretório com uma pasta por modelo e um CSV por execução (todos com os mesmos casos e prompts):

```
python3 -m src.reports results/v2
```

```
results/v2/
├── report.md                  ← comparação entre os modelos
└── claude-sonnet-5-5/
    ├── 1.csv  1_report.md     ← relatório de src.metrics de cada execução
    ├── 2.csv  2_report.md
    ├── 3.csv  3_report.md
    └── report.md              ← resumo das execuções do modelo
```

O resumo de cada modelo (`src/comparison.py`) traz as métricas por execução, por prompt e por fator como média e intervalo (mín–máx) entre as execuções, a estabilidade (chamadas com a mesma resposta em todas as execuções) e as métricas da resposta da maioria das execuções. A comparação entre modelos traz o resultado geral de cada modelo, F1, recall e precisão por prompt e por fator, e os casos difíceis: aqueles em que todos os modelos acertam menos da metade das chamadas. Os relatórios existentes são sobrescritos.
