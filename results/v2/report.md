# Comparação entre modelos — `v2`

- **Modelos:** `claude-haiku-5-5` (3 execuções), `claude-sonnet-5-5` (3 execuções)
- **Casos:** 79 (29 YES, 50 NO); **prompts:** 8; **chamadas por execução:** 632
- As métricas aparecem como média entre as execuções, com o intervalo (mín–máx) entre parênteses, e consideram só as chamadas com resposta YES/NO.

## 1. Resultado geral por modelo

| Modelo | Acurácia | Precisão | Recall | F1 | Especificidade | Sem resposta (soma) | Estabilidade |
|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 71,8% (69,5%–73,7%) | 62,1% (58,4%–65,3%) | 59,8% (58,2%–60,8%) | 0,61 (0,58–0,63) | 78,7% (76,0%–81,2%) | 2 | 74,4% |
| claude-sonnet-5-5 | 66,0% (65,3%–66,8%) | 64,0% (61,4%–67,2%) | 16,7% (15,1%–18,5%) | 0,26 (0,24–0,29) | 94,6% (94,5%–94,8%) | 0 | 93,7% |

Estabilidade: fração das chamadas respondidas em todas as execuções que tiveram a mesma resposta em todas.

Usando a resposta da maioria das execuções para cada caso e prompt:

| Modelo | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 72,4% | 63,1% | 60,3% | 0,62 | 79,4% | 140 | 316 | 82 | 92 | 2 |
| claude-sonnet-5-5 | 65,7% | 62,7% | 15,9% | 0,25 | 94,5% | 37 | 378 | 22 | 195 | 0 |

## 2. Resultado por prompt (média entre as execuções)

### F1

| Prompt | claude-haiku-5-5 | claude-sonnet-5-5 |
|---|---|---|
| zero_shot_guided_none | 0,53 | 0,22 |
| zero_shot_guided_summaries | 0,60 | 0,27 |
| zero_shot_guided_target | 0,65 | 0,26 |
| zero_shot_guided_both | 0,65 | 0,28 |
| few_shot_guided_none | 0,56 | 0,20 |
| few_shot_guided_summaries | 0,59 | 0,27 |
| few_shot_guided_target | 0,62 | 0,28 |
| few_shot_guided_both | 0,66 | 0,34 |

### Recall

| Prompt | claude-haiku-5-5 | claude-sonnet-5-5 |
|---|---|---|
| zero_shot_guided_none | 48,3% | 13,8% |
| zero_shot_guided_summaries | 56,3% | 17,2% |
| zero_shot_guided_target | 59,8% | 16,1% |
| zero_shot_guided_both | 64,4% | 17,2% |
| few_shot_guided_none | 55,2% | 12,6% |
| few_shot_guided_summaries | 59,8% | 17,2% |
| few_shot_guided_target | 64,4% | 17,2% |
| few_shot_guided_both | 70,1% | 21,8% |

### Precisão

| Prompt | claude-haiku-5-5 | claude-sonnet-5-5 |
|---|---|---|
| zero_shot_guided_none | 58,7% | 55,6% |
| zero_shot_guided_summaries | 64,4% | 60,8% |
| zero_shot_guided_target | 72,2% | 66,7% |
| zero_shot_guided_both | 66,1% | 71,6% |
| few_shot_guided_none | 56,4% | 50,0% |
| few_shot_guided_summaries | 58,3% | 59,7% |
| few_shot_guided_target | 60,2% | 78,6% |
| few_shot_guided_both | 62,3% | 72,7% |

## 3. Efeito de cada fator (F1 médio entre as execuções)

### Zero-shot vs. few-shot (somando as variantes de contexto)

| Tipo | claude-haiku-5-5 | claude-sonnet-5-5 |
|---|---|---|
| zero-shot | 0,61 | 0,26 |
| few-shot | 0,61 | 0,27 |

### Contexto fornecido (somando zero-shot e few-shot)

| Contexto | claude-haiku-5-5 | claude-sonnet-5-5 |
|---|---|---|
| none | 0,54 | 0,21 |
| summaries | 0,59 | 0,27 |
| target | 0,64 | 0,27 |
| both | 0,66 | 0,31 |

## 4. Casos difíceis

Taxa de acerto de cada caso: fração das chamadas, somando prompts e execuções, com a resposta esperada (chamadas sem resposta contam como erro).

Casos em que todos os modelos acertaram menos da metade das chamadas: 12/79

| Caso | Esperado | claude-haiku-5-5 | claude-sonnet-5-5 |
|---|---|---|---|
| jsoup__a8b6982d__HttpConnection#execute | YES | 0,0% | 0,0% |
| jsoup__a44e18aa__TextNode#outerHtmlHead | YES | 0,0% | 0,0% |
| spring-boot__fdd3f12e__AutoConfigurationReportLoggingInitializer#logAutoConfigurationReport | YES | 0,0% | 0,0% |
| quickml__bae968d9__OutOfTimeCrossValidatorRunner#getRandomForestBuilder | NO | 0,0% | 0,0% |
| elasticsearch__59cb67c7__MultiMatchQueryBuilder#doXContent | YES | 0,0% | 0,0% |
| resty-gwt__867b917c__DirectRestServiceInterfaceClassCreator#getMethodCallback | YES | 16,7% | 0,0% |
| HikariCP__1bca94af__HikariConfig#validate | YES | 20,8% | 0,0% |
| spring-boot__6664ce19__AtomikosProperties#asProperties | YES | 25,0% | 4,2% |
| fitnesse__4d9ba9d2__SlimTableFactory#SlimTableFactory | YES | 41,7% | 0,0% |
| netty__193acdb3__LengthFieldBasedFrameDecoder#decode | YES | 45,8% | 0,0% |
| OpenTripPlanner__4c506dce__MultiShortestPathTree#dominates | YES | 45,8% | 0,0% |
| jOOQ__d96120f3__DSL#coalesce | NO | 20,8% | 45,8% |

Conflitos (YES) que nenhuma chamada de nenhum modelo detectou: 4/29
- `jsoup__a8b6982d__HttpConnection#execute`
- `jsoup__a44e18aa__TextNode#outerHtmlHead`
- `spring-boot__fdd3f12e__AutoConfigurationReportLoggingInitializer#logAutoConfigurationReport`
- `elasticsearch__59cb67c7__MultiMatchQueryBuilder#doXContent`
