# Relatório por prompt — `claude-sonnet-5-5/2.csv`

- **Casos:** 79 (29 YES, 50 NO)
- **Prompts:** 8; **chamadas:** 632
- **Sem resposta YES/NO:** nenhuma
- As métricas consideram só as chamadas com resposta YES/NO; as demais aparecem em "Sem resposta".

## 1. Resultado geral

| Chamadas | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| todas | 65,8% | 63,3% | 16,4% | 0,26 | 94,5% | 38 | 378 | 22 | 194 | 0 |

Baseline: sempre responder "NO" daria 63,3% de acurácia (400/632). Proporção real de YES nas chamadas: 36,7%.

## 2. Resultado por prompt

| Prompt | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| zero_shot_guided_none | 65,8% | 66,7% | 13,8% | 0,23 | 96,0% | 4 | 48 | 2 | 25 | 0 |
| zero_shot_guided_summaries | 64,6% | 55,6% | 17,2% | 0,26 | 92,0% | 5 | 46 | 4 | 24 | 0 |
| zero_shot_guided_target | 64,6% | 57,1% | 13,8% | 0,22 | 94,0% | 4 | 47 | 3 | 25 | 0 |
| zero_shot_guided_both | 69,6% | 85,7% | 20,7% | 0,33 | 98,0% | 6 | 49 | 1 | 23 | 0 |
| few_shot_guided_none | 63,3% | 50,0% | 13,8% | 0,22 | 92,0% | 4 | 46 | 4 | 25 | 0 |
| few_shot_guided_summaries | 63,3% | 50,0% | 13,8% | 0,22 | 92,0% | 4 | 46 | 4 | 25 | 0 |
| few_shot_guided_target | 65,8% | 66,7% | 13,8% | 0,23 | 96,0% | 4 | 48 | 2 | 25 | 0 |
| few_shot_guided_both | 69,6% | 77,8% | 24,1% | 0,37 | 96,0% | 7 | 48 | 2 | 22 | 0 |

| Prompt | Respostas YES | Respostas NO | Sem resposta | % YES (das respondidas) |
|---|---|---|---|---|
| zero_shot_guided_none | 6 | 73 | 0 | 7,6% |
| zero_shot_guided_summaries | 9 | 70 | 0 | 11,4% |
| zero_shot_guided_target | 7 | 72 | 0 | 8,9% |
| zero_shot_guided_both | 7 | 72 | 0 | 8,9% |
| few_shot_guided_none | 8 | 71 | 0 | 10,1% |
| few_shot_guided_summaries | 8 | 71 | 0 | 10,1% |
| few_shot_guided_target | 6 | 73 | 0 | 7,6% |
| few_shot_guided_both | 9 | 70 | 0 | 11,4% |

## 3. Efeito de cada fator

### Zero-shot vs. few-shot (somando as variantes de contexto)

| Tipo | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| zero-shot | 66,1% | 65,5% | 16,4% | 0,26 | 95,0% | 19 | 190 | 10 | 97 | 0 |
| few-shot | 65,5% | 61,3% | 16,4% | 0,26 | 94,0% | 19 | 188 | 12 | 97 | 0 |

### Contexto fornecido (somando zero-shot e few-shot)

| Contexto | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| none | 64,6% | 57,1% | 13,8% | 0,22 | 94,0% | 8 | 94 | 6 | 50 | 0 |
| summaries | 63,9% | 52,9% | 15,5% | 0,24 | 92,0% | 9 | 92 | 8 | 49 | 0 |
| target | 65,2% | 61,5% | 13,8% | 0,23 | 95,0% | 8 | 95 | 5 | 50 | 0 |
| both | 69,6% | 81,2% | 22,4% | 0,35 | 97,0% | 13 | 97 | 3 | 45 | 0 |

## 4. Concordância entre os prompts

Votos "YES" por caso, somando os 8 prompts (chamadas sem resposta não contam como YES):

| Votos YES (de 8) | Casos YES reais | Casos NO reais |
|---|---|---|
| 0 | 20 | 45 |
| 1 | 3 | 0 |
| 2 | 1 | 1 |
| 3 | 1 | 0 |
| 4 | 0 | 3 |
| 5 | 0 | 0 |
| 6 | 0 | 0 |
| 7 | 2 | 0 |
| 8 | 2 | 1 |

- YES reais que nenhum prompt detectou: 20/29
- NO reais marcados como YES por ≥1 prompt: 5/50

Ensemble por voto (por caso, 79 casos):

| Regra (YES se…) | Acurácia | Precisão | Recall | F1 | TP | FP |
|---|---|---|---|---|---|---|
| ≥1 de 8 | 68,4% | 64,3% | 31,0% | 0,42 | 9 | 5 |
| ≥2 de 8 | 64,6% | 54,5% | 20,7% | 0,30 | 6 | 5 |
| ≥3 de 8 | 64,6% | 55,6% | 17,2% | 0,26 | 5 | 4 |
| ≥4 de 8 | 63,3% | 50,0% | 13,8% | 0,22 | 4 | 4 |
| ≥5 de 8 | 67,1% | 80,0% | 13,8% | 0,24 | 4 | 1 |
| ≥6 de 8 | 67,1% | 80,0% | 13,8% | 0,24 | 4 | 1 |
| ≥7 de 8 | 67,1% | 80,0% | 13,8% | 0,24 | 4 | 1 |
| ≥8 de 8 | 64,6% | 66,7% | 6,9% | 0,12 | 2 | 1 |

Concordância par a par (mesma resposta, sobre os casos respondidos pelos dois prompts):

|  | zero_shot_guided_none | zero_shot_guided_summaries | zero_shot_guided_target | zero_shot_guided_both | few_shot_guided_none | few_shot_guided_summaries | few_shot_guided_target | few_shot_guided_both |
|---|---|---|---|---|---|---|---|---|
| **zero_shot_guided_none** | 100,0% | 96,2% | 96,2% | 96,2% | 97,5% | 94,9% | 97,5% | 91,1% |
| **zero_shot_guided_summaries** | 96,2% | 100,0% | 97,5% | 92,4% | 96,2% | 96,2% | 96,2% | 92,4% |
| **zero_shot_guided_target** | 96,2% | 97,5% | 100,0% | 92,4% | 93,7% | 93,7% | 93,7% | 92,4% |
| **zero_shot_guided_both** | 96,2% | 92,4% | 92,4% | 100,0% | 93,7% | 93,7% | 96,2% | 92,4% |
| **few_shot_guided_none** | 97,5% | 96,2% | 93,7% | 93,7% | 100,0% | 97,5% | 97,5% | 88,6% |
| **few_shot_guided_summaries** | 94,9% | 96,2% | 93,7% | 93,7% | 97,5% | 100,0% | 97,5% | 91,1% |
| **few_shot_guided_target** | 97,5% | 96,2% | 93,7% | 96,2% | 97,5% | 97,5% | 100,0% | 91,1% |
| **few_shot_guided_both** | 91,1% | 92,4% | 92,4% | 92,4% | 88,6% | 91,1% | 91,1% | 100,0% |

## 5. Condição violada (A/B/C) nas respostas YES

| Prompt | A | B | C | outra/vazia | Entre os TP: A | B | C |
|---|---|---|---|---|---|---|---|
| zero_shot_guided_none | 2 | 4 | 0 | 0 | 2 | 2 | 0 |
| zero_shot_guided_summaries | 0 | 6 | 3 | 0 | 0 | 4 | 1 |
| zero_shot_guided_target | 1 | 6 | 0 | 0 | 1 | 3 | 0 |
| zero_shot_guided_both | 1 | 5 | 1 | 0 | 1 | 4 | 1 |
| few_shot_guided_none | 0 | 5 | 3 | 0 | 0 | 3 | 1 |
| few_shot_guided_summaries | 1 | 4 | 3 | 0 | 1 | 2 | 1 |
| few_shot_guided_target | 1 | 3 | 2 | 0 | 1 | 2 | 1 |
| few_shot_guided_both | 1 | 7 | 1 | 0 | 1 | 5 | 1 |

O dataset não traz a condição esperada, então não é possível medir a acurácia dessa classificação.

## 6. Resultado por projeto (acertos / chamadas, contando chamadas sem resposta como incorretas)

| Projeto | Casos (YES/NO) | zero_shot_guided_none | zero_shot_guided_summaries | zero_shot_guided_target | zero_shot_guided_both | few_shot_guided_none | few_shot_guided_summaries | few_shot_guided_target | few_shot_guided_both |
|---|---|---|---|---|---|---|---|---|---|
| elasticsearch | 22 (5/17) | 17/22 | 17/22 | 17/22 | 17/22 | 17/22 | 17/22 | 17/22 | 17/22 |
| spring-boot | 10 (5/5) | 5/10 | 6/10 | 6/10 | 6/10 | 5/10 | 5/10 | 5/10 | 8/10 |
| elasticsearch-river-mongodb | 6 (2/4) | 4/6 | 4/6 | 4/6 | 5/6 | 4/6 | 5/6 | 5/6 | 4/6 |
| jsoup | 4 (3/1) | 1/4 | 1/4 | 1/4 | 1/4 | 1/4 | 1/4 | 1/4 | 1/4 |
| hector | 4 (0/4) | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 |
| retrofit | 3 (1/2) | 2/3 | 2/3 | 2/3 | 2/3 | 2/3 | 2/3 | 2/3 | 3/3 |
| storm | 2 (1/1) | 1/2 | 1/2 | 1/2 | 2/2 | 1/2 | 1/2 | 1/2 | 1/2 |
| antlr4 | 2 (2/0) | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 |
| fitnesse | 2 (2/0) | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 |
| okhttp | 2 (0/2) | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 |
| activiti | 2 (1/1) | 2/2 | 2/2 | 1/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 |
| HikariCP | 2 (2/0) | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 |
| pushy | 2 (0/2) | 2/2 | 1/2 | 2/2 | 2/2 | 0/2 | 0/2 | 1/2 | 2/2 |
| cloud-slang | 1 (1/0) | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 |
| jOOQ | 1 (0/1) | 1/1 | 0/1 | 0/1 | 1/1 | 1/1 | 0/1 | 1/1 | 0/1 |
| swagger-maven-plugin | 1 (1/0) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| SimianArmy | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
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
| zero_shot_guided_none | 0 | 0 | 0 | 0 | 0 | 0 |
| zero_shot_guided_summaries | 0 | 0 | 0 | 0 | 0 | 0 |
| zero_shot_guided_target | 0 | 0 | 0 | 0 | 0 | 0 |
| zero_shot_guided_both | 0 | 0 | 0 | 0 | 0 | 0 |
| few_shot_guided_none | 0 | 0 | 0 | 0 | 0 | 0 |
| few_shot_guided_summaries | 0 | 0 | 0 | 0 | 0 | 0 |
| few_shot_guided_target | 0 | 0 | 0 | 0 | 0 | 0 |
| few_shot_guided_both | 0 | 0 | 0 | 0 | 0 | 0 |

## Observações

- Precisão, recall, F1 e especificidade são da classe YES (conflito semântico).
- Cada caso foi avaliado uma única vez por prompt, sem repetições, então não há medida de variância.
