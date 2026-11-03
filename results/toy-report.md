# Relatório por prompt — `toy_anthropic_20261102-212945_response.csv`

- **Dataset:** `toy` — 3 casos (2 YES, 1 NO)
- **Provedor:** `anthropic`
- **Prompts:** 8; **chamadas:** 24
- **Sem resposta YES/NO:** nenhuma
- As métricas consideram só as chamadas com resposta YES/NO; as demais aparecem em "Sem resposta".

## 1. Resultado geral

| Chamadas | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| todas | 87,5% | 84,2% | 100,0% | 0,91 | 62,5% | 16 | 5 | 3 | 0 | 0 |

Baseline: sempre responder "NO" daria 33,3% de acurácia (8/24). Proporção real de YES nas chamadas: 66,7%.

## 2. Resultado por prompt

| Prompt | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| zero_shot_guided_none | 66,7% | 66,7% | 100,0% | 0,80 | 0,0% | 2 | 0 | 1 | 0 | 0 |
| zero_shot_guided_summaries | 100,0% | 100,0% | 100,0% | 1,00 | 100,0% | 2 | 1 | 0 | 0 | 0 |
| zero_shot_guided_target | 100,0% | 100,0% | 100,0% | 1,00 | 100,0% | 2 | 1 | 0 | 0 | 0 |
| zero_shot_guided_both | 100,0% | 100,0% | 100,0% | 1,00 | 100,0% | 2 | 1 | 0 | 0 | 0 |
| few_shot_guided_none | 66,7% | 66,7% | 100,0% | 0,80 | 0,0% | 2 | 0 | 1 | 0 | 0 |
| few_shot_guided_summaries | 100,0% | 100,0% | 100,0% | 1,00 | 100,0% | 2 | 1 | 0 | 0 | 0 |
| few_shot_guided_target | 66,7% | 66,7% | 100,0% | 0,80 | 0,0% | 2 | 0 | 1 | 0 | 0 |
| few_shot_guided_both | 100,0% | 100,0% | 100,0% | 1,00 | 100,0% | 2 | 1 | 0 | 0 | 0 |

| Prompt | Respostas YES | Respostas NO | Sem resposta | % YES (das respondidas) |
|---|---|---|---|---|
| zero_shot_guided_none | 3 | 0 | 0 | 100,0% |
| zero_shot_guided_summaries | 2 | 1 | 0 | 66,7% |
| zero_shot_guided_target | 2 | 1 | 0 | 66,7% |
| zero_shot_guided_both | 2 | 1 | 0 | 66,7% |
| few_shot_guided_none | 3 | 0 | 0 | 100,0% |
| few_shot_guided_summaries | 2 | 1 | 0 | 66,7% |
| few_shot_guided_target | 3 | 0 | 0 | 100,0% |
| few_shot_guided_both | 2 | 1 | 0 | 66,7% |

## 3. Efeito de cada fator

### Zero-shot vs. few-shot (somando as variantes de contexto)

| Tipo | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| zero-shot | 91,7% | 88,9% | 100,0% | 0,94 | 75,0% | 8 | 3 | 1 | 0 | 0 |
| few-shot | 83,3% | 80,0% | 100,0% | 0,89 | 50,0% | 8 | 2 | 2 | 0 | 0 |

### Contexto fornecido (somando zero-shot e few-shot)

| Contexto | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| none | 66,7% | 66,7% | 100,0% | 0,80 | 0,0% | 4 | 0 | 2 | 0 | 0 |
| summaries | 100,0% | 100,0% | 100,0% | 1,00 | 100,0% | 4 | 2 | 0 | 0 | 0 |
| target | 83,3% | 80,0% | 100,0% | 0,89 | 50,0% | 4 | 1 | 1 | 0 | 0 |
| both | 100,0% | 100,0% | 100,0% | 1,00 | 100,0% | 4 | 2 | 0 | 0 | 0 |

## 4. Concordância entre os prompts

Votos "YES" por caso, somando os 8 prompts (chamadas sem resposta não contam como YES):

| Votos YES (de 8) | Casos YES reais | Casos NO reais |
|---|---|---|
| 0 | 0 | 0 |
| 1 | 0 | 0 |
| 2 | 0 | 0 |
| 3 | 0 | 1 |
| 4 | 0 | 0 |
| 5 | 0 | 0 |
| 6 | 0 | 0 |
| 7 | 0 | 0 |
| 8 | 2 | 0 |

- YES reais que nenhum prompt detectou: 0/2
- NO reais marcados como YES por ≥1 prompt: 1/1

Ensemble por voto (por caso, 3 casos):

| Regra (YES se…) | Acurácia | Precisão | Recall | F1 | TP | FP |
|---|---|---|---|---|---|---|
| ≥1 de 8 | 66,7% | 66,7% | 100,0% | 0,80 | 2 | 1 |
| ≥2 de 8 | 66,7% | 66,7% | 100,0% | 0,80 | 2 | 1 |
| ≥3 de 8 | 66,7% | 66,7% | 100,0% | 0,80 | 2 | 1 |
| ≥4 de 8 | 100,0% | 100,0% | 100,0% | 1,00 | 2 | 0 |
| ≥5 de 8 | 100,0% | 100,0% | 100,0% | 1,00 | 2 | 0 |
| ≥6 de 8 | 100,0% | 100,0% | 100,0% | 1,00 | 2 | 0 |
| ≥7 de 8 | 100,0% | 100,0% | 100,0% | 1,00 | 2 | 0 |
| ≥8 de 8 | 100,0% | 100,0% | 100,0% | 1,00 | 2 | 0 |

Concordância par a par (mesma resposta, sobre os casos respondidos pelos dois prompts):

|  | zero_shot_guided_none | zero_shot_guided_summaries | zero_shot_guided_target | zero_shot_guided_both | few_shot_guided_none | few_shot_guided_summaries | few_shot_guided_target | few_shot_guided_both |
|---|---|---|---|---|---|---|---|---|
| **zero_shot_guided_none** | 100,0% | 66,7% | 66,7% | 66,7% | 100,0% | 66,7% | 100,0% | 66,7% |
| **zero_shot_guided_summaries** | 66,7% | 100,0% | 100,0% | 100,0% | 66,7% | 100,0% | 66,7% | 100,0% |
| **zero_shot_guided_target** | 66,7% | 100,0% | 100,0% | 100,0% | 66,7% | 100,0% | 66,7% | 100,0% |
| **zero_shot_guided_both** | 66,7% | 100,0% | 100,0% | 100,0% | 66,7% | 100,0% | 66,7% | 100,0% |
| **few_shot_guided_none** | 100,0% | 66,7% | 66,7% | 66,7% | 100,0% | 66,7% | 100,0% | 66,7% |
| **few_shot_guided_summaries** | 66,7% | 100,0% | 100,0% | 100,0% | 66,7% | 100,0% | 66,7% | 100,0% |
| **few_shot_guided_target** | 100,0% | 66,7% | 66,7% | 66,7% | 100,0% | 66,7% | 100,0% | 66,7% |
| **few_shot_guided_both** | 66,7% | 100,0% | 100,0% | 100,0% | 66,7% | 100,0% | 66,7% | 100,0% |

## 5. Condição violada (A/B/C) nas respostas YES

| Prompt | A | B | C | outra/vazia | Entre os TP: A | B | C |
|---|---|---|---|---|---|---|---|
| zero_shot_guided_none | 1 | 0 | 2 | 0 | 0 | 0 | 2 |
| zero_shot_guided_summaries | 0 | 0 | 2 | 0 | 0 | 0 | 2 |
| zero_shot_guided_target | 0 | 0 | 2 | 0 | 0 | 0 | 2 |
| zero_shot_guided_both | 0 | 0 | 2 | 0 | 0 | 0 | 2 |
| few_shot_guided_none | 0 | 0 | 3 | 0 | 0 | 0 | 2 |
| few_shot_guided_summaries | 0 | 0 | 2 | 0 | 0 | 0 | 2 |
| few_shot_guided_target | 1 | 0 | 2 | 0 | 0 | 0 | 2 |
| few_shot_guided_both | 0 | 0 | 2 | 0 | 0 | 0 | 2 |

O dataset não traz a condição esperada, então não é possível medir a acurácia dessa classificação.

## 6. Resultado por projeto (acertos / chamadas, contando chamadas sem resposta como incorretas)

| Projeto | Casos (YES/NO) | zero_shot_guided_none | zero_shot_guided_summaries | zero_shot_guided_target | zero_shot_guided_both | few_shot_guided_none | few_shot_guided_summaries | few_shot_guided_target | few_shot_guided_both |
|---|---|---|---|---|---|---|---|---|---|
| c01_porcentagem_fracao | 1 (1/0) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| n02_nova_view_sem_duplicar | 1 (0/1) | 0/1 | 1/1 | 1/1 | 1/1 | 0/1 | 1/1 | 0/1 | 1/1 |
| c05_lista_vira_gerador | 1 (1/0) | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |

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
