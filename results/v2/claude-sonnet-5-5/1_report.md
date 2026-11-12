# Relatório por prompt — `claude-sonnet-5-5/1.csv`

- **Casos:** 79 (29 YES, 50 NO)
- **Prompts:** 8; **chamadas:** 632
- **Sem resposta YES/NO:** nenhuma
- As métricas consideram só as chamadas com resposta YES/NO; as demais aparecem em "Sem resposta".

## 1. Resultado geral

| Chamadas | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| todas | 65,3% | 61,4% | 15,1% | 0,24 | 94,5% | 35 | 378 | 22 | 197 | 0 |

Baseline: sempre responder "NO" daria 63,3% de acurácia (400/632). Proporção real de YES nas chamadas: 36,7%.

## 2. Resultado por prompt

| Prompt | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| zero_shot_guided_none | 63,3% | 50,0% | 13,8% | 0,22 | 92,0% | 4 | 46 | 4 | 25 | 0 |
| zero_shot_guided_summaries | 67,1% | 71,4% | 17,2% | 0,28 | 96,0% | 5 | 48 | 2 | 24 | 0 |
| zero_shot_guided_target | 64,6% | 57,1% | 13,8% | 0,22 | 94,0% | 4 | 47 | 3 | 25 | 0 |
| zero_shot_guided_both | 65,8% | 66,7% | 13,8% | 0,23 | 96,0% | 4 | 48 | 2 | 25 | 0 |
| few_shot_guided_none | 62,0% | 42,9% | 10,3% | 0,17 | 92,0% | 3 | 46 | 4 | 26 | 0 |
| few_shot_guided_summaries | 65,8% | 62,5% | 17,2% | 0,27 | 94,0% | 5 | 47 | 3 | 24 | 0 |
| few_shot_guided_target | 68,4% | 83,3% | 17,2% | 0,29 | 98,0% | 5 | 49 | 1 | 24 | 0 |
| few_shot_guided_both | 65,8% | 62,5% | 17,2% | 0,27 | 94,0% | 5 | 47 | 3 | 24 | 0 |

| Prompt | Respostas YES | Respostas NO | Sem resposta | % YES (das respondidas) |
|---|---|---|---|---|
| zero_shot_guided_none | 8 | 71 | 0 | 10,1% |
| zero_shot_guided_summaries | 7 | 72 | 0 | 8,9% |
| zero_shot_guided_target | 7 | 72 | 0 | 8,9% |
| zero_shot_guided_both | 6 | 73 | 0 | 7,6% |
| few_shot_guided_none | 7 | 72 | 0 | 8,9% |
| few_shot_guided_summaries | 8 | 71 | 0 | 10,1% |
| few_shot_guided_target | 6 | 73 | 0 | 7,6% |
| few_shot_guided_both | 8 | 71 | 0 | 10,1% |

## 3. Efeito de cada fator

### Zero-shot vs. few-shot (somando as variantes de contexto)

| Tipo | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| zero-shot | 65,2% | 60,7% | 14,7% | 0,24 | 94,5% | 17 | 189 | 11 | 99 | 0 |
| few-shot | 65,5% | 62,1% | 15,5% | 0,25 | 94,5% | 18 | 189 | 11 | 98 | 0 |

### Contexto fornecido (somando zero-shot e few-shot)

| Contexto | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| none | 62,7% | 46,7% | 12,1% | 0,19 | 92,0% | 7 | 92 | 8 | 51 | 0 |
| summaries | 66,5% | 66,7% | 17,2% | 0,27 | 95,0% | 10 | 95 | 5 | 48 | 0 |
| target | 66,5% | 69,2% | 15,5% | 0,25 | 96,0% | 9 | 96 | 4 | 49 | 0 |
| both | 65,8% | 64,3% | 15,5% | 0,25 | 95,0% | 9 | 95 | 5 | 49 | 0 |

## 4. Concordância entre os prompts

Votos "YES" por caso, somando os 8 prompts (chamadas sem resposta não contam como YES):

| Votos YES (de 8) | Casos YES reais | Casos NO reais |
|---|---|---|
| 0 | 20 | 45 |
| 1 | 3 | 0 |
| 2 | 0 | 1 |
| 3 | 2 | 1 |
| 4 | 1 | 1 |
| 5 | 0 | 1 |
| 6 | 1 | 0 |
| 7 | 0 | 0 |
| 8 | 2 | 1 |

- YES reais que nenhum prompt detectou: 20/29
- NO reais marcados como YES por ≥1 prompt: 5/50

Ensemble por voto (por caso, 79 casos):

| Regra (YES se…) | Acurácia | Precisão | Recall | F1 | TP | FP |
|---|---|---|---|---|---|---|
| ≥1 de 8 | 68,4% | 64,3% | 31,0% | 0,42 | 9 | 5 |
| ≥2 de 8 | 64,6% | 54,5% | 20,7% | 0,30 | 6 | 5 |
| ≥3 de 8 | 65,8% | 60,0% | 20,7% | 0,31 | 6 | 4 |
| ≥4 de 8 | 64,6% | 57,1% | 13,8% | 0,22 | 4 | 3 |
| ≥5 de 8 | 64,6% | 60,0% | 10,3% | 0,18 | 3 | 2 |
| ≥6 de 8 | 65,8% | 75,0% | 10,3% | 0,18 | 3 | 1 |
| ≥7 de 8 | 64,6% | 66,7% | 6,9% | 0,12 | 2 | 1 |
| ≥8 de 8 | 64,6% | 66,7% | 6,9% | 0,12 | 2 | 1 |

Concordância par a par (mesma resposta, sobre os casos respondidos pelos dois prompts):

|  | zero_shot_guided_none | zero_shot_guided_summaries | zero_shot_guided_target | zero_shot_guided_both | few_shot_guided_none | few_shot_guided_summaries | few_shot_guided_target | few_shot_guided_both |
|---|---|---|---|---|---|---|---|---|
| **zero_shot_guided_none** | 100,0% | 93,7% | 98,7% | 94,9% | 96,2% | 92,4% | 92,4% | 92,4% |
| **zero_shot_guided_summaries** | 93,7% | 100,0% | 94,9% | 96,2% | 92,4% | 91,1% | 93,7% | 93,7% |
| **zero_shot_guided_target** | 98,7% | 94,9% | 100,0% | 96,2% | 94,9% | 93,7% | 93,7% | 93,7% |
| **zero_shot_guided_both** | 94,9% | 96,2% | 96,2% | 100,0% | 91,1% | 89,9% | 92,4% | 97,5% |
| **few_shot_guided_none** | 96,2% | 92,4% | 94,9% | 91,1% | 100,0% | 96,2% | 93,7% | 91,1% |
| **few_shot_guided_summaries** | 92,4% | 91,1% | 93,7% | 89,9% | 96,2% | 100,0% | 94,9% | 92,4% |
| **few_shot_guided_target** | 92,4% | 93,7% | 93,7% | 92,4% | 93,7% | 94,9% | 100,0% | 92,4% |
| **few_shot_guided_both** | 92,4% | 93,7% | 93,7% | 97,5% | 91,1% | 92,4% | 92,4% | 100,0% |

## 5. Condição violada (A/B/C) nas respostas YES

| Prompt | A | B | C | outra/vazia | Entre os TP: A | B | C |
|---|---|---|---|---|---|---|---|
| zero_shot_guided_none | 0 | 6 | 2 | 0 | 0 | 3 | 1 |
| zero_shot_guided_summaries | 0 | 6 | 1 | 0 | 0 | 4 | 1 |
| zero_shot_guided_target | 1 | 4 | 2 | 0 | 1 | 2 | 1 |
| zero_shot_guided_both | 1 | 5 | 0 | 0 | 1 | 3 | 0 |
| few_shot_guided_none | 1 | 4 | 2 | 0 | 1 | 2 | 0 |
| few_shot_guided_summaries | 1 | 3 | 4 | 0 | 1 | 2 | 2 |
| few_shot_guided_target | 1 | 4 | 1 | 0 | 1 | 3 | 1 |
| few_shot_guided_both | 2 | 5 | 1 | 0 | 2 | 3 | 0 |

O dataset não traz a condição esperada, então não é possível medir a acurácia dessa classificação.

## 6. Resultado por projeto (acertos / chamadas, contando chamadas sem resposta como incorretas)

| Projeto | Casos (YES/NO) | zero_shot_guided_none | zero_shot_guided_summaries | zero_shot_guided_target | zero_shot_guided_both | few_shot_guided_none | few_shot_guided_summaries | few_shot_guided_target | few_shot_guided_both |
|---|---|---|---|---|---|---|---|---|---|
| elasticsearch | 22 (5/17) | 17/22 | 17/22 | 17/22 | 17/22 | 17/22 | 17/22 | 17/22 | 17/22 |
| spring-boot | 10 (5/5) | 6/10 | 6/10 | 6/10 | 7/10 | 5/10 | 5/10 | 5/10 | 7/10 |
| elasticsearch-river-mongodb | 6 (2/4) | 4/6 | 5/6 | 5/6 | 4/6 | 4/6 | 6/6 | 5/6 | 4/6 |
| jsoup | 4 (3/1) | 1/4 | 1/4 | 1/4 | 1/4 | 1/4 | 1/4 | 1/4 | 1/4 |
| hector | 4 (0/4) | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 |
| retrofit | 3 (1/2) | 2/3 | 2/3 | 2/3 | 2/3 | 2/3 | 2/3 | 2/3 | 2/3 |
| storm | 2 (1/1) | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 2/2 | 1/2 |
| antlr4 | 2 (2/0) | 0/2 | 1/2 | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 |
| fitnesse | 2 (2/0) | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 |
| okhttp | 2 (0/2) | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 |
| activiti | 2 (1/1) | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 2/2 | 2/2 | 2/2 |
| HikariCP | 2 (2/0) | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 |
| pushy | 2 (0/2) | 1/2 | 2/2 | 1/2 | 2/2 | 0/2 | 0/2 | 2/2 | 1/2 |
| cloud-slang | 1 (1/0) | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 |
| jOOQ | 1 (0/1) | 0/1 | 0/1 | 0/1 | 0/1 | 1/1 | 1/1 | 1/1 | 0/1 |
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
