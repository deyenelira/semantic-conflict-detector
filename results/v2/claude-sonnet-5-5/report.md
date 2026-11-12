# Relatório do modelo — `claude-sonnet-5-5`

- **Execuções:** 3 (`1.csv`, `2.csv`, `3.csv`)
- **Casos:** 79 (29 YES, 50 NO); **prompts:** 8; **chamadas por execução:** 632
- As métricas aparecem como média entre as execuções, com o intervalo (mín–máx) entre parênteses, e consideram só as chamadas com resposta YES/NO.

## 1. Resultado por execução

| Execução | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| 1.csv | 65,3% | 61,4% | 15,1% | 0,24 | 94,5% | 35 | 378 | 22 | 197 | 0 |
| 2.csv | 65,8% | 63,3% | 16,4% | 0,26 | 94,5% | 38 | 378 | 22 | 194 | 0 |
| 3.csv | 66,8% | 67,2% | 18,5% | 0,29 | 94,8% | 43 | 379 | 21 | 189 | 0 |

|  | Acurácia | Precisão | Recall | F1 | Especificidade | Sem resposta (soma) |
|---|---|---|---|---|---|---|
| média | 66,0% (65,3%–66,8%) | 64,0% (61,4%–67,2%) | 16,7% (15,1%–18,5%) | 0,26 (0,24–0,29) | 94,6% (94,5%–94,8%) | 0 |

## 2. Resultado por prompt

| Prompt | Acurácia | Precisão | Recall | F1 | Especificidade | Sem resposta (soma) |
|---|---|---|---|---|---|---|
| zero_shot_guided_none | 64,1% (63,3%–65,8%) | 55,6% (50,0%–66,7%) | 13,8% | 0,22 (0,22–0,23) | 93,3% (92,0%–96,0%) | 0 |
| zero_shot_guided_summaries | 65,4% (64,6%–67,1%) | 60,8% (55,6%–71,4%) | 17,2% | 0,27 (0,26–0,28) | 93,3% (92,0%–96,0%) | 0 |
| zero_shot_guided_target | 66,2% (64,6%–69,6%) | 66,7% (57,1%–85,7%) | 16,1% (13,8%–20,7%) | 0,26 (0,22–0,33) | 95,3% (94,0%–98,0%) | 0 |
| zero_shot_guided_both | 67,1% (65,8%–69,6%) | 71,6% (62,5%–85,7%) | 17,2% (13,8%–20,7%) | 0,28 (0,23–0,33) | 96,0% (94,0%–98,0%) | 0 |
| few_shot_guided_none | 63,3% (62,0%–64,6%) | 50,0% (42,9%–57,1%) | 12,6% (10,3%–13,8%) | 0,20 (0,17–0,22) | 92,7% (92,0%–94,0%) | 0 |
| few_shot_guided_summaries | 65,4% (63,3%–67,1%) | 59,7% (50,0%–66,7%) | 17,2% (13,8%–20,7%) | 0,27 (0,22–0,32) | 93,3% (92,0%–94,0%) | 0 |
| few_shot_guided_target | 67,9% (65,8%–69,6%) | 78,6% (66,7%–85,7%) | 17,2% (13,8%–20,7%) | 0,28 (0,23–0,33) | 97,3% (96,0%–98,0%) | 0 |
| few_shot_guided_both | 68,4% (65,8%–69,6%) | 72,7% (62,5%–77,8%) | 21,8% (17,2%–24,1%) | 0,34 (0,27–0,37) | 95,3% (94,0%–96,0%) | 0 |

## 3. Efeito de cada fator

### Zero-shot vs. few-shot (somando as variantes de contexto)

| Tipo | Acurácia | Precisão | Recall | F1 | Especificidade | Sem resposta (soma) |
|---|---|---|---|---|---|---|
| zero-shot | 65,7% (65,2%–66,1%) | 62,9% (60,7%–65,5%) | 16,1% (14,7%–17,2%) | 0,26 (0,24–0,27) | 94,5% (94,0%–95,0%) | 0 |
| few-shot | 66,2% (65,5%–67,7%) | 65,1% (61,3%–71,9%) | 17,2% (15,5%–19,8%) | 0,27 (0,25–0,31) | 94,7% (94,0%–95,5%) | 0 |

### Contexto fornecido (somando zero-shot e few-shot)

| Contexto | Acurácia | Precisão | Recall | F1 | Especificidade | Sem resposta (soma) |
|---|---|---|---|---|---|---|
| none | 63,7% (62,7%–64,6%) | 52,4% (46,7%–57,1%) | 13,2% (12,1%–13,8%) | 0,21 (0,19–0,22) | 93,0% (92,0%–94,0%) | 0 |
| summaries | 65,4% (63,9%–66,5%) | 60,2% (52,9%–66,7%) | 17,2% (15,5%–19,0%) | 0,27 (0,24–0,29) | 93,3% (92,0%–95,0%) | 0 |
| target | 67,1% (65,2%–69,6%) | 72,2% (61,5%–85,7%) | 16,7% (13,8%–20,7%) | 0,27 (0,23–0,33) | 96,3% (95,0%–98,0%) | 0 |
| both | 67,7% (65,8%–69,6%) | 72,0% (64,3%–81,2%) | 19,5% (15,5%–22,4%) | 0,31 (0,25–0,35) | 95,7% (95,0%–97,0%) | 0 |

## 4. Estabilidade entre as execuções

Chamadas (caso e prompt) respondidas em todas as execuções e quantas delas tiveram a mesma resposta em todas:

| Prompt | Respondidas em todas | Mesma resposta | Estabilidade |
|---|---|---|---|
| zero_shot_guided_none | 79 | 74 | 93,7% |
| zero_shot_guided_summaries | 79 | 72 | 91,1% |
| zero_shot_guided_target | 79 | 74 | 93,7% |
| zero_shot_guided_both | 79 | 73 | 92,4% |
| few_shot_guided_none | 79 | 77 | 97,5% |
| few_shot_guided_summaries | 79 | 73 | 92,4% |
| few_shot_guided_target | 79 | 76 | 96,2% |
| few_shot_guided_both | 79 | 73 | 92,4% |
| todos | 632 | 592 | 93,7% |

Casos com respostas YES e NO entre as execuções: 14/79. Os 10 com mais prompts divergentes:

| Caso | Esperado | Prompts divergentes |
|---|---|---|
| pushy__58901c84__PushManager#handleConnectionClosure | NO | 7/8 |
| jOOQ__d96120f3__DSL#coalesce | NO | 5/8 |
| spring-boot__6664ce19__AtomikosPropertiesTests#testProperties | YES | 5/8 |
| storm__ad2be678__KafkaSpoutConfig#toString | YES | 4/8 |
| activiti__50d8e43e__DeploymentEntityManager#deleteDeployment | YES | 4/8 |
| pushy__58901c84__PushManager#handleConnectionFailure | NO | 4/8 |
| spring-boot__6664ce19__AtomikosPropertiesTests#testDefaultProperties | YES | 2/8 |
| elasticsearch-river-mongodb__3d4f9951__Slurper#assignCollections | YES | 2/8 |
| elasticsearch-river-mongodb__6b6ce8e8__Slurper#run | NO | 2/8 |
| antlr4__69ff2669__Python2Target#python2Keywords | YES | 1/8 |

## 5. Resposta da maioria das execuções

Para cada caso e prompt, a resposta dada pela maioria das execuções. Empates (ex.: uma execução sem resposta e as outras divergindo) contam como "Sem resposta".

| Prompt | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| zero_shot_guided_none | 64,6% | 57,1% | 13,8% | 0,22 | 94,0% | 4 | 47 | 3 | 25 | 0 |
| zero_shot_guided_summaries | 65,8% | 62,5% | 17,2% | 0,27 | 94,0% | 5 | 47 | 3 | 24 | 0 |
| zero_shot_guided_target | 65,8% | 66,7% | 13,8% | 0,23 | 96,0% | 4 | 48 | 2 | 25 | 0 |
| zero_shot_guided_both | 67,1% | 71,4% | 17,2% | 0,28 | 96,0% | 5 | 48 | 2 | 24 | 0 |
| few_shot_guided_none | 63,3% | 50,0% | 13,8% | 0,22 | 92,0% | 4 | 46 | 4 | 25 | 0 |
| few_shot_guided_summaries | 64,6% | 55,6% | 17,2% | 0,26 | 92,0% | 5 | 46 | 4 | 24 | 0 |
| few_shot_guided_target | 68,4% | 83,3% | 17,2% | 0,29 | 98,0% | 5 | 49 | 1 | 24 | 0 |
| few_shot_guided_both | 65,8% | 62,5% | 17,2% | 0,27 | 94,0% | 5 | 47 | 3 | 24 | 0 |
| todos | 65,7% | 62,7% | 15,9% | 0,25 | 94,5% | 37 | 378 | 22 | 195 | 0 |

## 6. Chamadas sem resposta YES/NO por execução

| Execução | Ignoradas (prompt grande demais) | Erros | Recusas | Fora do formato |
|---|---|---|---|---|
| 1.csv | 0 | 0 | 0 | 0 |
| 2.csv | 0 | 0 | 0 | 0 |
| 3.csv | 0 | 0 | 0 | 0 |
