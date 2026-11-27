# Sumário

- [Setup do projeto Python](#setup-do-projeto-python)
  - [Criação de ambiente virtual](#criacao-de-ambiente-virtual)
  - [Instalando dependências](#instalando-dependencias)
  - [Variáveis de ambiente](#variaveis-de-ambiente)
  - [Execução](#execucao)
  - [Provedor](#provedor)
  - [Datasets](#datasets) ([toy](#toy), [mergedataset](#mergedataset))
  - [Saída](#saída)
  - [Métricas](#métricas) ([várias execuções e modelos](#várias-execuções-e-modelos))
- [Docker](#docker)
  - [Pré-requisitos](#pré-requisitos)
  - [Passo a passo](#passo-a-passo)
  - [Gerando métricas e relatórios](#gerando-métricas-e-relatórios)
  - [Usando um dataset próprio](#usando-um-dataset-próprio)
  - [Problemas comuns](#problemas-comuns)

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

Copie `.env.example` para `.env` e preencha:

- `ANTHROPIC_API_KEY`: chave da API da Anthropic;
- `ANTHROPIC_WORKSPACE_ID`: só é necessária se a chave não estiver vinculada a um workspace.

## Execucao

```
source venv/bin/activate
python3 -m src.conflict_detector --provider anthropic
python3 -m src.conflict_detector --provider anthropic --dataset mergedataset
python3 -m src.conflict_detector --provider anthropic --model claude-sonnet-5-5 --dataset mergedataset
```

Opções:

- `--provider`: use `anthropic`.
- `--model`: modelo a usar (padrão: o `MODEL` de `src/providers/<provedor>.py`). O nome do modelo entra no nome do CSV gerado.
- `--dataset`: nome de um diretório em `data/` que tenha um `dataset.csv` (padrão: `toy`).

Cada caso do dataset é enviado uma vez para cada prompt de `src/prompts.py` (8 prompts: 24 chamadas no `toy`, 632 no `mergedataset`). Os prompts combinam zero-shot ou few-shot (6 exemplos) com quatro variantes de contexto: sem target nem resumos (`none`), só resumos (`summaries`), só target (`target`) e ambos (`both`).

## Provedor

O modelo padrão e o limite de tamanho do prompt ficam em `src/providers/anthropic.py` (`MODEL`, `MAX_PROMPT_TOKENS`). O modelo pode ser trocado com `--model`, sem editar o arquivo.

| Provedor | Modelo | Prompts ignorados acima de |
|---|---|---|
| `anthropic` | `claude-fable-5-1` | ~984k tokens (contexto de 1M menos 16k para a resposta) |

Prompts maiores que o limite (`MAX_PROMPT_TOKENS`, comparado com uma estimativa do tamanho do prompt) não são enviados ao modelo. A chamada é repetida com espera crescente quando a falha é temporária (ex.: limite de requisições, erro do servidor). Uma recusa do modelo é registrada como erro.

## Datasets

Todo dataset segue a mesma estrutura:

- `data/<dataset>/dataset.csv`, com as colunas:
  - `id`: `<pasta>#<alvo>`, onde `<pasta>` contém o código e `<alvo>` é o nome do método ou campo alvo, sem parâmetros. Uma mesma pasta pode ter mais de um alvo.
  - `target`: assinatura do método ou campo alvo.
  - `label`: `Yes` se há conflito semântico, `No` caso contrário.
  - `left_summary` e `right_summary`: resumo das mudanças de cada lado (podem ser vazios).
  - `justification`: por que o caso tem ou não conflito. Serve para conferir as respostas; nenhum prompt usa esta coluna.
- `data/<dataset>/<pasta>/{base,left,right,merge}.<extensão>`: o código de cada versão.

Ao carregar um caso, `{base}` recebe o código completo de BASE e `{left}`, `{right}` e `{merge}` recebem diffs unificados em relação a BASE, o que os prompts informam explicitamente. As demais colunas ficam disponíveis para prompts que as usem (`{target}`, `{left_summary}`, `{right_summary}`).

Os prompts, em `src/prompts.py`, são 8: zero-shot ou few-shot (6 exemplos), cada um em quatro variantes de contexto. Todos recebem o código das quatro versões, pedem a análise no bloco `<analise>` e a resposta final no bloco `<resultado>`:

- `*_none`: sem `target` e sem resumos;
- `*_summaries`: com os resumos do dataset (`left_summary`, `right_summary`);
- `*_target`: com o `target`, o método ou campo alvo, como foco da análise;
- `*_both`: com o `target` e os resumos.

Os nomes completos são `zero_shot_guided_<variante>` e `few_shot_guided_<variante>`.

### toy

3 casos pequenos em Python. Rótulos: `c01` e `c05` com conflito, `n02` sem conflito. Alvos, resumos das mudanças e justificativas foram escritos manualmente: nesses casos LEFT e RIGHT alteram funções diferentes, então o alvo é a função compartilhada (alterada por LEFT e usada pelo código novo de RIGHT).

### mergedataset

As 71 classes que contêm os 79 alvos usados em Barbosa et al. (2026), *Assessing the Effectiveness of Large Language Models in Detecting Semantic Conflicts*, JSERD. As pastas se chamam `<projeto>__<commit[:8]>__<Classe>`.

- Código: copiado das pastas `source/` do branch `master` de [spgroup/mergedataset](https://github.com/spgroup/mergedataset). O conteúdo foi conferido com os commits dos repositórios originais (merge, pais e merge base).
- Alvos e resumos das mudanças: arquivo de entrada do artigo (`inputs/input-smat.json` do [material suplementar](https://doi.org/10.5281/zenodo.20938400)).
- Rótulos: 29 casos com conflito e 50 sem, como no artigo.

## Saída

Os resultados de `src.conflict_detector` são armazenados em `results/<dataset>_<provider>_<modelo>_<data-hora>_response.csv` (ex.: `toy_anthropic_claude-sonnet-5-5_20261028-004741_response.csv`; com `--cache`, o nome termina em `_cache_response.csv`), então uma nova execução nunca sobrescreve as anteriores. Em nomes de modelo, `/` e `:` viram `-`. O `src.experiment` grava os mesmos CSVs em `<diretório>/<modelo>/<n>.csv` (veja [Várias execuções e modelos](#várias-execuções-e-modelos)).

Colunas (em inglês): `id`, `prompt`, `expected answer` (o `label` do dataset, `YES`/`NO`), `model answer` (`YES`/`NO`, convertido do `SIM`/`NAO` que os prompts pedem), `violated condition` (`A`/`B`/`C`), `state variable`, `analysis` (o texto do bloco `<analise>`) e `status`. As colunas `model answer`, `violated condition` e `state variable` ficam vazias quando o modelo não segue o formato `SIM - Condição A: <variável>` / `NAO`, e `analysis` fica vazia quando ele não usa o bloco `<analise>`. O `status` pode ser:

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

Para rodar o experimento completo de uma vez, `src/experiment.py` executa cada modelo várias vezes e depois gera os relatórios abaixo (padrão: `claude-haiku-5-5`, `claude-sonnet-5-5` e `claude-opus-5-5`, 3 execuções cada, no `mergedataset`):

```
python3 -m src.experiment results/v3
python3 -m src.experiment results/v3 --models claude-sonnet-5-5 --runs 3 --cache
docker compose run --rm detector results/v3
```

Cada execução é gravada em `<diretório>/<modelo>/<n>.csv`. Execuções que já têm CSV são puladas, então rodar o mesmo comando de novo continua um experimento interrompido.

`src/reports.py` gera todos os relatórios de um diretório com uma pasta por modelo e um CSV por execução (todos com os mesmos casos e prompts):

```
python3 -m src.reports results/v2
```

```
results/v2/
├── report.md                  ← comparação entre os modelos
├── divergent_cases.md         ← casos em que os modelos divergem, para análise manual
└── claude-sonnet-5-5/
    ├── 1.csv  1_report.md     ← relatório de src.metrics de cada execução
    ├── 2.csv  2_report.md
    ├── 3.csv  3_report.md
    └── report.md              ← resumo das execuções do modelo
```

O resumo de cada modelo (`src/comparison.py`) traz as métricas por execução, por prompt e por fator como média e intervalo (mín–máx) entre as execuções, a estabilidade (chamadas com a mesma resposta em todas as execuções) e as métricas da resposta da maioria das execuções. A comparação entre modelos traz o resultado geral de cada modelo, F1, recall e precisão por prompt e por fator, e os casos difíceis: aqueles em que todos os modelos acertam menos da metade das chamadas.

O `divergent_cases.md` (`src/divergent_cases.py`) serve para a análise manual dos casos em que os modelos divergem no prompt `few_shot_guided_both`. Entram os casos em que cada modelo deu a mesma resposta em todas as suas execuções, e ao menos um modelo respondeu YES e outro NO, separados em conflitos detectados só por parte dos modelos e falsos positivos de parte dos modelos. Para cada caso, o relatório traz o target, um link para o código, os resumos de LEFT e RIGHT, a justificativa do dataset e, para cada modelo (primeiro os que acertam), a resposta e a análise de cada execução em blocos recolhidos, que se abrem com um clique.

Os relatórios existentes são sobrescritos.

# Docker

Forma mais simples de rodar o projeto, sem instalar Python nem dependências. Por padrão, o container roda o experimento completo ([`src.experiment`](#várias-execuções-e-modelos)) com o provedor **Anthropic**.

## Pré-requisitos

- [Docker](https://docs.docker.com/engine/install/) com o plugin Compose (`docker compose version` deve funcionar). No Windows, use o Docker Desktop com a integração com o WSL ativada.
- Uma chave da API da Anthropic.

## Passo a passo

1. **Entre na pasta do projeto**:

   ```
   cd merge_and_code_review
   ```

2. **Crie o arquivo `.env`** a partir do exemplo e preencha a chave da Anthropic:

   ```
   cp .env.example .env
   ```

   ```
   ANTHROPIC_API_KEY=sua_chave_aqui
   # só se a chave não estiver vinculada a um workspace:
   ANTHROPIC_WORKSPACE_ID=seu_workspace_id
   ```

   O `.env` não é copiado para a imagem; o Compose o injeta só como variáveis de ambiente na execução.

3. **Construa a imagem** (só na primeira vez, ou depois de alterar `src/`, `data/` ou `requirements.txt`):

   ```
   docker compose build
   ```

4. **Execute**. Sem argumentos, roda o experimento completo e grava em `results/experiment/`: `claude-haiku-5-5`, `claude-sonnet-5-5` e `claude-opus-5-5`, 3 execuções cada, no `mergedataset` (cerca de 5.700 chamadas, gera custo na API):

   ```
   docker compose run --rm detector
   ```

   Tudo que vem depois de `detector` substitui o padrão e é repassado ao `src.experiment`, então comece pelo diretório de saída. Para testar com o dataset `toy` (1 modelo, 24 chamadas):

   ```
   docker compose run --rm detector results/teste --models claude-haiku-5-5 --runs 1 --dataset toy
   ```

   Outras opções, por exemplo `--cache`:

   ```
   docker compose run --rm detector results/v4 --cache
   ```

   Para uma execução avulsa (um modelo, uma vez), use o `src.conflict_detector` (opções em [Execução](#execucao)):

   ```
   docker compose run --rm --entrypoint python detector -m src.conflict_detector --provider anthropic --model claude-sonnet-5-5
   ```

5. **Veja o resultado** em `results/experiment/` (CSVs e relatórios, veja [Várias execuções e modelos](#várias-execuções-e-modelos)). A pasta `results/` do container é a mesma do seu computador (volume), então os arquivos continuam lá depois que o container termina.

## Gerando métricas e relatórios

O experimento já gera os relatórios no fim. Para gerá-los de novo, ou para outros resultados, os módulos de métricas também rodam no container; basta trocar o entrypoint:

```
docker compose run --rm --entrypoint python detector -m src.metrics results/<arquivo>_response.csv
docker compose run --rm --entrypoint python detector -m src.reports results/v2
```

## Usando um dataset próprio

A pasta `data/` é montada no container, então um novo dataset em `data/<nome>/dataset.csv` (veja [Datasets](#datasets)) fica disponível sem reconstruir a imagem. Qualquer pasta de `data/` com um `dataset.csv` é aceita por `--dataset`.

## Problemas comuns

| Sintoma | Causa e solução |
|---|---|
| `env file .env not found` | Falta criar o `.env` (passo 2). |
| Erro de autenticação da Anthropic | Chave ausente ou incorreta no `.env`; confira `ANTHROPIC_API_KEY`. |
| `permission denied` ao apagar ou editar arquivos de `results/` | O container roda como root e criou os arquivos. Rode com `--user "$(id -u):$(id -g)"` (ex.: `docker compose run --rm --user "$(id -u):$(id -g)" detector`) ou ajuste com `sudo chown -R $USER results`. |
| Mudei o código e nada mudou | Reconstrua a imagem: `docker compose build`. |
| Execução longa interrompida | Rode o mesmo comando de novo: as execuções que já têm CSV são puladas e o experimento continua de onde parou. |
