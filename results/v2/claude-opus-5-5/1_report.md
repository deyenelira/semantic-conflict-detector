# Relatório por prompt — `claude-opus-5-5/1.csv`

- **Casos:** 79 (29 YES, 50 NO)
- **Prompts:** 8; **chamadas:** 632
- **Sem resposta YES/NO:** recusa: 19
- As métricas consideram só as chamadas com resposta YES/NO; as demais aparecem em "Sem resposta".

## 1. Resultado geral

| Chamadas | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| todas | 68,7% | 72,9% | 26,8% | 0,39 | 94,0% | 62 | 359 | 23 | 169 | 19 |

Baseline: sempre responder "NO" daria 63,3% de acurácia (400/632). Proporção real de YES nas chamadas: 36,7%.

## 2. Resultado por prompt

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

| Prompt | Respostas YES | Respostas NO | Sem resposta | % YES (das respondidas) |
|---|---|---|---|---|
| zero_shot_guided_none | 9 | 66 | 4 | 12,0% |
| zero_shot_guided_summaries | 18 | 55 | 6 | 24,7% |
| zero_shot_guided_target | 8 | 68 | 3 | 10,5% |
| zero_shot_guided_both | 12 | 63 | 4 | 16,0% |
| few_shot_guided_none | 9 | 69 | 1 | 11,5% |
| few_shot_guided_summaries | 9 | 69 | 1 | 11,5% |
| few_shot_guided_target | 9 | 70 | 0 | 11,4% |
| few_shot_guided_both | 11 | 68 | 0 | 13,9% |

## 3. Efeito de cada fator

### Zero-shot vs. few-shot (somando as variantes de contexto)

| Tipo | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| zero-shot | 69,9% | 76,6% | 31,3% | 0,44 | 94,0% | 36 | 173 | 11 | 79 | 17 |
| few-shot | 67,5% | 68,4% | 22,4% | 0,34 | 93,9% | 26 | 186 | 12 | 90 | 2 |

### Contexto fornecido (somando zero-shot e few-shot)

| Contexto | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| none | 67,3% | 72,2% | 22,4% | 0,34 | 94,7% | 13 | 90 | 5 | 45 | 5 |
| summaries | 68,2% | 66,7% | 31,6% | 0,43 | 90,4% | 18 | 85 | 9 | 39 | 7 |
| target | 68,4% | 76,5% | 22,4% | 0,35 | 95,9% | 13 | 93 | 4 | 45 | 3 |
| both | 70,8% | 78,3% | 31,0% | 0,44 | 94,8% | 18 | 91 | 5 | 40 | 4 |

## 4. Concordância entre os prompts

Votos "YES" por caso, somando os 8 prompts (chamadas sem resposta não contam como YES):

| Votos YES (de 8) | Casos YES reais | Casos NO reais |
|---|---|---|
| 0 | 11 | 43 |
| 1 | 6 | 4 |
| 2 | 2 | 0 |
| 3 | 4 | 1 |
| 4 | 0 | 0 |
| 5 | 2 | 0 |
| 6 | 0 | 0 |
| 7 | 2 | 0 |
| 8 | 2 | 2 |

- YES reais que nenhum prompt detectou: 11/29
- NO reais marcados como YES por ≥1 prompt: 7/50

Ensemble por voto (por caso, 79 casos):

| Regra (YES se…) | Acurácia | Precisão | Recall | F1 | TP | FP |
|---|---|---|---|---|---|---|
| ≥1 de 8 | 77,2% | 72,0% | 62,1% | 0,67 | 18 | 7 |
| ≥2 de 8 | 74,7% | 80,0% | 41,4% | 0,55 | 12 | 3 |
| ≥3 de 8 | 72,2% | 76,9% | 34,5% | 0,48 | 10 | 3 |
| ≥4 de 8 | 68,4% | 75,0% | 20,7% | 0,32 | 6 | 2 |
| ≥5 de 8 | 68,4% | 75,0% | 20,7% | 0,32 | 6 | 2 |
| ≥6 de 8 | 65,8% | 66,7% | 13,8% | 0,23 | 4 | 2 |
| ≥7 de 8 | 65,8% | 66,7% | 13,8% | 0,23 | 4 | 2 |
| ≥8 de 8 | 63,3% | 50,0% | 6,9% | 0,12 | 2 | 2 |

Concordância par a par (mesma resposta, sobre os casos respondidos pelos dois prompts):

|  | zero_shot_guided_none | zero_shot_guided_summaries | zero_shot_guided_target | zero_shot_guided_both | few_shot_guided_none | few_shot_guided_summaries | few_shot_guided_target | few_shot_guided_both |
|---|---|---|---|---|---|---|---|---|
| **zero_shot_guided_none** | 100,0% | 84,7% | 96,0% | 87,8% | 94,7% | 89,3% | 89,3% | 93,3% |
| **zero_shot_guided_summaries** | 84,7% | 100,0% | 86,3% | 86,3% | 84,9% | 84,9% | 82,2% | 89,0% |
| **zero_shot_guided_target** | 96,0% | 86,3% | 100,0% | 92,0% | 93,4% | 93,4% | 90,8% | 94,7% |
| **zero_shot_guided_both** | 87,8% | 86,3% | 92,0% | 100,0% | 88,0% | 88,0% | 88,0% | 92,0% |
| **few_shot_guided_none** | 94,7% | 84,9% | 93,4% | 88,0% | 100,0% | 94,9% | 92,3% | 93,6% |
| **few_shot_guided_summaries** | 89,3% | 84,9% | 93,4% | 88,0% | 94,9% | 100,0% | 89,7% | 93,6% |
| **few_shot_guided_target** | 89,3% | 82,2% | 90,8% | 88,0% | 92,3% | 89,7% | 100,0% | 89,9% |
| **few_shot_guided_both** | 93,3% | 89,0% | 94,7% | 92,0% | 93,6% | 93,6% | 89,9% | 100,0% |

## 5. Condição violada (A/B/C) nas respostas YES

| Prompt | A | B | C | outra/vazia | Entre os TP: A | B | C |
|---|---|---|---|---|---|---|---|
| zero_shot_guided_none | 1 | 8 | 0 | 0 | 1 | 6 | 0 |
| zero_shot_guided_summaries | 3 | 14 | 1 | 0 | 2 | 11 | 0 |
| zero_shot_guided_target | 1 | 7 | 0 | 0 | 1 | 5 | 0 |
| zero_shot_guided_both | 1 | 11 | 0 | 0 | 1 | 9 | 0 |
| few_shot_guided_none | 1 | 5 | 3 | 0 | 1 | 3 | 2 |
| few_shot_guided_summaries | 1 | 5 | 3 | 0 | 1 | 3 | 1 |
| few_shot_guided_target | 1 | 7 | 1 | 0 | 1 | 5 | 1 |
| few_shot_guided_both | 1 | 9 | 1 | 0 | 1 | 6 | 1 |

O dataset não traz a condição esperada, então não é possível medir a acurácia dessa classificação.

## 6. Resultado por projeto (acertos / chamadas, contando chamadas sem resposta como incorretas)

| Projeto | Casos (YES/NO) | zero_shot_guided_none | zero_shot_guided_summaries | zero_shot_guided_target | zero_shot_guided_both | few_shot_guided_none | few_shot_guided_summaries | few_shot_guided_target | few_shot_guided_both |
|---|---|---|---|---|---|---|---|---|---|
| elasticsearch | 22 (5/17) | 15/22 | 15/22 | 16/22 | 15/22 | 17/22 | 18/22 | 17/22 | 18/22 |
| spring-boot | 10 (5/5) | 7/10 | 7/10 | 5/10 | 6/10 | 6/10 | 5/10 | 6/10 | 6/10 |
| elasticsearch-river-mongodb | 6 (2/4) | 4/6 | 3/6 | 4/6 | 4/6 | 4/6 | 4/6 | 3/6 | 4/6 |
| jsoup | 4 (3/1) | 0/4 | 2/4 | 1/4 | 1/4 | 1/4 | 1/4 | 2/4 | 1/4 |
| hector | 4 (0/4) | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 |
| retrofit | 3 (1/2) | 2/3 | 3/3 | 2/3 | 3/3 | 2/3 | 2/3 | 3/3 | 2/3 |
| storm | 2 (1/1) | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 1/2 | 2/2 | 2/2 |
| antlr4 | 2 (2/0) | 0/2 | 1/2 | 0/2 | 2/2 | 0/2 | 0/2 | 0/2 | 1/2 |
| fitnesse | 2 (2/0) | 0/2 | 0/2 | 0/2 | 1/2 | 0/2 | 0/2 | 0/2 | 0/2 |
| okhttp | 2 (0/2) | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 |
| activiti | 2 (1/1) | 1/2 | 2/2 | 1/2 | 1/2 | 2/2 | 2/2 | 2/2 | 2/2 |
| HikariCP | 2 (2/0) | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 |
| pushy | 2 (0/2) | 2/2 | 1/2 | 2/2 | 2/2 | 1/2 | 0/2 | 2/2 | 2/2 |
| cloud-slang | 1 (1/0) | 1/1 | 1/1 | 1/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 |
| jOOQ | 1 (0/1) | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 1/1 | 0/1 |
| swagger-maven-plugin | 1 (1/0) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| SimianArmy | 1 (0/1) | 1/1 | 0/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| titan | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| druid | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| netty | 1 (1/0) | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 |
| OpenTripPlanner | 1 (1/0) | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 |
| webbit | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| eureka | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| atmosphere | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| resty-gwt | 1 (1/0) | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 |
| quickml | 1 (0/1) | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 |
| java-faker | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| swagger-core | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| cucumber-jvm | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |

## 7. Chamadas sem resposta YES/NO

| Prompt | Ignoradas (prompt grande demais) | Erros | Recusas | Fora do formato | Em casos YES | Em casos NO |
|---|---|---|---|---|---|---|
| zero_shot_guided_none | 0 | 0 | 4 | 0 | 0 | 4 |
| zero_shot_guided_summaries | 0 | 0 | 6 | 0 | 1 | 5 |
| zero_shot_guided_target | 0 | 0 | 3 | 0 | 0 | 3 |
| zero_shot_guided_both | 0 | 0 | 4 | 0 | 0 | 4 |
| few_shot_guided_none | 0 | 0 | 1 | 0 | 0 | 1 |
| few_shot_guided_summaries | 0 | 0 | 1 | 0 | 0 | 1 |
| few_shot_guided_target | 0 | 0 | 0 | 0 | 0 | 0 |
| few_shot_guided_both | 0 | 0 | 0 | 0 | 0 | 0 |

## Observações

- Precisão, recall, F1 e especificidade são da classe YES (conflito semântico).
- Cada caso foi avaliado uma única vez por prompt, sem repetições, então não há medida de variância.
