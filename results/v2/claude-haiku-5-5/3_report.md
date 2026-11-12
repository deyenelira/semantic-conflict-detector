# Relatório por prompt — `claude-haiku-5-5/3.csv`

- **Casos:** 79 (29 YES, 50 NO)
- **Prompts:** 8; **chamadas:** 632
- **Sem resposta YES/NO:** fora do formato: 1
- As métricas consideram só as chamadas com resposta YES/NO; as demais aparecem em "Sem resposta".

## 1. Resultado geral

| Chamadas | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| todas | 73,7% | 65,3% | 60,8% | 0,63 | 81,2% | 141 | 324 | 75 | 91 | 1 |

Baseline: sempre responder "NO" daria 63,3% de acurácia (400/632). Proporção real de YES nas chamadas: 36,7%.

## 2. Resultado por prompt

| Prompt | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| zero_shot_guided_none | 70,9% | 63,6% | 48,3% | 0,55 | 84,0% | 14 | 42 | 8 | 15 | 0 |
| zero_shot_guided_summaries | 75,9% | 69,2% | 62,1% | 0,65 | 84,0% | 18 | 42 | 8 | 11 | 0 |
| zero_shot_guided_target | 75,9% | 72,7% | 55,2% | 0,63 | 88,0% | 16 | 44 | 6 | 13 | 0 |
| zero_shot_guided_both | 77,2% | 70,4% | 65,5% | 0,68 | 84,0% | 19 | 42 | 8 | 10 | 0 |
| few_shot_guided_none | 64,1% | 51,9% | 48,3% | 0,50 | 73,5% | 14 | 36 | 13 | 15 | 1 |
| few_shot_guided_summaries | 74,7% | 66,7% | 62,1% | 0,64 | 82,0% | 18 | 41 | 9 | 11 | 0 |
| few_shot_guided_target | 77,2% | 67,7% | 72,4% | 0,70 | 80,0% | 21 | 40 | 10 | 8 | 0 |
| few_shot_guided_both | 73,4% | 61,8% | 72,4% | 0,67 | 74,0% | 21 | 37 | 13 | 8 | 0 |

| Prompt | Respostas YES | Respostas NO | Sem resposta | % YES (das respondidas) |
|---|---|---|---|---|
| zero_shot_guided_none | 22 | 57 | 0 | 27,8% |
| zero_shot_guided_summaries | 26 | 53 | 0 | 32,9% |
| zero_shot_guided_target | 22 | 57 | 0 | 27,8% |
| zero_shot_guided_both | 27 | 52 | 0 | 34,2% |
| few_shot_guided_none | 27 | 51 | 1 | 34,6% |
| few_shot_guided_summaries | 27 | 52 | 0 | 34,2% |
| few_shot_guided_target | 31 | 48 | 0 | 39,2% |
| few_shot_guided_both | 34 | 45 | 0 | 43,0% |

## 3. Efeito de cada fator

### Zero-shot vs. few-shot (somando as variantes de contexto)

| Tipo | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| zero-shot | 75,0% | 69,1% | 57,8% | 0,63 | 85,0% | 67 | 170 | 30 | 49 | 0 |
| few-shot | 72,4% | 62,2% | 63,8% | 0,63 | 77,4% | 74 | 154 | 45 | 42 | 1 |

### Contexto fornecido (somando zero-shot e few-shot)

| Contexto | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| none | 67,5% | 57,1% | 48,3% | 0,52 | 78,8% | 28 | 78 | 21 | 30 | 1 |
| summaries | 75,3% | 67,9% | 62,1% | 0,65 | 83,0% | 36 | 83 | 17 | 22 | 0 |
| target | 76,6% | 69,8% | 63,8% | 0,67 | 84,0% | 37 | 84 | 16 | 21 | 0 |
| both | 75,3% | 65,6% | 69,0% | 0,67 | 79,0% | 40 | 79 | 21 | 18 | 0 |

## 4. Concordância entre os prompts

Votos "YES" por caso, somando os 8 prompts (chamadas sem resposta não contam como YES):

| Votos YES (de 8) | Casos YES reais | Casos NO reais |
|---|---|---|
| 0 | 4 | 31 |
| 1 | 2 | 5 |
| 2 | 1 | 2 |
| 3 | 2 | 2 |
| 4 | 2 | 3 |
| 5 | 4 | 1 |
| 6 | 1 | 1 |
| 7 | 7 | 3 |
| 8 | 6 | 2 |

- YES reais que nenhum prompt detectou: 4/29
- NO reais marcados como YES por ≥1 prompt: 19/50

Ensemble por voto (por caso, 79 casos):

| Regra (YES se…) | Acurácia | Precisão | Recall | F1 | TP | FP |
|---|---|---|---|---|---|---|
| ≥1 de 8 | 70,9% | 56,8% | 86,2% | 0,68 | 25 | 19 |
| ≥2 de 8 | 74,7% | 62,2% | 79,3% | 0,70 | 23 | 14 |
| ≥3 de 8 | 75,9% | 64,7% | 75,9% | 0,70 | 22 | 12 |
| ≥4 de 8 | 75,9% | 66,7% | 69,0% | 0,68 | 20 | 10 |
| ≥5 de 8 | 77,2% | 72,0% | 62,1% | 0,67 | 18 | 7 |
| ≥6 de 8 | 73,4% | 70,0% | 48,3% | 0,57 | 14 | 6 |
| ≥7 de 8 | 73,4% | 72,2% | 44,8% | 0,55 | 13 | 5 |
| ≥8 de 8 | 68,4% | 75,0% | 20,7% | 0,32 | 6 | 2 |

Concordância par a par (mesma resposta, sobre os casos respondidos pelos dois prompts):

|  | zero_shot_guided_none | zero_shot_guided_summaries | zero_shot_guided_target | zero_shot_guided_both | few_shot_guided_none | few_shot_guided_summaries | few_shot_guided_target | few_shot_guided_both |
|---|---|---|---|---|---|---|---|---|
| **zero_shot_guided_none** | 100,0% | 82,3% | 84,8% | 78,5% | 83,3% | 81,0% | 78,5% | 77,2% |
| **zero_shot_guided_summaries** | 82,3% | 100,0% | 84,8% | 86,1% | 85,9% | 88,6% | 81,0% | 82,3% |
| **zero_shot_guided_target** | 84,8% | 84,8% | 100,0% | 91,1% | 82,1% | 81,0% | 83,5% | 79,7% |
| **zero_shot_guided_both** | 78,5% | 86,1% | 91,1% | 100,0% | 78,2% | 84,8% | 84,8% | 81,0% |
| **few_shot_guided_none** | 83,3% | 85,9% | 82,1% | 78,2% | 100,0% | 82,1% | 83,3% | 79,5% |
| **few_shot_guided_summaries** | 81,0% | 88,6% | 81,0% | 84,8% | 82,1% | 100,0% | 77,2% | 78,5% |
| **few_shot_guided_target** | 78,5% | 81,0% | 83,5% | 84,8% | 83,3% | 77,2% | 100,0% | 83,5% |
| **few_shot_guided_both** | 77,2% | 82,3% | 79,7% | 81,0% | 79,5% | 78,5% | 83,5% | 100,0% |

## 5. Condição violada (A/B/C) nas respostas YES

| Prompt | A | B | C | outra/vazia | Entre os TP: A | B | C |
|---|---|---|---|---|---|---|---|
| zero_shot_guided_none | 1 | 12 | 9 | 0 | 1 | 8 | 5 |
| zero_shot_guided_summaries | 1 | 13 | 12 | 0 | 1 | 10 | 7 |
| zero_shot_guided_target | 1 | 12 | 9 | 0 | 1 | 11 | 4 |
| zero_shot_guided_both | 1 | 16 | 10 | 0 | 1 | 14 | 4 |
| few_shot_guided_none | 1 | 12 | 14 | 0 | 1 | 8 | 5 |
| few_shot_guided_summaries | 2 | 16 | 9 | 0 | 1 | 11 | 6 |
| few_shot_guided_target | 1 | 19 | 11 | 0 | 1 | 15 | 5 |
| few_shot_guided_both | 1 | 18 | 15 | 0 | 1 | 13 | 7 |

O dataset não traz a condição esperada, então não é possível medir a acurácia dessa classificação.

## 6. Resultado por projeto (acertos / chamadas, contando chamadas sem resposta como incorretas)

| Projeto | Casos (YES/NO) | zero_shot_guided_none | zero_shot_guided_summaries | zero_shot_guided_target | zero_shot_guided_both | few_shot_guided_none | few_shot_guided_summaries | few_shot_guided_target | few_shot_guided_both |
|---|---|---|---|---|---|---|---|---|---|
| elasticsearch | 22 (5/17) | 14/22 | 18/22 | 17/22 | 18/22 | 14/22 | 18/22 | 17/22 | 17/22 |
| spring-boot | 10 (5/5) | 6/10 | 7/10 | 7/10 | 8/10 | 7/10 | 7/10 | 9/10 | 6/10 |
| elasticsearch-river-mongodb | 6 (2/4) | 5/6 | 5/6 | 5/6 | 5/6 | 4/6 | 5/6 | 6/6 | 4/6 |
| jsoup | 4 (3/1) | 2/4 | 2/4 | 1/4 | 1/4 | 2/4 | 2/4 | 2/4 | 2/4 |
| hector | 4 (0/4) | 4/4 | 4/4 | 4/4 | 4/4 | 3/4 | 3/4 | 3/4 | 3/4 |
| retrofit | 3 (1/2) | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| storm | 2 (1/1) | 2/2 | 2/2 | 1/2 | 1/2 | 1/2 | 2/2 | 1/2 | 1/2 |
| antlr4 | 2 (2/0) | 2/2 | 2/2 | 2/2 | 2/2 | 1/2 | 2/2 | 1/2 | 2/2 |
| fitnesse | 2 (2/0) | 1/2 | 0/2 | 2/2 | 2/2 | 0/2 | 0/2 | 2/2 | 2/2 |
| okhttp | 2 (0/2) | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 |
| activiti | 2 (1/1) | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 |
| HikariCP | 2 (2/0) | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 2/2 |
| pushy | 2 (0/2) | 2/2 | 1/2 | 2/2 | 1/2 | 0/2 | 0/2 | 1/2 | 1/2 |
| cloud-slang | 1 (1/0) | 0/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| jOOQ | 1 (0/1) | 0/1 | 0/1 | 1/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 |
| swagger-maven-plugin | 1 (1/0) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| SimianArmy | 1 (0/1) | 1/1 | 0/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 0/1 |
| titan | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| druid | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| netty | 1 (1/0) | 1/1 | 0/1 | 0/1 | 0/1 | 0/1 | 1/1 | 0/1 | 1/1 |
| OpenTripPlanner | 1 (1/0) | 1/1 | 1/1 | 0/1 | 0/1 | 1/1 | 0/1 | 1/1 | 1/1 |
| webbit | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 0/1 | 1/1 | 1/1 | 1/1 |
| eureka | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| atmosphere | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| resty-gwt | 1 (1/0) | 0/1 | 1/1 | 0/1 | 1/1 | 0/1 | 1/1 | 0/1 | 0/1 |
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
| few_shot_guided_none | 0 | 0 | 0 | 1 | 0 | 1 |
| few_shot_guided_summaries | 0 | 0 | 0 | 0 | 0 | 0 |
| few_shot_guided_target | 0 | 0 | 0 | 0 | 0 | 0 |
| few_shot_guided_both | 0 | 0 | 0 | 0 | 0 | 0 |

## Observações

- Precisão, recall, F1 e especificidade são da classe YES (conflito semântico).
- Cada caso foi avaliado uma única vez por prompt, sem repetições, então não há medida de variância.
