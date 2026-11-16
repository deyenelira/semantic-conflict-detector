# Relatório do modelo — `claude-opus-5-5`

- **Execuções:** 1 (`1.csv`)
- **Casos:** 79 (29 YES, 50 NO); **prompts:** 8; **chamadas por execução:** 632
- As métricas aparecem como média entre as execuções, com o intervalo (mín–máx) entre parênteses, e consideram só as chamadas com resposta YES/NO.

## 1. Resultado por execução

| Execução | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| 1.csv | 68,7% | 72,9% | 26,8% | 0,39 | 94,0% | 62 | 359 | 23 | 169 | 19 |

|  | Acurácia | Precisão | Recall | F1 | Especificidade | Sem resposta (soma) |
|---|---|---|---|---|---|---|
| média | 68,7% | 72,9% | 26,8% | 0,39 | 94,0% | 19 |

## 2. Resultado por prompt

| Prompt | Acurácia | Precisão | Recall | F1 | Especificidade | Sem resposta (soma) |
|---|---|---|---|---|---|---|
| zero_shot_guided_none | 68,0% | 77,8% | 24,1% | 0,37 | 95,7% | 4 |
| zero_shot_guided_summaries | 72,6% | 72,2% | 46,4% | 0,57 | 88,9% | 6 |
| zero_shot_guided_target | 67,1% | 75,0% | 20,7% | 0,32 | 95,7% | 3 |
| zero_shot_guided_both | 72,0% | 83,3% | 34,5% | 0,49 | 95,7% | 4 |
| few_shot_guided_none | 66,7% | 66,7% | 20,7% | 0,32 | 93,9% | 1 |
| few_shot_guided_summaries | 64,1% | 55,6% | 17,2% | 0,26 | 91,8% | 1 |
| few_shot_guided_target | 69,6% | 77,8% | 24,1% | 0,37 | 96,0% | 0 |
| few_shot_guided_both | 69,6% | 72,7% | 27,6% | 0,40 | 94,0% | 0 |

## 3. Efeito de cada fator

### Zero-shot vs. few-shot (somando as variantes de contexto)

| Tipo | Acurácia | Precisão | Recall | F1 | Especificidade | Sem resposta (soma) |
|---|---|---|---|---|---|---|
| zero-shot | 69,9% | 76,6% | 31,3% | 0,44 | 94,0% | 17 |
| few-shot | 67,5% | 68,4% | 22,4% | 0,34 | 93,9% | 2 |

### Contexto fornecido (somando zero-shot e few-shot)

| Contexto | Acurácia | Precisão | Recall | F1 | Especificidade | Sem resposta (soma) |
|---|---|---|---|---|---|---|
| none | 67,3% | 72,2% | 22,4% | 0,34 | 94,7% | 5 |
| summaries | 68,2% | 66,7% | 31,6% | 0,43 | 90,4% | 7 |
| target | 68,4% | 76,5% | 22,4% | 0,35 | 95,9% | 3 |
| both | 70,8% | 78,3% | 31,0% | 0,44 | 94,8% | 4 |

## 4. Estabilidade entre as execuções

Chamadas (caso e prompt) respondidas em todas as execuções e quantas delas tiveram a mesma resposta em todas:

| Prompt | Respondidas em todas | Mesma resposta | Estabilidade |
|---|---|---|---|
| zero_shot_guided_none | 75 | 75 | 100,0% |
| zero_shot_guided_summaries | 73 | 73 | 100,0% |
| zero_shot_guided_target | 76 | 76 | 100,0% |
| zero_shot_guided_both | 75 | 75 | 100,0% |
| few_shot_guided_none | 78 | 78 | 100,0% |
| few_shot_guided_summaries | 78 | 78 | 100,0% |
| few_shot_guided_target | 79 | 79 | 100,0% |
| few_shot_guided_both | 79 | 79 | 100,0% |
| todos | 613 | 613 | 100,0% |

Nenhum caso teve respostas diferentes entre as execuções.

## 5. Resposta da maioria das execuções

Para cada caso e prompt, a resposta dada pela maioria das execuções. Empates (ex.: uma execução sem resposta e as outras divergindo) contam como "Sem resposta".

| Prompt | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| zero_shot_guided_none | 68,0% | 77,8% | 24,1% | 0,37 | 95,7% | 7 | 44 | 2 | 22 | 4 |
| zero_shot_guided_summaries | 72,6% | 72,2% | 46,4% | 0,57 | 88,9% | 13 | 40 | 5 | 15 | 6 |
| zero_shot_guided_target | 67,1% | 75,0% | 20,7% | 0,32 | 95,7% | 6 | 45 | 2 | 23 | 3 |
| zero_shot_guided_both | 72,0% | 83,3% | 34,5% | 0,49 | 95,7% | 10 | 44 | 2 | 19 | 4 |
| few_shot_guided_none | 66,7% | 66,7% | 20,7% | 0,32 | 93,9% | 6 | 46 | 3 | 23 | 1 |
| few_shot_guided_summaries | 64,1% | 55,6% | 17,2% | 0,26 | 91,8% | 5 | 45 | 4 | 24 | 1 |
| few_shot_guided_target | 69,6% | 77,8% | 24,1% | 0,37 | 96,0% | 7 | 48 | 2 | 22 | 0 |
| few_shot_guided_both | 69,6% | 72,7% | 27,6% | 0,40 | 94,0% | 8 | 47 | 3 | 21 | 0 |
| todos | 68,7% | 72,9% | 26,8% | 0,39 | 94,0% | 62 | 359 | 23 | 169 | 19 |

## 6. Chamadas sem resposta YES/NO por execução

| Execução | Ignoradas (prompt grande demais) | Erros | Recusas | Fora do formato |
|---|---|---|---|---|
| 1.csv | 0 | 0 | 19 | 0 |
