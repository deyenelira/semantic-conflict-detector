# Relatório do modelo — `claude-haiku-5-5`

- **Execuções:** 3 (`1.csv`, `2.csv`, `3.csv`)
- **Casos:** 79 (29 YES, 50 NO); **prompts:** 8; **chamadas por execução:** 632
- As métricas aparecem como média entre as execuções, com o intervalo (mín–máx) entre parênteses, e consideram só as chamadas com resposta YES/NO.

## 1. Resultado por execução

| Execução | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| 1.csv | 72,1% | 62,5% | 60,3% | 0,61 | 78,9% | 140 | 315 | 84 | 92 | 1 |
| 2.csv | 69,5% | 58,4% | 58,2% | 0,58 | 76,0% | 135 | 304 | 96 | 97 | 0 |
| 3.csv | 73,7% | 65,3% | 60,8% | 0,63 | 81,2% | 141 | 324 | 75 | 91 | 1 |

|  | Acurácia | Precisão | Recall | F1 | Especificidade | Sem resposta (soma) |
|---|---|---|---|---|---|---|
| média | 71,8% (69,5%–73,7%) | 62,1% (58,4%–65,3%) | 59,8% (58,2%–60,8%) | 0,61 (0,58–0,63) | 78,7% (76,0%–81,2%) | 2 |

## 2. Resultado por prompt

| Prompt | Acurácia | Precisão | Recall | F1 | Especificidade | Sem resposta (soma) |
|---|---|---|---|---|---|---|
| zero_shot_guided_none | 68,4% (63,3%–70,9%) | 58,7% (50,0%–63,6%) | 48,3% (44,8%–51,7%) | 0,53 (0,47–0,57) | 80,0% (74,0%–84,0%) | 0 |
| zero_shot_guided_summaries | 72,6% (70,9%–75,9%) | 64,4% (61,5%–69,2%) | 56,3% (51,7%–62,1%) | 0,60 (0,57–0,65) | 82,0% (80,0%–84,0%) | 0 |
| zero_shot_guided_target | 76,7% (75,9%–77,2%) | 72,2% (72,0%–72,7%) | 59,8% (55,2%–62,1%) | 0,65 (0,63–0,67) | 86,6% (85,7%–88,0%) | 1 |
| zero_shot_guided_both | 74,7% (72,2%–77,2%) | 66,1% (61,3%–70,4%) | 64,4% (62,1%–65,5%) | 0,65 (0,63–0,68) | 80,7% (76,0%–84,0%) | 0 |
| few_shot_guided_none | 67,8% (64,1%–74,7%) | 56,4% (51,7%–65,5%) | 55,2% (48,3%–65,5%) | 0,56 (0,50–0,66) | 75,2% (72,0%–80,0%) | 1 |
| few_shot_guided_summaries | 69,2% (64,6%–74,7%) | 58,3% (51,5%–66,7%) | 59,8% (58,6%–62,1%) | 0,59 (0,55–0,64) | 74,7% (68,0%–82,0%) | 0 |
| few_shot_guided_target | 71,3% (68,4%–77,2%) | 60,2% (56,2%–67,7%) | 64,4% (58,6%–72,4%) | 0,62 (0,58–0,70) | 75,3% (72,0%–80,0%) | 0 |
| few_shot_guided_both | 73,4% (72,2%–74,7%) | 62,3% (60,6%–64,5%) | 70,1% (69,0%–72,4%) | 0,66 (0,65–0,67) | 75,3% (74,0%–78,0%) | 0 |

## 3. Efeito de cada fator

### Zero-shot vs. few-shot (somando as variantes de contexto)

| Tipo | Acurácia | Precisão | Recall | F1 | Especificidade | Sem resposta (soma) |
|---|---|---|---|---|---|---|
| zero-shot | 73,1% (71,5%–75,0%) | 65,3% (62,5%–69,1%) | 57,2% (56,0%–57,8%) | 0,61 (0,59–0,63) | 82,3% (80,5%–85,0%) | 1 |
| few-shot | 70,4% (67,4%–72,4%) | 59,4% (55,1%–62,2%) | 62,4% (60,3%–63,8%) | 0,61 (0,58–0,63) | 75,1% (71,5%–77,4%) | 1 |

### Contexto fornecido (somando zero-shot e few-shot)

| Contexto | Acurácia | Precisão | Recall | F1 | Especificidade | Sem resposta (soma) |
|---|---|---|---|---|---|---|
| none | 68,1% (63,9%–72,8%) | 57,4% (50,9%–64,2%) | 51,7% (48,3%–58,6%) | 0,54 (0,50–0,61) | 77,6% (73,0%–81,0%) | 1 |
| summaries | 70,9% (67,7%–75,3%) | 61,0% (55,9%–67,9%) | 58,0% (55,2%–62,1%) | 0,59 (0,56–0,65) | 78,3% (74,0%–83,0%) | 0 |
| target | 74,0% (72,6%–76,6%) | 65,5% (63,2%–69,8%) | 62,1% (60,3%–63,8%) | 0,64 (0,62–0,67) | 80,9% (79,0%–84,0%) | 1 |
| both | 74,1% (73,4%–75,3%) | 63,9% (62,9%–65,6%) | 67,2% (65,5%–69,0%) | 0,66 (0,64–0,67) | 78,0% (77,0%–79,0%) | 0 |

## 4. Estabilidade entre as execuções

Chamadas (caso e prompt) respondidas em todas as execuções e quantas delas tiveram a mesma resposta em todas:

| Prompt | Respondidas em todas | Mesma resposta | Estabilidade |
|---|---|---|---|
| zero_shot_guided_none | 79 | 55 | 69,6% |
| zero_shot_guided_summaries | 79 | 56 | 70,9% |
| zero_shot_guided_target | 78 | 59 | 75,6% |
| zero_shot_guided_both | 79 | 60 | 75,9% |
| few_shot_guided_none | 78 | 60 | 76,9% |
| few_shot_guided_summaries | 79 | 59 | 74,7% |
| few_shot_guided_target | 79 | 58 | 73,4% |
| few_shot_guided_both | 79 | 62 | 78,5% |
| todos | 630 | 469 | 74,4% |

Casos com respostas YES e NO entre as execuções: 45/79. Os 10 com mais prompts divergentes:

| Caso | Esperado | Prompts divergentes |
|---|---|---|
| spring-boot__af20dc6c__ExplodedArchive#getUrl | YES | 8/8 |
| hector__a33a4650__HThriftClient#open | NO | 8/8 |
| pushy__58901c84__PushManager#handleConnectionFailure | NO | 7/8 |
| storm__bd1f5c54__KafkaSpout#emitTupleIfNotEmitted | NO | 6/8 |
| netty__193acdb3__LengthFieldBasedFrameDecoder#decode | YES | 6/8 |
| pushy__58901c84__PushManager#handleConnectionClosure | NO | 6/8 |
| elasticsearch__d8968869__TransportReplicationAction#doRun | YES | 6/8 |
| elasticsearch__d8968869__TransportDeleteAction#executeDeleteRequestOnPrimary | NO | 6/8 |
| OpenTripPlanner__4c506dce__MultiShortestPathTree#dominates | YES | 5/8 |
| hector__a33a4650__HKerberosThriftClient#open | NO | 5/8 |

## 5. Resposta da maioria das execuções

Para cada caso e prompt, a resposta dada pela maioria das execuções. Empates (ex.: uma execução sem resposta e as outras divergindo) contam como "Sem resposta".

| Prompt | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| zero_shot_guided_none | 68,4% | 58,3% | 48,3% | 0,53 | 80,0% | 14 | 40 | 10 | 15 | 0 |
| zero_shot_guided_summaries | 69,6% | 60,0% | 51,7% | 0,56 | 80,0% | 15 | 40 | 10 | 14 | 0 |
| zero_shot_guided_target | 80,8% | 81,8% | 62,1% | 0,71 | 91,8% | 18 | 45 | 4 | 11 | 1 |
| zero_shot_guided_both | 75,9% | 67,9% | 65,5% | 0,67 | 82,0% | 19 | 41 | 9 | 10 | 0 |
| few_shot_guided_none | 67,9% | 57,7% | 51,7% | 0,55 | 77,6% | 15 | 38 | 11 | 14 | 1 |
| few_shot_guided_summaries | 68,4% | 56,2% | 62,1% | 0,59 | 72,0% | 18 | 36 | 14 | 11 | 0 |
| few_shot_guided_target | 73,4% | 62,5% | 69,0% | 0,66 | 76,0% | 20 | 38 | 12 | 9 | 0 |
| few_shot_guided_both | 74,7% | 63,6% | 72,4% | 0,68 | 76,0% | 21 | 38 | 12 | 8 | 0 |
| todos | 72,4% | 63,1% | 60,3% | 0,62 | 79,4% | 140 | 316 | 82 | 92 | 2 |

## 6. Chamadas sem resposta YES/NO por execução

| Execução | Ignoradas (prompt grande demais) | Erros | Recusas | Fora do formato |
|---|---|---|---|---|
| 1.csv | 0 | 0 | 0 | 1 |
| 2.csv | 0 | 0 | 0 | 0 |
| 3.csv | 0 | 0 | 0 | 1 |
