# Relatório por prompt — `claude-haiku-5-5/1.csv`

- **Casos:** 79 (29 YES, 50 NO)
- **Prompts:** 8; **chamadas:** 632
- **Sem resposta YES/NO:** fora do formato: 1
- As métricas consideram só as chamadas com resposta YES/NO; as demais aparecem em "Sem resposta".

## 1. Resultado geral

| Chamadas | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| todas | 72,1% | 62,5% | 60,3% | 0,61 | 78,9% | 140 | 315 | 84 | 92 | 1 |

Baseline: sempre responder "NO" daria 63,3% de acurácia (400/632). Proporção real de YES nas chamadas: 36,7%.

## 2. Resultado por prompt

| Prompt | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| zero_shot_guided_none | 70,9% | 62,5% | 51,7% | 0,57 | 82,0% | 15 | 41 | 9 | 14 | 0 |
| zero_shot_guided_summaries | 70,9% | 62,5% | 51,7% | 0,57 | 82,0% | 15 | 41 | 9 | 14 | 0 |
| zero_shot_guided_target | 76,9% | 72,0% | 62,1% | 0,67 | 85,7% | 18 | 42 | 7 | 11 | 1 |
| zero_shot_guided_both | 72,2% | 61,3% | 65,5% | 0,63 | 76,0% | 19 | 38 | 12 | 10 | 0 |
| few_shot_guided_none | 74,7% | 65,5% | 65,5% | 0,66 | 80,0% | 19 | 40 | 10 | 10 | 0 |
| few_shot_guided_summaries | 68,4% | 56,7% | 58,6% | 0,58 | 74,0% | 17 | 37 | 13 | 12 | 0 |
| few_shot_guided_target | 68,4% | 56,7% | 58,6% | 0,58 | 74,0% | 17 | 37 | 13 | 12 | 0 |
| few_shot_guided_both | 74,7% | 64,5% | 69,0% | 0,67 | 78,0% | 20 | 39 | 11 | 9 | 0 |

| Prompt | Respostas YES | Respostas NO | Sem resposta | % YES (das respondidas) |
|---|---|---|---|---|
| zero_shot_guided_none | 24 | 55 | 0 | 30,4% |
| zero_shot_guided_summaries | 24 | 55 | 0 | 30,4% |
| zero_shot_guided_target | 25 | 53 | 1 | 32,1% |
| zero_shot_guided_both | 31 | 48 | 0 | 39,2% |
| few_shot_guided_none | 29 | 50 | 0 | 36,7% |
| few_shot_guided_summaries | 30 | 49 | 0 | 38,0% |
| few_shot_guided_target | 30 | 49 | 0 | 38,0% |
| few_shot_guided_both | 31 | 48 | 0 | 39,2% |

## 3. Efeito de cada fator

### Zero-shot vs. few-shot (somando as variantes de contexto)

| Tipo | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| zero-shot | 72,7% | 64,4% | 57,8% | 0,61 | 81,4% | 67 | 162 | 37 | 49 | 1 |
| few-shot | 71,5% | 60,8% | 62,9% | 0,62 | 76,5% | 73 | 153 | 47 | 43 | 0 |

### Contexto fornecido (somando zero-shot e few-shot)

| Contexto | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| none | 72,8% | 64,2% | 58,6% | 0,61 | 81,0% | 34 | 81 | 19 | 24 | 0 |
| summaries | 69,6% | 59,3% | 55,2% | 0,57 | 78,0% | 32 | 78 | 22 | 26 | 0 |
| target | 72,6% | 63,6% | 60,3% | 0,62 | 79,8% | 35 | 79 | 20 | 23 | 1 |
| both | 73,4% | 62,9% | 67,2% | 0,65 | 77,0% | 39 | 77 | 23 | 19 | 0 |

## 4. Concordância entre os prompts

Votos "YES" por caso, somando os 8 prompts (chamadas sem resposta não contam como YES):

| Votos YES (de 8) | Casos YES reais | Casos NO reais |
|---|---|---|
| 0 | 4 | 30 |
| 1 | 2 | 3 |
| 2 | 1 | 4 |
| 3 | 1 | 0 |
| 4 | 2 | 3 |
| 5 | 5 | 4 |
| 6 | 4 | 3 |
| 7 | 4 | 1 |
| 8 | 6 | 2 |

- YES reais que nenhum prompt detectou: 4/29
- NO reais marcados como YES por ≥1 prompt: 20/50

Ensemble por voto (por caso, 79 casos):

| Regra (YES se…) | Acurácia | Precisão | Recall | F1 | TP | FP |
|---|---|---|---|---|---|---|
| ≥1 de 8 | 69,6% | 55,6% | 86,2% | 0,68 | 25 | 20 |
| ≥2 de 8 | 70,9% | 57,5% | 79,3% | 0,67 | 23 | 17 |
| ≥3 de 8 | 74,7% | 62,9% | 75,9% | 0,69 | 22 | 13 |
| ≥4 de 8 | 73,4% | 61,8% | 72,4% | 0,67 | 21 | 13 |
| ≥5 de 8 | 74,7% | 65,5% | 65,5% | 0,66 | 19 | 10 |
| ≥6 de 8 | 73,4% | 70,0% | 48,3% | 0,57 | 14 | 6 |
| ≥7 de 8 | 72,2% | 76,9% | 34,5% | 0,48 | 10 | 3 |
| ≥8 de 8 | 68,4% | 75,0% | 20,7% | 0,32 | 6 | 2 |

Concordância par a par (mesma resposta, sobre os casos respondidos pelos dois prompts):

|  | zero_shot_guided_none | zero_shot_guided_summaries | zero_shot_guided_target | zero_shot_guided_both | few_shot_guided_none | few_shot_guided_summaries | few_shot_guided_target | few_shot_guided_both |
|---|---|---|---|---|---|---|---|---|
| **zero_shot_guided_none** | 100,0% | 89,9% | 76,9% | 86,1% | 78,5% | 77,2% | 77,2% | 78,5% |
| **zero_shot_guided_summaries** | 89,9% | 100,0% | 82,1% | 86,1% | 78,5% | 79,7% | 74,7% | 78,5% |
| **zero_shot_guided_target** | 76,9% | 82,1% | 100,0% | 78,2% | 76,9% | 87,2% | 87,2% | 83,3% |
| **zero_shot_guided_both** | 86,1% | 86,1% | 78,2% | 100,0% | 74,7% | 78,5% | 78,5% | 74,7% |
| **few_shot_guided_none** | 78,5% | 78,5% | 76,9% | 74,7% | 100,0% | 78,5% | 78,5% | 77,2% |
| **few_shot_guided_summaries** | 77,2% | 79,7% | 87,2% | 78,5% | 78,5% | 100,0% | 79,7% | 81,0% |
| **few_shot_guided_target** | 77,2% | 74,7% | 87,2% | 78,5% | 78,5% | 79,7% | 100,0% | 86,1% |
| **few_shot_guided_both** | 78,5% | 78,5% | 83,3% | 74,7% | 77,2% | 81,0% | 86,1% | 100,0% |

## 5. Condição violada (A/B/C) nas respostas YES

| Prompt | A | B | C | outra/vazia | Entre os TP: A | B | C |
|---|---|---|---|---|---|---|---|
| zero_shot_guided_none | 1 | 15 | 8 | 0 | 1 | 10 | 4 |
| zero_shot_guided_summaries | 1 | 14 | 9 | 0 | 1 | 10 | 4 |
| zero_shot_guided_target | 1 | 15 | 9 | 0 | 1 | 12 | 5 |
| zero_shot_guided_both | 1 | 18 | 12 | 0 | 1 | 12 | 6 |
| few_shot_guided_none | 1 | 13 | 15 | 0 | 1 | 9 | 9 |
| few_shot_guided_summaries | 2 | 14 | 14 | 0 | 1 | 10 | 6 |
| few_shot_guided_target | 1 | 17 | 12 | 0 | 1 | 12 | 4 |
| few_shot_guided_both | 1 | 15 | 15 | 0 | 1 | 12 | 7 |

O dataset não traz a condição esperada, então não é possível medir a acurácia dessa classificação.

## 6. Resultado por projeto (acertos / chamadas, contando chamadas sem resposta como incorretas)

| Projeto | Casos (YES/NO) | zero_shot_guided_none | zero_shot_guided_summaries | zero_shot_guided_target | zero_shot_guided_both | few_shot_guided_none | few_shot_guided_summaries | few_shot_guided_target | few_shot_guided_both |
|---|---|---|---|---|---|---|---|---|---|
| elasticsearch | 22 (5/17) | 19/22 | 17/22 | 18/22 | 18/22 | 16/22 | 17/22 | 13/22 | 17/22 |
| spring-boot | 10 (5/5) | 6/10 | 7/10 | 9/10 | 7/10 | 8/10 | 8/10 | 8/10 | 6/10 |
| elasticsearch-river-mongodb | 6 (2/4) | 5/6 | 5/6 | 6/6 | 5/6 | 5/6 | 4/6 | 6/6 | 5/6 |
| jsoup | 4 (3/1) | 1/4 | 1/4 | 2/4 | 1/4 | 2/4 | 2/4 | 2/4 | 2/4 |
| hector | 4 (0/4) | 3/4 | 3/4 | 2/4 | 4/4 | 3/4 | 2/4 | 2/4 | 3/4 |
| retrofit | 3 (1/2) | 2/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| storm | 2 (1/1) | 1/2 | 1/2 | 1/2 | 1/2 | 2/2 | 1/2 | 1/2 | 1/2 |
| antlr4 | 2 (2/0) | 1/2 | 2/2 | 1/2 | 2/2 | 1/2 | 2/2 | 1/2 | 1/2 |
| fitnesse | 2 (2/0) | 2/2 | 1/2 | 1/2 | 2/2 | 1/2 | 0/2 | 2/2 | 2/2 |
| okhttp | 2 (0/2) | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 |
| activiti | 2 (1/1) | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 |
| HikariCP | 2 (2/0) | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 2/2 |
| pushy | 2 (0/2) | 1/2 | 1/2 | 1/2 | 0/2 | 1/2 | 1/2 | 1/2 | 2/2 |
| cloud-slang | 1 (1/0) | 0/1 | 0/1 | 1/1 | 0/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| jOOQ | 1 (0/1) | 0/1 | 1/1 | 1/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 |
| swagger-maven-plugin | 1 (1/0) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| SimianArmy | 1 (0/1) | 1/1 | 1/1 | 1/1 | 0/1 | 1/1 | 0/1 | 1/1 | 1/1 |
| titan | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| druid | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| netty | 1 (1/0) | 0/1 | 0/1 | 0/1 | 0/1 | 1/1 | 0/1 | 0/1 | 1/1 |
| OpenTripPlanner | 1 (1/0) | 1/1 | 1/1 | 0/1 | 1/1 | 1/1 | 0/1 | 0/1 | 0/1 |
| webbit | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| eureka | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| atmosphere | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| resty-gwt | 1 (1/0) | 0/1 | 0/1 | 0/1 | 0/1 | 1/1 | 0/1 | 0/1 | 0/1 |
| quickml | 1 (0/1) | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 |
| java-faker | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| swagger-core | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 0/1 | 1/1 | 1/1 | 1/1 |
| cucumber-jvm | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |

## 7. Chamadas sem resposta YES/NO

| Prompt | Ignoradas (prompt grande demais) | Erros | Recusas | Fora do formato | Em casos YES | Em casos NO |
|---|---|---|---|---|---|---|
| zero_shot_guided_none | 0 | 0 | 0 | 0 | 0 | 0 |
| zero_shot_guided_summaries | 0 | 0 | 0 | 0 | 0 | 0 |
| zero_shot_guided_target | 0 | 0 | 0 | 1 | 0 | 1 |
| zero_shot_guided_both | 0 | 0 | 0 | 0 | 0 | 0 |
| few_shot_guided_none | 0 | 0 | 0 | 0 | 0 | 0 |
| few_shot_guided_summaries | 0 | 0 | 0 | 0 | 0 | 0 |
| few_shot_guided_target | 0 | 0 | 0 | 0 | 0 | 0 |
| few_shot_guided_both | 0 | 0 | 0 | 0 | 0 | 0 |

## Observações

- Precisão, recall, F1 e especificidade são da classe YES (conflito semântico).
- Cada caso foi avaliado uma única vez por prompt, sem repetições, então não há medida de variância.
