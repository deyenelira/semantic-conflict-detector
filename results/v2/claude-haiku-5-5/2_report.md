# Relatório por prompt — `claude-haiku-5-5/2.csv`

- **Casos:** 79 (29 YES, 50 NO)
- **Prompts:** 8; **chamadas:** 632
- **Sem resposta YES/NO:** nenhuma
- As métricas consideram só as chamadas com resposta YES/NO; as demais aparecem em "Sem resposta".

## 1. Resultado geral

| Chamadas | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| todas | 69,5% | 58,4% | 58,2% | 0,58 | 76,0% | 135 | 304 | 96 | 97 | 0 |

Baseline: sempre responder "NO" daria 63,3% de acurácia (400/632). Proporção real de YES nas chamadas: 36,7%.

## 2. Resultado por prompt

| Prompt | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| zero_shot_guided_none | 63,3% | 50,0% | 44,8% | 0,47 | 74,0% | 13 | 37 | 13 | 16 | 0 |
| zero_shot_guided_summaries | 70,9% | 61,5% | 55,2% | 0,58 | 80,0% | 16 | 40 | 10 | 13 | 0 |
| zero_shot_guided_target | 77,2% | 72,0% | 62,1% | 0,67 | 86,0% | 18 | 43 | 7 | 11 | 0 |
| zero_shot_guided_both | 74,7% | 66,7% | 62,1% | 0,64 | 82,0% | 18 | 41 | 9 | 11 | 0 |
| few_shot_guided_none | 64,6% | 51,7% | 51,7% | 0,52 | 72,0% | 15 | 36 | 14 | 14 | 0 |
| few_shot_guided_summaries | 64,6% | 51,5% | 58,6% | 0,55 | 68,0% | 17 | 34 | 16 | 12 | 0 |
| few_shot_guided_target | 68,4% | 56,2% | 62,1% | 0,59 | 72,0% | 18 | 36 | 14 | 11 | 0 |
| few_shot_guided_both | 72,2% | 60,6% | 69,0% | 0,65 | 74,0% | 20 | 37 | 13 | 9 | 0 |

| Prompt | Respostas YES | Respostas NO | Sem resposta | % YES (das respondidas) |
|---|---|---|---|---|
| zero_shot_guided_none | 26 | 53 | 0 | 32,9% |
| zero_shot_guided_summaries | 26 | 53 | 0 | 32,9% |
| zero_shot_guided_target | 25 | 54 | 0 | 31,6% |
| zero_shot_guided_both | 27 | 52 | 0 | 34,2% |
| few_shot_guided_none | 29 | 50 | 0 | 36,7% |
| few_shot_guided_summaries | 33 | 46 | 0 | 41,8% |
| few_shot_guided_target | 32 | 47 | 0 | 40,5% |
| few_shot_guided_both | 33 | 46 | 0 | 41,8% |

## 3. Efeito de cada fator

### Zero-shot vs. few-shot (somando as variantes de contexto)

| Tipo | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| zero-shot | 71,5% | 62,5% | 56,0% | 0,59 | 80,5% | 65 | 161 | 39 | 51 | 0 |
| few-shot | 67,4% | 55,1% | 60,3% | 0,58 | 71,5% | 70 | 143 | 57 | 46 | 0 |

### Contexto fornecido (somando zero-shot e few-shot)

| Contexto | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| none | 63,9% | 50,9% | 48,3% | 0,50 | 73,0% | 28 | 73 | 27 | 30 | 0 |
| summaries | 67,7% | 55,9% | 56,9% | 0,56 | 74,0% | 33 | 74 | 26 | 25 | 0 |
| target | 72,8% | 63,2% | 62,1% | 0,63 | 79,0% | 36 | 79 | 21 | 22 | 0 |
| both | 73,4% | 63,3% | 65,5% | 0,64 | 78,0% | 38 | 78 | 22 | 20 | 0 |

## 4. Concordância entre os prompts

Votos "YES" por caso, somando os 8 prompts (chamadas sem resposta não contam como YES):

| Votos YES (de 8) | Casos YES reais | Casos NO reais |
|---|---|---|
| 0 | 5 | 27 |
| 1 | 0 | 5 |
| 2 | 3 | 3 |
| 3 | 2 | 2 |
| 4 | 2 | 1 |
| 5 | 4 | 4 |
| 6 | 3 | 4 |
| 7 | 3 | 1 |
| 8 | 7 | 3 |

- YES reais que nenhum prompt detectou: 5/29
- NO reais marcados como YES por ≥1 prompt: 23/50

Ensemble por voto (por caso, 79 casos):

| Regra (YES se…) | Acurácia | Precisão | Recall | F1 | TP | FP |
|---|---|---|---|---|---|---|
| ≥1 de 8 | 64,6% | 51,1% | 82,8% | 0,63 | 24 | 23 |
| ≥2 de 8 | 70,9% | 57,1% | 82,8% | 0,68 | 24 | 18 |
| ≥3 de 8 | 70,9% | 58,3% | 72,4% | 0,65 | 21 | 15 |
| ≥4 de 8 | 70,9% | 59,4% | 65,5% | 0,62 | 19 | 13 |
| ≥5 de 8 | 69,6% | 58,6% | 58,6% | 0,59 | 17 | 12 |
| ≥6 de 8 | 69,6% | 61,9% | 44,8% | 0,52 | 13 | 8 |
| ≥7 de 8 | 70,9% | 71,4% | 34,5% | 0,47 | 10 | 4 |
| ≥8 de 8 | 68,4% | 70,0% | 24,1% | 0,36 | 7 | 3 |

Concordância par a par (mesma resposta, sobre os casos respondidos pelos dois prompts):

|  | zero_shot_guided_none | zero_shot_guided_summaries | zero_shot_guided_target | zero_shot_guided_both | few_shot_guided_none | few_shot_guided_summaries | few_shot_guided_target | few_shot_guided_both |
|---|---|---|---|---|---|---|---|---|
| **zero_shot_guided_none** | 100,0% | 84,8% | 81,0% | 73,4% | 88,6% | 81,0% | 79,7% | 81,0% |
| **zero_shot_guided_summaries** | 84,8% | 100,0% | 83,5% | 81,0% | 81,0% | 83,5% | 82,3% | 83,5% |
| **zero_shot_guided_target** | 81,0% | 83,5% | 100,0% | 77,2% | 79,7% | 74,7% | 78,5% | 79,7% |
| **zero_shot_guided_both** | 73,4% | 81,0% | 77,2% | 100,0% | 72,2% | 67,1% | 78,5% | 79,7% |
| **few_shot_guided_none** | 88,6% | 81,0% | 79,7% | 72,2% | 100,0% | 82,3% | 78,5% | 79,7% |
| **few_shot_guided_summaries** | 81,0% | 83,5% | 74,7% | 67,1% | 82,3% | 100,0% | 81,0% | 79,7% |
| **few_shot_guided_target** | 79,7% | 82,3% | 78,5% | 78,5% | 78,5% | 81,0% | 100,0% | 81,0% |
| **few_shot_guided_both** | 81,0% | 83,5% | 79,7% | 79,7% | 79,7% | 79,7% | 81,0% | 100,0% |

## 5. Condição violada (A/B/C) nas respostas YES

| Prompt | A | B | C | outra/vazia | Entre os TP: A | B | C |
|---|---|---|---|---|---|---|---|
| zero_shot_guided_none | 1 | 12 | 13 | 0 | 1 | 7 | 5 |
| zero_shot_guided_summaries | 2 | 13 | 11 | 0 | 2 | 10 | 4 |
| zero_shot_guided_target | 1 | 16 | 8 | 0 | 1 | 13 | 4 |
| zero_shot_guided_both | 1 | 17 | 9 | 0 | 1 | 13 | 4 |
| few_shot_guided_none | 0 | 12 | 17 | 0 | 0 | 6 | 9 |
| few_shot_guided_summaries | 1 | 14 | 18 | 0 | 1 | 8 | 8 |
| few_shot_guided_target | 1 | 16 | 15 | 0 | 1 | 11 | 6 |
| few_shot_guided_both | 1 | 17 | 15 | 0 | 1 | 12 | 7 |

O dataset não traz a condição esperada, então não é possível medir a acurácia dessa classificação.

## 6. Resultado por projeto (acertos / chamadas, contando chamadas sem resposta como incorretas)

| Projeto | Casos (YES/NO) | zero_shot_guided_none | zero_shot_guided_summaries | zero_shot_guided_target | zero_shot_guided_both | few_shot_guided_none | few_shot_guided_summaries | few_shot_guided_target | few_shot_guided_both |
|---|---|---|---|---|---|---|---|---|---|
| elasticsearch | 22 (5/17) | 14/22 | 17/22 | 19/22 | 18/22 | 13/22 | 14/22 | 14/22 | 17/22 |
| spring-boot | 10 (5/5) | 8/10 | 7/10 | 6/10 | 7/10 | 7/10 | 8/10 | 7/10 | 8/10 |
| elasticsearch-river-mongodb | 6 (2/4) | 5/6 | 5/6 | 5/6 | 6/6 | 4/6 | 2/6 | 4/6 | 6/6 |
| jsoup | 4 (3/1) | 2/4 | 2/4 | 2/4 | 2/4 | 2/4 | 2/4 | 2/4 | 2/4 |
| hector | 4 (0/4) | 2/4 | 3/4 | 4/4 | 3/4 | 2/4 | 3/4 | 2/4 | 2/4 |
| retrofit | 3 (1/2) | 2/3 | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| storm | 2 (1/1) | 1/2 | 1/2 | 2/2 | 1/2 | 1/2 | 1/2 | 2/2 | 1/2 |
| antlr4 | 2 (2/0) | 1/2 | 2/2 | 2/2 | 2/2 | 1/2 | 1/2 | 2/2 | 1/2 |
| fitnesse | 2 (2/0) | 0/2 | 0/2 | 1/2 | 2/2 | 0/2 | 0/2 | 2/2 | 1/2 |
| okhttp | 2 (0/2) | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 |
| activiti | 2 (1/1) | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 |
| HikariCP | 2 (2/0) | 1/2 | 2/2 | 1/2 | 1/2 | 1/2 | 2/2 | 1/2 | 2/2 |
| pushy | 2 (0/2) | 0/2 | 0/2 | 1/2 | 1/2 | 1/2 | 0/2 | 0/2 | 0/2 |
| cloud-slang | 1 (1/0) | 1/1 | 0/1 | 1/1 | 0/1 | 1/1 | 1/1 | 0/1 | 1/1 |
| jOOQ | 1 (0/1) | 0/1 | 0/1 | 1/1 | 0/1 | 0/1 | 0/1 | 1/1 | 0/1 |
| swagger-maven-plugin | 1 (1/0) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| SimianArmy | 1 (0/1) | 1/1 | 1/1 | 1/1 | 0/1 | 1/1 | 1/1 | 1/1 | 0/1 |
| titan | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| druid | 1 (0/1) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| netty | 1 (1/0) | 0/1 | 1/1 | 1/1 | 0/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| OpenTripPlanner | 1 (1/0) | 0/1 | 0/1 | 0/1 | 1/1 | 1/1 | 0/1 | 0/1 | 0/1 |
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
