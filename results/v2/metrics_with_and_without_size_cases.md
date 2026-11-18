# Métricas — v2, com e sem os 6 casos de tamanho derivado

- Dataset completo: 79 casos (29 YES, 50 NO). Sem os 6 casos: 73 casos (23 YES, 50 NO).
- Casos removidos (todos YES): `antlr4__69ff2669__Python2Target#python2Keywords`, `antlr4__69ff2669__Python3Target#python3Keywords`, `cloud-slang__20bac30d__SlangImpl#getAllEventTypes`, `elasticsearch__d8968869__IndexScopedSettings#BUILT_IN_INDEX_SETTINGS`, `fitnesse__4d9ba9d2__SlimTableFactory#SlimTableFactory`, `fitnesse__4d9ba9d2__SlimTableFactoryTest#setUp`.
- Métricas da classe YES, calculadas com `src/metrics.py` sobre as chamadas com resposta YES/NO. A linha de média é a média aritmética das métricas de cada execução.

## `few_shot_guided_both` — Dataset completo

| Modelo | Execução | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN |
|---|---|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 1 | 74,7% | 64,5% | 69,0% | 0,67 | 78,0% | 20 | 39 | 11 | 9 |
| claude-haiku-5-5 | 2 | 72,2% | 60,6% | 69,0% | 0,65 | 74,0% | 20 | 37 | 13 | 9 |
| claude-haiku-5-5 | 3 | 73,4% | 61,8% | 72,4% | 0,67 | 74,0% | 21 | 37 | 13 | 8 |
| **claude-haiku-5-5** | **média** | **73,4%** | **62,3%** | **70,1%** | **0,66** | **75,3%** |  |  |  |  |
| claude-sonnet-5-5 | 1 | 65,8% | 62,5% | 17,2% | 0,27 | 94,0% | 5 | 47 | 3 | 24 |
| claude-sonnet-5-5 | 2 | 69,6% | 77,8% | 24,1% | 0,37 | 96,0% | 7 | 48 | 2 | 22 |
| claude-sonnet-5-5 | 3 | 69,6% | 77,8% | 24,1% | 0,37 | 96,0% | 7 | 48 | 2 | 22 |
| **claude-sonnet-5-5** | **média** | **68,4%** | **72,7%** | **21,8%** | **0,34** | **95,3%** |  |  |  |  |
| claude-opus-5-5 | 1 | 69,6% | 72,7% | 27,6% | 0,40 | 94,0% | 8 | 47 | 3 | 21 |

## `few_shot_guided_both` — Sem os 6 casos

| Modelo | Execução | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN |
|---|---|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 1 | 74,0% | 57,7% | 65,2% | 0,61 | 78,0% | 15 | 39 | 11 | 8 |
| claude-haiku-5-5 | 2 | 74,0% | 56,7% | 73,9% | 0,64 | 74,0% | 17 | 37 | 13 | 6 |
| claude-haiku-5-5 | 3 | 71,2% | 53,6% | 65,2% | 0,59 | 74,0% | 15 | 37 | 13 | 8 |
| **claude-haiku-5-5** | **média** | **73,1%** | **56,0%** | **68,1%** | **0,61** | **75,3%** |  |  |  |  |
| claude-sonnet-5-5 | 1 | 71,2% | 62,5% | 21,7% | 0,32 | 94,0% | 5 | 47 | 3 | 18 |
| claude-sonnet-5-5 | 2 | 75,3% | 77,8% | 30,4% | 0,44 | 96,0% | 7 | 48 | 2 | 16 |
| claude-sonnet-5-5 | 3 | 75,3% | 77,8% | 30,4% | 0,44 | 96,0% | 7 | 48 | 2 | 16 |
| **claude-sonnet-5-5** | **média** | **74,0%** | **72,7%** | **27,5%** | **0,40** | **95,3%** |  |  |  |  |
| claude-opus-5-5 | 1 | 74,0% | 70,0% | 30,4% | 0,42 | 94,0% | 7 | 47 | 3 | 16 |

## Todos os prompts — Dataset completo

| Modelo | Execução | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN |
|---|---|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 1 | 72,1% | 62,5% | 60,3% | 0,61 | 78,9% | 140 | 315 | 84 | 92 |
| claude-haiku-5-5 | 2 | 69,5% | 58,4% | 58,2% | 0,58 | 76,0% | 135 | 304 | 96 | 97 |
| claude-haiku-5-5 | 3 | 73,7% | 65,3% | 60,8% | 0,63 | 81,2% | 141 | 324 | 75 | 91 |
| **claude-haiku-5-5** | **média** | **71,8%** | **62,1%** | **59,8%** | **0,61** | **78,7%** |  |  |  |  |
| claude-sonnet-5-5 | 1 | 65,3% | 61,4% | 15,1% | 0,24 | 94,5% | 35 | 378 | 22 | 197 |
| claude-sonnet-5-5 | 2 | 65,8% | 63,3% | 16,4% | 0,26 | 94,5% | 38 | 378 | 22 | 194 |
| claude-sonnet-5-5 | 3 | 66,8% | 67,2% | 18,5% | 0,29 | 94,8% | 43 | 379 | 21 | 189 |
| **claude-sonnet-5-5** | **média** | **66,0%** | **64,0%** | **16,7%** | **0,26** | **94,6%** |  |  |  |  |
| claude-opus-5-5 | 1 | 68,7% | 72,9% | 26,8% | 0,39 | 94,0% | 62 | 359 | 23 | 169 |

## Todos os prompts — Sem os 6 casos

| Modelo | Execução | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN |
|---|---|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 1 | 72,4% | 56,0% | 58,2% | 0,57 | 78,9% | 107 | 315 | 84 | 77 |
| claude-haiku-5-5 | 2 | 70,5% | 52,9% | 58,7% | 0,56 | 76,0% | 108 | 304 | 96 | 76 |
| claude-haiku-5-5 | 3 | 73,4% | 58,1% | 56,5% | 0,57 | 81,2% | 104 | 324 | 75 | 80 |
| **claude-haiku-5-5** | **média** | **72,1%** | **55,7%** | **57,8%** | **0,57** | **78,7%** |  |  |  |  |
| claude-sonnet-5-5 | 1 | 70,5% | 60,7% | 18,5% | 0,28 | 94,5% | 34 | 378 | 22 | 150 |
| claude-sonnet-5-5 | 2 | 71,2% | 63,3% | 20,7% | 0,31 | 94,5% | 38 | 378 | 22 | 146 |
| claude-sonnet-5-5 | 3 | 72,3% | 67,2% | 23,4% | 0,35 | 94,8% | 43 | 379 | 21 | 141 |
| **claude-sonnet-5-5** | **média** | **71,3%** | **63,7%** | **20,8%** | **0,31** | **94,6%** |  |  |  |  |
| claude-opus-5-5 | 1 | 73,1% | 70,1% | 29,5% | 0,42 | 94,0% | 54 | 359 | 23 | 129 |
