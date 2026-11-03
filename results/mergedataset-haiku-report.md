# Relatório por prompt — `mergedataset_anthropic_20261102-213704_response.csv`

- **Dataset:** `mergedataset` — 79 casos (29 YES, 50 NO)
- **Provedor:** `anthropic`
- **Prompts:** 8; **chamadas:** 632
- **Sem resposta YES/NO:** fora do formato: 2
- As métricas consideram só as chamadas com resposta YES/NO; as demais aparecem em "Sem resposta".

## 1. Resultado geral

| Chamadas | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| todas | 71,7% | 62,4% | 57,6% | 0,60 | 79,9% | 133 | 319 | 80 | 98 | 2 |

Baseline: sempre responder "NO" daria 63,3% de acurácia (400/632). Proporção real de YES nas chamadas: 36,7%.

## 2. Resultado por prompt

| Prompt | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| zero_shot_guided_none | 73,1% | 65,4% | 58,6% | 0,62 | 81,6% | 17 | 40 | 9 | 12 | 1 |
| zero_shot_guided_summaries | 65,8% | 54,2% | 44,8% | 0,49 | 78,0% | 13 | 39 | 11 | 16 | 0 |
| zero_shot_guided_target | 73,4% | 65,4% | 58,6% | 0,62 | 82,0% | 17 | 41 | 9 | 12 | 0 |
| zero_shot_guided_both | 73,1% | 63,0% | 60,7% | 0,62 | 80,0% | 17 | 40 | 10 | 11 | 1 |
| few_shot_guided_none | 70,9% | 60,7% | 58,6% | 0,60 | 78,0% | 17 | 39 | 11 | 12 | 0 |
| few_shot_guided_summaries | 68,4% | 56,7% | 58,6% | 0,58 | 74,0% | 17 | 37 | 13 | 12 | 0 |
| few_shot_guided_target | 77,2% | 72,0% | 62,1% | 0,67 | 86,0% | 18 | 43 | 7 | 11 | 0 |
| few_shot_guided_both | 72,2% | 63,0% | 58,6% | 0,61 | 80,0% | 17 | 40 | 10 | 12 | 0 |

| Prompt | Respostas YES | Respostas NO | Sem resposta | % YES (das respondidas) |
|---|---|---|---|---|
| zero_shot_guided_none | 26 | 52 | 1 | 33,3% |
| zero_shot_guided_summaries | 24 | 55 | 0 | 30,4% |
| zero_shot_guided_target | 26 | 53 | 0 | 32,9% |
| zero_shot_guided_both | 27 | 51 | 1 | 34,6% |
| few_shot_guided_none | 28 | 51 | 0 | 35,4% |
| few_shot_guided_summaries | 30 | 49 | 0 | 38,0% |
| few_shot_guided_target | 25 | 54 | 0 | 31,6% |
| few_shot_guided_both | 27 | 52 | 0 | 34,2% |

## 3. Efeito de cada fator

### Zero-shot vs. few-shot (somando as variantes de contexto)

| Tipo | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| zero-shot | 71,3% | 62,1% | 55,7% | 0,59 | 80,4% | 64 | 160 | 39 | 51 | 2 |
| few-shot | 72,2% | 62,7% | 59,5% | 0,61 | 79,5% | 69 | 159 | 41 | 47 | 0 |

### Contexto fornecido (somando zero-shot e few-shot)

| Contexto | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| none | 72,0% | 63,0% | 58,6% | 0,61 | 79,8% | 34 | 79 | 20 | 24 | 1 |
| summaries | 67,1% | 55,6% | 51,7% | 0,54 | 76,0% | 30 | 76 | 24 | 28 | 0 |
| target | 75,3% | 68,6% | 60,3% | 0,64 | 84,0% | 35 | 84 | 16 | 23 | 0 |
| both | 72,6% | 63,0% | 59,6% | 0,61 | 80,0% | 34 | 80 | 20 | 23 | 1 |

## 4. Concordância entre os prompts

Votos "YES" por caso, somando os 8 prompts (chamadas sem resposta não contam como YES):

| Votos YES (de 8) | Casos YES reais | Casos NO reais |
|---|---|---|
| 0 | 3 | 27 |
| 1 | 1 | 6 |
| 2 | 4 | 5 |
| 3 | 2 | 1 |
| 4 | 4 | 5 |
| 5 | 3 | 0 |
| 6 | 3 | 3 |
| 7 | 3 | 1 |
| 8 | 6 | 2 |

- YES reais que nenhum prompt detectou: 3/29
- NO reais marcados como YES por ≥1 prompt: 23/50

Ensemble por voto (por caso, 79 casos):

| Regra (YES se…) | Acurácia | Precisão | Recall | F1 | TP | FP |
|---|---|---|---|---|---|---|
| ≥1 de 8 | 67,1% | 53,1% | 89,7% | 0,67 | 26 | 23 |
| ≥2 de 8 | 73,4% | 59,5% | 86,2% | 0,70 | 25 | 17 |
| ≥3 de 8 | 74,7% | 63,6% | 72,4% | 0,68 | 21 | 12 |
| ≥4 de 8 | 73,4% | 63,3% | 65,5% | 0,64 | 19 | 11 |
| ≥5 de 8 | 74,7% | 71,4% | 51,7% | 0,60 | 15 | 6 |
| ≥6 de 8 | 70,9% | 66,7% | 41,4% | 0,51 | 12 | 6 |
| ≥7 de 8 | 70,9% | 75,0% | 31,0% | 0,44 | 9 | 3 |
| ≥8 de 8 | 68,4% | 75,0% | 20,7% | 0,32 | 6 | 2 |

Concordância par a par (mesma resposta, sobre os casos respondidos pelos dois prompts):

|  | zero_shot_guided_none | zero_shot_guided_summaries | zero_shot_guided_target | zero_shot_guided_both | few_shot_guided_none | few_shot_guided_summaries | few_shot_guided_target | few_shot_guided_both |
|---|---|---|---|---|---|---|---|---|
| **zero_shot_guided_none** | 100,0% | 83,3% | 75,6% | 84,4% | 83,3% | 76,9% | 73,1% | 73,1% |
| **zero_shot_guided_summaries** | 83,3% | 100,0% | 77,2% | 80,8% | 89,9% | 79,7% | 70,9% | 81,0% |
| **zero_shot_guided_target** | 75,6% | 77,2% | 100,0% | 80,8% | 77,2% | 69,6% | 73,4% | 70,9% |
| **zero_shot_guided_both** | 84,4% | 80,8% | 80,8% | 100,0% | 80,8% | 79,5% | 73,1% | 82,1% |
| **few_shot_guided_none** | 83,3% | 89,9% | 77,2% | 80,8% | 100,0% | 77,2% | 70,9% | 78,5% |
| **few_shot_guided_summaries** | 76,9% | 79,7% | 69,6% | 79,5% | 77,2% | 100,0% | 78,5% | 83,5% |
| **few_shot_guided_target** | 73,1% | 70,9% | 73,4% | 73,1% | 70,9% | 78,5% | 100,0% | 77,2% |
| **few_shot_guided_both** | 73,1% | 81,0% | 70,9% | 82,1% | 78,5% | 83,5% | 77,2% | 100,0% |

## 5. Condição violada (A/B/C) nas respostas YES

| Prompt | A | B | C | outra/vazia | Entre os TP: A | B | C |
|---|---|---|---|---|---|---|---|
| zero_shot_guided_none | 1 | 15 | 10 | 0 | 1 | 11 | 5 |
| zero_shot_guided_summaries | 1 | 12 | 11 | 0 | 1 | 9 | 3 |
| zero_shot_guided_target | 2 | 15 | 9 | 0 | 2 | 10 | 5 |
| zero_shot_guided_both | 1 | 13 | 13 | 0 | 1 | 10 | 6 |
| few_shot_guided_none | 1 | 12 | 15 | 0 | 0 | 9 | 8 |
| few_shot_guided_summaries | 0 | 16 | 14 | 0 | 0 | 11 | 6 |
| few_shot_guided_target | 1 | 14 | 10 | 0 | 1 | 12 | 5 |
| few_shot_guided_both | 1 | 14 | 12 | 0 | 1 | 11 | 5 |

O dataset não traz a condição esperada, então não é possível medir a acurácia dessa classificação.

## 6. Resultado por projeto (acertos / chamadas, contando chamadas sem resposta como incorretas)

| Projeto | Casos (YES/NO) | zero_shot_guided_none | zero_shot_guided_summaries | zero_shot_guided_target | zero_shot_guided_both | few_shot_guided_none | few_shot_guided_summaries | few_shot_guided_target | few_shot_guided_both |
|---|---|---|---|---|---|---|---|---|---|
| elasticsearch | 22 (5/17) | 18/22 | 15/22 | 18/22 | 15/22 | 17/22 | 17/22 | 19/22 | 16/22 |
| spring-boot | 10 (5/5) | 7/10 | 7/10 | 6/10 | 7/10 | 8/10 | 8/10 | 7/10 | 8/10 |
| elasticsearch-river-mongodb | 6 (2/4) | 5/6 | 5/6 | 5/6 | 5/6 | 5/6 | 3/6 | 5/6 | 4/6 |
| jsoup | 4 (3/1) | 1/4 | 1/4 | 2/4 | 2/4 | 1/4 | 2/4 | 2/4 | 2/4 |
| hector | 4 (0/4) | 3/4 | 3/4 | 4/4 | 3/4 | 3/4 | 3/4 | 3/4 | 3/4 |
| retrofit | 3 (1/2) | 2/3 | 2/3 | 3/3 | 3/3 | 1/3 | 3/3 | 2/3 | 3/3 |
| storm | 2 (1/1) | 1/2 | 1/2 | 1/2 | 2/2 | 1/2 | 2/2 | 2/2 | 2/2 |
| antlr4 | 2 (2/0) | 2/2 | 2/2 | 1/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 |
| fitnesse | 2 (2/0) | 2/2 | 0/2 | 2/2 | 2/2 | 0/2 | 0/2 | 1/2 | 0/2 |
| okhttp | 2 (0/2) | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 |
| activiti | 2 (1/1) | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 |
| HikariCP | 2 (2/0) | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 2/2 | 2/2 |
| pushy | 2 (0/2) | 0/2 | 0/2 | 1/2 | 1/2 | 0/2 | 0/2 | 2/2 | 1/2 |
| cloud-slang | 1 (1/0) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 0/1 | 0/1 | 1/1 |
| jOOQ | 1 (0/1) | 0/1 | 0/1 | 1/1 | 0/1 | 0/1 | 0/1 | 1/1 | 0/1 |
| swagger-maven-plugin | 1 (1/0) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| SimianArmy | 1 (0/1) | 0/1 | 1/1 | 1/1 | 0/1 | 1/1 | 0/1 | 1/1 | 0/1 |
| titan | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| druid | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| netty | 1 (1/0) | 0/1 | 1/1 | 0/1 | 1/1 | 1/1 | 1/1 | 0/1 | 1/1 |
| OpenTripPlanner | 1 (1/0) | 1/1 | 0/1 | 0/1 | 0/1 | 1/1 | 0/1 | 0/1 | 0/1 |
| webbit | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| eureka | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| atmosphere | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| resty-gwt | 1 (1/0) | 1/1 | 0/1 | 0/1 | 0/1 | 1/1 | 0/1 | 0/1 | 0/1 |
| quickml | 1 (0/1) | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 |
| java-faker | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| swagger-core | 1 (0/1) | 1/1 | 1/1 | 0/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| cucumber-jvm | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |

## 7. Chamadas sem resposta YES/NO

| Prompt | Ignoradas (prompt grande demais) | Erros | Recusas | Fora do formato | Em casos YES | Em casos NO |
|---|---|---|---|---|---|---|
| zero_shot_guided_none | 0 | 0 | 0 | 1 | 0 | 1 |
| zero_shot_guided_summaries | 0 | 0 | 0 | 0 | 0 | 0 |
| zero_shot_guided_target | 0 | 0 | 0 | 0 | 0 | 0 |
| zero_shot_guided_both | 0 | 0 | 0 | 1 | 1 | 0 |
| few_shot_guided_none | 0 | 0 | 0 | 0 | 0 | 0 |
| few_shot_guided_summaries | 0 | 0 | 0 | 0 | 0 | 0 |
| few_shot_guided_target | 0 | 0 | 0 | 0 | 0 | 0 |
| few_shot_guided_both | 0 | 0 | 0 | 0 | 0 | 0 |

## Observações

- Precisão, recall, F1 e especificidade são da classe YES (conflito semântico).
- Cada caso foi avaliado uma única vez por prompt, sem repetições, então não há medida de variância.
