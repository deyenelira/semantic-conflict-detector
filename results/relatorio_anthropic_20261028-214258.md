# Relatório — Detecção de conflitos semânticos em merges (Anthropic)

- **Modelo:** `claude-haiku-5-5`
- **Dataset:** `mergedataset` — 79 merges (29 com conflito semântico = YES, 50 sem = NO), de 29 projetos Java
- **Execução:** 2026-10-28 21:42 · `results/mergedataset_anthropic_20261028-214258_response.csv`
- **Chamadas:** 316 (79 casos × 4 prompts) — todas com `status = ok`, nenhuma pulada ou com erro
- **Respostas não parseáveis:** 2 (0,6%), contadas como erro nas métricas

## 1. Resultado geral

| Métrica | Valor |
|---|---|
| Acurácia | **61,1%** (193/316) |
| Precisão (YES) | 43,9% (18/41) |
| Recall (YES) | **15,5%** (18/116) |
| F1 (YES) | 0,23 |
| Especificidade (NO) | 87,5% (175/200) |

Baseline: sempre responder "NO" daria 63,3% de acurácia (200/316). O modelo ficou **abaixo** dessa linha de base, porque quase não detecta conflitos.

## 2. Resultado por prompt

| Prompt | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| one_shot_autonomous | 57,0% | 33,3% | 13,8% | 0,20 | 82,0% | 4 | 41 | 8 | 25 | 1 |
| one_shot_guided | **64,6%** | **55,6%** | **17,2%** | **0,26** | **92,0%** | 5 | 46 | 4 | 24 | 0 |
| zero_shot_autonomous | 59,5% | 41,7% | 17,2% | 0,24 | 84,0% | 5 | 42 | 7 | 24 | 1 |
| zero_shot_guided | 63,3% | 50,0% | 13,8% | 0,22 | 92,0% | 4 | 46 | 4 | 25 | 0 |
| **Global** | 61,1% | 43,9% | 15,5% | 0,23 | 87,5% | 18 | 175 | 23 | 98 | 2 |

Comparações por tipo de prompt (acurácia):

| Estratégia | Acurácia | | Modo | Acurácia |
|---|---|---|---|---|
| zero-shot | 61,4% | | autonomous | 58,2% |
| one-shot | 60,8% | | guided | 63,9% |

- **guided > autonomous** (+5,7 p.p.): o guiado gera menos falsos positivos (8 vs. 15) com o mesmo recall.
- **one-shot ≈ zero-shot**: o exemplo não trouxe ganho relevante.
- As diferenças entre prompts são pequenas (poucos acertos de diferença) e não têm significância estatística com 79 casos.

## 3. Consistência entre os prompts

| Votos "YES" nos 4 prompts | Casos YES (29) | Casos NO (50) |
|---|---|---|
| 0 | 21 (72%) | 41 (82%) |
| 1 | 3 | 1 |
| 2 | 2 | 4 |
| 3 | 1 | 2 |
| 4 | 2 (7%) | 2 (4%) |

- Os 4 prompts deram a mesma resposta em 65/79 casos (82%).
- **21 dos 29 conflitos reais (72%) nunca foram detectados** por nenhum prompt.
- Só 2 conflitos foram detectados pelos 4 prompts; 2 casos NO foram marcados como YES pelos 4 (falsos positivos sistemáticos).
- Voto majoritário (≥2 de 4): apenas 5 dos 29 conflitos detectados.

## 4. Condição violada (A/B)

Nas 41 respostas YES o modelo indicou a condição violada: **B em 25, A em 16**. Entre os 18 verdadeiros positivos: B em 12 e A em 6. O dataset não traz a condição esperada, então não é possível medir a acurácia dessa classificação.

## 5. Resultado por projeto (acertos / chamadas)

Maiores projetos: elasticsearch 64/88 (73%), spring-boot 20/40 (50%), elasticsearch-river-mongodb 17/24 (71%), hector 15/16 (94%), jsoup 5/16 (31%), retrofit 8/12 (67%).

- 100% de acerto: okhttp, swagger-maven-plugin, SimianArmy, titan, druid, webbit, eureka, atmosphere, java-faker, swagger-core, cucumber-jvm.
- 0% de acerto: antlr4, cloud-slang, fitnesse, jOOQ, netty, OpenTripPlanner, resty-gwt, quickml.
- O resultado por projeto reflete sobretudo a proporção de YES/NO de cada um (projetos com só casos NO acertam quase tudo; os de 0% são projetos de casos YES não detectados), e não a capacidade real do modelo no projeto.

## 6. Conclusões

1. O modelo é **conservador**: responde NO em 86% das chamadas (273/316), contra 37% de casos YES reais (116/316). Isso gera alta especificidade (87,5%) e recall muito baixo (15,5%).
2. Quando afirma haver conflito, acerta menos da metade das vezes (precisão 43,9%).
3. Os prompts *guided* tiveram o melhor equilíbrio; o melhor foi **one_shot_guided** (acurácia 64,6%, F1 0,26).
4. Para o objetivo de detectar conflitos, o recall é o ponto crítico. Possíveis próximos passos: calibrar o prompt para reduzir o viés para NO, testar um modelo maior e comparar com os resultados de Groq e Gemini no mesmo dataset.

## 7. Observações metodológicas

- Dataset desbalanceado (63% NO), por isso a acurácia sozinha engana; use recall/F1.
- Cada merge foi avaliado uma única vez por prompt, sem repetições, então não há medida de variância.
- Respostas sem YES/NO parseável (2) foram contadas como erro.
