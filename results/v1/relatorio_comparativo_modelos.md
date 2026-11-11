# Relatório comparativo — Detecção de conflitos semânticos em merges (família Claude)

- **Modelos:** `claude-haiku-5-5`, `claude-sonnet-5-5`, `claude-opus-5-5`, `claude-fable-5-1` 
- **Dataset:** `mergedataset` — 79 merges (29 com conflito semântico = YES, 50 sem = NO)
- **Fonte:** `results/final/claude-*.csv`
- **Prompts avaliados:** apenas 2 (`zero_shot_guided` e `one_shot_guided`) — as variantes *autonomous* não constam nesses arquivos
- **Chamadas:** 158 por modelo (79 casos × 2 prompts)
- **Respostas sem resposta (erro):** claude-haiku-5-5: 0; claude-sonnet-5-5: 0; claude-opus-5-5: 15; claude-fable-5-1: 8. Todas as falhas são `RuntimeError: refusal (category=reasoning_extraction)` (recusa da API), contadas como erro nas métricas (YES esperado → FN; NO esperado → erro, sem TN)

## 1. Resultado geral por modelo

| Modelo | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 76,6% | 67,2% | 70,7% | 0,69 | 80,0% | 41 | 80 | 20 | 17 | 0 |
| claude-sonnet-5-5 | 67,1% | 75,0% | 15,5% | 0,26 | 97,0% | 9 | 97 | 3 | 49 | 0 |
| claude-opus-5-5 | 68,4% | 80,8% | 36,2% | 0,50 | 87,0% | 21 | 87 | 5 | 37 | 15 |
| claude-fable-5-1 | 67,1% | 76,2% | 27,6% | 0,41 | 90,0% | 16 | 90 | 5 | 42 | 8 |

Baseline: sempre responder "NO" daria 63,3% de acurácia (100/158).

| Modelo | Respostas YES | Respostas NO | Sem resposta | % YES (das respondidas) | Acurácia vs. baseline |
|---|---|---|---|---|---|
| claude-haiku-5-5 | 61 | 97 | 0 | 38,6% | +13,3 p.p. |
| claude-sonnet-5-5 | 12 | 146 | 0 | 7,6% | +3,8 p.p. |
| claude-opus-5-5 | 26 | 117 | 15 | 18,2% | +5,1 p.p. |
| claude-fable-5-1 | 21 | 129 | 8 | 14,0% | +3,8 p.p. |

Proporção real de YES nas chamadas: 36,7%.

## 2. Resultado por prompt

### zero_shot_guided

| Modelo | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 77,2% | 67,7% | 72,4% | 0,70 | 80,0% | 21 | 40 | 10 | 8 | 0 |
| claude-sonnet-5-5 | 65,8% | 75,0% | 10,3% | 0,18 | 98,0% | 3 | 49 | 1 | 26 | 0 |
| claude-opus-5-5 | 72,2% | 80,0% | 41,4% | 0,55 | 90,0% | 12 | 45 | 3 | 17 | 5 |
| claude-fable-5-1 | 70,9% | 80,0% | 27,6% | 0,41 | 96,0% | 8 | 48 | 2 | 21 | 0 |

### one_shot_guided

| Modelo | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 75,9% | 66,7% | 69,0% | 0,68 | 80,0% | 20 | 40 | 10 | 9 | 0 |
| claude-sonnet-5-5 | 68,4% | 75,0% | 20,7% | 0,32 | 96,0% | 6 | 48 | 2 | 23 | 0 |
| claude-opus-5-5 | 64,6% | 81,8% | 31,0% | 0,45 | 84,0% | 9 | 42 | 2 | 20 | 10 |
| claude-fable-5-1 | 63,3% | 72,7% | 27,6% | 0,40 | 84,0% | 8 | 42 | 3 | 21 | 8 |

### Comparação entre os prompts (acurácia / F1 / recall)

| Modelo | zero_shot acc | one_shot acc | Δ acc (one − zero) | zero_shot F1 | one_shot F1 | zero_shot recall | one_shot recall |
|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 77,2% | 75,9% | -1,3 p.p. | 0,70 | 0,68 | 72,4% | 69,0% |
| claude-sonnet-5-5 | 65,8% | 68,4% | +2,5 p.p. | 0,18 | 0,32 | 10,3% | 20,7% |
| claude-opus-5-5 | 72,2% | 64,6% | -7,6 p.p. | 0,55 | 0,45 | 41,4% | 31,0% |
| claude-fable-5-1 | 70,9% | 63,3% | -7,6 p.p. | 0,41 | 0,40 | 27,6% | 27,6% |

Agregado dos 4 modelos:

| Prompt | Acurácia | Precisão | Recall | F1 | Especificidade | TP | TN | FP | FN | Sem resposta |
|---|---|---|---|---|---|---|---|---|---|---|
| zero_shot_guided | 71,5% | 73,3% | 37,9% | 0,50 | 91,0% | 44 | 182 | 16 | 72 | 5 |
| one_shot_guided | 68,0% | 71,7% | 37,1% | 0,49 | 86,0% | 43 | 172 | 17 | 73 | 18 |

## 3. Consistência entre os dois prompts (por modelo)

| Modelo | Mesma resposta nos 2 prompts | YES reais detectados por 0 | por 1 | por 2 | NO reais marcados YES por 0 | por 1 | por 2 |
|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 70/79 (88,6%) | 7 | 3 | 19 | 37 | 6 | 7 |
| claude-sonnet-5-5 | 75/79 (94,9%) | 23 | 3 | 3 | 48 | 1 | 1 |
| claude-opus-5-5 | 66/79 (83,5%) | 17 | 3 | 9 | 47 | 1 | 2 |
| claude-fable-5-1 | 68/79 (86,1%) | 20 | 2 | 7 | 47 | 1 | 2 |

## 4. Concordância entre os modelos

Votos "YES" somando os 4 modelos × 2 prompts (8 votos por caso; erros não contam como YES):

| Votos YES (de 8) | Casos YES reais | Casos NO reais |
|---|---|---|
| 0 | 6 | 37 |
| 1 | 3 | 5 |
| 2 | 8 | 4 |
| 3 | 1 | 1 |
| 4 | 3 | 1 |
| 5 | 1 | 1 |
| 6 | 3 | 0 |
| 7 | 2 | 0 |
| 8 | 2 | 1 |

- YES reais que **nenhum** modelo/prompt detectou: 6/29
- YES reais detectados por pelo menos um modelo/prompt: 23/29
- NO reais marcados como YES por ≥1 voto: 13/50

Ensemble por voto (por caso, 79 casos):

| Regra (YES se…) | Acurácia | Precisão | Recall | F1 | TP | FP |
|---|---|---|---|---|---|---|
| ≥1 de 8 | 75,9% | 63,9% | 79,3% | 0,71 | 23 | 13 |
| ≥2 de 8 | 78,5% | 71,4% | 69,0% | 0,70 | 20 | 8 |
| ≥3 de 8 | 73,4% | 75,0% | 41,4% | 0,53 | 12 | 4 |
| ≥4 de 8 | 73,4% | 78,6% | 37,9% | 0,51 | 11 | 3 |
| ≥5 de 8 | 70,9% | 80,0% | 27,6% | 0,41 | 8 | 2 |

Concordância par a par (mesma resposta, sobre as chamadas respondidas por ambos):

| | claude-haiku-5-5 | claude-sonnet-5-5 | claude-opus-5-5 | claude-fable-5-1 |
|---|---|---|---|---|
| **claude-haiku-5-5** | 100,0% | 69,0% | 76,9% | 72,7% |
| **claude-sonnet-5-5** | 69,0% | 100,0% | 87,4% | 90,0% |
| **claude-opus-5-5** | 76,9% | 87,4% | 100,0% | 90,8% |
| **claude-fable-5-1** | 72,7% | 90,0% | 90,8% | 100,0% |

## 5. Condição violada (A/B/C) nas respostas YES

| Modelo | A | B | C | outra/vazia | Entre os TP: A | B | C |
|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 2 | 38 | 21 | 0 | 2 | 29 | 10 |
| claude-sonnet-5-5 | 2 | 9 | 1 | 0 | 2 | 6 | 1 |
| claude-opus-5-5 | 3 | 22 | 1 | 0 | 3 | 17 | 1 |
| claude-fable-5-1 | 2 | 15 | 4 | 0 | 2 | 12 | 2 |

O dataset não traz a condição esperada, então não é possível medir a acurácia dessa classificação.

## 6. Resultado por projeto (acertos / chamadas, contando erros como incorretos)

| Projeto | Casos (YES/NO) | claude-haiku-5-5 | claude-sonnet-5-5 | claude-opus-5-5 | claude-fable-5-1 |
|---|---|---|---|---|---|
| elasticsearch | 22 (5/17) | 34/44 | 34/44 | 33/44 | 33/44 |
| spring-boot | 10 (5/5) | 16/20 | 13/20 | 14/20 | 11/20 |
| elasticsearch-river-mongodb | 6 (2/4) | 10/12 | 8/12 | 7/12 | 9/12 |
| jsoup | 4 (3/1) | 4/8 | 2/8 | 1/8 | 3/8 |
| hector | 4 (0/4) | 8/8 | 8/8 | 7/8 | 8/8 |
| retrofit | 3 (1/2) | 6/6 | 4/6 | 6/6 | 4/6 |
| storm | 2 (1/1) | 4/4 | 2/4 | 4/4 | 4/4 |
| antlr4 | 2 (2/0) | 4/4 | 0/4 | 1/4 | 0/4 |
| fitnesse | 2 (2/0) | 4/4 | 0/4 | 0/4 | 0/4 |
| okhttp | 2 (0/2) | 4/4 | 4/4 | 3/4 | 3/4 |
| activiti | 2 (1/1) | 2/4 | 3/4 | 4/4 | 2/4 |
| HikariCP | 2 (2/0) | 2/4 | 2/4 | 2/4 | 2/4 |
| pushy | 2 (0/2) | 2/4 | 4/4 | 4/4 | 4/4 |
| cloud-slang | 1 (1/0) | 2/2 | 1/2 | 2/2 | 2/2 |
| jOOQ | 1 (0/1) | 0/2 | 1/2 | 1/2 | 1/2 |
| swagger-maven-plugin | 1 (1/0) | 2/2 | 2/2 | 2/2 | 2/2 |
| SimianArmy | 1 (0/1) | 0/2 | 2/2 | 2/2 | 2/2 |
| titan | 1 (0/1) | 2/2 | 2/2 | 2/2 | 2/2 |
| druid | 1 (0/1) | 2/2 | 2/2 | 2/2 | 2/2 |
| netty | 1 (1/0) | 1/2 | 0/2 | 0/2 | 0/2 |
| OpenTripPlanner | 1 (1/0) | 0/2 | 0/2 | 0/2 | 0/2 |
| webbit | 1 (0/1) | 2/2 | 2/2 | 2/2 | 2/2 |
| eureka | 1 (0/1) | 2/2 | 2/2 | 2/2 | 2/2 |
| atmosphere | 1 (0/1) | 2/2 | 2/2 | 2/2 | 2/2 |
| resty-gwt | 1 (1/0) | 0/2 | 0/2 | 0/2 | 0/2 |
| quickml | 1 (0/1) | 0/2 | 0/2 | 0/2 | 0/2 |
| java-faker | 1 (0/1) | 2/2 | 2/2 | 2/2 | 2/2 |
| swagger-core | 1 (0/1) | 2/2 | 2/2 | 1/2 | 2/2 |
| cucumber-jvm | 1 (0/1) | 2/2 | 2/2 | 2/2 | 2/2 |

O resultado por projeto reflete sobretudo a proporção de YES/NO de cada projeto (projetos só com NO acertam quase tudo) e não a capacidade real do modelo.

## 7. Recusas da API

| Modelo | Recusas | zero_shot_guided | one_shot_guided | Em casos YES | Em casos NO |
|---|---|---|---|---|---|
| claude-haiku-5-5 | 0 | 0 | 0 | 0 | 0 |
| claude-sonnet-5-5 | 0 | 0 | 0 | 0 | 0 |
| claude-opus-5-5 | 15 | 5 | 10 | 7 | 8 |
| claude-fable-5-1 | 8 | 0 | 8 | 3 | 5 |
## 8. Conclusões

1. **Haiku 5,5 foi o melhor modelo nesta execução**: acurácia 76,6%, recall 70,7% e F1 0,69, muito à frente dos demais (F1 entre 0,26 e 0,50). É o único que supera de forma clara a baseline "sempre NO" (63,3%) e o único com recall relevante. O custo é uma especificidade menor (80%) e mais falsos positivos (20, contra 3–5 dos outros).
2. **Os modelos maiores são muito conservadores**: respondem YES em apenas 7,6% (Sonnet), 14,0% (Fable) e 18,2% (Opus) das chamadas respondidas, contra 36,7% de YES reais. Têm a maior precisão (75–81%) e especificidade (87–97%), mas recall de 15–36%. Ou seja, quando afirmam haver conflito costumam acertar, mas deixam passar a maioria. Sonnet e Fable ficam apenas ~4 p.p. acima da baseline.
3. **Tamanho do modelo não correlaciona com desempenho** neste dataset e com estes prompts: o menor modelo (Haiku) venceu. A ordem de F1 é Haiku (0,69) > Opus (0,50) > Fable (0,41) > Sonnet (0,26).
4. **Prompts**: o efeito de zero-shot vs. one-shot é inconsistente. Haiku quase não muda (−1,3 p.p.); Sonnet melhora com one-shot (+2,5 p.p., recall 10% → 21%); Opus e Fable pioram (−7,6 p.p. cada, em parte porque as recusas se concentram no one-shot). No agregado, zero_shot_guided (71,5%) fica à frente de one_shot_guided (68,0%), mas a diferença é pequena e sem significância estatística com 79 casos e uma execução por prompt.
5. **Recusas da API**: Opus (15) e Fable (8) tiveram recusas `reasoning_extraction`, concentradas no `one_shot_guided` (18 de 23). Elas reduzem a acurácia medida desses modelos (contam como erro) e tornam a comparação com Haiku/Sonnet (0 recusas) menos justa. Com as recusas desconsideradas, a acurácia seria 75,5% (Opus: 108/143) e 70,7% (Fable: 106/150); a ordem geral não muda.
6. **Os modelos grandes concordam entre si** (Sonnet–Opus 87%, Sonnet–Fable 90%, Opus–Fable 91%) e discordam bastante do Haiku (69–77%): Sonnet, Opus e Fable erram nos mesmos casos, em geral YES reais não detectados.
7. **Casos difíceis**: 6 dos 29 conflitos reais não foram detectados por nenhum modelo/prompt (23 por ao menos um). Projetos como OpenTripPlanner, resty-gwt, netty, fitnesse e antlr4 (só casos YES) foram quase sempre errados pelos três modelos maiores; Haiku acerta fitnesse e antlr4 mas erra jOOQ, SimianArmy e quickml (casos NO), refletindo seu viés para YES.
8. **Ensemble**: combinar os 8 votos (4 modelos × 2 prompts) ajuda. A regra "YES com ≥2 votos" atinge 78,5% de acurácia, F1 0,70 e precisão 71,4%, superando qualquer modelo isolado em acurácia (Haiku: 76,6%) com menos falsos positivos (8 casos NO marcados como YES, contra 13 casos em Haiku, que errou 20 chamadas). "≥1 voto" maximiza o recall (79,3%).
9. **Condição violada**: B domina em todos os modelos (Haiku 38/61, Sonnet 9/12, Opus 22/26, Fable 15/21); Haiku é o único que usa C com frequência (21). Não há gabarito para medir a acurácia dessa classificação.
10. **Próximos passos**: calibrar o prompt dos modelos grandes para reduzir o viés para NO (recall é o ponto crítico); investigar as recusas `reasoning_extraction` (ajustar o prompt para não pedir o raciocínio); rodar também os prompts *autonomous* para os 4 modelos, com repetições para medir variância; e comparar com Groq e Gemini no mesmo dataset.

## 9. Observações metodológicas

- Dataset desbalanceado (63% NO), então a acurácia sozinha engana; use recall e F1.
- Só os prompts `zero_shot_guided` e `one_shot_guided` estão nos arquivos finais, portanto os números não são diretamente comparáveis com o relatório anterior (4 prompts, só Haiku). Em especial, o Haiku aqui (76,6%) difere do relatório anterior (61,1%) porque o prompt *guided* foi refinado nas últimas execuções (commits "prompt refinement").
- Cada merge foi avaliado uma única vez por prompt e modelo, sem repetições, então não há medida de variância.
- Respostas sem YES/NO (recusas) foram contadas como erro: para casos YES esperados entram como FN; para casos NO esperados não contam como TN nem como FP (reduzem a acurácia e a especificidade).
- Métricas de precisão, recall, F1 e especificidade são da classe YES (conflito semântico).
