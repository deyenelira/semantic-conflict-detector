# Casos divergentes — `v2`

- **Prompt:** `few_shot_guided_both`
- **Modelos (execuções):** `claude-haiku-5-5` (3), `claude-opus-5-5` (1), `claude-sonnet-5-5` (3)
- Entram os casos em que cada modelo deu a mesma resposta em todas as suas execuções, e ao menos um modelo respondeu YES e outro NO. Um modelo com uma única execução é sempre considerado estável.
- Em cada caso, os modelos que acertam vêm primeiro. A análise de cada execução começa recolhida; clique na execução para abri-la.

## 1. Conflitos detectados só por parte dos modelos

Casos com conflito (YES) em que algum modelo detecta o conflito e outro não: 10 casos.

| Caso | claude-haiku-5-5 | claude-opus-5-5 | claude-sonnet-5-5 |
|---|---|---|---|
| `antlr4__69ff2669__Python2Target#python2Keywords` | YES | YES | NO |
| `cloud-slang__20bac30d__SlangImpl#getAllEventTypes` | YES | NO | NO |
| `fitnesse__4d9ba9d2__SlimTableFactoryTest#setUp` | YES | NO | NO |
| `jsoup__3f7d2c71__HttpConnection#execute` | YES | NO | NO |
| `netty__193acdb3__LengthFieldBasedFrameDecoder#decode` | YES | NO | NO |
| `spring-boot__6664ce19__AtomikosPropertiesTests#testDefaultProperties` | YES | NO | YES |
| `HikariCP__1bca94af__HikariConfig#validate` | YES | NO | NO |
| `elasticsearch__d8968869__TransportReplicationAction#doRun` | YES | NO | NO |
| `elasticsearch__d8968869__DocWriteResponse#writeTo` | YES | YES | NO |
| `elasticsearch__d8968869__DocWriteResponse#toXContent` | YES | NO | NO |

### 1. `antlr4__69ff2669__Python2Target#python2Keywords`

- **Target:** `python2Keywords`
- **Esperado:** YES; **acertam:** claude-haiku-5-5, claude-opus-5-5; **erram:** claude-sonnet-5-5
- **Código:** [antlr4__69ff2669__Python2Target](../../data/mergedataset/antlr4__69ff2669__Python2Target)

**LEFT:** Left changes the list of values of an array of Strings during its initialization (adition of a new value)

**RIGHT:** Right changes the list of values of an array of Strings during its initialization (adition of a new value)

**Justificativa do dataset:** Left and Right change the same array list, which means they change the size field. A test case should explore the array size in each merge scenario commit.

#### claude-haiku-5-5: YES ✅

<details><summary>Execução 1 (<code>1.csv</code>): YES — Condição B: python2Keywords</summary>

1. INTENÇÃO: LEFT adiciona a palavra "return" ao array `python2Keywords`. RIGHT adiciona a palavra "del" ao mesmo array. Os diffs confirmam os resumos. Os dois trechos são diferentes e não se sobrepõem textualmente.

2. ESTADO: O elemento de estado é o array estático `python2Keywords`, lido por `addBadWords()` através de `badWords`. O trecho alterado por cada lado é a sua inicialização.

3. TABELA DE ESTADOS:
   - Entrada: a inicialização do array, tomada como um todo, com os itens da BASE.
   - `python2Keywords` (conteúdo inteiro):
     - BASE = {…, "delattr", "dict", …, "reload", "repr", "reversed", …}
     - LEFT = BASE + "return"
     - RIGHT = BASE + "del"
     - MERGE = BASE + "del" + "return"

4. CRITÉRIO DE CONFLITO: X = `python2Keywords` (valor do array inteiro).
   - (A) Não se aplica: o valor de X em LEFT e em RIGHT difere de BASE.
   - (B) O valor de X em LEFT difere de BASE. O MERGE contém também "del", portanto MERGE ≠ LEFT e o MERGE não preserva o valor de LEFT. A condição se aplica pela letra da regra, que compara o elemento inteiro e não apenas a parte alterada por um lado. O mesmo vale para RIGHT, já que MERGE ≠ RIGHT.
   - (C) Não é necessária, pois B já se aplica. Além disso, nenhum código alterado lê ou é controlado por X de forma que mude de comportamento: as duas alterações são apenas inserções de literais no array.

   Observação: a união das duas inserções é semanticamente a intenção de ambos os lados, pois o conjunto de palavras reservadas cresce com "del" e "return" e não há interferência de fluxo de dados ou de controle. Ainda assim, pela aplicação literal das condições à tabela, a condição B se verifica sobre o elemento de estado inteiro.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): YES — Condição B: python2Keywords</summary>

1. INTENÇÃO: LEFT adiciona "return" à lista de palavras reservadas (linha de "repr"/"reversed"). RIGHT adiciona "del" antes de "delattr". Os dois resumos batem com os diffs.

2. ESTADO: O array estático `python2Keywords`, cujos elementos são escritos pela inicialização e lidos por `addBadWords()` (via `getBadWords()`). O target `python2Keywords` é o próprio array.

3. TABELA DE ESTADOS:
   - Entrada: a inicialização do array, sem leitura dinâmica de parâmetros.
   - python2Keywords (conjunto inteiro, em ordem):
     - BASE: [..., "delattr", ..., "repr", "reversed", ...] (sem "del" e sem "return")
     - LEFT: [..., "delattr", ..., "repr", "return", "reversed", ...] (com "return", sem "del")
     - RIGHT: [..., "del", "delattr", ..., "repr", "reversed", ...] (com "del", sem "return")
     - MERGE: [..., "del", "delattr", ..., "repr", "return", "reversed", ...] (com "del" e "return")

4. CRITÉRIO DE CONFLITO: X = python2Keywords, tomado como o valor do elemento inteiro, conforme as instruções.
   - (A) não se aplica: o valor de X em LEFT e em RIGHT difere de BASE.
   - (B) o valor de X em LEFT difere de BASE, e o MERGE não é igual a LEFT, pois MERGE também contém "del". O valor de X em RIGHT difere de BASE, e o MERGE não é igual a RIGHT, pois MERGE também contém "return". Logo, a condição B se aplica.
   - (C) não é necessária para a decisão, pois B já se aplica. Observação: não há leitura de X que dependa de controle ou de dados entre as duas alterações. As duas adições são independentes e preservadas, e o MERGE é a união exata das duas modificações.

Ressalva: pela leitura elemento a elemento, cada palavra adicionada está presente no MERGE e nenhuma foi perdida. A condição B foi aplicada ao valor do array inteiro, como as instruções exigem. Por isso o resultado é SIM, embora o comportamento real pareça não ter interferência entre as duas adições.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): YES — Condição B: python2Keywords</summary>

1. INTENÇÃO: LEFT adiciona "return" ao array python2Keywords. RIGHT adiciona "del" ao mesmo array. Os diffs confirmam os resumos, e as duas mudanças estão em linhas diferentes, por isso não há conflito textual.

2. ESTADO: O array estático python2Keywords, escrito pela inicialização e lido por addBadWords(), que o copia para badWords. O elemento de estado relevante é o conteúdo do array inteiro, e badWords, que é derivado dele.

3. TABELA DE ESTADOS:
   - Entrada: a inicialização do array python2Keywords, com N elementos na BASE.
   - python2Keywords:
     - BASE = N elementos (sem "return" e sem "del")
     - LEFT = N+1 elementos (com "return", sem "del")
     - RIGHT = N+1 elementos (com "del", sem "return")
     - MERGE = N+2 elementos (com "return" e "del")
   - badWords (após addBadWords()):
     - BASE = conjunto base
     - LEFT = conjunto base + {"return"}
     - RIGHT = conjunto base + {"del"}
     - MERGE = conjunto base + {"return", "del"}

4. CRITÉRIO DE CONFLITO: X = python2Keywords (valor do array inteiro).
   - (A) não se aplica: o valor de X muda em LEFT e em RIGHT, portanto difere de BASE nos dois pais.
   - (B) o valor de X em LEFT difere de BASE. O valor de X no MERGE (N+2 elementos, com "del") não é igual ao de LEFT (N+1 elementos, sem "del"). Pela regra literal, LEFT não é preservado, então B se aplica. O mesmo vale para RIGHT, pelo lado oposto.
   - (C) não se aplica: o código alterado por cada lado é a própria lista literal. Nenhum dos dois lados lê ou é controlado pela outra adição.
   
   Observação: na prática, ambas as intenções estão preservadas em badWords, que é o conjunto consumido pelo gerador. Mesmo assim, a regra (B) é aplicada literalmente, como no exemplo 1, porque o valor do elemento inteiro no MERGE não coincide com o de nenhum pai alterado.

</details>

#### claude-opus-5-5: YES ✅

<details><summary>Execução 1 (<code>1.csv</code>): YES — Condição B: python2Keywords</summary>

1. **INTENÇÃO:** LEFT insere `"return"` no array `python2Keywords`, entre `"repr"` e `"reversed"`. RIGHT insere `"del"` no mesmo array, antes de `"delattr"`. O MERGE contém as duas inserções. Os diffs confirmam os resumos.

2. **ESTADO:** O campo estático `python2Keywords` (array de Strings) é o elemento de estado principal: conteúdo, tamanho e posições. Ele é lido por `addBadWords()`, que o copia para o campo de instância `badWords`. `badWords` é retornado por `getBadWords()` e consultado em `visibleGrammarSymbolCausesIssueInGeneratedCode()`.

3. **TABELA DE ESTADOS:**
   - Entrada: inicialização da classe e chamada a `getBadWords()`. Seja N o tamanho do array em BASE.
   - `python2Keywords`:
     - BASE: N elementos, sem `"del"` e sem `"return"`.
     - LEFT: N+1 elementos, com `"return"` e sem `"del"`.
     - RIGHT: N+1 elementos, com `"del"` e sem `"return"`.
     - MERGE: N+2 elementos, com `"del"` e com `"return"`.
   - Posição de `"return"`: LEFT = índice k | MERGE = índice k+1 (deslocado pela inserção de `"del"`).
   - `badWords`:
     - BASE = B
     - LEFT = B ∪ {"return"}
     - RIGHT = B ∪ {"del"}
     - MERGE = B ∪ {"del", "return"}

4. **CRITÉRIO DE CONFLITO:** X = `python2Keywords` (e, por consequência, `badWords`).
   - **(A)** Não se aplica: o valor de X em LEFT e em RIGHT difere de BASE.
   - **(B)** Aplica-se:
     - O valor de X em LEFT (N+1 elementos, com `"return"`, sem `"del"`) difere de BASE. O valor no MERGE (N+2 elementos, com `"del"` e `"return"`) é diferente do valor de LEFT, então LEFT não é preservado.
     - O mesmo vale para RIGHT, cujo valor também não é preservado.
     - Considerando o elemento inteiro, o valor final do array no MERGE não é igual ao de nenhum dos pais.
   - **(C)** Não é necessária, pois B já se aplica. Além disso, nenhum código alterado lê o valor escrito pelo outro lado de forma condicional.

</details>

#### claude-sonnet-5-5: NO ❌

<details><summary>Execução 1 (<code>1.csv</code>): NO</summary>

1. INTENÇÃO: LEFT adiciona "return" ao array python2Keywords, na linha de "repr"/"reversed". RIGHT adiciona "del" ao mesmo array, na linha de "delattr". Os diffs confirmam os resumos, e as edições ocorrem em linhas distintas do inicializador.

2. ESTADO: O campo estático python2Keywords (conteúdo do array). Indiretamente, badWords, preenchido por addBadWords() com Arrays.asList(python2Keywords), e o retorno de getBadWords() e de visibleGrammarSymbolCausesIssueInGeneratedCode().

3. TABELA DE ESTADOS:
   - Entrada: consulta de contains("del") e contains("return") em getBadWords().
   - python2Keywords contém "del": BASE = não | LEFT = não | RIGHT = sim | MERGE = sim
   - python2Keywords contém "return": BASE = não | LEFT = sim | RIGHT = não | MERGE = sim
   - badWords.contains("del"): BASE = false | LEFT = false | RIGHT = true | MERGE = true
   - badWords.contains("return"): BASE = false | LEFT = true | RIGHT = false | MERGE = true
   - Os demais elementos do array são iguais em todas as versões.

4. CRITÉRIO DE CONFLITO: X = python2Keywords e badWords.
   - (A) não se aplica: o valor muda em LEFT e em RIGHT.
   - (B) o MERGE preserva as adições de LEFT ("return") e de RIGHT ("del"), pois contém ambas. Cada pai é preservado nos elementos que alterou.
   - (C) addBadWords() e getBadWords() leem o array inteiro, mas se comportam no MERGE como se espera: incluem as duas palavras adicionais, sem interferência entre elas. As adições são independentes e aditivas.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): NO</summary>

1. INTENÇÃO: LEFT adiciona "return" ao array python2Keywords. RIGHT adiciona "del" ao mesmo array. Os diffs confirmam os resumos. As mudanças são em linhas distintas do inicializador.

2. ESTADO: O array estático python2Keywords. Ele é lido por addBadWords(), que o copia para o conjunto badWords, e depois por getBadWords() e visibleGrammarSymbolCausesIssueInGeneratedCode().

3. TABELA DE ESTADOS:
   - Entrada: o conteúdo do array python2Keywords, e o resultado de badWords.contains("del") e badWords.contains("return").
   - BASE: array sem "del" e sem "return"; contains("del") = false; contains("return") = false.
   - LEFT: array com "return"; contains("del") = false; contains("return") = true.
   - RIGHT: array com "del"; contains("del") = true; contains("return") = false.
   - MERGE: array com "del" e "return"; contains("del") = true; contains("return") = true.

4. CRITÉRIO DE CONFLITO: X = python2Keywords (e, por derivação, badWords).
   - (A) não se aplica: o valor de X em LEFT e em RIGHT difere de BASE, e o MERGE difere de BASE por causa dessas mudanças.
   - (B) o MERGE contém a adição de LEFT ("return") e a de RIGHT ("del"), então preserva ambas as contribuições. Não há elemento sobrescrito nem perdido.
   - (C) o código que lê o array (addBadWords e getBadWords) não é alterado por nenhum dos lados. As adições são independentes e aditivas, e cada palavra só afeta o próprio contains().
   
   Não há interferência entre as mudanças.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): NO</summary>

1. INTENÇÃO: LEFT adiciona "return" ao array python2Keywords, na linha de "repr"/"reversed". RIGHT adiciona "del" ao mesmo array, na linha de "delattr". Os diffs confirmam os resumos, e as alterações estão em linhas diferentes e independentes.

2. ESTADO: O campo estático python2Keywords (conteúdo do array). Indiretamente, o conjunto badWords, preenchido por addBadWords() com Arrays.asList(python2Keywords) e lido por getBadWords() e visibleGrammarSymbolCausesIssueInGeneratedCode().

3. TABELA DE ESTADOS:
   - python2Keywords:
     - BASE: contém "delattr" e não contém "del" nem "return".
     - LEFT: BASE mais "return".
     - RIGHT: BASE mais "del".
     - MERGE: BASE mais "del" e "return".
   - badWords, após a primeira chamada de getBadWords(): usa o conteúdo do array em cada versão, então fica com os mesmos acréscimos.
   - Entrada: idNode.getText() = "del". BASE = false, LEFT = false, RIGHT = true, MERGE = true.
   - Entrada: idNode.getText() = "return". BASE = false, LEFT = true, RIGHT = false, MERGE = true.

4. CRITÉRIO DE CONFLITO: X = python2Keywords (e badWords, derivado dele).
   - (A) não se aplica: o valor de X em LEFT e em RIGHT difere de BASE.
   - (B) o valor de X em LEFT (com "return") e em RIGHT (com "del") difere de BASE. O MERGE contém ambas as adições, então preserva as duas contribuições (união aditiva).
   - (C) o código que lê o array (addBadWords e as consultas a badWords) apenas itera ou consulta o conjunto, sem depender de qual elemento foi adicionado. No MERGE ele se comporta como em cada pai, sendo apenas mais abrangente. Nenhuma interferência indesejada.

</details>

### 2. `cloud-slang__20bac30d__SlangImpl#getAllEventTypes`

- **Target:** `getAllEventTypes()`
- **Esperado:** YES; **acertam:** claude-haiku-5-5; **erram:** claude-opus-5-5, claude-sonnet-5-5
- **Código:** [cloud-slang__20bac30d__SlangImpl](../../data/mergedataset/cloud-slang__20bac30d__SlangImpl)

**LEFT:** Left adds new values into a list

**RIGHT:** Right adds new values into a list

**Justificativa do dataset:** Left and right add new values of a same list, which means they change the field size.

#### claude-haiku-5-5: YES ✅

<details><summary>Execução 1 (<code>1.csv</code>): YES — Condição B: eventTypes (conjunto retornado por getAllEventTypes())</summary>

1. INTENÇÃO: LEFT adiciona `EVENT_TASK_START` ao conjunto retornado por `getAllEventTypes()`. RIGHT remove os quatro `EVENT_ASYNC_LOOP_*` e adiciona `EVENT_SPLIT_BRANCHES`, `EVENT_JOIN_BRANCHES_START` e `EVENT_JOIN_BRANCHES_END`. Os resumos conferem com os diffs.

2. ESTADO: O `HashSet<String> eventTypes` local, construído e retornado por `getAllEventTypes()`. Ele é o único elemento de estado escrito pelo target. O método `subscribeOnAllEvents()` lê esse retorno, por isso o conjunto é lido pelo código chamador.

3. TABELA DE ESTADOS: O método não recebe entradas. Seja S o conjunto de BASE, que contém os quatro ASYNC_LOOP e não contém TASK_START, SPLIT_BRANCHES, JOIN_BRANCHES_START nem JOIN_BRANCHES_END.
   - eventTypes:
     - BASE = S
     - LEFT = S ∪ {TASK_START}
     - RIGHT = (S \ {ASYNC_LOOP_EXPRESSION_START, ASYNC_LOOP_EXPRESSION_END, ASYNC_LOOP_OUTPUT_START, ASYNC_LOOP_OUTPUT_END}) ∪ {SPLIT_BRANCHES, JOIN_BRANCHES_START, JOIN_BRANCHES_END}
     - MERGE = (S ∪ {TASK_START}) \ {os quatro ASYNC_LOOP} ∪ {SPLIT_BRANCHES, JOIN_BRANCHES_START, JOIN_BRANCHES_END}
   - Assim, MERGE contém as alterações de LEFT e de RIGHT juntas. Não é igual a LEFT nem a RIGHT.

4. CRITÉRIO DE CONFLITO: X = o conjunto eventTypes retornado, tratado como elemento inteiro, conforme a definição das instruções.
   - (A) não se aplica: o valor de X em LEFT e em RIGHT difere de BASE, e a condição exige igualdade em BASE, LEFT e RIGHT.
   - (B) se aplica: o valor de X em LEFT difere de BASE (acréscimo de TASK_START). O MERGE não preserva LEFT, porque contém também as remoções e adições de RIGHT, de modo que MERGE ≠ LEFT. O mesmo ocorre com RIGHT, cujo valor também não é preservado no MERGE.
   - (C) não precisa ser avaliada, porque B já se aplica. Não há controle nem leitura cruzada entre os trechos, mas isso não afasta a condição B, que é literal e não depende de interferência.
   - Observação: se X fosse tratado item a item (cada tipo de evento como elemento separado), não haveria conflito, pois cada inclusão e remoção seria preservada. As instruções, porém, exigem o valor do elemento inteiro. Por isso a análise adota X como o conjunto completo. Isso é coerente com o exemplo 1, em que a mudança de RIGHT também fez o MERGE diferir de LEFT e o caso foi classificado como B.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): YES — Condição B: eventTypes</summary>

1. INTENÇÃO: O resumo diz que LEFT e RIGHT "adicionam valores a uma lista", mas o diff mostra outra coisa. Confirmo no diff:
   - LEFT adiciona `EVENT_TASK_START` ao conjunto.
   - RIGHT remove os quatro `EVENT_ASYNC_LOOP_*` e adiciona `EVENT_SPLIT_BRANCHES`, `EVENT_JOIN_BRANCHES_START` e `EVENT_JOIN_BRANCHES_END`.
   - O alvo é um `HashSet<String>`, não uma lista. Trusto o diff, que mostra remoções além de adições.

2. ESTADO: O valor retornado por `getAllEventTypes()`, ou seja, o conjunto `eventTypes` inteiro. Ele é escrito pelos `add` do método e lido por `subscribeOnAllEvents()`, que o passa a `subscribeOnEvents()`. Esse é o único elemento de estado afetado pelas mudanças.

3. TABELA DE ESTADOS:
   Como o método não recebe entrada, a "entrada" é a própria BASE. Sejam A = {os quatro ASYNC_LOOP}, T = {EVENT_TASK_START}, S = {SPLIT_BRANCHES, JOIN_BRANCHES_START, JOIN_BRANCHES_END} e R = o restante de BASE, sem A.
   - eventTypes: BASE = R ∪ A | LEFT = R ∪ A ∪ T | RIGHT = R ∪ S | MERGE = R ∪ S ∪ T

   Não há colisão entre as constantes, então as operações são independentes. O MERGE contém T (de LEFT), não contém A (removido por RIGHT) e contém S (de RIGHT).

4. CRITÉRIO DE CONFLITO: X = eventTypes, tomado como o conjunto inteiro.
   - (A) Não se aplica: LEFT e RIGHT diferem de BASE.
   - (B) LEFT difere de BASE (acrescentou T). MERGE = R ∪ S ∪ T é diferente de LEFT = R ∪ A ∪ T, porque o MERGE perdeu A e ganhou S. Logo o MERGE não preserva o valor de LEFT. A condição se aplica. Isso acontece mesmo que a remoção de A tenha sido intencional do RIGHT, pois a regra não permite descartar a condição com base na intenção. LEFT nunca pretendeu remover A, e o MERGE os perdeu.
   - (C) Não é necessário avaliar, porque B já se aplica.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): YES — Condição B: eventTypes</summary>

1. INTENÇÃO: LEFT adiciona EVENT_TASK_START ao conjunto de eventos. RIGHT troca os quatro eventos EVENT_ASYNC_LOOP_* por EVENT_SPLIT_BRANCHES, EVENT_JOIN_BRANCHES_START e EVENT_JOIN_BRANCHES_END. Os diffs confirmam os resumos, que não são contraditórios: o resumo genérico "adds new values into a list" descreve apenas parte da mudança de RIGHT, que também remove elementos.

2. ESTADO: A variável local eventTypes (HashSet), construída e retornada por getAllEventTypes(). Ela é o único elemento de estado escrito pelo método TARGET e pelos trechos alterados. Ela é lida pelo chamador em subscribeOnAllEvents(), que a passa para eventBus.subscribe(). Nenhum código alterado lê eventTypes além do próprio método.

3. TABELA DE ESTADOS (conjunto de eventos retornado; S0 = os demais eventos comuns, que não mudam):
   - BASE: S0 ∪ {ASYNC_LOOP_EXPRESSION_START, ASYNC_LOOP_EXPRESSION_END, ASYNC_LOOP_OUTPUT_START, ASYNC_LOOP_OUTPUT_END}
   - LEFT: S0 ∪ {ASYNC_LOOP_* (4)} ∪ {TASK_START}
   - RIGHT: S0 ∪ {SPLIT_BRANCHES, JOIN_BRANCHES_START, JOIN_BRANCHES_END}
   - MERGE: S0 ∪ {TASK_START} ∪ {SPLIT_BRANCHES, JOIN_BRANCHES_START, JOIN_BRANCHES_END}

4. CRITÉRIO DE CONFLITO: X = eventTypes (o conjunto inteiro, não apenas as partes alteradas por cada lado).
   - (A) não se aplica: BASE, LEFT e RIGHT não têm o mesmo valor de X.
   - (B) se aplica: LEFT difere de BASE (adiciona TASK_START), e o MERGE não preserva o valor de LEFT, pois o MERGE não contém os ASYNC_LOOP_* de LEFT e contém SPLIT/JOIN, que LEFT não tem. Da mesma forma, o MERGE não é igual a RIGHT, pois falta TASK_START. Embora as duas intenções apareçam no MERGE, o valor final do conjunto não é igual ao de nenhum dos pais que o alterou.
   - (C) não se aplica: nenhum código alterado lê eventTypes para decidir seu próprio comportamento.

</details>

#### claude-opus-5-5: NO ❌

<details><summary>Execução 1 (<code>1.csv</code>): NO</summary>

1. INTENÇÃO:
   - LEFT acrescenta `EventConstants`… mais precisamente `ScoreLangConstants.EVENT_TASK_START` ao conjunto retornado por `getAllEventTypes()`.
   - RIGHT remove os quatro eventos `EVENT_ASYNC_LOOP_*` e adiciona `EVENT_SPLIT_BRANCHES`, `EVENT_JOIN_BRANCHES_START` e `EVENT_JOIN_BRANCHES_END`.
   - O MERGE aplica as duas mudanças. Os diffs confirmam os resumos.

2. ESTADO: O conjunto local `eventTypes`, que é a expressão de retorno de `getAllEventTypes()`. Esse retorno é lido por `subscribeOnAllEvents()` e repassado a `eventBus.subscribe`. Os elementos de estado relevantes são os elementos dessa coleção, ou seja, a presença de cada constante no conjunto.

3. TABELA DE ESTADOS (chamada `getAllEventTypes()`, sem parâmetros):
   - EVENT_TASK_START ∈ eventTypes: BASE = não | LEFT = sim | RIGHT = não | MERGE = sim
   - EVENT_ASYNC_LOOP_EXPRESSION_START/END e EVENT_ASYNC_LOOP_OUTPUT_START/END ∈ eventTypes: BASE = sim | LEFT = sim | RIGHT = não | MERGE = não
   - EVENT_SPLIT_BRANCHES, EVENT_JOIN_BRANCHES_START e EVENT_JOIN_BRANCHES_END ∈ eventTypes: BASE = não | LEFT = não | RIGHT = sim | MERGE = sim
   - Demais constantes (SCORE_*, ACTION_*, INPUT_*, OUTPUT_*, BRANCH_*, EXECUTION_FINISHED): sim nas quatro versões.
   - Conjunto inteiro:
     - BASE = B
     - LEFT = B ∪ {TASK_START}
     - RIGHT = (B − ASYNC_LOOP×4) ∪ {SPLIT, JOIN_START, JOIN_END}
     - MERGE = (B − ASYNC_LOOP×4) ∪ {TASK_START, SPLIT, JOIN_START, JOIN_END}

4. CRITÉRIO DE CONFLITO: X = cada elemento do conjunto `eventTypes`.
   - (A) Não se aplica. As constantes que são iguais em BASE, LEFT e RIGHT continuam presentes no MERGE.
   - (B) Não se aplica. A presença de TASK_START mudou só em LEFT, e o MERGE a preserva. A remoção dos ASYNC_LOOP e a inclusão de SPLIT/JOIN mudaram só em RIGHT, e o MERGE as preserva. As mudanças atingem elementos disjuntos da coleção, e a operação é inserção em um Set, que não depende de ordem. Portanto não há elemento cujo valor no MERGE divirja do pai que o alterou.
   - (C) Não se aplica. A linha adicionada por LEFT não lê nem é controlada pelas constantes alteradas por RIGHT, e vice-versa. O consumidor (`subscribe`) recebe a união das intenções, sem interferência entre elas.

</details>

#### claude-sonnet-5-5: NO ❌

<details><summary>Execução 1 (<code>1.csv</code>): NO</summary>

1. INTENÇÃO: LEFT adiciona EVENT_TASK_START ao conjunto. RIGHT substitui os quatro eventos ASYNC_LOOP (EXPRESSION_START/END, OUTPUT_START/END) por três eventos novos (SPLIT_BRANCHES, JOIN_BRANCHES_START, JOIN_BRANCHES_END). Os diffs confirmam os resumos. O resumo de RIGHT só menciona adições, mas o diff também remove linhas.

2. ESTADO: A variável local eventTypes (um Set&lt;String&gt;), que é o valor retornado por getAllEventTypes().

3. TABELA DE ESTADOS:
   - Entrada: chamada de getAllEventTypes(). Os elementos do conjunto são listados abaixo, omitindo os comuns (SCORE_*, SLANG_EXECUTION_EXCEPTION, ACTION_*, INPUT_*, OUTPUT_*, BRANCH_START/END e EXECUTION_FINISHED).
   - BASE: comuns + {ASYNC_LOOP_EXPRESSION_START, ASYNC_LOOP_EXPRESSION_END, ASYNC_LOOP_OUTPUT_START, ASYNC_LOOP_OUTPUT_END}
   - LEFT: comuns + TASK_START + os 4 ASYNC_LOOP
   - RIGHT: comuns + SPLIT_BRANCHES, JOIN_BRANCHES_START, JOIN_BRANCHES_END (sem os ASYNC_LOOP)
   - MERGE: comuns + TASK_START + SPLIT_BRANCHES, JOIN_BRANCHES_START, JOIN_BRANCHES_END (sem os ASYNC_LOOP)

4. CRITÉRIO DE CONFLITO: X = eventTypes (conjunto retornado).
   - (A) não se aplica: LEFT e RIGHT diferem de BASE.
   - (B) o valor de X em LEFT difere de BASE, e o MERGE (sem os ASYNC_LOOP) não é igual a LEFT. O mesmo vale para RIGHT, pois o MERGE contém TASK_START, que RIGHT não tem. Como o valor é o conjunto inteiro, nenhum dos pais é preservado literalmente.
   - Pela leitura do conjunto como um todo, B se aplica. Examinando as intenções, porém, as mudanças são aditivas e independentes: o MERGE tem a união das adições e a remoção de RIGHT. Isso é o resultado composto esperado, sem interferência. Uma versão composta equivalente seria BASE + adição de LEFT + modificação de RIGHT.
   - (C) não se aplica: nenhum código alterado lê eventTypes nem é controlado por ele. Só há chamadas add independentes.
   - Aplicar B literalmente a qualquer merge em que os dois lados alteram o mesmo conjunto classificaria quase todo merge limpo como conflito. Nesse caso, ambos os lados editam o mesmo elemento de estado e o MERGE não é igual a nenhum dos pais, mas cada alteração está preservada no MERGE (TASK_START de LEFT; a troca dos eventos de RIGHT). Não há interferência entre os adds.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): NO</summary>

1. INTENÇÃO: LEFT adiciona EVENT_TASK_START ao conjunto. RIGHT substitui os quatro eventos ASYNC_LOOP por SPLIT_BRANCHES, JOIN_BRANCHES_START e JOIN_BRANCHES_END. O diff confirma os dois resumos. O resumo de RIGHT é impreciso, pois RIGHT também remove elementos.

2. ESTADO: O conjunto local eventTypes, escrito por eventTypes.add(...) e retornado por getAllEventTypes(). O valor do return é o conteúdo desse conjunto.

3. TABELA DE ESTADOS (a entrada não tem parâmetros, pois o método é determinístico):
   - BASE: 7 eventos SCORE, SLANG_EXECUTION_EXCEPTION, ACTION_START, ACTION_END, ACTION_ERROR, INPUT_START, INPUT_END, OUTPUT_START, OUTPUT_END, BRANCH_START, BRANCH_END, ASYNC_LOOP_EXPRESSION_START, ASYNC_LOOP_EXPRESSION_END, ASYNC_LOOP_OUTPUT_START, ASYNC_LOOP_OUTPUT_END, EXECUTION_FINISHED.
   - LEFT: BASE + TASK_START.
   - RIGHT: BASE − {4 ASYNC_LOOP} + {SPLIT_BRANCHES, JOIN_BRANCHES_START, JOIN_BRANCHES_END}.
   - MERGE: BASE + TASK_START − {4 ASYNC_LOOP} + {SPLIT_BRANCHES, JOIN_BRANCHES_START, JOIN_BRANCHES_END}.

   O conjunto de MERGE é a união exata das mudanças de LEFT e RIGHT, e as duas são independentes.

4. CRITÉRIO DE CONFLITO: X = eventTypes (o conjunto retornado).
   - (A) não se aplica: X difere de BASE em LEFT e em RIGHT.
   - (B) O MERGE não é igual ao conjunto de LEFT nem ao de RIGHT, porque contém as adições de ambos. Isso, porém, é a composição esperada de adições independentes: o MERGE mantém todas as adições de LEFT (TASK_START) e todas as adições e remoções de RIGHT. Por elemento, o MERGE preserva as contribuições de cada pai.
   - (C) Cada `add` só escreve no conjunto e não lê X. Nenhum código alterado depende de um valor escrito pelo outro lado, e a ordem não importa em um HashSet. Não há interferência.

Não há conflito semântico.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): NO</summary>

1. INTENÇÃO: Confirmando nos diffs, LEFT adiciona EVENT_TASK_START ao conjunto. RIGHT substitui os quatro eventos ASYNC_LOOP por EVENT_SPLIT_BRANCHES, EVENT_JOIN_BRANCHES_START e EVENT_JOIN_BRANCHES_END. O resumo de RIGHT ("adds new values") é incompleto, porque RIGHT também remove valores.

2. ESTADO: O conjunto local eventTypes, que é o valor retornado por getAllEventTypes(). Ele é escrito pelas chamadas add().

3. TABELA DE ESTADOS (a entrada é irrelevante, pois o método não tem parâmetros):
   - Notação: ACTION* = ACTION_START, ACTION_END e ACTION_ERROR; INPUT/OUTPUT/BRANCH = os eventos _START e _END de cada um.
   - BASE: SCORE_* (7), SLANG_EXECUTION_EXCEPTION, ACTION*, INPUT, OUTPUT, BRANCH, ASYNC_LOOP (4 eventos), EXECUTION_FINISHED.
   - LEFT: BASE + TASK_START.
   - RIGHT: BASE − ASYNC_LOOP (4 eventos) + SPLIT_BRANCHES + JOIN_BRANCHES_START + JOIN_BRANCHES_END.
   - MERGE: BASE + TASK_START − ASYNC_LOOP (4 eventos) + SPLIT_BRANCHES + JOIN_BRANCHES_START + JOIN_BRANCHES_END.

4. CRITÉRIO DE CONFLITO: X = eventTypes (o conjunto retornado).
   - (A) não se aplica: LEFT e RIGHT diferem de BASE.
   - (B) o valor de X em LEFT (BASE + TASK_START) difere de BASE. O MERGE não é igual a LEFT, porque tem a mais os eventos de RIGHT e a menos os ASYNC_LOOP. Em sentido estrito, isso significa que o MERGE "não preserva" nenhum dos pais. Mas essa leitura literal trataria como conflito qualquer combinação de adições independentes a um conjunto. A combinação aqui é a união das mudanças de ambos: o MERGE contém a adição de LEFT e todas as adições e remoções de RIGHT. O resultado reflete as duas intenções.
   - (C) o código alterado por um lado não lê nem é controlado pelo conjunto escrito pelo outro. As chamadas add() são independentes, e TASK_START não interage com os eventos de RIGHT. Os add() de conjunto são comutativos e os elementos são distintos.

   Pelo critério literal de B, o valor do conjunto no MERGE não é igual ao de LEFT nem ao de RIGHT, mas é a composição esperada das duas mudanças, sem interferência de dados ou de controle. Concluo que não há conflito semântico.

</details>

### 3. `fitnesse__4d9ba9d2__SlimTableFactoryTest#setUp`

- **Target:** `setUp()`
- **Esperado:** YES; **acertam:** claude-haiku-5-5; **erram:** claude-opus-5-5, claude-sonnet-5-5
- **Código:** [fitnesse__4d9ba9d2__SlimTableFactoryTest](../../data/mergedataset/fitnesse__4d9ba9d2__SlimTableFactoryTest)

**LEFT:** Left adds two entries on the field map.

**RIGHT:** Right adds one entry on the field map.

**Justificativa do dataset:** The interference occurs because both parents change the field size of map. A test case assert should explore the map size.

#### claude-haiku-5-5: YES ✅

<details><summary>Execução 1 (<code>1.csv</code>): YES — Condição B: map</summary>

1. INTENÇÃO: LEFT adiciona as chaves "ddt:" e "dynamic decision:" ao mapa em setUp(). RIGHT adiciona a chave "script:" ao mapa em setUp() e, em outro método (checkTableTypeDefineUsedForTable), uma nova asserção. Os diffs confirmam os resumos. A asserção de RIGHT não está em TARGET, então não entra na análise de setUp().

2. ESTADO: O campo `map` (Map&lt;String, Class&lt;? extends SlimTable&gt;&gt;), escrito por setUp() via `put`. Não há outros elementos de estado escritos por setUp() nos trechos alterados (`slimTableFactory` e `table` são recriados sem alteração de código).

3. TABELA DE ESTADOS:
   - Entrada: execução de setUp() sobre um HashMap novo.
   - map (BASE): 12 entradas (dt:, dT:, decision:, ordered query:, subset query:, query:, table:, script, scenario, import, something, library)
   - map (LEFT): 14 entradas = BASE + "ddt:" + "dynamic decision:"
   - map (RIGHT): 13 entradas = BASE + "script:"
   - map (MERGE): 15 entradas = BASE + "ddt:" + "dynamic decision:" + "script:"

4. CRITÉRIO DE CONFLITO: X = map (valor do elemento inteiro).
   - (A) não se aplica: o valor de X em LEFT e em RIGHT difere de BASE.
   - (B) o valor de X em LEFT difere de BASE (14 vs 12 entradas) e o valor de X no MERGE (15 entradas) não é igual ao de LEFT, portanto LEFT não é preservado no MERGE. O mesmo ocorre com RIGHT (13 entradas, diferente de 15). A condição B se aplica literalmente. A intenção de que as adições são independentes e não se sobrepõem não basta para descartá-la, conforme as instruções.
   - (C) verificada e não aplicada: o código alterado por LEFT (as próprias chamadas `put` em setUp()) não lê `map`. A asserção nova de RIGHT também não lê `map`, pois usa apenas a factory com uma tabela mockada. O teste inalterado shouldCreateCorrectSlimTableForTablesType lê `map`, mas não foi alterado por nenhum dos pais, então C não se aplica.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): YES — Condição B: map</summary>

1. INTENÇÃO: LEFT adiciona as chaves "ddt:" e "dynamic decision:" ao map em setUp(). RIGHT adiciona a chave "script:" ao map em setUp() e também um novo assert em checkTableTypeDefineUsedForTable(), que não faz parte do TARGET. Os diffs confirmam os resumos.

2. ESTADO: A variável de instância `map` (Map&lt;String, Class&lt;? extends SlimTable&gt;&gt;), escrita por setUp() com os put() e lida pelos testes. As demais variáveis escritas em setUp() (`slimTableFactory`, `table`) não são alteradas pelos trechos modificados.

3. TABELA DE ESTADOS:
   - Entrada: execução de setUp() seguida do conjunto de chaves de `map`.
   - map, conteúdo final (número de entradas):
     - BASE: 12 entradas (dt:, dT:, decision:, ordered query:, subset query:, query:, table:, script, scenario, import, something, library)
     - LEFT: 14 entradas (BASE + ddt:, dynamic decision:)
     - RIGHT: 13 entradas (BASE + script:)
     - MERGE: 15 entradas (BASE + ddt:, dynamic decision:, script:)

4. CRITÉRIO DE CONFLITO: X = map, tratado como o elemento inteiro, conforme a definição.
   - (A) não se aplica: o valor de `map` em LEFT e em RIGHT difere de BASE.
   - (B) o valor de `map` em LEFT (14 entradas) difere de BASE, e o MERGE (15 entradas) não é igual a LEFT, portanto LEFT não é preservado. O mesmo ocorre com RIGHT (13 entradas), que também não é preservado no MERGE. A condição se aplica.
   - (C) não é necessária, pois B já se aplica. Além disso, o assert novo de RIGHT não lê diretamente `map` nem é controlado por ele.

   Observação: as chaves adicionadas por cada lado são distintas e não há interferência semântica evidente. Ainda assim, pela regra de que X é o valor do elemento inteiro, o MERGE não coincide com nenhum dos pais alterados, e a condição B é aplicada como definida.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): YES — Condição B: map</summary>

1. INTENÇÃO: LEFT adiciona duas entradas ao mapa de tipos de tabela em setUp(): "ddt:" e "dynamic decision:". RIGHT adiciona a entrada "script:" em setUp() e um novo assert em checkTableTypeDefineUsedForTable(), que não está no target. Os resumos batem com os diffs.

2. ESTADO: O campo `map` (Map&lt;String, Class&lt;? extends SlimTable&gt;&gt;), escrito por setUp() através de map.put(). Ele é lido por shouldCreateCorrectSlimTableForTablesType(), que itera sobre todas as entradas. O assert adicionado por RIGHT usa `slimTableFactory` e `table`, não `map`.

3. TABELA DE ESTADOS:
   - Entrada: setUp() executado uma vez, com o mapa inicial vazio.
   - map (número de entradas e chaves extras em relação a BASE):
     - BASE = 12 entradas (dt:, dT:, decision:, ordered query:, subset query:, query:, table:, script, scenario, import, something, library)
     - LEFT = 14 entradas (BASE + "ddt:" + "dynamic decision:")
     - RIGHT = 13 entradas (BASE + "script:")
     - MERGE = 15 entradas (BASE + "ddt:" + "dynamic decision:" + "script:")
   - Os assert e os demais trechos não escrevem em `map`, e o assert adicionado por RIGHT não lê `map`.

4. CRITÉRIO DE CONFLITO: X = map, valor do campo inteiro.
   - (A) não se aplica: o valor de map muda em LEFT e em RIGHT, portanto BASE, LEFT e RIGHT não são iguais.
   - (B) se aplica: o valor de map em LEFT (14 entradas) difere de BASE (12), e o MERGE (15) não é igual a LEFT, pois contém "script:". Pelo mesmo critério, o valor de map em RIGHT (13) difere de BASE, e o MERGE também não é igual a RIGHT, pois contém "ddt:" e "dynamic decision:". Nenhum pai é preservado como valor do elemento inteiro. A intenção de união das duas adições não descarta essa condição, pois a definição exige que o MERGE preserve o valor de um pai.
   - (C) não se aplica: o código alterado por RIGHT (o assert novo) não lê `map`, e o código alterado por LEFT (os map.put) não é controlado por `map`. O teste que lê `map` não foi alterado por nenhum dos lados.

</details>

#### claude-opus-5-5: NO ❌

<details><summary>Execução 1 (<code>1.csv</code>): NO</summary>

1. INTENÇÃO: O diff confirma os resumos.
   - LEFT adiciona duas entradas ao map em setUp(): "ddt:" e "dynamic decision:", ambas mapeadas para DynamicDecisionTable.class.
   - RIGHT adiciona uma entrada ao map em setUp(): "script:" mapeada para ScriptTable.class. Fora do TARGET, RIGHT também acrescenta uma asserção em checkTableTypeDefineUsedForTable().
   - O MERGE contém todas essas adições.

2. ESTADO:
   - O campo map, escrito por setUp() com as entradas novas de LEFT e de RIGHT.
   - Os campos slimTableFactory e table, que não foram alterados por nenhum dos lados.
   - O map é lido por shouldCreateCorrectSlimTableForTablesType(), que não foi alterado.

3. TABELA DE ESTADOS:
   - Entrada: execução de setUp() (sem parâmetros).
   - BASE: map = {12 entradas originais}.
   - LEFT: map = {12 originais, "ddt:"→DynamicDecisionTable, "dynamic decision:"→DynamicDecisionTable}, total de 14 entradas.
   - RIGHT: map = {12 originais, "script:"→ScriptTable}, total de 13 entradas.
   - MERGE: map = {12 originais, "ddt:"→DynamicDecisionTable, "dynamic decision:"→DynamicDecisionTable, "script:"→ScriptTable}, total de 15 entradas.

4. CRITÉRIO DE CONFLITO: X = map. Como as chaves são todas distintas, nenhuma adição sobrescreve outra. Por isso as entradas de cada lado coexistem no MERGE com o mesmo valor que têm no pai que as escreveu.
   - (A) não se aplica: o valor de X em LEFT e em RIGHT difere de BASE.
   - (B) o valor de X no MERGE (15 entradas) não é igual, como mapa inteiro, ao de LEFT (14) nem ao de RIGHT (13). Isso apenas reflete a união de adições independentes de chaves distintas. Cada entrada que um pai escreveu está no MERGE com o valor que esse pai lhe deu, e nenhuma entrada foi removida ou alterada. Nesse sentido o MERGE preserva as alterações de ambos os pais, de forma análoga ao exemplo 4, em que campos independentes recebem cada um a sua alteração.
   - (C) não se aplica:
     - Nenhum código alterado por um lado lê as entradas escritas pelo outro.
     - O teste que itera sobre o map não foi modificado. Ele apenas verifica cada par chave→classe, e cada par é verificado de forma independente dos demais.
     - A asserção adicionada por RIGHT em checkTableTypeDefineUsedForTable() não lê o map.

</details>

#### claude-sonnet-5-5: NO ❌

<details><summary>Execução 1 (<code>1.csv</code>): NO</summary>

1. INTENÇÃO: LEFT adiciona duas entradas ao map em setUp() ("ddt:" e "dynamic decision:", ambas para DynamicDecisionTable). RIGHT adiciona a entrada "script:" -&gt; ScriptTable e, em outro método de teste, um novo assert de importação de tabela de script. O resumo menciona só o map, mas o diff mostra também a mudança em checkTableTypeDefineUsedForTable().

2. ESTADO: O campo map, escrito por setUp(). Os trechos alterados também escrevem o estado interno de slimTableFactory (via addTableTypeImport) e as asserções do teste, mas essas últimas vêm só de RIGHT.

3. TABELA DE ESTADOS:
   - Entrada: execução de setUp() seguida de shouldCreateCorrectSlimTableForTablesType(), que itera sobre o map.
   - map (chaves adicionadas ao conjunto base de 12 entradas):
     - BASE: 12 entradas, sem "ddt:", "dynamic decision:" e "script:"
     - LEFT: 14 entradas, com "ddt:" e "dynamic decision:"
     - RIGHT: 13 entradas, com "script:"
     - MERGE: 15 entradas, com as três chaves
   - As chaves são distintas, então nenhuma entrada sobrescreve outra. O MERGE é a união exata das adições de LEFT e RIGHT.
   - O teste de iteração chama makeSlimTable para cada chave:
     - "ddt:" e "dynamic decision:" produzem o mesmo resultado que em LEFT.
     - "script:" produz o mesmo resultado que em RIGHT.
     - Cada entrada é independente das outras.
   - O novo assert de RIGHT em checkTableTypeDefineUsedForTable() não lê o map. Ele usa o slimTableFactory e o mock da table, que LEFT não altera.

4. CRITÉRIO DE CONFLITO: X = map.
   - (A) não se aplica: o valor de X difere de BASE em LEFT e em RIGHT.
   - (B) o MERGE contém todas as adições de LEFT e de RIGHT, então preserva ambos os pais.
   - (C) o código que itera sobre o map lê X, mas trata cada entrada de forma independente, então se comporta no MERGE como nos pais. O código adicionado por RIGHT não depende do map, e as entradas de LEFT não interferem nele. As entradas "ddt:" e "dynamic decision:" também não colidem com "script:".

</details>

<details><summary>Execução 2 (<code>2.csv</code>): NO</summary>

1. INTENÇÃO: LEFT adiciona duas entradas ao map em setUp(): "ddt:" e "dynamic decision:", ambas para DynamicDecisionTable. RIGHT adiciona a entrada "script:" para ScriptTable e um novo assert em checkTableTypeDefineUsedForTable(). O diff confirma os resumos, e o resumo de RIGHT omite o novo assert.

2. ESTADO: O campo map, escrito em setUp(). Ele é lido por shouldCreateCorrectSlimTableForTablesType(), que itera sobre todas as entradas. O estado também inclui o resultado do teste, ou seja, as asserções.

3. TABELA DE ESTADOS:
   - Entrada: execução de setUp() e depois de shouldCreateCorrectSlimTableForTablesType().
   - map (chaves adicionadas):
     - BASE: 12 entradas, sem "ddt:", "dynamic decision:" ou "script:".
     - LEFT: 14 entradas, com "ddt:" e "dynamic decision:".
     - RIGHT: 13 entradas, com "script:".
     - MERGE: 15 entradas, com "ddt:", "dynamic decision:" e "script:".
   - O novo assert de RIGHT usa o import "My script table" com tipo "Script" e depois cria a tabela "My script Table". Esse fluxo não lê o map e é independente das entradas de LEFT.
   - Para as chaves de LEFT, makeSlimTable("ddt:") deve criar DynamicDecisionTable. Isso depende de a factory registrar o prefixo "ddt:", o que é o mesmo em LEFT e em MERGE.
   - Para "script:", o comportamento de RIGHT depende de a factory reconhecer "script:". Como RIGHT já pressupõe isso, o MERGE se comporta como RIGHT.
   - Resultado dos testes: em LEFT, as entradas de LEFT são verificadas pelo loop. Em RIGHT, as de RIGHT são verificadas. No MERGE, todas as entradas são verificadas, sem interferência entre as chaves.

4. CRITÉRIO DE CONFLITO: X = map.
   - (A) não se aplica: o valor de X difere de BASE em LEFT e em RIGHT.
   - (B) o MERGE contém todas as entradas de LEFT e todas as de RIGHT, então preserva ambos os pais. O mesmo vale para o assert adicionado.
   - (C) o código alterado por um lado lê o map apenas via iteração, e as chaves são independentes. O novo assert de RIGHT não lê o map. As chaves "ddt:", "dynamic decision:" e "script:" são distintas e não se sobrescrevem, então o código de cada lado se comporta no MERGE como no pai que o escreveu.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): NO</summary>

1. INTENÇÃO: LEFT adiciona duas entradas ao map em setUp() ("ddt:" e "dynamic decision:", ambas mapeadas para DynamicDecisionTable). RIGHT adiciona a entrada "script:" → ScriptTable em setUp() e um novo assert em checkTableTypeDefineUsedForTable(). O resumo menciona apenas as entradas do map, mas o diff mostra também o assert adicional.

2. ESTADO: O elemento de estado escrito por setUp() é o campo map, uma coleção. Também são escritos slimTableFactory e table. O conteúdo de map é lido por shouldCreateCorrectSlimTableForTablesType(), que itera sobre as entradas. O novo assert de RIGHT escreve o estado dos mocks e da factory via addTableTypeImport.

3. TABELA DE ESTADOS:
   - Entrada: execução de setUp() seguida de shouldCreateCorrectSlimTableForTablesType().
   - map (chaves adicionadas):
     - BASE: 12 entradas, sem "ddt:", sem "dynamic decision:" e sem "script:".
     - LEFT: 14 entradas, com "ddt:" e "dynamic decision:".
     - RIGHT: 13 entradas, com "script:".
     - MERGE: 15 entradas, com "ddt:", "dynamic decision:" e "script:".
   - Chaves distintas, sem sobreposição. O resultado do MERGE é a união das duas adições.
   - Novo assert de RIGHT: ele usa a factory e o mock table, e o tableName "My script Table" resolve para ScriptTable via o import "Define Table Type". Isso não depende de map nem das entradas de LEFT.
   - Comportamento da factory com "ddt:" e "script:": cada chave tem seu prefixo próprio, sem interferência. "script:" não colide com "ddt:" nem com "dynamic decision:". No teste iterativo, cada entrada é verificada de forma independente.

4. CRITÉRIO DE CONFLITO: X = map.
   - (A) não se aplica: o valor de map difere de BASE em LEFT e em RIGHT.
   - (B) o MERGE contém as adições de LEFT e de RIGHT, então preserva ambos.
   - (C) o código alterado por RIGHT (o assert extra) não lê as chaves adicionadas por LEFT. Também não há código de LEFT controlado por algo que RIGHT tenha alterado. O loop de shouldCreateCorrectSlimTableForTablesType lê map, mas apenas itera sobre entradas independentes, e cada uma se comporta como se comportaria no pai que a escreveu.

</details>

### 4. `jsoup__3f7d2c71__HttpConnection#execute`

- **Target:** `execute(Connection.Request, Response)`
- **Esperado:** YES; **acertam:** claude-haiku-5-5; **erram:** claude-opus-5-5, claude-sonnet-5-5
- **Código:** [jsoup__3f7d2c71__HttpConnection](../../data/mergedataset/jsoup__3f7d2c71__HttpConnection)

**LEFT:** Left adds a new condition (OR) that is reponsible for changing the value of the local variable needsRedirect.

**RIGHT:** Right updates another if statement conditions; it changes a set of conditions grouped with AND, to the OR operator. This if is responsible for throw a new exception.

**Justificativa do dataset:** There is a locally observable interference as an unexpected behavior is caused by the control flow. Based on the changes, different excpetions ca be thrown during the execution.

#### claude-haiku-5-5: YES ✅

<details><summary>Execução 1 (<code>1.csv</code>): YES — Condição C: needsRedirect</summary>

1. INTENÇÃO: O resumo de LEFT está correto: adiciona `status == HTTP_TEMP_REDIR (307)` à condição OR que define `needsRedirect`. O resumo de RIGHT não confere com o diff. Não há troca de AND por OR. A condição original `!(A || B || C)` vira `!A && !B && !D`, em que D é `xmlContentTypeRxp.matcher(contentType).matches()`. Ou seja, RIGHT troca o `startsWith("application/xhtml+xml")` por um regex mais amplo (`application/\w+\+xml.*`) e mantém a mesma forma de negação. A exceção `UnsupportedMimeTypeException` já existia; RIGHT não cria uma nova. O restante do diff de RIGHT é formatação (espaços em branco, import, Javadoc).

2. ESTADO: Em `execute(req, previousResponse)`:
   - `needsRedirect`: escrito por LEFT (a condição do 307) e lido pelo `if (needsRedirect && req.followRedirects())`, que dá `return execute(req, res)` antes da checagem de content-type.
   - `contentType` / a condição de `UnsupportedMimeTypeException`: alterada por RIGHT. Esse trecho está depois do desvio de redirecionamento, então é controlado por `needsRedirect`.
   - `status`: lido pelas duas condições alteradas.

3. TABELA DE ESTADOS: Entrada escolhida: status = 307, followRedirects = true, ignoreHttpErrors = true, Content-Type = application/pdf, Location válida.
   - needsRedirect: BASE = false | LEFT = true | RIGHT = false | MERGE = true
   - Caminho de execução: BASE = chega à checagem de content-type | LEFT = redireciona (chama execute recursivamente) | RIGHT = chega à checagem de content-type | MERGE = redireciona
   - Resultado da checagem de content-type (código alterado por RIGHT): BASE = lança UnsupportedMimeTypeException | LEFT = não executada | RIGHT = lança UnsupportedMimeTypeException | MERGE = não executada
   - Entrada de controle para o caso 307 sem ignoreHttpErrors: BASE = HttpStatusException | RIGHT = HttpStatusException | MERGE = redireciona (intenção de LEFT)

4. CRITÉRIO DE CONFLITO: X = needsRedirect.
   - (A) não se aplica: o valor de needsRedirect muda em LEFT (false → true para 307), então não é igual nos três.
   - (B) não se aplica diretamente: o valor de X em LEFT difere de BASE, mas o MERGE preserva LEFT (true = true). A condição B só se aplica a LEFT, e LEFT é preservado.
   - (C) se aplica: X é escrito por LEFT (difere de BASE), e o código alterado por RIGHT (a checagem de content-type e sua exceção) é controlado por X. Na entrada escolhida, a checagem é executada em RIGHT (lança exceção) e não é executada no MERGE. Assim, o código de RIGHT se comporta no MERGE de forma diferente de como se comporta no pai que o escreveu. A mudança de LEFT é intencional em si, mas o critério é aplicado sobre a dependência de controle, e ela existe.
   - Também não há conflito pelo lado do valor da condição de RIGHT: LEFT não lê nem escreve a expressão de content-type.
   - Como C se aplica a needsRedirect, a conclusão é SIM.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): YES — Condição C: needsRedirect</summary>

1. INTENÇÃO: O resumo de LEFT é confirmado pelo diff. LEFT adiciona a constante HTTP_TEMP_REDIR = 307 à condição que define `needsRedirect` em `execute`. O resumo de RIGHT está incorreto. O diff não troca AND por OR. A condição original `!(A || B || C)` vira `!A && !B && !D`, que é a mesma lógica De Morgan, e `application/xhtml+xml` é substituído pela regex `application/\w+\+xml.*`. Além disso, RIGHT altera o `if` que lança `UnsupportedMimeTypeException`, como o resumo indica. Segue-se o diff.

2. ESTADO: Em `execute(req, previousResponse)`, os elementos relevantes são:
   - `needsRedirect`, escrito por LEFT e lido pelo `if (needsRedirect && req.followRedirects())`, que faz o `return execute(req, res)` antecipado.
   - A expressão do `if` de content-type (alterada por RIGHT), que lança `UnsupportedMimeTypeException`. Ela é executada apenas quando não há redirecionamento, portanto é controlada por `needsRedirect`.
   - A exceção lançada (`UnsupportedMimeTypeException`) e o retorno do método.

3. TABELA DE ESTADOS: Entrada: status = 307, followRedirects = true, ignoreHttpErrors = true, Content-Type = "image/png", header Location presente.
   - needsRedirect: BASE = false | LEFT = true | RIGHT = false | MERGE = true
   - Resultado do content-type check: BASE = lança UnsupportedMimeTypeException | LEFT = não alcançado (redireciona antes) | RIGHT = lança UnsupportedMimeTypeException | MERGE = não alcançado (redireciona antes)
   - Resultado observável: BASE = exceção | LEFT = redirecionamento | RIGHT = exceção | MERGE = redirecionamento

4. CRITÉRIO DE CONFLITO: X = needsRedirect e X = a expressão do content-type check (resultado observável).
   - (A) Não se aplica: needsRedirect difere de BASE em LEFT, e o resultado do content-type check difere de BASE em RIGHT.
   - (B) O valor de needsRedirect em LEFT (true) é preservado no MERGE (true). O resultado do content-type check em RIGHT é preservado no MERGE, porque o código de RIGHT não foi alterado de forma conflitante. Não há violação de B.
   - (C) O valor de needsRedirect em LEFT difere de BASE. O código alterado por RIGHT (o `if` de content-type) é controlado por needsRedirect, pois só é alcançado quando não há redirecionamento. Para a entrada acima, esse código lança exceção em RIGHT e não é alcançado no MERGE, então se comporta de forma diferente no MERGE do que no pai que o escreveu. A condição C se aplica literalmente. Que essa mudança de comportamento seja a intenção de LEFT (seguir redirecionamentos 307) não a descarta, segundo as instruções.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): YES — Condição C: needsRedirect</summary>

1. INTENÇÃO: LEFT adiciona a constante HTTP_TEMP_REDIR (307) e a inclui na condição que define `needsRedirect`, então um status 307 passa a provocar redirecionamento. RIGHT muda a condição de tipo de conteúdo. O resumo diz que RIGHT troca AND por OR, mas o diff não mostra isso: a condição original `!(A || B || C)` vira `!A && !B && !D`, em que D é `xmlContentTypeRxp.matcher(contentType).matches()`. A lógica é equivalente, exceto pela substituição de C por D, que é mais ampla. Confio no diff. O `throw UnsupportedMimeTypeException` é a instrução cuja condição RIGHT altera.

2. ESTADO: Escritos pelos trechos alterados:
   - `needsRedirect` (escrito por LEFT e lido pelo `if` de redirecionamento, que controla o `return execute(req, res)`).
   - A condição de tipo de conteúdo (RIGHT), que controla o `throw UnsupportedMimeTypeException`.
   - A constante `HTTP_TEMP_REDIR` e o padrão `xmlContentTypeRxp`, que não são alterados por outros lados.
   - O valor de retorno/exceção de `execute`.

3. TABELA DE ESTADOS: entrada com status = 307, ignoreHttpErrors = true, ignoreContentType = false, followRedirects = true, Content-Type = "application/atom+xml".
   - needsRedirect: BASE = false | LEFT = true | RIGHT = false | MERGE = true
   - Resultado observável: BASE = UnsupportedMimeTypeException (o status 307 não gera redirecionamento, então chega à checagem de tipo, e "application/atom+xml" não começa com text/ nem application/xml, portanto lança a exceção) | LEFT = redirecionamento (execute recursivo; a checagem de tipo não é alcançada) | RIGHT = sem exceção, retorna a resposta (o regex casa com "application/atom+xml") | MERGE = redirecionamento (a checagem de tipo não é alcançada)

4. CRITÉRIO DE CONFLITO: X = needsRedirect.
   - (A) não se aplica: X difere entre BASE e LEFT (false × true).
   - (B) LEFT difere de BASE em X (true ≠ false), e MERGE (true) preserva o valor de LEFT. RIGHT não altera X (igual a BASE), então B não se aplica a RIGHT. Não há violação de B.
   - (C) LEFT escreve X, e o código alterado por RIGHT (a checagem de tipo) é controlado por X, pois só é alcançado quando `needsRedirect` é falso. Em RIGHT, com status 307, esse código é executado e aceita o tipo "application/atom+xml". No MERGE, com o mesmo status, o fluxo é desviado para o redirecionamento e esse código não é executado. O comportamento de RIGHT é alterado no MERGE, e isso se aplica.
   
   Existe conflito por C. A intenção de LEFT (redirecionar em 307) é preservada, mas a condição de tipo de RIGHT deixa de ser avaliada para esses status, o que é interferência de controle indesejada para RIGHT.

</details>

#### claude-opus-5-5: NO ❌

<details><summary>Execução 1 (<code>1.csv</code>): NO</summary>

1. INTENÇÃO:
   - LEFT cria a constante `HTTP_TEMP_REDIR = 307` e a acrescenta, com OR, à condição que define `needsRedirect = true`. Assim, respostas 307 passam a ser seguidas como redirecionamento.
   - RIGHT reescreve a verificação de content-type. O resumo fala em trocar AND por OR, mas o diff mostra outra coisa: a condição é reescrita por De Morgan em uma cadeia de ANDs, e `startsWith("application/xhtml+xml")` é substituído pelo regex `application/\w+\+xml.*`. O regex aceita `xhtml+xml` e também tipos como `atom+xml` e `rss+xml`. Confio no diff.
   - O MERGE contém as duas alterações sem modificação.

2. ESTADO (em `execute(req, previousResponse)`):
   - variável local `needsRedirect`;
   - exceção lançada (`HttpStatusException` ou `UnsupportedMimeTypeException`);
   - `req` (method, data, url, cookies) e a chamada recursiva no redirecionamento;
   - retorno `res`.

3. TABELA DE ESTADOS:
   - Entrada A: status = 307, Location válido, depois 200 com `text/html`, ignoreHttpErrors = false.
     - needsRedirect: BASE = false | LEFT = true | RIGHT = false | MERGE = true
     - exceção/retorno: BASE = HttpStatusException(307) | LEFT = res da URL redirecionada | RIGHT = HttpStatusException(307) | MERGE = res da URL redirecionada
   - Entrada B: status = 200, contentType = `application/atom+xml;charset=utf-8`, ignoreContentType = false.
     - needsRedirect: false nas quatro versões.
     - exceção/retorno: BASE = UnsupportedMimeTypeException | LEFT = UnsupportedMimeTypeException | RIGHT = res retornado | MERGE = res retornado
   - Entrada C: status = 200, contentType = `application/xhtml+xml`.
     - res retornado nas quatro versões.
   - Entrada D (as duas mudanças juntas): status 307, depois 200 com `application/atom+xml`.
     - BASE = HttpStatusException | LEFT = UnsupportedMimeTypeException | RIGHT = HttpStatusException | MERGE = res retornado.

4. CRITÉRIO DE CONFLITO:
   - (A) Não se aplica. Nas entradas A, B e C, nenhum elemento fica igual em BASE, LEFT e RIGHT e diferente só no MERGE.
   - (B) Nas entradas A, B e C, o MERGE preserva o pai que alterou cada elemento:
     - na entrada A, o MERGE é igual a LEFT em `needsRedirect` e no retorno;
     - na entrada B, o MERGE é igual a RIGHT no retorno.
   - (B) e (C) na entrada D: o MERGE difere de LEFT. Porém essa diferença vem apenas de o MERGE aplicar à resposta final a verificação de content-type de RIGHT. Essa verificação dá o mesmo resultado que em RIGHT para essa resposta (aceita `atom+xml`). A mudança de LEFT só define se o redirecionamento ocorre, e o MERGE o segue exatamente como LEFT. Nenhum lado lê um valor alterado pelo outro de forma que mude o seu próprio comportamento. O resultado é a composição independente das duas mudanças, e não uma interferência.
   - (C) A verificação de content-type de RIGHT não lê `needsRedirect` nem `HTTP_TEMP_REDIR`. A condição de redirecionamento de LEFT não lê `contentType` nem o regex. Em todas as entradas, a verificação de RIGHT se comporta no MERGE como em RIGHT para o mesmo content-type, e o redirecionamento se comporta como em LEFT para o mesmo status.

</details>

#### claude-sonnet-5-5: NO ❌

<details><summary>Execução 1 (<code>1.csv</code>): NO</summary>

1. INTENÇÃO: LEFT adiciona o status 307 (HTTP_TEMP_REDIR) à condição que define needsRedirect = true. RIGHT reescreve a condição de content type, que lança UnsupportedMimeTypeException. O resumo diz que RIGHT troca AND por OR, mas o diff mostra algo diferente: RIGHT apenas remove um parêntese de negação e passa a usar "&& !startsWith". Isso equivale logicamente à condição original. A mudança real é trocar `startsWith("application/xhtml+xml")` por `!xmlContentTypeRxp.matcher(contentType).matches()`, que aceita `application/\w+\+xml.*`. Confio no diff.

2. ESTADO: needsRedirect (local), a exceção HttpStatusException, a exceção UnsupportedMimeTypeException, o retorno de execute (res) e as chamadas recursivas.

3. TABELA DE ESTADOS:
   - Entrada 1: status = 307, contentType = "text/html".
     - BASE: needsRedirect = false e, sem ignoreHttpErrors, lança HttpStatusException.
     - LEFT: needsRedirect = true e segue o redirect.
     - RIGHT: igual a BASE, lança HttpStatusException.
     - MERGE: igual a LEFT, segue o redirect.
   - Entrada 2: status = 200, contentType = "application/atom+xml".
     - BASE: lança UnsupportedMimeTypeException.
     - LEFT: igual a BASE, lança a exceção.
     - RIGHT: não lança, pois o regex casa.
     - MERGE: igual a RIGHT, não lança.
   - Entrada 3: status = 307, redirecionando para uma página com contentType "application/atom+xml".
     - BASE: HttpStatusException.
     - LEFT: segue o redirect e, na chamada recursiva, lança UnsupportedMimeTypeException.
     - RIGHT: HttpStatusException.
     - MERGE: segue o redirect e retorna a resposta normalmente.
   - Em todas as entradas, o MERGE iguala LEFT ou RIGHT conforme o trecho que cada um alterou.

4. CRITÉRIO DE CONFLITO:
   - (A) não se aplica: nenhum valor muda no MERGE sem ter mudado em LEFT ou RIGHT.
   - (B) needsRedirect: o MERGE preserva o valor de LEFT. Exceção de content type: o MERGE preserva o valor de RIGHT. Na entrada 3, o MERGE retorna a resposta, enquanto LEFT lança a exceção de mime type, pois só o RIGHT muda o content type. Esse valor de LEFT difere de BASE e não é preservado, mas isso é consequência da mudança de RIGHT e é compatível com ela. Seria um caso de B apenas formalmente.
   - (C) o código alterado por RIGHT (a verificação de content type) não lê needsRedirect nem é controlado por ele, a não ser pelo fluxo normal de redirecionamento. Ele se comporta igual no MERGE e em RIGHT para qualquer resposta que chegue a essa verificação. As mudanças são independentes e ortogonais: uma decide se há redirect e a outra decide se o content type é aceito.
   - Conclusão: nenhuma interferência indesejada. A entrada 3 é a combinação natural das duas intenções.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): NO</summary>

1. INTENÇÃO: LEFT adiciona o status 307 (HTTP_TEMP_REDIR) à condição que define needsRedirect = true. RIGHT reescreve a condição do if que lança UnsupportedMimeTypeException: troca o teste "application/xhtml+xml" por um regex de XML (application/\w+\+xml.*) e reestrutura os operadores. O resumo diz que RIGHT muda AND para OR, mas o diff mostra apenas a reescrita de !(A||B||C) como !A && !B && !C, mais a troca de C pelo regex.

2. ESTADO: needsRedirect (local), a exceção HttpStatusException lançada quando o status não é redirecionamento e ignoreHttpErrors é falso, o fluxo de controle de followRedirects/execute recursivo, e a exceção UnsupportedMimeTypeException.

3. TABELA DE ESTADOS:
   - Entrada A: status = 307, ignoreHttpErrors = false, followRedirects = true, Location válido.
     - needsRedirect: BASE = false (e lança HttpStatusException) | LEFT = true | RIGHT = false (lança HttpStatusException) | MERGE = true.
     - Comportamento: BASE lança HttpStatusException, LEFT segue o redirect, RIGHT lança HttpStatusException, MERGE segue o redirect. O MERGE é igual a LEFT.
   - Entrada B: status = 200, contentType = "application/xhtml+xml".
     - BASE: sem exceção | LEFT: sem exceção | RIGHT: o regex exige \w+ entre "application/" e "+xml", e "xhtml+xml" contém "xhtml" seguido de "+xml", então "application/xhtml+xml" casa com o regex. Sem exceção. | MERGE: sem exceção.
   - Entrada C: contentType = "application/atom+xml".
     - BASE: lança UnsupportedMimeTypeException | LEFT: lança | RIGHT: não lança | MERGE: não lança. O MERGE é igual a RIGHT.
   - Entrada D: status = 307 com resposta de contentType inválido, após o redirect.
     - O redirect de LEFT leva a uma nova execução, e o código do RIGHT é executado na resposta final. O código de RIGHT não depende de needsRedirect, e só lê res.contentType() e req.ignoreContentType().

4. CRITÉRIO DE CONFLITO:
   - (A) não se aplica: onde o valor muda no MERGE, ele também mudou em LEFT ou RIGHT.
   - (B) o MERGE preserva o valor de LEFT para needsRedirect e o de RIGHT para a exceção de content type. As duas mudanças são em ramos independentes.
   - (C) o código alterado por RIGHT (checagem de content type) não lê needsRedirect, e o código alterado por LEFT não lê contentType. A checagem de RIGHT só é alcançada se não houver redirect, e isso vale igualmente em RIGHT e no MERGE. O comportamento do código de cada lado no MERGE é o mesmo que no pai que o escreveu.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): NO</summary>

1. INTENÇÃO: LEFT adiciona o status 307 (HTTP_TEMP_REDIR) à condição que define needsRedirect = true. RIGHT reescreve a condição do if que lança UnsupportedMimeTypeException. Ele troca o grupo negado com `||` por uma cadeia de `&&` com negações e passa a usar o regex xmlContentTypeRxp (`application/\w+\+xml.*`) em vez de startsWith("application/xhtml+xml").

2. ESTADO: no método execute, a variável local needsRedirect (LEFT), a exceção HttpStatusException lançada, o fluxo de controle (redirect ou continuação), a exceção UnsupportedMimeTypeException (RIGHT) e o retorno res.

3. TABELA DE ESTADOS:
   - Entrada A: status = 307, ignoreHttpErrors = false, followRedirects = true.
     - needsRedirect: BASE = false (lança HttpStatusException) | LEFT = true | RIGHT = false (lança HttpStatusException) | MERGE = true.
     - Fluxo: BASE e RIGHT lançam HttpStatusException. LEFT e MERGE redirecionam.
   - Entrada B: status = 200, contentType = "application/xhtml+xml".
     - BASE: aceita, sem exceção.
     - LEFT: aceita.
     - RIGHT: startsWith("application/xhtml+xml") foi removido. O regex exige `\w+` após "application/" e antes de "\+xml". "xhtml+xml" casa com `\w+\+xml`, pois "xhtml" são caracteres de palavra, então o regex casa e não lança exceção.
     - MERGE: aceita.
   - Entrada C: contentType = "application/pdf".
     - Todos lançam UnsupportedMimeTypeException, inclusive o MERGE.
   - Na entrada A, o redirect do MERGE continua em execute(req, res), e o conteúdo da resposta seguinte passa pelo novo check de content type de RIGHT. Isso é o comportamento esperado de cada lado e não difere do que ocorreria em cada pai isoladamente.

4. CRITÉRIO DE CONFLITO:
   - (A) não se aplica: needsRedirect em LEFT difere de BASE, e os outros valores não mudam no MERGE sem terem mudado em um dos pais.
   - (B) needsRedirect no MERGE (true) é igual ao de LEFT. O check de content type no MERGE é igual ao de RIGHT. Ambos são preservados.
   - (C) o código alterado por RIGHT (check de content type) não lê needsRedirect nem é controlado por ele. A condição alterada por LEFT não lê contentType nem depende do que RIGHT escreveu. As mudanças afetam trechos independentes, com ordem sequencial e sem interferência de dados.

</details>

### 5. `netty__193acdb3__LengthFieldBasedFrameDecoder#decode`

- **Target:** `decode(ChannelHandlerContext, Channel, ChannelBuffer)`
- **Esperado:** YES; **acertam:** claude-haiku-5-5; **erram:** claude-opus-5-5, claude-sonnet-5-5
- **Código:** [netty__193acdb3__LengthFieldBasedFrameDecoder](../../data/mergedataset/netty__193acdb3__LengthFieldBasedFrameDecoder)

**LEFT:** Left updates how variable frameLength is incremented, which is done only if the new conditional in the if statement is true.

**RIGHT:** Right updates method call failIfNecessary adding a new parameter (boolean value). [But these changes were also done by Left.]

**Justificativa do dataset:** There is a locally observable interference as the changes performed by right will only be executed in some cases because of the change performed by Left.

#### claude-haiku-5-5: YES ✅

<details><summary>Execução 1 (<code>1.csv</code>): YES — Condição C: frameLength</summary>

1. INTENÇÃO: O resumo de RIGHT diz que ela "adiciona um novo parâmetro" a failIfNecessary. O diff confirma isso, mas o parâmetro é adicionado à assinatura de failIfNecessary e não às chamadas que LEFT alterou. Além disso, RIGHT adiciona o campo failImmediatelyOnTooLongFrame (padrão false) e o setter. O resumo de LEFT diz que o incremento de frameLength ocorre "somente se o if é verdadeiro". O diff mostra que a soma `frameLength += lengthAdjustment + lengthFieldEndOffset` só ocorre quando `!lengthFieldIncludedInFrameLength`. Trecho com a mesma intenção, mas a condição é a negação do flag. A nota "[these changes were also done by Left]" do resumo de RIGHT não é confirmada pelo diff: LEFT não altera as chamadas de failIfNecessary.

2. ESTADO: No método TARGET decode(), os elementos escritos ou lidos pelas alterações são:
   - frameLength (local): escrito por LEFT (soma condicionada ao flag) e lido pelo `if (frameLength > maxFrameLength)`, que controla a chamada `failIfNecessary(ctx, true)` alterada por RIGHT.
   - bytesToDiscard (campo): escrito a partir de frameLength na branch de too-long e lido por failIfNecessary, que é alterado por RIGHT.
   - tooLongFrameLength (campo): escrito a partir de frameLength e lido por fail().
   - lengthFieldIncludedInFrameLength (campo): escrito por LEFT no construtor e lido em decode().
   - failImmediatelyOnTooLongFrame (campo): escrito por RIGHT e lido por failIfNecessary.

3. TABELA DE ESTADOS:
   Entrada: lengthFieldOffset = 0, lengthFieldLength = 2, lengthAdjustment = 0, initialBytesToStrip = 0, maxFrameLength = 10, buffer legível com 10 bytes, cabeçalho com valor 9.
   - BASE (flag inexistente, equivalente a false): frameLength = 9 + 0 + 2 = 11. Como 11 &gt; 10, entra na branch de too-long: bytesToDiscard = 11 − 10 = 1, failIfNecessary(ctx, true) executa com bytesToDiscard ≠ 0 e não lança exceção. Resultado: modo de descarte.
   - LEFT (lengthFieldIncludedInFrameLength = true): frameLength = 9 (sem soma). 9 ≤ 10, então não entra na branch de too-long. Como 10 ≥ 9, extrai o frame de 9 bytes.
   - RIGHT (failImmediatelyOnTooLongFrame = true, flag false): frameLength = 11, entra na branch de too-long, bytesToDiscard = 1, failIfNecessary(ctx, true) executa com failImmediately = true e firstDetection = true, então dispara fail() → TooLongFrameException imediata.
   - MERGE (flag true e failImmediately = true): frameLength = 9, não entra na branch de too-long. failIfNecessary(ctx, true) não é chamado. Nenhuma exceção é disparada.
   Valores:
   - frameLength: BASE = 11 | LEFT = 9 | RIGHT = 11 | MERGE = 9
   - bytesToDiscard: BASE = 1 | LEFT = 0 (não usado) | RIGHT = 1 | MERGE = 0 (não usado)
   - Chamada de fail() (TooLongFrameException): BASE = não | LEFT = não | RIGHT = sim | MERGE = não

4. CRITÉRIO DE CONFLITO: X = frameLength (também relevante para bytesToDiscard e tooLongFrameLength, que derivam dele).
   - (A) não se aplica: o valor de frameLength difere de BASE em LEFT e em RIGHT difere de BASE? Em RIGHT o valor é igual a BASE, mas em LEFT é diferente, e a condição (A) exige igualdade em BASE, LEFT e RIGHT. Não se aplica.
   - (B) o valor de frameLength em LEFT difere de BASE (9 ≠ 11 no caso de teste). O MERGE preserva esse valor (9 = 9), então esta condição não é violada. Não se aplica para frameLength. Para o campo lengthFieldIncludedInFrameLength, o MERGE também preserva o valor de LEFT.
   - (C) o valor de frameLength em LEFT difere de BASE. O código alterado por RIGHT (a chamada failIfNecessary(ctx, true) e o corpo de failIfNecessary, que lê bytesToDiscard, derivado de frameLength) está dentro de um bloco controlado por `frameLength > maxFrameLength`. No MERGE, essa chamada deixa de ser executada para o mesmo frame em que RIGHT a executava, e o comportamento do recurso de failImmediatelyOnTooLongFrame muda: RIGHT lança a exceção imediata, enquanto MERGE não a lança. Isso é o mesmo padrão do exemplo 3 (LEFT altera o valor que controla o código que RIGHT adicionou dentro do if). Aplica-se.

Não uso a intenção de LEFT (tornar o tamanho correto quando o campo inclui o próprio cabeçalho) para descartar a condição, porque o critério avalia o comportamento, e não a intenção.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): YES — Condição C: frameLength</summary>

1. INTENÇÃO: LEFT adiciona o campo `lengthFieldIncludedInFrameLength`, um novo construtor de 6 parâmetros e torna o ajuste `frameLength += lengthAdjustment + lengthFieldEndOffset` condicional a esse campo. RIGHT adiciona o campo `failImmediatelyOnTooLongFrame` com seu setter, acrescenta o parâmetro `firstDetectionOfTooLongFrame` a `failIfNecessary` e passa `true`/`false` nas duas chamadas dentro de `decode`. Os diffs confirmam os resumos. O resumo de LEFT diz que o incremento é feito "somente se o novo if for verdadeiro", o que corresponde ao diff: o incremento é pulado quando a flag é `true`. O resumo de RIGHT ("adding a new parameter") é impreciso: o parâmetro foi adicionado a `failIfNecessary`, não a um método público. O MERGE é a união textual das duas mudanças.

2. ESTADO: Em `decode`, o alvo escreve e lê a variável local `frameLength`, que controla o `if (frameLength > maxFrameLength)` e alimenta `bytesToDiscard` (campo de instância). Na branch de descarte, RIGHT chama `failIfNecessary(ctx, true|false)`, que lê `bytesToDiscard`, `failImmediatelyOnTooLongFrame` e `tooLongFrameLength`. Também são escritos `discardingTooLongFrame`, `tooLongFrameLength` e o valor de retorno (frame ou null).

3. TABELA DE ESTADOS: Entrada escolhida: `lengthFieldOffset=0`, `lengthFieldLength=2`, `lengthAdjustment=0`, `initialBytesToStrip=0`, `maxFrameLength=13`. O buffer tem 12 bytes legíveis e o campo de tamanho vale 12. Para LEFT e MERGE, a flag `lengthFieldIncludedInFrameLength` é `true`.
   - `frameLength` antes do `if (frameLength > maxFrameLength)`: BASE = 12 + 0 + 2 = 14 | LEFT = 12 | RIGHT = 14 | MERGE = 12
   - Desvio do branch de descarte: BASE = entra (14 &gt; 13) | LEFT = não entra | RIGHT = entra | MERGE = não entra
   - `bytesToDiscard` (após o branch): BASE = 14 − 12 = 2 | LEFT = não alterado | RIGHT = 2 | MERGE = não alterado
   - `failIfNecessary` chamado: BASE = (ctx) | LEFT = nenhum | RIGHT = (ctx, true) | MERGE = nenhum
   - Resultado de `decode`: BASE = null, descarte em andamento | LEFT = frame de 12 bytes | RIGHT = null, descarte em andamento | MERGE = frame de 12 bytes
   - Com `failImmediatelyOnTooLongFrame = true` (escrito por RIGHT): RIGHT dispara `fail(ctx, 14)` imediatamente, pois `bytesToDiscard != 0` e `firstDetectionOfTooLongFrame` é `true`. MERGE não entra no branch e não dispara nada.

4. CRITÉRIO DE CONFLITO: X = frameLength (com seu efeito em bytesToDiscard).
   - (A) não se aplica: `frameLength` muda em LEFT (de 14 para 12), então o valor em LEFT difere de BASE.
   - (B) o valor de X em LEFT (12) difere de BASE (14), e o MERGE (12) é igual a LEFT. O pai LEFT é preservado. Não dispara B.
   - (C) o valor de X em RIGHT (14) difere do valor de X em LEFT (12). Não é preciso considerar qual é "o" valor de BASE: basta que o valor escrito por LEFT difira de BASE. O código alterado por RIGHT (a chamada `failIfNecessary(ctx, true)` e o uso de `bytesToDiscard` dentro dela) é controlado por `frameLength` por meio do `if` e lê `bytesToDiscard`, que depende de `frameLength`. No MERGE, esse código se comporta de forma diferente do que em RIGHT: a branch de descarte não é executada para essa entrada, e a notificação antecipada (`fail` imediato) deixa de ocorrer. Logo, a condição C se aplica.
   
   A condição C se aplica a `frameLength`. A variável observável que sofre a interferência é `frameLength`, propagada para `bytesToDiscard`.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): YES — Condição C: frameLength</summary>

1. INTENÇÃO: LEFT adiciona o campo `lengthFieldIncludedInFrameLength`, cria um construtor que o recebe e, em `decode()`, só soma `lengthAdjustment + lengthFieldEndOffset` a `frameLength` quando esse flag é false. RIGHT adiciona o campo `failImmediatelyOnTooLongFrame` (padrão false), um setter, e altera `failIfNecessary` para receber `firstDetectionOfTooLongFrame`, notificando antes ao detectar frame longo quando o modo imediato está ativo. Os diffs confirmam o resumo de LEFT. O resumo de RIGHT ("these changes were also done by Left") contradiz os diffs: LEFT não altera `failIfNecessary`. Confio no diff. O MERGE contém as duas famílias de mudanças.

2. ESTADO: Elementos escritos pelo TARGET e pelos trechos alterados:
   - `frameLength` (local em `decode`): escrito por LEFT, lido na checagem `frameLength > maxFrameLength`, que controla a chamada `failIfNecessary(ctx, true)` de RIGHT.
   - `tooLongFrameLength` (campo): recebe `frameLength` em `decode`; lido por `failIfNecessary` (código de RIGHT) em `fail(ctx, this.tooLongFrameLength)`.
   - `bytesToDiscard` (campo): recebe `frameLength - readableBytes` em `decode`; lido por `failIfNecessary` (código de RIGHT) na condição `bytesToDiscard == 0`.
   - `failImmediatelyOnTooLongFrame` e `lengthFieldIncludedInFrameLength`: campos independentes.

3. TABELA DE ESTADOS:
   Entrada: `lengthFieldOffset=0`, `lengthFieldLength=2`, `lengthAdjustment=0`, `initialBytesToStrip=0`, `maxFrameLength=10`, buffer com cabeçalho de length = 9 e 9 bytes de corpo (mais 2 bytes de cabeçalho, total 11 legíveis), flag `lengthFieldIncludedInFrameLength=true`, `failImmediatelyOnTooLongFrame=true`.
   - `frameLength` (após cálculo): BASE = 9 + 0 + 2 = 11 | LEFT = 9 (sem soma) | RIGHT = 11 | MERGE = 9
   - Checagem `frameLength > maxFrameLength`: BASE = verdadeiro | LEFT = falso | RIGHT = verdadeiro | MERGE = falso
   - `tooLongFrameLength` e `bytesToDiscard` (só no ramo de frame longo): BASE = 11 e 0 | LEFT = não atingido | RIGHT = 11 e 0 (dispara `fail` com 11) | MERGE = não atingido (nenhum fail)
   - Comportamento observado: BASE/RIGHT emitem TooLongFrameException(11); MERGE não emite nada e entrega o frame de 9 bytes como válido.

4. CRITÉRIO DE CONFLITO: X = `frameLength` (com `tooLongFrameLength` e `bytesToDiscard` derivados dele).
   - (A) não se aplica: o valor de X muda em LEFT, então há ao menos um pai que difere de BASE.
   - (B) o valor de `frameLength` em LEFT (9) difere de BASE (11), e o MERGE preserva LEFT (9). Não há violação por (B) para o próprio campo, pois LEFT é preservado.
   - (C) o valor de X em LEFT difere de BASE, e o código adicionado/alterado por RIGHT lê X: a condição `frameLength > maxFrameLength` controla a chamada `failIfNecessary(ctx, true)` alterada por RIGHT, e `failIfNecessary` (código novo de RIGHT) lê `bytesToDiscard` e `tooLongFrameLength`, ambos derivados de `frameLength`. No MERGE, esse código se comporta de forma diferente do que em RIGHT: o frame de 11 bytes deixa de disparar a exceção que RIGHT dispararia. Há interferência de fluxo de controle e de dados indesejada, pois a intenção de RIGHT (detectar frame longo com o tamanho ajustado) não se mantém quando LEFT está ativo.
   Conclusão: a condição C se aplica a `frameLength`.

</details>

#### claude-opus-5-5: NO ❌

<details><summary>Execução 1 (<code>1.csv</code>): NO</summary>

1. INTENÇÃO:
   - LEFT adiciona o campo `final` `lengthFieldIncludedInFrameLength`, definido por um novo construtor de 6 parâmetros. Os construtores antigos delegam a ele com `false`. Em `decode`, o ajuste `frameLength += lengthAdjustment + lengthFieldEndOffset` passa a ocorrer só quando o flag é `false`.
   - RIGHT adiciona o campo `failImmediatelyOnTooLongFrame` (padrão `false`) e o setter correspondente. Também adiciona o parâmetro `firstDetectionOfTooLongFrame` a `failIfNecessary`: `false` no ramo de descarte e `true` na primeira detecção de frame longo demais. Com o flag ligado, `fail()` é disparado já na primeira detecção.
   - Ao contrário do que sugere o resumo, a mudança em `failIfNecessary` aparece só no diff de RIGHT, não no de LEFT.
   - O MERGE contém as duas mudanças integralmente.

2. ESTADO:
   - Variável local `frameLength`.
   - Campos `discardingTooLongFrame`, `tooLongFrameLength` e `bytesToDiscard`.
   - Posição de leitura do buffer (`readerIndex`).
   - Exceção disparada via `fail()`, que chama `Channels.fireExceptionCaught`.
   - Retorno de `decode`.

3. TABELA DE ESTADOS:
   - Entrada 1: `maxFrameLength = 10`, `lengthFieldOffset = 0`, `lengthFieldLength = 2`, `lengthAdjustment = 0`, construtor padrão (`lengthFieldIncludedInFrameLength = false`). Em RIGHT e MERGE chama-se `setFailImmediatelyOnTooLongFrame(true)`. O buffer tem 5 bytes legíveis e o campo de comprimento vale 20.
     - `frameLength`: BASE = 22 | LEFT = 22 | RIGHT = 22 | MERGE = 22
     - `tooLongFrameLength`: 22 nas quatro versões.
     - `bytesToDiscard`: 17 nas quatro versões.
     - `discardingTooLongFrame`: `true` nas quatro versões.
     - Exceção disparada: BASE = nenhuma | LEFT = nenhuma | RIGHT = `TooLongFrameException("... exceeds 10: 22 - discarded")` | MERGE = a mesma de RIGHT.
     - Retorno: `null` nas quatro versões.
   - Entrada 2: mesma configuração, mas com `lengthFieldIncludedInFrameLength = true`. Esse construtor só existe em LEFT e MERGE.
     - `frameLength`: LEFT = 20 | MERGE = 20
     - `bytesToDiscard`: LEFT = 15 | MERGE = 15
     - Exceção com `failImmediately = false`: LEFT = nenhuma | MERGE = nenhuma.
     - Exceção com `failImmediately = true` (só no MERGE): `TooLongFrameException(20)`. Isso é exatamente o que a lógica de RIGHT produz para um `frameLength` de 20.

4. CRITÉRIO DE CONFLITO:
   - (A) Não se aplica. Os elementos iguais em BASE, LEFT e RIGHT, como `frameLength` e `bytesToDiscard` na entrada 1, também são iguais no MERGE.
   - (B) Não se aplica.
     - A exceção de RIGHT (disparo imediato) é preservada no MERGE.
     - O `frameLength` de LEFT (20, sem ajuste) é preservado no MERGE.
   - (C) Não se aplica.
     - O código de RIGHT é controlado por `frameLength > maxFrameLength` e lê `tooLongFrameLength` e `bytesToDiscard`. Mas para o mesmo `frameLength` ele decide disparar ou não exatamente como em RIGHT.
     - O código de LEFT não lê `failImmediatelyOnTooLongFrame` nem o novo parâmetro de `failIfNecessary`.
     - Com os padrões (`lengthFieldIncludedInFrameLength = false`, `failImmediately = false`), o comportamento é idêntico ao de BASE.

</details>

#### claude-sonnet-5-5: NO ❌

<details><summary>Execução 1 (<code>1.csv</code>): NO</summary>

1. INTENÇÃO: LEFT adiciona o campo lengthFieldIncludedInFrameLength. Quando ele é true, o decode deixa de somar lengthAdjustment + lengthFieldEndOffset a frameLength. RIGHT adiciona o modo failImmediatelyOnTooLongFrame, com o parâmetro firstDetectionOfTooLongFrame em failIfNecessary. Com isso, o fail() é chamado já na primeira detecção do frame longo, e não só ao fim do descarte. O resumo diz que RIGHT também fez as mudanças de LEFT, mas o diff de RIGHT não contém o campo nem o if novo; confio no diff.

2. ESTADO: Em decode, as escritas relevantes são frameLength, discardingTooLongFrame, tooLongFrameLength, bytesToDiscard, o buffer (skipBytes), as exceções disparadas por fail() e o valor retornado.

3. TABELA DE ESTADOS:
   Entrada: lengthFieldOffset=0, lengthFieldLength=2, adjustment=0, maxFrameLength=100, campo de comprimento = 200, buffer com 10 bytes legíveis. Usa-se o construtor padrão, com lengthFieldIncludedInFrameLength=false e failImmediately=false.
   - frameLength: BASE = 202 | LEFT = 202 | RIGHT = 202 | MERGE = 202
   - tooLongFrameLength: 202 em todas as versões.
   - bytesToDiscard: 192 em todas as versões.
   - Exceção disparada na primeira chamada: nenhuma em todas as versões, pois bytesToDiscard != 0 e failImmediately=false.
   
   Variação com failImmediately=true (só RIGHT e MERGE):
   - BASE e LEFT: nenhuma exceção na primeira chamada.
   - RIGHT: a exceção TooLongFrameException(202) é disparada imediatamente.
   - MERGE: a exceção é disparada imediatamente, igual a RIGHT.

   Variação com lengthFieldIncludedInFrameLength=true (só LEFT e MERGE), campo = 200:
   - LEFT: frameLength = 200, sem adição. 
   - MERGE: frameLength = 200, igual a LEFT.
   - Se frameLength &gt; maxFrameLength, o MERGE chama failIfNecessary(ctx, true), que em RIGHT se comporta como esperado. Com tooLongFrameLength = frameLength (já ajustado por LEFT), a exceção sai com o valor de LEFT, consistente com o intencionado.

4. CRITÉRIO DE CONFLITO:
   - (A) não se aplica: nenhum valor muda no MERGE sem ter mudado em LEFT ou RIGHT.
   - (B) em cada variação, o MERGE é igual ao pai que alterou o valor.
   - (C) o código de RIGHT lê tooLongFrameLength e firstDetectionOfTooLongFrame, e o de LEFT só altera como frameLength é calculado. O código de RIGHT no MERGE usa o valor de frameLength produzido por LEFT, o que é o comportamento desejado, pois a mensagem de erro deve refletir o comprimento calculado. Não há comportamento divergente do pai que escreveu o valor. O novo parâmetro de failIfNecessary foi aplicado a todas as chamadas, inclusive as de LEFT, que não tinha chamadas novas.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): NO</summary>

1. INTENÇÃO: LEFT adiciona o campo lengthFieldIncludedInFrameLength e só soma lengthAdjustment + lengthFieldEndOffset a frameLength quando esse campo é false. O diff de LEFT não altera as chamadas a failIfNecessary, ao contrário do que diz o resumo. RIGHT adiciona o parâmetro firstDetectionOfTooLongFrame a failIfNecessary e o campo failImmediatelyOnTooLongFrame, que decide quando fail() é chamado.

2. ESTADO: Em decode(), os elementos escritos são frameLength, tooLongFrameLength, bytesToDiscard, discardingTooLongFrame, a exceção lançada e o retorno. Pelos trechos alterados, também entram as chamadas a fail(), que disparam a exceção TooLongFrameException no canal.

3. TABELA DE ESTADOS:
   - Entrada: lengthFieldLength = 2, campo lido = 10, lengthAdjustment = 0, lengthFieldEndOffset = 2, maxFrameLength = 5. Construtor de 6 argumentos com lengthFieldIncludedInFrameLength = true. buffer com 4 bytes legíveis, failImmediatelyOnTooLongFrame = true.
   - frameLength: BASE = 12 | LEFT = 10 (não soma) | RIGHT = 12 | MERGE = 10.
   - Como a entrada usa lengthFieldIncludedInFrameLength = true, o campo só existe em LEFT e MERGE. Em BASE e RIGHT, frameLength = 12.
   - Com maxFrameLength = 5, frameLength &gt; max em todas as versões, então entra no modo de descarte. bytesToDiscard = frameLength - 4: BASE = 8, LEFT = 6, RIGHT = 8, MERGE = 6.
   - fail() em RIGHT é chamado imediatamente com tooLongFrameLength = 12, enquanto em MERGE é chamado com tooLongFrameLength = 10.
   - Exceção: BASE dispara só no fim do descarte, com 12. LEFT dispara só no fim, com 10. RIGHT dispara imediatamente, com 12. MERGE dispara imediatamente, com 10.

4. CRITÉRIO DE CONFLITO: X = frameLength (e o valor passado a fail()).
   - (A) não se aplica: X difere em LEFT.
   - (B) o MERGE preserva o valor de frameLength de LEFT (10). Em RIGHT, frameLength é igual a BASE, então não há violação aqui.
   - (C) a mudança de LEFT altera frameLength, e o código alterado por RIGHT (failIfNecessary, que lê tooLongFrameLength derivado de frameLength) é controlado por esse valor. Mas esse código se comporta no MERGE do mesmo modo que se comporta em LEFT: usa o valor de frameLength de LEFT apenas para o conteúdo da mensagem. A lógica de RIGHT (quando falhar) não depende do valor modificado de forma a divergir da intenção. Em RIGHT, o código lê frameLength na versão de BASE, e no MERGE lê a versão de LEFT, que é a esperada pelo campo novo.
   - Comparando as entradas com lengthFieldIncludedInFrameLength = false (padrão dos construtores antigos), o comportamento é idêntico ao de BASE/RIGHT, sem interferência. As duas modificações são ortogonais: uma altera o cálculo do comprimento, a outra altera o momento da notificação.
   - Nenhuma condição se aplica.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): NO</summary>

1. INTENÇÃO: LEFT adiciona o campo lengthFieldIncludedInFrameLength e um novo construtor. Em decode(), só soma lengthAdjustment + lengthFieldEndOffset a frameLength se !lengthFieldIncludedInFrameLength. O resumo diz que LEFT também alterou failIfNecessary, mas o diff mostra que isso não ocorre; vale o diff. RIGHT adiciona o campo failImmediatelyOnTooLongFrame (padrão false), um parâmetro boolean em failIfNecessary e um setter. Em decode(), as chamadas passam false (modo de descarte) e true (primeira detecção).

2. ESTADO: Em decode() e nos trechos alterados, os elementos escritos são:
   - frameLength (local);
   - discardingTooLongFrame, tooLongFrameLength e bytesToDiscard (campos);
   - as exceções disparadas por fail(), via fireExceptionCaught;
   - a exceção CorruptedFrameException;
   - o valor retornado.

3. TABELA DE ESTADOS:
   - Entrada: lengthFieldLength=2, offset=0, adjustment=0, maxFrameLength=100, campo de comprimento = 200, buffer com 10 bytes legíveis, construtor padrão (included=false, failImmediately=false).
   - frameLength após o ajuste: BASE = 202 | LEFT = 202 | RIGHT = 202 | MERGE = 202.
   - Como 202 &gt; 100, entra no modo de descarte. bytesToDiscard = 192 em todas as versões. A exceção não é disparada nesse momento (bytesToDiscard != 0) em nenhuma versão.
   - Com included=true (só em LEFT e MERGE), frameLength = 200 em vez de 202, e o restante do fluxo é o mesmo.
   - Com failImmediately=true (só em RIGHT e MERGE): na primeira detecção, a exceção é disparada com tooLongFrameLength = 202. No MERGE, com included=false, o valor é o mesmo de RIGHT.
   - Com included=true e failImmediately=true no MERGE: a exceção é disparada com tooLongFrameLength = 200, que é o valor que LEFT calcularia. RIGHT apenas lê tooLongFrameLength, e esse valor vem do cálculo de LEFT, que está de acordo com a intenção de LEFT.

4. CRITÉRIO DE CONFLITO:
   - X = frameLength, tooLongFrameLength e a exceção.
   - (A) não se aplica: os valores que mudam no MERGE já mudaram em LEFT ou em RIGHT.
   - (B) o MERGE preserva o valor de cada pai nas combinações de configuração correspondentes: included=true reproduz LEFT, e failImmediately=true reproduz RIGHT.
   - (C) o código de RIGHT lê tooLongFrameLength, derivado do frameLength de LEFT. Esse valor no MERGE é o mesmo que LEFT produziria, e a lógica de RIGHT apenas o repassa à mensagem. Não há mudança de comportamento indesejada: as duas mudanças são ortogonais, uma sobre o cálculo do comprimento e outra sobre quando notificar.

</details>

### 6. `spring-boot__6664ce19__AtomikosPropertiesTests#testDefaultProperties`

- **Target:** `testDefaultProperties()`
- **Esperado:** YES; **acertam:** claude-haiku-5-5, claude-sonnet-5-5; **erram:** claude-opus-5-5
- **Código:** [spring-boot__6664ce19__AtomikosPropertiesTests](../../data/mergedataset/spring-boot__6664ce19__AtomikosPropertiesTests)

**LEFT:** Added some attributes for a test, changing the quantity of the parameters and the key.length() attribute.

**RIGHT:** Removed some attributes for a test, changing the quantity of the parameters and the key.length() attribute.

**Justificativa do dataset:** Left changed the number of attributes of the testing and right created a test with the size of the attributes in class MapEntry. An exception can occur if left tries to access attributes of right., because right removed some parameter.

#### claude-haiku-5-5: YES ✅

<details><summary>Execução 1 (<code>1.csv</code>): YES — Condição B: properties</summary>

1. INTENÇÃO: LEFT adiciona propriedades de teste (allow_subtransactions, recovery) e passa a carregar os defaults de um arquivo `transactions-defaults.properties`. Ele também espera 18 entradas em `testDefaultProperties`. RIGHT remove as propriedades de console e espera 9 entradas. Os resumos conferem com os diffs.

2. ESTADO: O objeto `properties` retornado por `this.properties.asProperties()` e a asserção `hasSize(...)`, que compara o tamanho desse objeto. Também o `defaultSettings`, lido por `defaultOf(...)` e pelas asserções `contains`.

3. TABELA DE ESTADOS:
   - Entrada: instância padrão de `AtomikosProperties` (`this.properties` é criado sem setters em `testDefaultProperties`).
   - Tamanho de `asProperties()` na instância padrão: a classe de produção não é alterada por nenhum lado. A BASE afirma `hasSize(13)`, e as 13 chaves padrão (9 de defaults + 4 de console) confirmam esse valor, então o tamanho real é 13 em todas as versões.
   - Asserção `hasSize` (X = tamanho esperado):
     - BASE = 13 | LEFT = 18 | RIGHT = 9 | MERGE = 14
   - Lista de chaves em `defaultOf`: BASE = 9 | LEFT = 13 | RIGHT = 9 | MERGE = 13
   - Entradas `contains` de console: BASE = 4 | LEFT = 4 | RIGHT = 0 | MERGE = 0
   - Fonte de `defaultSettings`: BASE = reflexão em `getDefaultProperties` | LEFT = arquivo via `PropertiesLoaderUtils` | RIGHT = reflexão | MERGE = arquivo

4. CRITÉRIO DE CONFLITO: X = valor esperado de `hasSize` / tamanho de `properties`.
   - (A) não se aplica: o valor muda em LEFT e em RIGHT em relação a BASE (18 e 9, respectivamente).
   - (B) o valor de X em LEFT (18) difere de BASE (13), e o MERGE (14) não é igual a 18, então LEFT não é preservado. O mesmo vale para RIGHT: o valor 9 difere de BASE, e o MERGE (14) não é igual a 9. Como o MERGE não preserva nenhum dos dois pais, a condição B se aplica.
   - (C) para `defaultSettings`, LEFT muda a fonte, mas o código alterado por RIGHT (remoção das entradas de console e do `hasSize`) não lê `defaultSettings`. Assim, C não é necessária para justificar o conflito, já que B já se aplica.

   Além disso, no MERGE as 13 chaves de `defaultOf` (incluindo allow_subtransactions e oltp_*) exigem entradas que a instância padrão não produz (o tamanho real é 13 e o `hasSize` esperado é 14). Isso reforça que o comportamento do teste no MERGE diverge dos dois pais.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): YES — Condição B: properties.hasSize (número esperado de propriedades) em testDefaultProperties()</summary>

1. INTENÇÃO: LEFT troca o carregamento dos defaults por um arquivo `transactions-defaults.properties`, adiciona as chaves `allow_subtransactions`, `forget_orphaned_log_entries_delay`, `oltp_max_retries` e `oltp_retry_interval`, adiciona a entrada `recovery_delay` e mantém as quatro entradas de console. RIGHT remove as quatro entradas de console e reduz o tamanho esperado. Os diffs confirmam os dois resumos.

2. ESTADO: Em `testDefaultProperties()`, os elementos afetados são:
   - `properties.hasSize(...)`, a asserção sobre o número de entradas de `asProperties()`;
   - o conjunto de chaves verificado por `defaultOf(...)`;
   - as entradas `contains(entry(...))`, incluindo as de console e `recovery_delay`;
   - `defaultSettings`, carregado por reflexão em BASE/RIGHT e do arquivo em LEFT/MERGE.

3. TABELA DE ESTADOS (sem setters no teste, então o objeto parte dos defaults):
   - hasSize: BASE = 13 | LEFT = 18 | RIGHT = 9 | MERGE = 14
   - Chaves em `defaultOf`: BASE = 9 | LEFT = 13 | RIGHT = 9 | MERGE = 13
   - Entradas de console (4): BASE = presentes | LEFT = presentes | RIGHT = removidas | MERGE = removidas
   - `recovery_delay`: BASE = ausente | LEFT = presente | RIGHT = ausente | MERGE = presente
   - Origem de `defaultSettings`: BASE = reflexão | LEFT = arquivo | RIGHT = reflexão | MERGE = arquivo

4. CRITÉRIO DE CONFLITO: X = hasSize (número esperado de propriedades).
   - (A) não se aplica: X muda em LEFT e em RIGHT, então a igualdade de BASE, LEFT e RIGHT não ocorre.
   - (B) LEFT altera X (13 → 18) e o MERGE (14) não preserva 18. RIGHT também altera X (13 → 9) e o MERGE não preserva 9. Assim, a condição B se aplica a X.
   - (C) não é necessária para a conclusão, pois B já se aplica.

   Demais elementos: as chaves de `defaultOf`, as entradas `recovery_delay` e a origem de `defaultSettings` são preservadas pelo MERGE em relação ao pai que as alterou. As entradas de console seguem RIGHT, que foi o único pai que as alterou. Não há conflito nesses elementos.

   Observação: como o código de `AtomikosProperties` não foi alterado, o número real de propriedades não deveria depender do merge. Os valores 18, 9 e 14 são, portanto, expectativas incompatíveis entre si. O MERGE ficou com 14, que corresponde às asserções presentes no próprio merge, mas não ao valor pretendido por nenhum dos lados.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): YES — Condição B: tamanho do mapa de propriedades verificado em testDefaultProperties() (hasSize)</summary>

1. INTENÇÃO: LEFT adiciona propriedades de recovery e allow_subtransactions, troca o carregamento dos defaults por um arquivo de recurso e passa a verificar essas novas chaves em testDefaultProperties(). RIGHT remove as propriedades de console e reduz as asserções correspondentes. Os resumos conferem com os diffs.

2. ESTADO: Em testDefaultProperties(), os elementos lidos e verificados são: (a) o tamanho do mapa de propriedades, verificado por hasSize(); (b) o conjunto de chaves verificado por contains(defaultOf(...)); (c) as entradas fixas verificadas por contains(entry(...)), incluindo recovery_delay e as quatro entradas de console; (d) defaultSettings, carregado por loadDefaultSettings().

3. TABELA DE ESTADOS (valores asseridos pelo teste):
   - hasSize (tamanho esperado): BASE = 13 | LEFT = 18 | RIGHT = 9 | MERGE = 14
     - LEFT: 13 chaves em defaultOf + recovery_delay + 4 de console = 18
     - RIGHT: 9 chaves em defaultOf = 9
     - MERGE: 13 chaves em defaultOf (de LEFT) + recovery_delay = 14, sem as de console (removidas por RIGHT)
   - conjunto de chaves em defaultOf: BASE = 9 | LEFT = 13 | RIGHT = 9 | MERGE = 13
   - entradas de console (WARN, tm.out, 1, -1): BASE = presentes | LEFT = presentes | RIGHT = ausentes | MERGE = ausentes
   - recovery_delay: BASE = ausente | LEFT = presente | RIGHT = ausente | MERGE = presente
   - defaultSettings: origem diferente em LEFT e MERGE (arquivo de recurso), BASE e RIGHT usam a reflexão original

4. CRITÉRIO DE CONFLITO:
   - Elemento hasSize (X = tamanho esperado do mapa):
     - (A) não se aplica: o valor muda em LEFT e em RIGHT em relação a BASE.
     - (B) se aplica: o valor em LEFT (18) difere de BASE (13), e o MERGE (14) não é igual a 18, então LEFT não é preservado. O mesmo ocorre com RIGHT (9 ≠ 13, e MERGE 14 ≠ 9).
     - (C) não é necessária, pois B já se aplica.
   - Conjunto de chaves em defaultOf (X): LEFT e MERGE têm 13 chaves; a alteração de LEFT é preservada. Sem conflito.
   - Entradas de console (X): RIGHT difere de BASE e MERGE é igual a RIGHT, então é preservado. A não se aplica, porque RIGHT difere de BASE. Sem conflito.
   - recovery_delay (X): LEFT difere de BASE e MERGE é igual a LEFT. Sem conflito.
   - defaultSettings: a origem alterada por LEFT está presente no MERGE. Sem conflito.

   O MERGE combina coerentemente as intenções, mas a condição B é aplicada literalmente aos valores da tabela: o valor final do tamanho asserido (14) não preserva o valor de nenhum dos pais alterados (18 em LEFT, 9 em RIGHT).

</details>

#### claude-sonnet-5-5: YES ✅

<details><summary>Execução 1 (<code>1.csv</code>): YES — Condição B: hasSize (tamanho esperado de properties)</summary>

1. INTENÇÃO: LEFT adiciona propriedades novas ao teste: allow_subtransactions e quatro propriedades de recovery. Com isso, o tamanho esperado em testDefaultProperties passa de 13 para 18, e o carregamento dos defaults passa a ser feito por transactions-defaults.properties. RIGHT remove as propriedades de console (log level, file name, count, limit, output dir). Com isso, o tamanho esperado em testDefaultProperties passa de 13 para 9, e as asserções sobre as entries de console são removidas.

2. ESTADO: Os elementos de estado são o resultado das asserções de testDefaultProperties (passa ou falha), o conteúdo de properties (asProperties()) e o tamanho esperado (hasSize).

3. TABELA DE ESTADOS:
   - Entrada: o teste executado sobre a classe AtomikosProperties, que no MERGE contém tanto as adições de LEFT quanto as remoções de RIGHT. Os valores abaixo supõem que a classe se comporta como em LEFT ou em RIGHT, conforme o caso.
   - Tamanho real de asProperties() com defaults:
     - BASE: 13 (9 chaves do defaultOf + 4 de console).
     - LEFT: 18 (13 + allow_subtransactions + forget_orphaned + oltp_max_retries + oltp_retry_interval + recovery_delay).
     - RIGHT: 9 (os campos de console foram removidos do teste, mas a classe ainda os produz; seu código-fonte não está no diff, então o valor real é incerto).
     - MERGE: o teste verifica 9 + 4 = 13 chaves no defaultOf/contains, mais recovery_delay, ou seja, 14 entradas, e espera hasSize(14).
   - hasSize esperado: BASE = 13 | LEFT = 18 | RIGHT = 9 | MERGE = 14.
   - Se a classe produz as 4 propriedades de console, o tamanho real no MERGE é 18 (como em LEFT), e o teste esperando 14 falha. Para o MERGE o valor esperado, 14, difere dos dois pais.

4. CRITÉRIO DE CONFLITO: X = tamanho esperado de properties (hasSize).
   - (A) não se aplica: LEFT e RIGHT diferem de BASE.
   - (B) o valor de X em LEFT (18) difere de BASE (13), e o MERGE (14) não o preserva. O mesmo vale para RIGHT (9). Ambos os pais mudam X e o MERGE não é igual a nenhum deles.
   - (C) não é necessária, pois B já se aplica.
   
   O 14 é uma combinação aritmética de duas mudanças que se justificavam pelo contexto de cada lado. A classe AtomikosProperties continua produzindo as propriedades de console (LEFT, que não as removeu, espera 18), então o MERGE se comporta de forma diferente de ambos os pais.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): YES — Condição B: properties (resultado da asserção hasSize em testDefaultProperties)</summary>

1. INTENÇÃO: LEFT adiciona propriedades novas (allow_subtransactions, forget_orphaned_log_entries_delay, recovery_delay, oltp_max_retries, oltp_retry_interval) e carrega os defaults de transactions-defaults.properties. Com isso, o tamanho esperado em testDefaultProperties passa de 13 para 18 e a asserção de recovery_delay é incluída. RIGHT remove as propriedades de console (console_log_level, output_dir, console_file_name, console_file_count, console_file_limit) do teste. O tamanho esperado em testDefaultProperties cai de 13 para 9, e a asserção das entradas de console é removida.

2. ESTADO: Em testDefaultProperties, os elementos de estado são o conjunto de propriedades retornado por this.properties.asProperties() e a asserção hasSize(N), que pode lançar AssertionError. As asserções contains também podem lançar AssertionError.

3. TABELA DE ESTADOS (entrada: AtomikosProperties com valores padrão; o teste não define nada):
   - Tamanho real de asProperties() com defaults. Em BASE, os defaults geram 13 entradas: 9 do defaultOf e 4 de console. Em LEFT, os defaults geram 18: os 13 de BASE mais 5 novas (allow_subtransactions, forget_orphaned_log_entries_delay, recovery_delay, oltp_max_retries, oltp_retry_interval). Isso é coerente com hasSize(18). Em RIGHT, a classe de produção não muda, e o teste só espera 9 entradas. O RIGHT remove as asserções de console, e a asserção de tamanho passaria a ser 9. Em MERGE, a classe de produção é a do LEFT, que tem as propriedades novas e, em tese, as de console também (os setters de console continuam existindo).
   - Valor do tamanho real no MERGE: 18 (13 + 5). A asserção do MERGE é hasSize(14). 
   - Resultado da asserção hasSize:
     - BASE: 13 == 13, passa.
     - LEFT: 18 == 18, passa.
     - RIGHT: 9 == 9, passa. Esta conta considera que RIGHT removeu as propriedades de console da classe. Se RIGHT só mexeu no teste, a asserção falharia, mas o diff de RIGHT altera apenas o teste.
     - MERGE: 14 vs. tamanho real 18, falha.
   - A ressalva sobre RIGHT: se as propriedades de console só passassem a existir quando definidas, o tamanho em RIGHT seria 9 e em LEFT 18 - 4 = 14, o que bate com o 14 do MERGE. Mas o LEFT espera 18 com as entradas de console ainda presentes, e a asserção de LEFT mantém as entradas de console. Portanto, o tamanho real no MERGE (a mesma classe de LEFT) é 18, e a asserção do MERGE (14) não bate.

4. CRITÉRIO DE CONFLITO: X = resultado da asserção hasSize / tamanho de properties.
   - (A) não se aplica: o valor difere de BASE em LEFT e RIGHT.
   - (B) O valor em LEFT (asserção passa, 18) difere de BASE, e o MERGE (asserção falha, 14 ≠ 18) não preserva esse valor.
   - (C) Não é necessária, pois B já se aplica.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): YES — Condição B: hasSize (tamanho esperado de properties) em testDefaultProperties()</summary>

1. INTENÇÃO: LEFT adiciona propriedades (allow_subtransactions e quatro propriedades de recovery) e as inclui nas asserções de testDefaultProperties(). Também passa a carregar os defaults de transactions-defaults.properties e ajusta o tamanho esperado para 18. RIGHT remove as propriedades de console (console_log_level, console_file_name, console_file_count, console_file_limit e output_dir) e as asserções delas. Em testDefaultProperties(), o tamanho esperado passa a ser 9.

2. ESTADO: Os elementos de estado são o resultado das asserções de testDefaultProperties() (sucesso ou falha) e o tamanho de properties, que é lido por hasSize(N). Há também o conjunto de entradas verificado por contains, o objeto properties retornado por asProperties() e o defaultSettings.

3. TABELA DE ESTADOS: Considere a entrada com um AtomikosProperties padrão. O número de propriedades de asProperties() em cada versão é:
   - BASE: 13 (9 propriedades de default + 4 de console), hasSize(13) passa.
   - LEFT: 18 (9 de BASE, mais allow_subtransactions, forget_orphaned, max_retries, retry_interval e recovery_delay), hasSize(18) passa. Esse número vale quando as 4 propriedades de console continuam existindo no código de produção, e LEFT também as verifica.
   - RIGHT: o teste espera 9, mas considera apenas o que RIGHT removeu do teste. O código de produção em RIGHT é o mesmo de BASE (13), então o tamanho real seria 13 e hasSize(9) falharia. Mesmo assim, a comparação relevante aqui é o valor do tamanho esperado.
   - MERGE: o teste espera hasSize(14). O código de produção em MERGE tem 18 propriedades (as de LEFT, cujo código está presente). O MERGE remove as 4 asserções de console, mas LEFT esperava 18 com console incluído. Se o console continua existindo, o tamanho real é 18 e o teste afirma 14, então o teste falha.

   Valores de hasSize: BASE = 13 | LEFT = 18 | RIGHT = 9 | MERGE = 14.

   Esse valor 14 não é igual a nenhum dos pais. Ele resulta da soma textual das modificações: 13 + 5 (LEFT) − 4 (RIGHT) = 14.

4. CRITÉRIO DE CONFLITO: X = valor esperado em hasSize / resultado da asserção.
   - (A) não se aplica: o valor de X difere de BASE em LEFT e em RIGHT.
   - (B) o valor de X em LEFT (18) difere de BASE (13), e o MERGE (14) não o preserva. O mesmo vale para RIGHT (9) em relação ao MERGE (14). Portanto B se aplica.
   - (C) não é necessária, pois B já se aplica.

</details>

#### claude-opus-5-5: NO ❌

<details><summary>Execução 1 (<code>1.csv</code>): NO</summary>

1. INTENÇÃO:
   - LEFT passa a carregar os defaults do Atomikos a partir de `transactions-defaults.properties`, em vez de usar reflexão. Também passa a verificar cinco chaves novas: `allow_subtransactions`, `forget_orphaned_log_entries_delay`, `oltp_max_retries`, `oltp_retry_interval` e `recovery_delay`. Por isso o tamanho esperado do mapa sobe de 13 para 18.
   - RIGHT remove as quatro verificações de console (`console_log_level`, `console_file_name`, `console_file_count`, `console_file_limit`) e reduz o tamanho esperado de 13 para 9.
   - O diff confirma os dois resumos.

2. ESTADO: Elementos escritos ou lidos em `testDefaultProperties()`:
   - `defaultSettings`, retornado por `loadDefaultSettings()` (alterado por LEFT).
   - `properties`, retornado por `asProperties()`.
   - O conjunto de entradas verificadas por `contains`.
   - O tamanho esperado em `hasSize`.
   - O resultado observável do teste: AssertionError lançada ou não.

3. TABELA DE ESTADOS:
   - Entrada: o `AtomikosProperties` padrão de cada versão. Em LEFT ele gera 5 chaves a mais. Em RIGHT ele deixa de gerar as 4 chaves de console.
   - `properties` (nº de entradas): BASE = 13 | LEFT = 18 | RIGHT = 9 | MERGE = 13 − 4 + 5 = 14.
   - Chaves verificadas: BASE = 9 por default + 4 de console | LEFT = BASE + 5 novas | RIGHT = BASE − 4 de console | MERGE = BASE + 5 novas − 4 de console.
   - `hasSize` esperado: BASE = 13 | LEFT = 18 | RIGHT = 9 | MERGE = 14, coerente com o mapa real do MERGE.
   - `defaultSettings`: BASE = obtido por reflexão | LEFT = lido do arquivo | RIGHT = obtido por reflexão | MERGE = lido do arquivo.
   - Resultado do teste: BASE = passa | LEFT = passa | RIGHT = passa | MERGE = passa.

4. CRITÉRIO DE CONFLITO:
   - (A) Não se aplica. Nenhum elemento é igual nos três pais e diferente no MERGE.
   - (B) Não se aplica.
     - Cada chave que LEFT passou a verificar continua verificada no MERGE com o mesmo valor esperado.
     - Cada chave que RIGHT removeu continua removida no MERGE.
     - O `defaultSettings` de LEFT é preservado.
     - O tamanho 14 não coincide com 18 nem com 9. Mas é apenas a constante esperada que reflete o mapa combinado: o mapa real do MERGE tem 14 entradas, e por isso a asserção se comporta como em cada pai, passando.
     - O resultado observável do teste (passa) é o mesmo em todos os pais e no MERGE.
   - (C) Não se aplica.
     - A troca da fonte de `defaultSettings` feita por LEFT é lida apenas por `defaultOf` para as chaves de default. RIGHT não altera essas chaves.
     - As chaves de console removidas por RIGHT não eram lidas de `defaultSettings`.
     - Portanto, nenhum código de um lado se comporta no MERGE de forma diferente de como se comporta no pai que o escreveu.

</details>

### 7. `HikariCP__1bca94af__HikariConfig#validate`

- **Target:** `validate()`
- **Esperado:** YES; **acertam:** claude-haiku-5-5; **erram:** claude-opus-5-5, claude-sonnet-5-5
- **Código:** [HikariCP__1bca94af__HikariConfig](../../data/mergedataset/HikariCP__1bca94af__HikariConfig)

**LEFT:** Left adds a new IF statement, which may write in logger calling method info

**RIGHT:** Right removes source code, which would write in logger calling method error or wanr, or even trhows an exception. Changes on formating

**Justificativa do dataset:** There is a locally observable interference as both contributions write on local variable logger.

#### claude-haiku-5-5: YES ✅

<details><summary>Execução 1 (<code>1.csv</code>): YES — Condição C: exceção lançada por validate() (controle de fluxo pelo check de acquireRetryDelay &lt; 0)</summary>

1. INTENÇÃO: LEFT adiciona, no início de validate(), após o bloco de connectionTimeout e antes da checagem de dataSource, um ramo `if (jdbcUrl != null)` que registra `logger.info` e cria `dataSource = new DriverDataSource(...)`. RIGHT remove o bloco inicial que verifica `acquireRetryDelay` (throw IllegalStateException se negativo, warn e reset se &lt; 100), e também remove o campo `acquireRetryDelay`. O resumo está correto e é confirmado pelos diffs.

2. ESTADO: Escritos ou lidos por validate() e pelos trechos alterados:
   - `dataSource` (escrito por LEFT, no ramo jdbcUrl)
   - `acquireRetryDelay` (lido e escrito pelo bloco removido por RIGHT)
   - a exceção lançada por validate() (controlada pelo check de acquireRetryDelay e pela checagem de dataSource)
   - a saída do logger (info de LEFT, error/warn removidos por RIGHT)
   - `jdbcUrl` (lido por LEFT)

3. TABELA DE ESTADOS: Entrada escolhida: `acquireRetryDelay = -1`, `jdbcUrl = "jdbc:..."`, `dataSource = null`, `dataSourceClassName = null`, demais campos com valores padrão.
   - Exceção lançada:
     - BASE: IllegalStateException("acquireRetryDelay cannot be negative.") (check inicial dispara antes do ramo jdbcUrl, que não existe em BASE)
     - LEFT: IllegalStateException("acquireRetryDelay cannot be negative.") (o check inicial ainda dispara antes do ramo jdbcUrl)
     - RIGHT: IllegalStateException("one of either dataSource or dataSourceClassName must be specified") (o check inicial foi removido; jdbcUrl é ignorado porque o ramo não existe em RIGHT)
     - MERGE: nenhuma exceção (o check inicial foi removido; o ramo jdbcUrl executa e define dataSource)
   - `dataSource`: BASE = null | LEFT = null | RIGHT = null | MERGE = DriverDataSource
   - Log: BASE = error "acquireRetryDelay cannot be negative." | LEFT = igual a BASE | RIGHT = nenhum log desse bloco e segue até a checagem de dataSource (error "one of either...") | MERGE = info "Really, a JDBC URL?..."

4. CRITÉRIO DE CONFLITO: X = exceção lançada (fluxo de controle).
   - (A) não se aplica: a exceção muda em RIGHT em relação a BASE, então não é igual nos três.
   - (B) não se aplica para LEFT: LEFT mantém a exceção de BASE. Para RIGHT, a exceção difere de BASE e MERGE é igual a RIGHT na exceção (nenhuma exceção do bloco removido), portanto RIGHT é preservado.
   - (C) aplica-se: o valor de X em RIGHT difere de BASE (o check que lançava a exceção foi removido). O código alterado por LEFT (o ramo jdbcUrl, que escreve dataSource e loga info) é controlado por X: só é alcançado quando o check inicial não lança. Em LEFT, com a entrada escolhida, o ramo não é alcançado; no MERGE ele é alcançado e se comporta de forma diferente (define dataSource, loga info, não lança). Observação: o campo `acquireRetryDelay` também é removido no MERGE, então o valor negativo deixa de ser representável; mesmo assim, para a mesma configuração de entrada (via setter em BASE/LEFT), o comportamento de jdbcUrl no MERGE difere do comportamento de LEFT, e a condição C se aplica ao controle de fluxo.
   - O logger não gera conflito: o info de LEFT e a remoção dos logs de RIGHT não se sobrescrevem.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): YES — Condição C: acquireRetryDelay</summary>

1. INTENÇÃO: LEFT adiciona, no início do bloco de `dataSource`, um ramo `if (jdbcUrl != null)` que registra `logger.info` e cria `dataSource = new DriverDataSource(...)`. O restante do bloco vira `else if`. RIGHT remove, em `validate()`, o bloco que verifica `acquireRetryDelay` (erro e lançamento de `IllegalStateException` se for negativo, aviso e reset para o padrão se for menor que 100). Também remove o campo e a constante correspondentes. O resumo de LEFT está incompleto (não menciona a alteração de `dataSource`), mas o diff confirma o que foi descrito acima.

2. ESTADO: Em `validate()`, são escritos e/ou lidos:
   - `acquireRetryDelay`: lido na checagem `< 0`, escrito pelo reset `= ACQUIRE_RETRY_DELAY` (BASE). RIGHT remove essa leitura e essa escrita.
   - `dataSource`: escrito por LEFT (`new DriverDataSource`) e lido pela checagem de `dataSource == null`.
   - `logger` (saída de log): LEFT acrescenta `info`; RIGHT remove `error`/`warn` do bloco de `acquireRetryDelay`.
   - Exceção lançada: `IllegalStateException` de `acquireRetryDelay`, e de `dataSource`/`dataSourceClassName` (checagem alterada por LEFT).

3. TABELA DE ESTADOS (entrada concreta: `acquireRetryDelay = -1`, `jdbcUrl = "jdbc:x"`, `dataSource = null`, `dataSourceClassName = null`):
   - Exceção lançada por validate():
     - BASE: `IllegalStateException("acquireRetryDelay cannot be negative.")`
     - LEFT: a mesma (a checagem de `acquireRetryDelay` ainda vem antes do ramo de `jdbcUrl`, que não é alcançado)
     - RIGHT: `IllegalStateException("one of either dataSource or dataSourceClassName must be specified")`
     - MERGE: nenhuma exceção (o ramo de `jdbcUrl` é executado)
   - `dataSource`:
     - BASE: null | LEFT: null | RIGHT: null | MERGE: `DriverDataSource`
   - Saída de log `info` ("Really, a JDBC URL?..."):
     - BASE: ausente | LEFT: presente | RIGHT: ausente | MERGE: presente

4. CRITÉRIO DE CONFLITO: X = `acquireRetryDelay` (a checagem que controla o fluxo, incluindo a exceção que ela lança).
   - (A) não se aplica: o valor de X em RIGHT difere de BASE (a checagem foi removida).
   - (B) não se aplica ao próprio X: o MERGE tem a checagem ausente, como RIGHT, então preserva RIGHT. LEFT não alterou X, então seu valor é igual ao de BASE.
   - (C) se aplica: em BASE e em LEFT, o código alterado por LEFT (o ramo `if (jdbcUrl != null)` e a cadeia `else if` que trata `dataSource`) é controlado por X, porque a checagem `acquireRetryDelay < 0` lança a exceção antes de chegar a esse código. RIGHT altera X (remove a checagem). No MERGE, esse código passa a executar mesmo com `acquireRetryDelay` negativo. Para a entrada A, LEFT lança a exceção de `acquireRetryDelay` e não configura `dataSource`, enquanto o MERGE não lança e configura `dataSource`. O comportamento desse código diverge do que LEFT produziu.

   Para os demais elementos:
   - `dataSource`: escrito só por LEFT, e o MERGE o preserva (igual a LEFT). RIGHT não lê nem escreve `dataSource` em `validate()`, então (C) não se aplica.
   - Logger: LEFT adiciona `info` e o MERGE o preserva. RIGHT remove `warn`/`error` e o MERGE também não os tem, então ambos os pais são preservados. Nenhum código de um lado lê a saída de log do outro.

   Como (C) se aplica a `acquireRetryDelay`, o merge introduz um conflito semântico. Não descarto a condição pela intenção de RIGHT (aposentar a checagem).

</details>

<details><summary>Execução 3 (<code>3.csv</code>): YES — Condição C: exceção lançada por validate() (IllegalStateException de acquireRetryDelay negativo), que controla a execução do novo bloco jdbcUrl de LEFT</summary>

1. INTENÇÃO: LEFT adiciona, em validate(), um bloco `if (jdbcUrl != null)` que cria `dataSource = new DriverDataSource(...)` e registra um log `info`. Esse bloco substitui a condição `dataSource == null && dataSourceClassName == null` por um `else if`. RIGHT remove a validação de `acquireRetryDelay` (o `throw` de valor negativo, o `warn` e a reatribuição para o padrão) e remove o campo, porque a propriedade foi aposentada. Os diffs confirmam os resumos.

2. ESTADO: Elementos escritos ou lidos por validate() e pelos trechos alterados:
   - `dataSource` (escrito por LEFT);
   - a exceção lançada por validate() (IllegalStateException de `acquireRetryDelay < 0`, removida por RIGHT);
   - o campo `acquireRetryDelay` (lido e reatribuído pelo bloco removido por RIGHT);
   - a saída do logger (mensagens `error`/`warn` removidas por RIGHT e `info` adicionado por LEFT).

3. TABELA DE ESTADOS: Entrada: `acquireRetryDelay = -1`, `jdbcUrl = "jdbc:x"`, `dataSource = null`, `dataSourceClassName = null`.
   - exceção lançada: BASE = IllegalStateException("acquireRetryDelay cannot be negative.") | LEFT = a mesma exceção | RIGHT = nenhuma (o bloco foi removido) | MERGE = nenhuma.
   - dataSource após validate(): BASE = null (a validação lança antes) | LEFT = DriverDataSource | RIGHT = null (BASE sem a parte de jdbcUrl, a checagem lança IllegalStateException de dataSource) | MERGE = DriverDataSource.
   - log: BASE = error("acquireRetryDelay cannot be negative.") | LEFT = error(...) | RIGHT = nenhum | MERGE = info("Really, a JDBC URL?...") (o bloco de jdbcUrl é executado).
   - acquireRetryDelay: BASE = -1 (lança antes de qualquer reatribuição) | LEFT = -1 | RIGHT = campo removido | MERGE = campo removido.

4. CRITÉRIO DE CONFLITO:
   - X = `dataSource`: (A) não se aplica, pois o valor muda em LEFT. (B) o valor de LEFT é DriverDataSource, e o MERGE é igual a ele, então é preservado. Não há conflito nesse elemento.
   - X = `acquireRetryDelay`: (B) o valor de RIGHT é "campo removido", e o MERGE também não tem campo, então é preservado. Não há conflito.
   - X = exceção lançada: não é alterada por LEFT, mas RIGHT a remove. O código de LEFT (o bloco `if (jdbcUrl != null)`) é controlado por essa exceção: em LEFT, com `acquireRetryDelay < 0`, esse bloco não é executado. No MERGE, a exceção não existe mais, então o bloco é executado nesse caso. O comportamento de LEFT no MERGE difere do comportamento no pai que o escreveu. Isso é uma dependência de controle, a condição (C). Observação: pelos setters da BASE, esse valor negativo só seria atingido por reflexão ou `copyState`, mas o critério pede que a condição seja avaliada sobre os valores, sem descartá-la pela intenção de aposentar a propriedade.
   - X = saída do logger: o `info` de LEFT não lê nem é controlado pelo `error`/`warn` removido por RIGHT. Não há conflito por essa via, mas a condição C para a exceção já se aplica.

   Conclusão: a condição C se aplica à exceção lançada por validate().

</details>

#### claude-opus-5-5: NO ❌

<details><summary>Execução 1 (<code>1.csv</code>): NO</summary>

1. INTENÇÃO:
   - **LEFT**: em `validate()`, adiciona um novo ramo `if (jdbcUrl != null)` antes da verificação de `dataSource`/`dataSourceClassName`. Esse ramo registra `logger.info("Really, a JDBC URL? ...")` e atribui `dataSource = new DriverDataSource(jdbcUrl, dataSourceProperties)`. Fora de `validate()`, LEFT acrescenta campos novos (`jdbcUrl`, `isReadOnly`, `isIsolateInternalQueries`), getters/setters, `setDriverClassName` e javadocs.
   - **RIGHT**: remove o campo `acquireRetryDelay` e a constante `ACQUIRE_RETRY_DELAY`. Em `validate()`, apaga o bloco inicial que validava `acquireRetryDelay`; esse bloco registrava error e lançava `IllegalStateException`, ou registrava warn e restaurava o valor padrão. Os setters `setAcquireIncrement`/`setAcquireRetryDelay` passam a apenas emitir um warn de "retired", e os getters retornam 0.
   - O diff confirma os resumos.

2. ESTADO (em `validate()` e nos trechos alterados):
   - campo `dataSource`, escrito pelo ramo de LEFT;
   - exceção lançada por `validate()`;
   - saída do logger (info, warn, error);
   - campo `acquireRetryDelay`: existe apenas em BASE e LEFT e é escrito pelo bloco que RIGHT remove.
   - Os campos lidos por LEFT são `jdbcUrl` e `dataSourceProperties`. RIGHT não lê nem escreve nenhum deles.

3. TABELA DE ESTADOS:
   - Entrada: configuração padrão (`acquireRetryDelay` = 750 onde existe), `jdbcUrl = "jdbc:h2:mem:x"`, `dataSource = null`, `dataSourceClassName = null`, demais valores válidos.
   - Bloco de `acquireRetryDelay`:
     - BASE e LEFT: 750 não é &lt; 0 nem &lt; 100, então não há log nem alteração.
     - RIGHT e MERGE: o bloco não existe.
     - Efeito nulo nos quatro.
   - `dataSource`: BASE = null | LEFT = DriverDataSource(url) | RIGHT = null | MERGE = DriverDataSource(url)
   - Exceção: BASE = IllegalStateException("one of either dataSource...") | LEFT = nenhuma | RIGHT = IllegalStateException("one of either dataSource...") | MERGE = nenhuma
   - Log: BASE = [error "one of either..."] | LEFT = [info "Really, a JDBC URL?..."] | RIGHT = [error "one of either..."] | MERGE = [info "Really, a JDBC URL?..."]
   - Entrada alternativa: `acquireRetryDelay` = 50.
     - Só é configurável em BASE e LEFT. Em RIGHT e MERGE o setter apenas emite o warn de "retired", e `validate()` não faz nada com esse valor.
     - Nesse aspecto, o comportamento do MERGE coincide com o de RIGHT, e o ramo de LEFT não depende dele.

4. CRITÉRIO DE CONFLITO:
   - **(A)** Não se aplica. Nenhum elemento é igual em BASE, LEFT e RIGHT e diferente no MERGE.
   - **(B)** Não se aplica. `dataSource`, exceção e log diferem de BASE em LEFT, e o MERGE é igual a LEFT. Em RIGHT, esses valores são iguais a BASE nesta entrada. O comportamento ligado a `acquireRetryDelay` (remoção da validação) diferente de BASE em RIGHT é preservado no MERGE.
   - **(C)** Não se aplica. O ramo de LEFT lê apenas `jdbcUrl` e `dataSourceProperties`, que RIGHT não altera. O código removido por RIGHT só tratava `acquireRetryDelay`, que LEFT não lê nem escreve. Não há dependência de dados ou de controle entre as mudanças.

</details>

#### claude-sonnet-5-5: NO ❌

<details><summary>Execução 1 (<code>1.csv</code>): NO</summary>

1. INTENÇÃO: LEFT adiciona suporte a jdbcUrl em validate(). Se jdbcUrl != null, registra um info e atribui dataSource = new DriverDataSource(...). O if original passa a ser um else if. RIGHT remove a validação de acquireRetryDelay em validate() (error, warn, exceção e atribuição) e aposenta as propriedades acquireIncrement e acquireRetryDelay. Os dois diffs confirmam os resumos.

2. ESTADO: Em validate(), os elementos de estado são:
   - dataSource, escrito por LEFT;
   - logger (saídas info, warn e error);
   - exceções lançadas;
   - acquireRetryDelay, escrito em BASE e removido por RIGHT;
   - connectionTimeout, idleTimeout, maxLifetime e outros campos, que nenhum dos lados altera.

3. TABELA DE ESTADOS:
   - Entrada A: jdbcUrl = "jdbc:x", dataSource = null, dataSourceClassName = null.
     - dataSource: BASE = null (lança IllegalStateException) | LEFT = DriverDataSource | RIGHT = null (lança exceção) | MERGE = DriverDataSource.
     - Log: BASE = error | LEFT = info | RIGHT = error | MERGE = info.
   - Entrada B: acquireRetryDelay = -1.
     - BASE: lança IllegalStateException("acquireRetryDelay cannot be negative.") | LEFT: igual a BASE | RIGHT: sem exceção por esse motivo | MERGE: sem exceção por esse motivo.
     - Com o campo removido, o valor é sempre 0 e o check não existe mais.
   - Entrada C: dataSource = null, dataSourceClassName = null, jdbcUrl = null.
     - Todas as versões lançam a mesma exceção.

4. CRITÉRIO DE CONFLITO:
   - (A) Não se aplica. Os valores mudam em MERGE apenas onde LEFT ou RIGHT já mudaram.
   - (B) Em cada elemento, o MERGE iguala o pai que o alterou. Na entrada A, dataSource e o log são iguais a LEFT. Na entrada B, a exceção é igual a RIGHT.
   - (C) O código de LEFT lê jdbcUrl, dataSource, dataSourceClassName e dataSourceProperties. RIGHT não escreve nenhum desses campos. O código removido por RIGHT (acquireRetryDelay) não é lido nem controlado por nada que LEFT escreve. Os dois conjuntos de mudanças são independentes e se comportam no MERGE como nos pais que os escreveram.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): NO</summary>

1. INTENÇÃO: LEFT adiciona o suporte a jdbcUrl em validate(). Se jdbcUrl != null, registra um log info e atribui dataSource = new DriverDataSource(jdbcUrl, dataSourceProperties). O antigo if (dataSource == null && dataSourceClassName == null) vira else if. RIGHT remove de validate() o bloco que checava acquireRetryDelay (log de erro, exceção e reatribuição) e aposenta a propriedade, além de mudar formatação. Os diffs confirmam os resumos.

2. ESTADO: Os elementos escritos ou lidos nos trechos alterados de validate() são:
   - o campo dataSource, escrito por LEFT;
   - a saída do logger (info, warn, error);
   - a exceção lançada;
   - o campo acquireRetryDelay, escrito e lido pelo bloco removido por RIGHT.

3. TABELA DE ESTADOS:
   - Entrada 1: acquireRetryDelay = -5, jdbcUrl = null, dataSource e dataSourceClassName informados.
     - exceção: BASE = IllegalStateException("acquireRetryDelay cannot be negative.") | LEFT = igual a BASE | RIGHT = nenhuma (o bloco foi removido) | MERGE = nenhuma.
     - O MERGE é igual a RIGHT, então preserva RIGHT.
   - Entrada 2: jdbcUrl = "jdbc:x", dataSource = null, dataSourceClassName = null.
     - dataSource: BASE = null (lança IllegalStateException) | LEFT = DriverDataSource | RIGHT = null (lança IllegalStateException) | MERGE = DriverDataSource.
     - O MERGE é igual a LEFT, e nenhum código alterado por RIGHT lê dataSource.
   - Entrada 3: jdbcUrl != null, dataSource e dataSourceClassName informados.
     - logger: BASE = warn "both ... ignoring" | LEFT = info, sem warn | RIGHT = igual a BASE | MERGE = info, sem warn.
     - O MERGE é igual a LEFT.
   - Entrada 4: acquireRetryDelay = 50.
     - acquireRetryDelay: BASE = 750 | LEFT = 750 | RIGHT = campo removido | MERGE = campo removido.
     - O MERGE é igual a RIGHT.

4. CRITÉRIO DE CONFLITO:
   - (A) não se aplica: nenhum valor muda no MERGE sem ter mudado em LEFT ou RIGHT.
   - (B) para cada elemento, o MERGE é igual ao pai que o alterou (LEFT para dataSource e logger; RIGHT para exceção e acquireRetryDelay).
   - (C) o código de LEFT lê jdbcUrl, dataSourceProperties, dataSource e dataSourceClassName. RIGHT não escreve nenhum deles. O bloco removido por RIGHT dependia apenas de acquireRetryDelay, que LEFT não toca. Portanto o código alterado por cada lado se comporta no MERGE como se comporta no pai que o escreveu.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): NO</summary>

1. INTENÇÃO: LEFT adiciona suporte a jdbcUrl em validate(). Se jdbcUrl != null, registra um info no logger e atribui dataSource = new DriverDataSource(jdbcUrl, dataSourceProperties). O if original passa a ser um else if. RIGHT remove o campo acquireRetryDelay e o bloco de validação correspondente em validate(), que registrava error/warn ou lançava IllegalStateException. As demais mudanças de RIGHT são de formatação ou aposentadoria de propriedades. Os diffs confirmam os resumos.

2. ESTADO: Em validate() e nos trechos alterados, os elementos de estado são:
   - a saída do logger (info, warn, error);
   - a exceção lançada;
   - o campo dataSource;
   - o campo acquireRetryDelay (removido em RIGHT);
   - o campo transactionIsolation.

3. TABELA DE ESTADOS:
   - Entrada 1: acquireRetryDelay = -1, jdbcUrl = null, dataSource e dataSourceClassName definidos.
     - Exceção: BASE = IllegalStateException("acquireRetryDelay cannot be negative.") | LEFT = igual a BASE | RIGHT = nenhuma (o campo não existe) | MERGE = nenhuma.
     - Esta diferença vem apenas da remoção feita por RIGHT, e o MERGE é igual a RIGHT.
   - Entrada 2: jdbcUrl = "jdbc:x", dataSource = null, dataSourceClassName = null.
     - dataSource: BASE = null (e lança IllegalStateException) | LEFT = DriverDataSource | RIGHT = null (lança exceção) | MERGE = DriverDataSource.
     - log: BASE = error | LEFT = info | RIGHT = error | MERGE = info.
     - Nesta entrada, o MERGE é igual a LEFT, e as mudanças de RIGHT não interferem.
   - Entrada 3: acquireRetryDelay = 50, que em BASE seria resetado para 750 com um warn.
     - Em LEFT esse comportamento é preservado.
     - Em RIGHT e no MERGE, o campo e a validação foram removidos.

4. CRITÉRIO DE CONFLITO:
   - (A) não se aplica: nenhum valor é igual em BASE, LEFT e RIGHT e diferente no MERGE.
   - (B) Para o valor de X em LEFT, o MERGE preserva o comportamento de LEFT nas partes que LEFT alterou (o ramo jdbcUrl). A validação de acquireRetryDelay, que existe em LEFT e é removida em RIGHT, é uma remoção intencional de RIGHT, e o MERGE segue RIGHT. Nenhum X observável é perdido de forma inesperada.
   - (C) O código adicionado por LEFT (ramo jdbcUrl) lê jdbcUrl, dataSourceProperties e dataSource, e não lê acquireRetryDelay nem depende do bloco removido por RIGHT. O código removido por RIGHT não escreve em nada que LEFT leia. As alterações são independentes.

</details>

### 8. `elasticsearch__d8968869__TransportReplicationAction#doRun`

- **Target:** `doRun()`
- **Esperado:** YES; **acertam:** claude-haiku-5-5; **erram:** claude-opus-5-5, claude-sonnet-5-5
- **Código:** [elasticsearch__d8968869__TransportReplicationAction](../../data/mergedataset/elasticsearch__d8968869__TransportReplicationAction)

**LEFT:** Left creates a new local variable, and assigns a value to it depending on a try, which was also changed by Left.

**RIGHT:** Right adds a new local variable and assings a value to it inside a try, which was chaged by Left.

**Justificativa do dataset:** Considering the changes performed by the integrator, it adds a parameter on the method call result.response. There is no interference, DF, CF, OA based on the parent contributions. In the base commit, there is write on the log object; in the right commit, no write is performed; in the merge commit, an exception can be thrown on class IndexShard.acquireReplicaOperationLock because of the changes from integrator.

#### claude-haiku-5-5: YES ✅

<details><summary>Execução 1 (<code>1.csv</code>): YES — Condição C: resposta enviada ao canal (channel.sendResponse) em AsyncReplicaAction.doRun()/ResponseListener.onResponse()</summary>

1. INTENÇÃO: O resumo afirma que LEFT cria uma variável local e a atribui dentro de um try que também foi alterado por LEFT, e que RIGHT adiciona uma variável local atribuída dentro de um try alterado por LEFT. Os diffs mostram outra coisa:
   - LEFT troca o lock de réplica por um `ShardReference`, faz `shardOperationOnReplica` dentro do try, cria `final ReplicaResponse response` com o allocationId e o checkpoint local, e envia `response` ao canal. Também altera `ReplicasProxy` para `ReplicaResponse::new`.
   - RIGHT troca o tipo de retorno de `shardOperationOnPrimary` e `shardOperationOnReplica` para `PrimaryResult` e `ReplicaResult`. Em `doRun`, guarda `result = shardOperationOnReplica(request)` dentro do try com o lock, chama `result.respond(new ResponseListener())` fora do try, e `ResponseListener.onResponse(Empty response)` envia esse `response` ao canal. Ou seja, RIGHT envia `Empty`, sem variável local nova dentro do try.
   O resumo não descreve com precisão o que os diffs fazem. Confio nos diffs.

2. ESTADO: Target = `AsyncReplicaAction.doRun()`. Os elementos de estado escritos pelo target e pelos trechos alterados são:
   - a resposta enviada ao canal (`channel.sendResponse`), escrita por `doRun` (BASE e LEFT) ou por `ResponseListener.onResponse` (RIGHT e MERGE);
   - a variável local `response` (LEFT) / `replicaResponse` (MERGE), que vem de `ReplicaResponse`;
   - a variável local `result` (RIGHT e MERGE), que é o `ReplicaResult` retornado por `shardOperationOnReplica`;
   - o lock/`ShardReference` e a fase da tarefa (`setPhase`).

3. TABELA DE ESTADOS: Entrada: uma réplica local com allocationId = "a1", localCheckpoint = 5, e `shardOperationOnReplica` retornando o `ReplicaResult` padrão.
   - Resposta enviada ao canal: BASE = `TransportResponse.Empty` | LEFT = `ReplicaResponse("a1", 5)` | RIGHT = `TransportResponse.Empty` | MERGE = `ReplicaResponse("a1", 5)`
   - Valor usado por `ResponseListener.onResponse` (parâmetro recebido de `result.respond`): BASE = não existe | LEFT = não existe | RIGHT = `Empty` (encaminhado ao canal) | MERGE = ignorado; o canal recebe `replicaResponse`
   - Fase da tarefa: BASE = "finished" | LEFT = "finished" | RIGHT = "finished" | MERGE = "finished"

4. CRITÉRIO DE CONFLITO: X = resposta enviada ao canal.
   - (A) não se aplica: X muda em LEFT, então o valor não é igual nos três pais.
   - (B) LEFT altera X (`ReplicaResponse` ≠ `Empty`), e o MERGE preserva esse valor (`ReplicaResponse`). RIGHT não altera X (ambos são `Empty`), então a condição não se aplica a RIGHT. Para LEFT, não há violação.
   - (C) X difere de BASE em LEFT. O código alterado por RIGHT (`ResponseListener.onResponse`) lê o parâmetro `response` e o encaminha ao canal. No MERGE, esse código passou a ignorar o parâmetro e envia `replicaResponse`. Assim, o código de RIGHT se comporta de forma diferente do que se comportava em RIGHT: o `ReplicaResult.respond(...)` da subclasse, que é o ponto de extensão introduzido por RIGHT, deixa de ser usado para decidir o que é enviado ao primário. Essa é uma interferência de fluxo de dados entre as modificações.
   - Observação fora da análise semântica: o MERGE remove `import org.elasticsearch.action.ReplicationResponse`, mas essa classe ainda é usada (`Response extends ReplicationResponse`, `ReplicationResponse.ShardInfo`). Isso causa erro de compilação. Também há um javadoc quebrado em `{@link #getReplicaShardReference(ShardId, long)} (ShardId, long)}`.

   Conclusão: a condição C se aplica.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): YES — Condição C: payload enviado ao canal (response / ReplicaResponse) em AsyncReplicaAction.doRun()</summary>

**Alvo:** o `doRun()` de `AsyncReplicaAction`, a classe interna que trata a operação na réplica. Há outros `doRun()` no arquivo, mas os diffs alteram este.

1. **INTENÇÃO:**
   - LEFT: captura a resposta da réplica (`ReplicaResponse` com allocationId e checkpoint local) dentro do bloco try, usando `getReplicaShardReference`, e envia essa resposta ao primário no lugar de `TransportResponse.Empty`. O resumo confere com o diff.
   - RIGHT: torna `shardOperationOnReplica` síncrono com retorno `ReplicaResult`, libera o lock antes do envio e envia a resposta pelo `ResponseListener`, que devolve `TransportResponse.Empty`. O resumo é incompleto: RIGHT também cria a classe `ResponseListener` e altera a assinatura de `shardOperationOnReplica`. O conteúdo do diff prevalece.

2. **ESTADO:** a resposta enviada ao canal (`channel.sendResponse(...)`), escrita por `doRun()` e pelo `ResponseListener`. Também o lock/referência da réplica (`ShardReference`), o `result` e o `response`.

3. **TABELA DE ESTADOS:** entrada concreta: réplica com allocationId `"A"`, localCheckpoint `5`, `shardOperationOnReplica` concluindo sem exceção.
   - Payload enviado ao primário (`channel.sendResponse`):
     - BASE: `TransportResponse.Empty.INSTANCE`
     - LEFT: `ReplicaResponse("A", 5)`
     - RIGHT: `TransportResponse.Empty.INSTANCE` (o `onResponse` de `ResponseListener` envia o parâmetro `response`, que vem de `ReplicaResult.respond`, com `Empty.INSTANCE`)
     - MERGE: `ReplicaResponse("A", 5)`
   - Trecho de RIGHT no MERGE: o `onResponse` de `ResponseListener` passa a enviar `replicaResponse`, um campo novo do construtor, e não o parâmetro `response` de RIGHT. Essa substituição não está em nenhum dos dois diffs; foi feita pelo merge sobre o código de RIGHT.
   - Lock/referência da réplica: aberto e fechado no mesmo escopo nos três casos, com `replica.routingEntry()` e `getLocalCheckpoint()` lidos antes do fechamento. Não há divergência.

4. **CRITÉRIO DE CONFLITO:** X = payload enviado ao canal.
   - (A) não se aplica: X muda em LEFT (`ReplicaResponse` ≠ `Empty`), então não é igual nos três pais.
   - (B) não se aplica ao valor de RIGHT: o valor de X em RIGHT (`Empty`) é igual ao de BASE. O valor de LEFT (`ReplicaResponse("A",5)`) é preservado no MERGE.
   - (C) se aplica: X difere de BASE em LEFT. O código adicionado por RIGHT (`ResponseListener.onResponse`) é controlado por X no MERGE: ele envia `replicaResponse`, o objeto criado por LEFT, e não o `Empty` que RIGHT envia. Assim, esse código se comporta no MERGE de forma diferente do que RIGHT escreveu. A intenção de RIGHT não foi preservada nesse trecho, e a regra não permite descartar a condição pela intenção de LEFT.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): YES — Condição C: resposta enviada ao canal (channel.sendResponse) em AsyncReplicaAction.doRun()/ResponseListener.onResponse</summary>

1. INTENÇÃO: LEFT faz o replica enviar de volta uma `ReplicaResponse` com `allocationId` e `localCheckpoint`, criada dentro do lock e enviada por `channel.sendResponse(response)`. RIGHT não altera o valor enviado: encapsula `shardOperationOnReplica` em `ReplicaResult`, chama `result.respond(new ResponseListener())` depois de liberar o lock, e o listener envia `TransportResponse.Empty`. Os diffs confirmam os dois resumos.

2. ESTADO: O objeto enviado pelo canal de resposta (`channel.sendResponse`), escrito em `doRun()` e no `onResponse` do `ResponseListener`. Também participam o campo `ResponseListener.replicaResponse` (presente só no MERGE) e o objeto `Empty` passado por `ReplicaResult.respond()`.

3. TABELA DE ESTADOS:
   - Entrada: request com shardId válido, allocationId da réplica = "A1", localCheckpoint = 7, `shardOperationOnReplica` concluindo sem exceção.
   - Resposta enviada ao canal (X):
     - BASE: `TransportResponse.Empty.INSTANCE`
     - LEFT: `ReplicaResponse("A1", 7)`
     - RIGHT: `TransportResponse.Empty.INSTANCE`
     - MERGE: `ReplicaResponse("A1", 7)`
   - Em MERGE, `doRun()` cria `response = new ReplicaResponse("A1", 7)` dentro do try e chama `result.respond(new ResponseListener(response))`. Em `ResponseListener.onResponse(Empty response)`, o parâmetro `response` é ignorado e o método envia `replicaResponse`. Em RIGHT, o mesmo método enviaria o parâmetro `Empty`.

4. CRITÉRIO DE CONFLITO: X = resposta enviada ao canal.
   - (A) não se aplica: X muda em LEFT (de Empty para ReplicaResponse), então os três valores de BASE, LEFT e RIGHT não são iguais.
   - (B) não se aplica: X em LEFT difere de BASE, mas MERGE é igual a LEFT (`ReplicaResponse("A1", 7)`), então LEFT é preservado. RIGHT não difere de BASE, então a condição não se aplica a ele.
   - (C) se aplica: X em LEFT difere de BASE. O código alterado por RIGHT, o `ResponseListener.onResponse` que chama `channel.sendResponse`, lê X no MERGE, porque envia o campo `replicaResponse` vindo de LEFT. Em RIGHT, esse mesmo código envia o `Empty` que recebe por parâmetro. Assim, o código de RIGHT passa a se comportar de forma diferente do que foi escrito: o objeto recebido por `onResponse` é descartado, e o valor enviado depende do valor produzido por LEFT. O LEFT, por sua vez, obtém o resultado que queria, mas ao custo de quebrar o contrato que RIGHT estabeleceu em `ReplicaResult.respond()`.

</details>

#### claude-opus-5-5: NO ❌

<details><summary>Execução 1 (<code>1.csv</code>): NO</summary>

1. INTENÇÃO:
   - **LEFT:** Em `doRun()`, troca `acquireReplicaOperationLock` por `getReplicaShardReference`, que devolve um `ShardReference`. Dentro do `try` cria a variável local `final ReplicaResponse response` com o `allocationId` e o `localCheckpoint` da réplica. Ao final envia `response` pelo canal em vez de `TransportResponse.Empty.INSTANCE`.
   - **RIGHT:** `shardOperationOnReplica` passa a retornar um `ReplicaResult`, guardado na nova variável local `result` dentro do `try`. Depois do `try`, chama `result.respond(new ResponseListener())`. O `ResponseListener.onResponse(Empty)` registra o trace, faz `setPhase(task, "finished")` e envia o `Empty` recebido. Em caso de falha, chama `responseWithFailure`.
   - Os diffs confirmam os resumos.

2. ESTADO: Elementos escritos por `doRun()` e pelos trechos alterados:
   - variável local `response` (LEFT/MERGE);
   - variável local `result` (RIGHT/MERGE);
   - fase do `task` ("replica" e depois "finished");
   - lock de operação da réplica (adquirido e liberado);
   - mensagem enviada por `channel.sendResponse(...)`;
   - exceção eventualmente propagada.

3. TABELA DE ESTADOS:
   - Entrada: request válido para o shard réplica com `allocationId = "a1"` e `localCheckpoint = 5`. A operação na réplica termina sem erro, e `ReplicaResult.respond` é o padrão (chama `onResponse(Empty.INSTANCE)`).
   - **lock da réplica:** BASE = adquirido e liberado após a operação | LEFT = igual | RIGHT = igual | MERGE = igual. O `ShardReference.close()` libera o mesmo lock.
   - **response:** BASE = inexistente | LEFT = ReplicaResponse("a1", 5) | RIGHT = inexistente | MERGE = ReplicaResponse("a1", 5).
   - **result:** BASE = inexistente | LEFT = inexistente | RIGHT = ReplicaResult padrão | MERGE = ReplicaResult padrão.
   - **fase do task:** BASE = "replica" → "finished" | LEFT = igual | RIGHT = igual (definida dentro do listener) | MERGE = igual (definida dentro do listener).
   - **mensagem enviada no canal:** BASE = Empty.INSTANCE | LEFT = ReplicaResponse("a1", 5) | RIGHT = Empty.INSTANCE | MERGE = ReplicaResponse("a1", 5).
   - **exceção:** se `shardOperationOnReplica` lançar, BASE, LEFT, RIGHT e MERGE propagam a mesma exceção, com o lock liberado. Se o envio falhar, RIGHT e MERGE chamam `responseWithFailure`.

4. CRITÉRIO DE CONFLITO:
   - **(A)** Não se aplica. Fase do task, lock e exceção são iguais em BASE, LEFT, RIGHT e MERGE. A mensagem enviada muda no MERGE, mas também mudou em LEFT.
   - **(B)** A mensagem enviada em LEFT (ReplicaResponse("a1", 5)) difere de BASE, e o MERGE produz o mesmo valor, então preserva LEFT. A variável `result` de RIGHT é preservada no MERGE. A mensagem de RIGHT é igual à de BASE, então não há exigência sobre ela. O `localCheckpoint` é lido no mesmo ponto em LEFT e em MERGE: depois de `shardOperationOnReplica` e antes da liberação do lock. Por isso o valor é o mesmo.
   - **(C)** O código de RIGHT (`ResponseListener`, `setPhase`, envio) não lê nenhum valor escrito por LEFT de forma divergente. O MERGE apenas repassa `response` ao listener, que o envia no lugar do `Empty`, exatamente como LEFT enviaria. O código de LEFT (`response`) não depende de `result`. A fase e o momento de envio seguem o comportamento de RIGHT, que é equivalente ao de LEFT para a entrada considerada.

</details>

#### claude-sonnet-5-5: NO ❌

<details><summary>Execução 1 (<code>1.csv</code>): NO</summary>

1. INTENÇÃO: O alvo é AsyncReplicaAction.doRun().
   - LEFT obtém uma ShardReference da réplica (getReplicaShardReference). Dentro do try, após shardOperationOnReplica(request), cria um ReplicaResponse com allocationId e localCheckpoint. No final, envia esse response ao primário em vez de Empty.
   - RIGHT faz shardOperationOnReplica retornar um ReplicaResult. Dentro do try, guarda o resultado em `result`. Após o try, chama result.respond(new ResponseListener()). O ResponseListener envia Empty via channel.sendResponse(response) e faz o trace e o setPhase "finished".
   - O MERGE combina os dois. Dentro do try, calcula result e response (ReplicaResponse). Depois chama result.respond(new ResponseListener(response)). O listener envia replicaResponse.

2. ESTADO:
   - O valor enviado por channel.sendResponse (a resposta ao primário).
   - As variáveis locais result e response.
   - O trace e o setPhase "finished".

3. TABELA DE ESTADOS (réplica com sucesso, allocationId "a1", checkpoint 5):
   - Resposta enviada: BASE = Empty | LEFT = ReplicaResponse(a1, 5) | RIGHT = Empty (via result.respond) | MERGE = ReplicaResponse(a1, 5), enviada via result.respond.
   - Fase final: BASE = finished | LEFT = finished | RIGHT = finished | MERGE = finished.
   - Trace: igual nos quatro casos.

   Em RIGHT, ReplicaResult.respond chama listener.onResponse(Empty). No MERGE, o ResponseListener ignora o Empty recebido e usa replicaResponse, que foi calculado dentro do try, antes de respond. O MERGE integrou os dois lados de forma consistente.

   Caso de subclasse que sobrescreve ReplicaResult.respond: o listener é chamado com Empty. O MERGE envia replicaResponse, que preserva a intenção de LEFT (enviar o ReplicaResponse). O ciclo de resposta de RIGHT (via respond e listener) também é preservado.

4. CRITÉRIO DE CONFLITO: X = resposta enviada ao primário.
   - (A) não se aplica: o valor em LEFT difere de BASE.
   - (B) o valor em LEFT (ReplicaResponse) difere de BASE, e o MERGE é igual a ele. RIGHT (Empty) difere de LEFT, mas no valor da resposta RIGHT é igual a BASE, então o MERGE só precisa preservar LEFT, e preserva.
   - (C) o código de RIGHT (listener) não lê um valor de X que se comporte de forma diferente. O response de LEFT é passado explicitamente ao listener e a ordem é correta. A chamada a replica.routingEntry() ocorre dentro do try, antes do close, como em LEFT. Nenhuma dependência é quebrada.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): NO</summary>

1. INTENÇÃO: O alvo é AsyncReplicaAction.doRun().
   - LEFT troca o lock da réplica por um ShardReference. Dentro do try, cria `response = new ReplicaResponse(allocationId, localCheckpoint)` e envia essa resposta pelo canal, no lugar de Empty.
   - RIGHT faz shardOperationOnReplica retornar um ReplicaResult. Ele é obtido dentro do try, e depois do try chama `result.respond(new ResponseListener())`. O ResponseListener registra o log, define a fase "finished" e envia `Empty.INSTANCE` pelo canal.
   - O MERGE combina os dois. Dentro do try-with-resources com ShardReference, faz `result = shardOperationOnReplica(request)` e `response = new ReplicaResponse(...)`. Depois chama `result.respond(new ResponseListener(response))`, e o listener envia `replicaResponse`.

2. ESTADO: Os elementos escritos são:
   - a variável local `response`;
   - a variável local `result`;
   - a mensagem enviada pelo canal (`channel.sendResponse`);
   - a fase da tarefa.

3. TABELA DE ESTADOS (entrada: réplica normal, operação com sucesso):
   - Mensagem enviada ao primário:
     - BASE: Empty
     - LEFT: ReplicaResponse(allocId, checkpoint)
     - RIGHT: Empty, enviada via result.respond(listener)
     - MERGE: ReplicaResponse(allocId, checkpoint), enviada via result.respond(listener)
   - `response`:
     - BASE: não existe
     - LEFT: ReplicaResponse
     - RIGHT: não existe
     - MERGE: ReplicaResponse
   - Fase final:
     - BASE: finished
     - LEFT: finished
     - RIGHT: finished
     - MERGE: finished

4. CRITÉRIO DE CONFLITO:
   - X = mensagem enviada pelo canal.
   - (A) não se aplica: o valor difere de BASE em LEFT.
   - (B) o valor em LEFT (ReplicaResponse) é preservado no MERGE. O valor em RIGHT é Empty, que difere de BASE apenas na forma de envio; o payload de BASE era Empty e RIGHT o mantém. Como RIGHT não difere de BASE no valor observável, não há violação.
   - (C) o código novo de RIGHT, o ResponseListener, não lê nem é controlado por valores escritos por LEFT. O MERGE adaptou-o para receber `replicaResponse` e enviá-lo, o que mantém a intenção de LEFT. O ResponseListener do RIGHT é integrado corretamente, e a chamada `result.respond` só ocorre depois do try.
   - Observação: no MERGE, `response` é lido no try de LEFT e usado depois do try, o que é válido porque é `final` e atribuído uma vez. Uma possível diferença é o `ReplicaResult.respond` de subclasses, que poderia responder de forma assíncrona e ignorar o ReplicaResponse. Mas o listener usa `replicaResponse` independentemente do que `respond` passa, então o comportamento esperado de LEFT se preserva.
   - Nenhuma condição se aplica.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): NO</summary>

1. INTENÇÃO: O target é AsyncReplicaAction.doRun().
   - LEFT troca o lock por um ShardReference e cria um ReplicaResponse com allocationId e localCheckpoint, dentro do try-with-resources. Esse response é enviado por channel.sendResponse(response) no fim do método.
   - RIGHT faz shardOperationOnReplica retornar um ReplicaResult. Fora do try, chama result.respond(new ResponseListener()). O listener envia TransportResponse.Empty.INSTANCE pelo canal, depois de logar e de setPhase("finished").
   - O MERGE combina as duas coisas: o response é criado dentro do try, o result é chamado no respond, e o ResponseListener(response) envia replicaResponse.

2. ESTADO: O que doRun escreve ou envia é a resposta enviada pelo channel (ReplicaResponse ou Empty), a fase da task, e as variáveis locais response e result.

3. TABELA DE ESTADOS (réplica com sucesso):
   - Resposta enviada pelo channel:
     - BASE: Empty.INSTANCE.
     - LEFT: ReplicaResponse(allocationId, localCheckpoint).
     - RIGHT: Empty.INSTANCE, enviada via result.respond, ou seja, via ResponseListener.
     - MERGE: ReplicaResponse(allocationId, localCheckpoint), enviada pelo ResponseListener após result.respond.
   - result.respond(listener):
     - BASE: não existe.
     - LEFT: não existe.
     - RIGHT: respond chama listener.onResponse(Empty).
     - MERGE: o respond de ReplicaResult chama listener.onResponse(Empty.INSTANCE). O ResponseListener ignora o parâmetro Empty e envia replicaResponse.

4. CRITÉRIO DE CONFLITO: X = resposta enviada pelo channel.
   - (A) não se aplica: o valor em LEFT difere de BASE.
   - (B) o valor em LEFT (ReplicaResponse) é preservado no MERGE. O valor em RIGHT é Empty, que difere de BASE apenas na rota de envio (via respond), e o MERGE tem ReplicaResponse. Mas o payload de RIGHT é o mesmo de BASE, e a intenção de RIGHT é permitir que subclasses controlem a resposta por ReplicaResult.respond. No MERGE, o ReplicaResult.respond de subclasses perde o controle sobre o payload enviado. Isso é mais uma questão de (C).
   - (C) o código de RIGHT (result.respond(listener) e o listener que envia a resposta) é controlado pelo valor do payload. Em RIGHT, o listener envia o valor que respond fornece (Empty). No MERGE, o listener ignora o valor passado por respond e envia o replicaResponse de LEFT, o que é uma adaptação consciente. O Empty de respond só é usado para disparar o envio. O ReplicaResponse mantém a intenção de LEFT e o fluxo de respond mantém a intenção de RIGHT. A semântica é preservada: as duas mudanças foram integradas e o MERGE envia o ReplicaResponse, como LEFT queria, depois de respond, como RIGHT queria.
   
   Em doRun, o shardOperationOnReplica fica dentro do try, antes do response, como em LEFT. O response é lido de replica, que ainda está aberta. A ordem das operações é coerente. Nenhuma das condições se aplica claramente.

</details>

### 9. `elasticsearch__d8968869__DocWriteResponse#writeTo`

- **Target:** `writeTo(org.elasticsearch.common.io.stream.StreamOutput)`
- **Esperado:** YES; **acertam:** claude-haiku-5-5, claude-opus-5-5; **erram:** claude-sonnet-5-5
- **Código:** [elasticsearch__d8968869__DocWriteResponse](../../data/mergedataset/elasticsearch__d8968869__DocWriteResponse)

**LEFT:** Left adds a call for method writeZLong on the out object sending a long value.

**RIGHT:** Right adds a call for method writeBoolean on the object out sending a boolean value.

**Justificativa do dataset:** When a new byte is added on a matrix of bytes (BigByteArray class), the field count is incremented by 1 (BytesStreamOutput class). As both parent contributions add a new call for adding a new byte, both changes the vaue of count. A test case could call method writeTo sending as parameter an object of type BytesStreamOutput. After the method execution, an assertion should check the value assigned to the field count. Consider that in base commit, count would have value X, in left commit value X+1, and in merge commit value X+2. (assertEquals(x+1, out.position())

#### claude-haiku-5-5: YES ✅

<details><summary>Execução 1 (<code>1.csv</code>): YES — Condição B: out</summary>

1. INTENÇÃO: LEFT acrescenta a escrita de `seqNo` (`out.writeZLong(seqNo)`) ao final de `writeTo`. RIGHT acrescenta a escrita de `forcedRefresh` (`out.writeBoolean(forcedRefresh)`) no mesmo ponto. Confirmado nos diffs.

2. ESTADO: O fluxo de saída `out` (StreamOutput), escrito por `writeTo` na ordem das chamadas. Também são afetados `seqNo` e `forcedRefresh`, mas o que muda na serialização é o conteúdo de `out`.

3. TABELA DE ESTADOS:
   Entrada concreta: `version = 1`, `seqNo = 5`, `forcedRefresh = true`. Mostro apenas a cauda do fluxo, após `super.writeTo`, `shardId`, `type` e `id`, que são idênticos nos quatro casos.
   - `out` (cauda após `version`):
     - BASE: [ ..., zlong(1) ]
     - LEFT: [ ..., zlong(1), zlong(5) ]
     - RIGHT: [ ..., zlong(1), bool(true) ]
     - MERGE: [ ..., zlong(1), zlong(5), bool(true) ]
   - Leitura correspondente no MERGE (`readFrom`): lê `seqNo` com `readZLong` e depois `forcedRefresh` com `readBoolean`, na mesma ordem em que o MERGE escreve. Os dois lados são consistentes entre si.

4. CRITÉRIO DE CONFLITO: X = conteúdo do fluxo `out`, considerado inteiro.
   - (A) Não se aplica: o valor de X em LEFT e em RIGHT difere de BASE, portanto X não é igual nos três.
   - (B) Se aplica: X em LEFT (`[..., zlong(1), zlong(5)]`) difere de BASE. O MERGE (`[..., zlong(1), zlong(5), bool(true)]`) não é igual a LEFT, então LEFT não é preservado. O mesmo vale para RIGHT, cujo valor não é preservado porque o MERGE também não é igual a ele. A condição B é verificada pelos valores, sem recorrer à intenção dos desenvolvedores.
   - (C) Não se aplica de forma adicional: nenhum código alterado por um lado lê `out` ou é controlado por ele. A escrita de cada lado não depende de valores escritos pelo outro. Não é necessário para o resultado, pois B já se aplica.

   Observação: o conflito aqui é de formato do fluxo serializado. Cada lado acrescentou um campo ao final, e o MERGE contém os dois campos, o que altera o fluxo em relação ao que cada pai produziu.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): YES — Condição B: out (StreamOutput escrito por writeTo)</summary>

1. INTENÇÃO: LEFT adiciona `out.writeZLong(seqNo)` ao final de `writeTo`, e RIGHT adiciona `out.writeBoolean(forcedRefresh)` no mesmo ponto, logo após `out.writeZLong(version)`. Os dois diffs confirmam os resumos. Ambos também alteram `readFrom` de forma simétrica, e o MERGE mantém essa simetria.

2. ESTADO: O fluxo `out` (StreamOutput), escrito pelo `writeTo` alterado. Elementos afetados: as chamadas de escrita `type`, `id`, `version`, `seqNo` (LEFT) e `forcedRefresh` (RIGHT). Não há leitura de `seqNo` ou `forcedRefresh` dentro de `writeTo`. `super.writeTo(out)` e `shardId.writeTo(out)` escrevem no mesmo fluxo, mas não são alterados.

3. TABELA DE ESTADOS:
   - Entrada: type = "t", id = "1", version = 5, seqNo = 7, forcedRefresh = true (supondo super e shardId escrevendo o mesmo conteúdo em todos os lados)
   - out (conteúdo escrito por writeTo, além de super/shardId):
     - BASE: "t", "1", 5
     - LEFT: "t", "1", 5, 7
     - RIGHT: "t", "1", 5, true
     - MERGE: "t", "1", 5, 7, true

4. CRITÉRIO DE CONFLITO: X = out, o fluxo inteiro, conforme a definição de elemento de estado, que inclui canal de saída.
   - (A) não se aplica: o valor de out muda em LEFT e em RIGHT em relação a BASE, então não é igual nos três.
   - (B) o valor de out em LEFT difere de BASE. O valor no MERGE ("t", "1", 5, 7, true) é diferente do valor de LEFT ("t", "1", 5, 7), então o MERGE não preserva LEFT. A condição se aplica. O mesmo vale para RIGHT, já que o MERGE também não é igual a ele.
   - (C) não é necessária, pois B já se aplica. Mesmo assim, nenhum código alterado lê out. O valor escrito por cada lado não controla o outro trecho.

   Observação: a serialização continua consistente entre `writeTo` e `readFrom` no MERGE (version, seqNo, forcedRefresh nessa ordem). Isso não elimina a divergência do valor observável de out em relação a LEFT e RIGHT, que é o critério aplicado aqui. O caso segue o mesmo padrão do exemplo 1 (dois acréscimos no mesmo método, MERGE diferente de LEFT).

</details>

<details><summary>Execução 3 (<code>3.csv</code>): YES — Condição B: out (fluxo StreamOutput)</summary>

1. INTENÇÃO: LEFT adiciona a escrita de `seqNo` (`out.writeZLong(seqNo)`) em `writeTo`, junto com o campo `seqNo` e a leitura correspondente em `readFrom`. RIGHT adiciona a escrita de `forcedRefresh` (`out.writeBoolean(forcedRefresh)`) em `writeTo`, junto com o campo e a leitura correspondente. Os resumos são confirmados pelos diffs.

2. ESTADO: O elemento de estado escrito por `writeTo` é o fluxo `out` (StreamOutput), que é um canal de saída. Os trechos alterados escrevem nele: `writeZLong(seqNo)` (LEFT) e `writeBoolean(forcedRefresh)` (RIGHT). Os campos `seqNo` e `forcedRefresh` são elementos de estado do objeto, mas `writeTo` apenas os lê.

3. TABELA DE ESTADOS: Entrada: shardId = S, type = "t", id = "i", version = 5, seqNo = 7, forcedRefresh = true. Considera-se o conteúdo final do fluxo `out` produzido por `writeTo` (escritas em ordem: super.writeTo, shardId, type, id, version, depois o que cada lado adiciona).
   - out (BASE): [S, "t", "i", 5]
   - out (LEFT): [S, "t", "i", 5, 7]
   - out (RIGHT): [S, "t", "i", 5, true]
   - out (MERGE): [S, "t", "i", 5, 7, true]

4. CRITÉRIO DE CONFLITO: X = out (o fluxo inteiro, com seu valor final observável).
   - (A) não se aplica: o valor de `out` difere de BASE em LEFT e em RIGHT.
   - (B) o valor de `out` em LEFT ([S, "t", "i", 5, 7]) difere de BASE, e o MERGE ([S, "t", "i", 5, 7, true]) não é igual a LEFT. Portanto LEFT não é preservado. O mesmo ocorre com RIGHT, cujo valor ([S, "t", "i", 5, true]) também não é preservado no MERGE. A condição B se aplica. A intenção de que ambos os campos devessem coexistir não descarta essa condição, pois o critério avalia o valor do elemento inteiro.
   - (C) não se aplica como condição adicional: nenhum código alterado lê `out` nem é controlado por ele. A ordem de escrita e de leitura (`readFrom` lê `seqNo` e depois `forcedRefresh`) é consistente no MERGE, mas isso não afeta a avaliação de B.

   Observação: o construtor de `DocWriteResponse` foi alterado apenas por LEFT e foi mantido no MERGE, mas isso está fora do alvo `writeTo` e não entra na avaliação.

</details>

#### claude-opus-5-5: YES ✅

<details><summary>Execução 1 (<code>1.csv</code>): YES — Condição B: out</summary>

1. INTENÇÃO: Os diffs confirmam os resumos. LEFT adiciona o campo `seqNo` e o serializa em `writeTo()` com `out.writeZLong(seqNo)` logo após `version`. O `readFrom()` lê esse valor na mesma posição. RIGHT adiciona o campo `forcedRefresh` e o serializa com `out.writeBoolean(forcedRefresh)` logo após `version`. O `readFrom()` também lê esse valor na mesma posição. O MERGE mantém as duas escritas, nesta ordem: `version`, `seqNo`, `forcedRefresh`.

2. ESTADO: O elemento escrito pelo TARGET e pelos trechos alterados é o fluxo de saída `out`, ou seja, a sequência de bytes serializada por `writeTo()`. As chamadas de LEFT e de RIGHT escrevem no mesmo fluxo e na mesma posição relativa, logo após `version`.

3. TABELA DE ESTADOS:
   - Entrada: shardId = S, type = "t", id = "1", version = 3, seqNo = 7, forcedRefresh = true. O conteúdo de `super.writeTo` (P) é igual em todas as versões.
   - BASE: out = [P, S, "t", "1", Z(3)]
   - LEFT: out = [P, S, "t", "1", Z(3), Z(7)]
   - RIGHT: out = [P, S, "t", "1", Z(3), B(true)]
   - MERGE: out = [P, S, "t", "1", Z(3), Z(7), B(true)]
   - Posição imediatamente após version: BASE = fim do fluxo | LEFT = Z(7) | RIGHT = B(true) | MERGE = Z(7)

4. CRITÉRIO DE CONFLITO: X = out (o conteúdo inteiro do fluxo serializado).
   - (A) Não se aplica. O valor de X em LEFT e em RIGHT difere de BASE.
   - (B) Se aplica. O valor de X em LEFT, [..., Z(3), Z(7)], difere de BASE, e o MERGE produz [..., Z(3), Z(7), B(true)], que é diferente. LEFT não é preservado. O valor de X em RIGHT, [..., Z(3), B(true)], também difere de BASE, e o MERGE é diferente dele. Na posição logo após version, RIGHT tem B(true) e MERGE tem Z(7). RIGHT também não é preservado.
   - (C) Não é necessária, pois B já se aplica. Ainda assim, o `readFrom` do MERGE segue a mesma ordem das escritas, então a ida e volta da serialização dentro do próprio MERGE continua consistente. O formato no fio, porém, difere do formato de cada pai.

</details>

#### claude-sonnet-5-5: NO ❌

<details><summary>Execução 1 (<code>1.csv</code>): NO</summary>

1. INTENÇÃO: LEFT adiciona o campo seqNo e o serializa com out.writeZLong(seqNo) depois de version em writeTo, e com in.readZLong() em readFrom. RIGHT adiciona o campo forcedRefresh e o serializa com out.writeBoolean(forcedRefresh) depois de version, e com in.readBoolean() em readFrom. Os diffs confirmam os dois resumos.

2. ESTADO: O fluxo de saída `out` em writeTo(), que recebe a sequência de bytes escritos. Em readFrom, o fluxo `in` é consumido e os campos seqNo e forcedRefresh são atribuídos.

3. TABELA DE ESTADOS:
   - Entrada: seqNo = 5, forcedRefresh = true, version = 1.
   - Sequência escrita em `out`:
     - BASE: [shardId, type, id, ZLong(version)]
     - LEFT: [shardId, type, id, ZLong(version), ZLong(seqNo)]
     - RIGHT: [shardId, type, id, ZLong(version), Boolean(forcedRefresh)]
     - MERGE: [shardId, type, id, ZLong(version), ZLong(seqNo), Boolean(forcedRefresh)]
   - Leitura em MERGE: readZLong (version), readZLong (seqNo), readBoolean (forcedRefresh), na mesma ordem da escrita.
   - O MERGE escreve e lê na mesma ordem, então a serialização é consistente. O valor de `out` no MERGE é a união das duas adições, sem interferência entre elas.

4. CRITÉRIO DE CONFLITO: X = fluxo `out`.
   - (A) não se aplica: LEFT e RIGHT diferem de BASE.
   - (B) o valor de `out` em LEFT contém ZLong(seqNo) no final, e o MERGE também contém esse trecho. O mesmo vale para o Boolean de RIGHT. Cada contribuição é preservada, porque as escritas são aditivas e independentes. Pode-se objetar que o fluxo inteiro difere do de cada pai, mas a diferença vem apenas da outra adição, que é a composição esperada.
   - (C) writeBoolean não lê nem é controlado por seqNo, e writeZLong não lê nem é controlado por forcedRefresh. A ordem relativa dos dois campos é a mesma em writeTo e em readFrom, então a desserialização permanece coerente.
   - Não há conflito.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): NO</summary>

1. INTENÇÃO: LEFT adiciona o campo seqNo e o serializa com out.writeZLong(seqNo) depois de version, em writeTo e em readFrom. RIGHT adiciona o campo forcedRefresh e o serializa com out.writeBoolean(forcedRefresh) depois de version, também em writeTo e em readFrom. Os diffs confirmam os dois resumos.

2. ESTADO: Em writeTo, o fluxo out recebe, em ordem, os dados do super, shardId, type, id, version e os novos campos de cada lado. O fluxo de saída é um canal de saída. Em readFrom, os campos seqNo e forcedRefresh são lidos do fluxo de entrada, na mesma ordem.

3. TABELA DE ESTADOS:
   - Entrada: seqNo = 5, forcedRefresh = true, version = 3.
   - Sequência escrita em out:
     - BASE: [super, shardId, type, id, Z(3)]
     - LEFT: [super, shardId, type, id, Z(3), Z(5)]
     - RIGHT: [super, shardId, type, id, Z(3), Bool(true)]
     - MERGE: [super, shardId, type, id, Z(3), Z(5), Bool(true)]
   - readFrom no MERGE: lê version, depois seqNo = readZLong, depois forcedRefresh = readBoolean. Isso é consistente com a ordem de escrita.
   - Os campos seqNo e forcedRefresh são independentes. A ordem relativa entre eles é arbitrária, mas simétrica entre leitura e escrita.

4. CRITÉRIO DE CONFLITO: X = a sequência de bytes em out.
   - (A) não se aplica: o valor de X difere de BASE em LEFT e em RIGHT.
   - (B) o MERGE contém a escrita de LEFT (Z(5)) e a de RIGHT (Bool), apenas combinadas. Cada adição é preservada como prefixo ou subsequência, sem alteração de valor. Não há perda dos dados que um pai escreveu.
   - (C) a escrita de um lado não lê nem é controlada por estado alterado pelo outro. Leitura e escrita permanecem simétricas. O construtor mudou de assinatura em LEFT, mas isso não afeta o writeTo. Os campos seqNo e forcedRefresh não interagem entre si.
   - Nenhuma condição se aplica.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): NO</summary>

1. INTENÇÃO: LEFT adiciona o campo seqNo e escreve out.writeZLong(seqNo) após version. RIGHT adiciona o campo forcedRefresh e escreve out.writeBoolean(forcedRefresh) após version. Os diffs confirmam os resumos.

2. ESTADO: O fluxo `out` (a sequência de bytes escrita em StreamOutput por writeTo). Os campos seqNo e forcedRefresh são apenas lidos por writeTo.

3. TABELA DE ESTADOS:
   - Entrada: version = 5, seqNo = 7, forcedRefresh = true
   - Sequência escrita em out (após super.writeTo, shardId, type e id):
     - BASE: [ZLong(5)]
     - LEFT: [ZLong(5), ZLong(7)]
     - RIGHT: [ZLong(5), Boolean(true)]
     - MERGE: [ZLong(5), ZLong(7), Boolean(true)]
   - Leitura (readFrom) no MERGE: version = readZLong, seqNo = readZLong, forcedRefresh = readBoolean. Isso é consistente com a ordem de escrita no MERGE.

4. CRITÉRIO DE CONFLITO: X = out (o fluxo escrito).
   - (A) não se aplica: o valor de X em LEFT e RIGHT difere de BASE.
   - (B) o valor de X em LEFT é [ZLong(5), ZLong(7)], e o MERGE contém esses bytes como prefixo, mas o valor inteiro do fluxo difere. O mesmo vale para RIGHT. Porém, cada lado acrescentou um campo independente, e o MERGE é a composição esperada das duas adições. Em nenhum dos pais o valor completo de X é preservado, o que é inevitável quando duas escritas aditivas se combinam. Na prática, a combinação mantém ambas as contribuições e a ordem de escrita coincide com a de leitura.
   - (C) o código de um lado não lê nem é controlado por valores escritos pelo outro. writeBoolean não depende de seqNo, e writeZLong(seqNo) não depende de forcedRefresh. A ordem em writeTo e readFrom é a mesma no MERGE, então a serialização é simétrica. Não há interferência de dados nem de controle.

</details>

### 10. `elasticsearch__d8968869__DocWriteResponse#toXContent`

- **Target:** `toXContent(org.elasticsearch.common.xcontent.XContentBuilder| org.elasticsearch.common.xcontent.ToXContent$Params)`
- **Esperado:** YES; **acertam:** claude-haiku-5-5; **erram:** claude-opus-5-5, claude-sonnet-5-5
- **Código:** [elasticsearch__d8968869__DocWriteResponse](../../data/mergedataset/elasticsearch__d8968869__DocWriteResponse)

**LEFT:** Left adds two calls for method field on the object builder.

**RIGHT:** Right adds a call for method field on the object builder.

**Justificativa do dataset:** Left and Right add different objects in the generator field on class JsonXContentGenerator. In the class WriterBasedJsonGenerator, there is an implementation of method writeFieldName, that increment the value of _outputTail. A test case should explore this field, after writing a new String by calling method field. assertEquals(X, xcontentBuilder._outputTail).

#### claude-haiku-5-5: YES ✅

<details><summary>Execução 1 (<code>1.csv</code>): YES — Condição B: builder</summary>

1. INTENÇÃO: LEFT adiciona seqNo ao DocWriteResponse e, em toXContent, emite `_shard_id` e `_seq_no` (quando seqNo &gt;= 0). RIGHT adiciona o campo `forced_refresh` (forcedRefresh) em toXContent. Os diffs confirmam os dois resumos.

2. ESTADO: O `builder` (XContentBuilder, um fluxo de saída) é escrito por toXContent e lido pelo chamador. Os trechos alterados escrevem nele os campos `_shard_id`, `_seq_no` (LEFT) e `forced_refresh` (RIGHT). Também é tocado o campo seqNo, mas ele não é lido por toXContent em RIGHT.

3. TABELA DE ESTADOS:
   - Entrada: shardId com índice "idx" e id 0, type "t", id "1", version 1, seqNo 5, forcedRefresh = true, shardInfo com seus campos padrão.
   - builder (saída XContent, em ordem):
     - BASE: `_index=idx, _type=t, _id=1, _version=1, <shardInfo>`
     - LEFT: `_index=idx, _type=t, _id=1, _version=1, <shardInfo>, _shard_id=0, _seq_no=5`
     - RIGHT: `_index=idx, _type=t, _id=1, _version=1, forced_refresh=true, <shardInfo>`
     - MERGE: `_index=idx, _type=t, _id=1, _version=1, forced_refresh=true, <shardInfo>, _shard_id=0, _seq_no=5`

4. CRITÉRIO DE CONFLITO: X = builder (a saída XContent inteira).
   - (A) não se aplica: o valor de X muda em LEFT e em RIGHT, então não é igual em BASE, LEFT e RIGHT.
   - (B) o valor de X em LEFT difere de BASE (acrescenta `_shard_id` e `_seq_no`). O MERGE não preserva esse valor, porque contém `forced_refresh`, que LEFT não tem. Além disso, o valor de X em RIGHT difere de BASE (acrescenta `forced_refresh`), e o MERGE não é igual a RIGHT, porque não contém `_shard_id` e `_seq_no`. Basta uma ocorrência para B se aplicar.
   - (C) também há indício: o `forced_refresh` de RIGHT é escrito no mesmo fluxo que o bloco de LEFT lê (`getSeqNo()`), mas B já se aplica, então C não é necessária para a decisão.

   Esse caso segue a mesma estrutura do exemplo 1: duas adições independentes no mesmo método, em que o MERGE combina ambas e, por isso, difere de cada pai. Pela regra B, isso é conflito.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): YES — Condição B: builder (saída do XContentBuilder em toXContent)</summary>

1. INTENÇÃO: LEFT adiciona ao `toXContent` os campos `_shard_id` e `_seq_no` (este último condicionado a `getSeqNo() >= 0`), além de reformatar a cadeia de `.field(...)`. RIGHT adiciona o campo `"forced_refresh"` à mesma cadeia. O resumo confere com os diffs: são duas chamadas `field` de LEFT e uma de RIGHT.

2. ESTADO: O `XContentBuilder` recebido como parâmetro, que é o canal de saída escrito por `toXContent` (via `builder.field(...)` e `shardInfo.toXContent(builder, params)`). Os trechos alterados também leem `getSeqNo()` (LEFT), `forcedRefresh` (RIGHT) e `shardId.id()`.

3. TABELA DE ESTADOS:
   Entrada: shardId = (índice "idx", shard 0), type = "doc", id = "1", seqNo = 5, version = 1, forcedRefresh = true, saída de `shardInfo.toXContent` = S (mesma em todos os casos).
   - builder (saída de toXContent):
     - BASE: `_index=idx, _type=doc, _id=1, _version=1, S`
     - LEFT: `_index=idx, _type=doc, _id=1, _version=1, S, _shard_id=0, _seq_no=5`
     - RIGHT: `_index=idx, _type=doc, _id=1, _version=1, forced_refresh=true, S`
     - MERGE: `_index=idx, _type=doc, _id=1, _version=1, forced_refresh=true, S, _shard_id=0, _seq_no=5`
   - Valores dos campos isolados (para referência): `forced_refresh` é ausente em BASE e LEFT e `true` em RIGHT e MERGE; `_shard_id` e `_seq_no` são ausentes em BASE e RIGHT e presentes em LEFT e MERGE.

4. CRITÉRIO DE CONFLITO: X = saída do builder (o valor final observável do elemento inteiro).
   - (A) não se aplica: o valor de X em LEFT e em RIGHT difere de BASE, então a igualdade exigida pela condição A não ocorre.
   - (B) o valor de X em LEFT difere de BASE (campos `_shard_id` e `_seq_no` adicionados). O MERGE não preserva LEFT: o MERGE contém `forced_refresh=true` entre `_version` e `S`, que não está em LEFT. O valor de X em RIGHT também difere de BASE, e o MERGE não é igual a RIGHT, pois falta `_shard_id`/`_seq_no`. Logo, a condição B se aplica. Isso segue o mesmo critério do exemplo 1, em que as duas adições à mesma sequência de chamadas geram conflito quando o MERGE não reproduz o resultado de um dos pais.
   - (C) não é necessária, pois B já se aplica. Além disso, o código de LEFT lê `seqNo` e `getSeqNo()`, enquanto RIGHT não escreve esses valores dentro de `toXContent`. O código de RIGHT lê `forcedRefresh`, que LEFT não altera. Não há dependência cruzada de dados ou de controle nesse trecho.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): YES — Condição B: builder (saída do XContentBuilder em toXContent)</summary>

1. INTENÇÃO: O resumo diz que LEFT adiciona duas chamadas `field` e RIGHT adiciona uma. Os diffs mostram outra coisa. LEFT acrescenta `_shard_id` e, condicionalmente (`getSeqNo() >= 0`), `_seq_no`, além de reindentar a cadeia de `field`. Também adiciona o campo `seqNo` e os métodos `getSeqNo()`, `readFrom` e `writeTo`. RIGHT acrescenta `.field("forced_refresh", forcedRefresh)` na cadeia de `toXContent` e adiciona o campo `forcedRefresh`, `forcedRefresh()`, `setForcedRefresh()` e a serialização de `forcedRefresh`. Confio nos diffs, não no resumo.

2. ESTADO: Elementos escritos pelo TARGET e pelos trechos alterados:
   - o `XContentBuilder` (canal de saída), escrito pelas chamadas `field` de `toXContent`;
   - o campo `seqNo`, escrito pelo construtor e por `readFrom`, e lido por `getSeqNo()` dentro de `toXContent`;
   - o campo `forcedRefresh`, lido por `toXContent` (campo `forced_refresh`).

3. TABELA DE ESTADOS: Entrada: shardId "idx", type "doc", id "1", version 1, seqNo 5, forcedRefresh true, `shardInfo` escrevendo o bloco S.
   - builder (sequência de campos gravada):
     - BASE: `_index=idx, _type=doc, _id=1, _version=1, S`
     - LEFT: `_index=idx, _type=doc, _id=1, _version=1, S, _shard_id=0, _seq_no=5`
     - RIGHT: `_index=idx, _type=doc, _id=1, _version=1, forced_refresh=true, S`
     - MERGE: `_index=idx, _type=doc, _id=1, _version=1, forced_refresh=true, S, _shard_id=0, _seq_no=5`
   - seqNo: BASE = 5 | LEFT = 5 | RIGHT = 5 | MERGE = 5
   - forcedRefresh: BASE = false | LEFT = false | RIGHT = true | MERGE = true

4. CRITÉRIO DE CONFLITO:
   - X = builder (valor final da saída inteira de `toXContent`).
     - (A) não se aplica: o valor muda em LEFT e em RIGHT.
     - (B) o valor em LEFT difere de BASE (adiciona `_shard_id` e `_seq_no`). O MERGE não é igual a LEFT, pois contém também `forced_refresh`. Logo LEFT não é preservado. O valor em RIGHT também difere de BASE e o MERGE não é igual a RIGHT, pois contém também `_shard_id` e `_seq_no`. Condição B se aplica.
     - (C) não é necessária, pois B já se aplica.
   - X = seqNo: o valor é igual nos quatro casos, então (A) e (B) não se aplicam. Para (C), o código de RIGHT em `toXContent` (`forced_refresh`) não lê nem é controlado por seqNo, então não se aplica.
   - X = forcedRefresh: o valor só muda em RIGHT, e o MERGE é igual a RIGHT (true), então está preservado. Para (C), o código de LEFT em `toXContent` (`_shard_id`, `_seq_no`) não lê nem é controlado por forcedRefresh, então não se aplica.

Conclusão: o conflito se manifesta na saída do `XContentBuilder`. O MERGE não preserva a saída de nenhum dos pais, pois combina as duas adições. A mudança de LEFT em `toXContent` (`_shard_id`/`_seq_no`) e a de RIGHT (`forced_refresh`) foram aplicadas de forma textualmente limpa, mas o conteúdo resultante do builder difere do que cada desenvolvedor produziu.

</details>

#### claude-opus-5-5: NO ❌

<details><summary>Execução 1 (<code>1.csv</code>): NO</summary>

1. INTENÇÃO:
   - LEFT acrescenta o campo `seqNo`. Ele é inicializado no construtor e serializado em `writeTo`/`readFrom`. Em `toXContent()`, depois de `shardInfo.toXContent`, LEFT emite `_shard_id` sempre e `_seq_no` somente quando `getSeqNo() >= 0`.
   - RIGHT acrescenta o campo `forcedRefresh`, com getter e setter, e o serializa. Em `toXContent()`, RIGHT encadeia `.field("forced_refresh", forcedRefresh)` logo após `_version`.
   - Os diffs confirmam os resumos.

2. ESTADO:
   - O objeto `builder`, isto é, o documento JSON produzido e retornado. Cada campo do documento é um elemento da coleção: `_index`, `_type`, `_id`, `_version`, `forced_refresh`, `_shards`, `_shard_id` e `_seq_no`.
   - Os campos `seqNo` e `forcedRefresh`, lidos por `toXContent()`.

3. TABELA DE ESTADOS:
   - Entrada: index "i", type "t", id "1", version 1, shard 0, seqNo = 5, forcedRefresh = true.
   - BASE: {_index:"i", _type:"t", _id:"1", _version:1, _shards:{...}}
   - LEFT: {_index:"i", _type:"t", _id:"1", _version:1, _shards:{...}, _shard_id:0, _seq_no:5}
   - RIGHT: {_index:"i", _type:"t", _id:"1", _version:1, forced_refresh:true, _shards:{...}}
   - MERGE: {_index:"i", _type:"t", _id:"1", _version:1, forced_refresh:true, _shards:{...}, _shard_id:0, _seq_no:5}
   - Por campo:
     - `forced_refresh`: BASE = ausente | LEFT = ausente | RIGHT = true | MERGE = true
     - `_shard_id`: BASE = ausente | LEFT = 0 | RIGHT = ausente | MERGE = 0
     - `_seq_no`: BASE = ausente | LEFT = 5 | RIGHT = ausente | MERGE = 5
     - Os demais campos são iguais nas quatro versões.
   - Com seqNo = -1, `_seq_no` fica ausente tanto em LEFT quanto em MERGE.

4. CRITÉRIO DE CONFLITO:
   - Escolha da granularidade: tratei o documento JSON como uma coleção de pares chave-valor e avaliei cada chave como um elemento de estado separado. A ordem das chaves num objeto JSON não tem significado. Ressalva: se o `builder` for tratado como um único valor, o MERGE difere de LEFT, pois inclui `forced_refresh`, e também de RIGHT, pois inclui `_shard_id` e `_seq_no`. Nesse caso, uma leitura literal da condição (B) daria SIM. Essa leitura, porém, classificaria como conflito qualquer par de inclusões independentes no mesmo objeto, então adotei a granularidade por chave.
   - (A) não se aplica. Os campos `_index`, `_type`, `_id`, `_version` e `_shards` são iguais em BASE, LEFT, RIGHT e MERGE.
   - (B) não se aplica.
     - `forced_refresh` muda em RIGHT e o MERGE preserva o valor (true).
     - `_shard_id` e `_seq_no` mudam em LEFT e o MERGE preserva os valores (0 e 5).
   - (C) não se aplica.
     - O código de RIGHT lê apenas `forcedRefresh`, que LEFT não escreve.
     - O código de LEFT lê apenas `seqNo` e `shardId`, que RIGHT não escreve.
     - A condição `getSeqNo() >= 0` não depende de nada que RIGHT altere.
     - A serialização em `writeTo`/`readFrom` mantém a mesma ordem nos dois métodos.

</details>

#### claude-sonnet-5-5: NO ❌

<details><summary>Execução 1 (<code>1.csv</code>): NO</summary>

1. INTENÇÃO: LEFT adiciona o campo seqNo e, em toXContent, emite "_shard_id" e, se seqNo &gt;= 0, "_seq_no" depois do shardInfo. RIGHT adiciona o campo forcedRefresh e emite "forced_refresh" logo após _version, antes do shardInfo. Os diffs confirmam os resumos.

2. ESTADO: O builder (a sequência de campos escritos em XContentBuilder), que é a saída do método. Também são lidos os campos shardId, type, id, version, seqNo e forcedRefresh.

3. TABELA DE ESTADOS:
   - Entrada: index "i", type "t", id "1", version 1, seqNo 5, forcedRefresh true, shardId.id() = 0.
   - BASE: _index, _type, _id, _version, depois o shardInfo.
   - LEFT: _index, _type, _id, _version, shardInfo, _shard_id=0, _seq_no=5.
   - RIGHT: _index, _type, _id, _version, forced_refresh, shardInfo.
   - MERGE: _index, _type, _id, _version, forced_refresh, shardInfo, _shard_id=0, _seq_no=5.

   O MERGE contém todas as adições de LEFT e de RIGHT, na posição em que cada lado as colocou. Os campos novos de LEFT continuam depois do shardInfo, e o de RIGHT continua antes dele.

4. CRITÉRIO DE CONFLITO: X = conteúdo do builder.
   - (A) não se aplica: o valor difere de BASE em LEFT e em RIGHT.
   - (B) o valor de X em LEFT difere de BASE. O MERGE tem forced_refresh a mais do que LEFT, mas isso é a contribuição de RIGHT. Cada pai tem uma saída diferente da base, e o MERGE é a união das duas mudanças. Isso é composição esperada, não perda do valor de um pai.
   - (C) o código novo de LEFT lê seqNo e shardId, que RIGHT não altera. O código novo de RIGHT lê forcedRefresh, que LEFT não altera. Não há dependência de dados nem de controle entre as duas mudanças. A ordem dos campos no JSON não afeta a semântica. As leituras e escritas de stream (readFrom e writeTo) são simétricas no MERGE (seqNo e depois forcedRefresh), mas ficam fora do TARGET.

   Nenhuma condição se aplica.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): NO</summary>

1. INTENÇÃO: LEFT adiciona o campo seqNo e, em toXContent, escreve `_shard_id` e, condicionalmente, `_seq_no` no builder, depois de shardInfo.toXContent. RIGHT adiciona o campo forcedRefresh e escreve `forced_refresh` no builder, logo após `_version` e antes de shardInfo. Os diffs confirmam esses resumos.

2. ESTADO: O estado escrito em toXContent é o conteúdo do builder, isto é, a sequência de campos emitidos, e o valor de retorno (builder). O método lê shardId, type, id, version, forcedRefresh e seqNo. Fora do TARGET, os campos seqNo e forcedRefresh são escritos por construtor, readFrom e writeTo.

3. TABELA DE ESTADOS:
   - Entrada: shardId = [idx][0], type = t, id = 1, version = 1, seqNo = 5, forcedRefresh = true
   - builder em BASE: _index, _type, _id, _version, shardInfo
   - builder em LEFT: _index, _type, _id, _version, shardInfo, _shard_id=0, _seq_no=5
   - builder em RIGHT: _index, _type, _id, _version, forced_refresh, shardInfo
   - builder em MERGE: _index, _type, _id, _version, forced_refresh, shardInfo, _shard_id=0, _seq_no=5
   - Ordem de serialização (writeTo) em BASE: version
   - Ordem de serialização (writeTo) em LEFT: version, seqNo
   - Ordem de serialização (writeTo) em RIGHT: version, forcedRefresh
   - Ordem de serialização (writeTo) em MERGE: version, seqNo, forcedRefresh
   - readFrom no MERGE lê seqNo e depois forcedRefresh, na mesma ordem de writeTo, então é consistente.
   - Construtor: o merge usa a assinatura do LEFT, que inclui seqNo, e o forcedRefresh mantém o padrão false. Isso não é conflito.

4. CRITÉRIO DE CONFLITO: X = builder (saída de toXContent).
   - (A) não se aplica: X difere de BASE em LEFT e em RIGHT.
   - (B) o MERGE contém todos os campos adicionados por LEFT e por RIGHT. Como a saída é uma sequência de campos, cada adição é preservada e a ordem relativa é mantida. Não há perda nem alteração dos campos escritos por cada lado.
   - (C) o código de LEFT lê seqNo e shardId, que RIGHT não altera. O código de RIGHT lê forcedRefresh, que LEFT não altera. Nenhum dos trechos depende de dados ou de controle escritos pelo outro. O shardInfo.toXContent entre eles não muda de comportamento.
   - Serialização: seqNo e forcedRefresh são escritos e lidos na mesma ordem no MERGE, então não há interferência.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): NO</summary>

1. INTENÇÃO: LEFT adiciona o campo seqNo e, em toXContent, escreve "_shard_id" e, se seqNo &gt;= 0, "_seq_no" no builder, depois do shardInfo.toXContent. RIGHT adiciona forcedRefresh e escreve "forced_refresh" no builder, logo após "_version" e antes do shardInfo.toXContent. Os diffs confirmam os resumos.

2. ESTADO: O builder (conteúdo XContent produzido por toXContent), que recebe as chamadas field. Também são lidos os campos seqNo e forcedRefresh. O return é o próprio builder.

3. TABELA DE ESTADOS:
   - Entrada: seqNo = 5, forcedRefresh = true, shardId.id() = 0
   - BASE: _index, _type, _id, _version, depois o conteúdo do shardInfo.
   - LEFT: _index, _type, _id, _version, shardInfo, _shard_id=0, _seq_no=5.
   - RIGHT: _index, _type, _id, _version, forced_refresh=true, shardInfo.
   - MERGE: _index, _type, _id, _version, forced_refresh=true, shardInfo, _shard_id=0, _seq_no=5.

   Os campos de cada lado são adicionados em pontos distintos e não se interferem. O MERGE contém a união das duas contribuições, na ordem natural.

4. CRITÉRIO DE CONFLITO: X = builder.
   - (A) não se aplica: o valor do builder difere de BASE em LEFT e em RIGHT.
   - (B) o valor do builder em LEFT difere de BASE, e o MERGE mantém todos os campos de LEFT. O mesmo vale para RIGHT. A única diferença é o acréscimo do campo do outro lado, o que é a união esperada. Os campos de cada lado ficam intactos e na mesma ordem relativa.
   - (C) o código de LEFT (_shard_id, _seq_no) não lê nem é controlado por forcedRefresh. O código de RIGHT (forced_refresh) não lê seqNo nem shardInfo. O construtor com seqNo não afeta o código de RIGHT em toXContent. Nenhum dos lados depende do valor escrito pelo outro.

   Não há interferência semântica.

</details>

## 2. Falsos positivos de parte dos modelos

Casos sem conflito (NO) em que algum modelo responde YES e outro acerta: 6 casos.

| Caso | claude-haiku-5-5 | claude-opus-5-5 | claude-sonnet-5-5 |
|---|---|---|---|
| `storm__bd1f5c54__KafkaSpout#emitTupleIfNotEmitted` | YES | NO | NO |
| `activiti__bf46684b__UserTaskActivityBehavior#execute` | YES | NO | NO |
| `spring-boot__ea8107b6__UndertowEmbeddedServletContainerFactory#createDeploymentManager` | YES | NO | NO |
| `elasticsearch__d8968869__TransportIndexAction#executeIndexRequestOnPrimary` | YES | NO | NO |
| `elasticsearch__d8968869__DocWriteResponse#readFrom` | YES | NO | NO |
| `elasticsearch__d8968869__MetaDataCreateIndexService#createIndex` | YES | NO | NO |

### 11. `storm__bd1f5c54__KafkaSpout#emitTupleIfNotEmitted`

- **Target:** `emitTupleIfNotEmitted(ConsumerRecord<K,V>)`
- **Esperado:** NO; **acertam:** claude-opus-5-5, claude-sonnet-5-5; **erram:** claude-haiku-5-5
- **Código:** [storm__bd1f5c54__KafkaSpout](../../data/mergedataset/storm__bd1f5c54__KafkaSpout)

**LEFT:** Left performs a refactoring extracting a variable of an IF statement.  it also changes another IF condition.

**RIGHT:** Right updates the method signature changing its return type for boolean and adds return statements.

**Justificativa do dataset:** There is no locally observable interference as the Left changes do not impact the method return.

#### claude-opus-5-5: NO ✅

<details><summary>Execução 1 (<code>1.csv</code>): NO</summary>

1. INTENÇÃO:
   - **LEFT:** em `emitTupleIfNotEmitted`, extrai `retryService.isScheduled(msgId)` para a variável local `isScheduled`. Também troca a condição de remoção do retry de `retryService.isReady(msgId)` para `isScheduled`. Fora do TARGET, LEFT passa a ignorar ack/fail de tuplas não rastreadas e limpa `emitted` das partições revogadas em `initialize`. O diff confirma o resumo.
   - **RIGHT:** muda o retorno de `emitTupleIfNotEmitted` para `boolean`. Retorna `true` quando a tupla é emitida e `false` caso contrário. `emit()` passa a usar esse retorno num laço que pula registros não emitidos. O diff confirma o resumo.

2. ESTADO (escrito pelo TARGET e pelos trechos alterados):
   - o valor de retorno de `emitTupleIfNotEmitted`, novo em RIGHT;
   - a coleção `emitted`;
   - o campo `numUncommittedOffsets`;
   - o estado do `retryService` (remoção de `msgId`);
   - a saída emitida via `kafkaSpoutStreams.emit(collector, ...)`;
   - a variável local `isScheduled`, nova em LEFT.

3. TABELA DE ESTADOS:
   - **Entrada 1:** registro cujo `msgId` falhou antes e está agendado e pronto (`isScheduled = true`, `isReady = true`), não está em `acked` nem em `emitted`; `numUncommittedOffsets = 0`.
     - tupla emitida: BASE = sim | LEFT = sim | RIGHT = sim | MERGE = sim
     - `emitted`: BASE = {msgId} | LEFT = {msgId} | RIGHT = {msgId} | MERGE = {msgId}
     - `numUncommittedOffsets`: BASE = 1 | LEFT = 1 | RIGHT = 1 | MERGE = 1
     - `retryService` contém `msgId`: BASE = não | LEFT = não (removido via `isScheduled = true`) | RIGHT = não | MERGE = não
     - retorno: BASE = void | LEFT = void | RIGHT = true | MERGE = true
   - **Entrada 2:** registro já presente em `acked`.
     - nenhum efeito colateral em nenhuma versão;
     - retorno: BASE = void | LEFT = void | RIGHT = false | MERGE = false.
   - **Entrada 3:** registro agendado mas ainda não pronto (`isScheduled = true`, `isReady = false`).
     - nada é emitido em nenhuma versão;
     - retorno: RIGHT = false | MERGE = false (o `return false` final é alcançado).
   - **Entrada 4:** registro nunca falhou (`isScheduled = false`).
     - emitido em todas as versões;
     - `retryService.remove` não é chamado: em BASE e RIGHT porque `isReady = false`, em LEFT e MERGE porque `isScheduled = false`;
     - retorno: RIGHT = true | MERGE = true.

4. CRITÉRIO DE CONFLITO:
   - **(A) não se aplica:** nenhum elemento tem valor no MERGE diferente de um valor comum a BASE, LEFT e RIGHT. `emitted`, `numUncommittedOffsets`, `retryService` e a saída emitida são idênticos nas quatro versões para todas as entradas.
   - **(B) não se aplica:** o retorno, alterado por RIGHT, tem no MERGE o mesmo valor que em RIGHT em todas as entradas. O `return true` está dentro do bloco de emissão e o `return false` cobre os demais caminhos. LEFT não altera nenhum valor final observável no TARGET em relação a BASE; a refatoração é equivalente, e o MERGE coincide com LEFT.
   - **(C) não se aplica:** o laço de `emit()` de RIGHT lê o retorno, que no MERGE é igual ao de RIGHT. LEFT altera `emitted` em `initialize`, `ack` e `fail`, e o TARGET lê `emitted`. Porém o código de RIGHT (os `return`) apenas reflete se houve emissão, de forma consistente com LEFT. Para um mesmo estado de `emitted`, o comportamento do código de RIGHT no MERGE é o mesmo que em RIGHT. Nenhum código de um lado passa a se comportar de modo diferente do pretendido por causa do outro.

</details>

#### claude-sonnet-5-5: NO ✅

<details><summary>Execução 1 (<code>1.csv</code>): NO</summary>

1. INTENÇÃO: LEFT extrai a variável isScheduled no else-if final de emitTupleIfNotEmitted. Ele também troca a condição de remoção do retryService de isReady(msgId) para isScheduled. RIGHT muda o retorno do método para boolean (true se emitiu, false caso contrário). Em emit(), RIGHT passa a fazer um loop que remove da fila os registros que não foram emitidos.

2. ESTADO: Os elementos escritos pelo método TARGET são:
   - o retorno do método (boolean), em RIGHT e no MERGE;
   - emitted, numUncommittedOffsets e o estado de retryService (remove);
   - a saída do collector (emit).

3. TABELA DE ESTADOS: Entrada: um registro cujo msgId está agendado para retry e ainda não está pronto (isScheduled = true, isReady = false), sem estar em acked nem em emitted.
   - Fluxo no método:
     - BASE: o else-if é `!true || false` = false. Nada é emitido e não há retorno (void).
     - LEFT: isScheduled = true e a condição é `false || false` = false. Nada é emitido (igual a BASE).
     - RIGHT: igual a BASE no fluxo, e retorna false.
     - MERGE: igual, e retorna false.
   - Entrada 2: msgId agendado e pronto (isReady = true).
     - BASE: emite e remove do retry, porque isReady é true.
     - LEFT: emite e remove, porque isScheduled é true.
     - RIGHT: igual a BASE, e retorna true.
     - MERGE: emite, remove do retry e retorna true.
   - Entrada 3: msgId nunca agendado.
     - BASE: emite, e retryService.isReady(msgId) é consultado, provavelmente false, então não remove.
     - LEFT: emite e isScheduled = false, então não remove.
     - RIGHT: igual a BASE, e retorna true.
     - MERGE: emite, não remove e retorna true.
   - Retorno nos casos de skip (acked ou emitted): RIGHT retorna false, e MERGE retorna false pelo `return false` final.
   - Resultado do retorno:
     - Emitiu: RIGHT = true, MERGE = true.
     - Não emitiu: RIGHT = false, MERGE = false.

4. CRITÉRIO DE CONFLITO:
   - O retorno em MERGE coincide com RIGHT em todos os caminhos. O `return true` está dentro do if interno, e o `return false` fica depois do else, cobrindo os skips e o caso de não pronto.
   - O estado de retry, emitted e numUncommittedOffsets em MERGE coincide com LEFT.
   - (A) não se aplica: não há valor que seja igual nos três pais e diferente no MERGE.
   - (B) não se aplica: o MERGE preserva LEFT nos efeitos e RIGHT no retorno.
   - (C) O código de RIGHT que usa o retorno (o loop em emit) depende de o método ter emitido ou não. Isso continua igual no MERGE. O código de LEFT não lê o retorno.
   - Outros pontos fora do TARGET, como a alteração de ack/fail em LEFT contra o loop de emit em RIGHT, não alteram o comportamento do TARGET.
   - Não há interferência.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): NO</summary>

1. INTENÇÃO: LEFT extrai a variável isScheduled no método alvo e troca a condição interna `retryService.isReady(msgId)` por `isScheduled` antes de `retryService.remove(msgId)`. RIGHT muda o retorno de emitTupleIfNotEmitted para boolean, retorna true após emitir e false no restante, e altera emit() para fazer um loop com esse retorno. O diff confirma os resumos.

2. ESTADO: Elementos escritos pelo alvo e pelos trechos alterados:
   - o retorno de emitTupleIfNotEmitted;
   - `emitted`, `numUncommittedOffsets` e o estado de retryService (remove);
   - o estado de `waitingToEmit` (remove em emit()).

3. TABELA DE ESTADOS:
   - Entrada: record com msgId não adquirido (acked), não em emitted, isScheduled = true e isReady = true.
   - Retorno: BASE = void | LEFT = void | RIGHT = true | MERGE = true.
   - emitted: BASE = {msgId} | LEFT = {msgId} | RIGHT = {msgId} | MERGE = {msgId}.
   - numUncommittedOffsets: BASE = +1 | LEFT = +1 | RIGHT = +1 | MERGE = +1.
   - retryService.remove: BASE = chamado | LEFT = chamado | RIGHT = chamado | MERGE = chamado.
   - Outra entrada: o record é ignorado, pois já foi acked ou está em emitted. O retorno é false em RIGHT e em MERGE. O estado dos demais elementos não muda.
   - Entrada em que isScheduled = true e isReady = false: nada é emitido em nenhuma versão. O retorno é false em RIGHT e em MERGE.
   - Entrada em que isScheduled = false: emite. O remove não é chamado em BASE, e LEFT e MERGE também não o chamam. O retorno é true em RIGHT e em MERGE.

   A fusão colocou `return true` dentro do if aninhado e `return false` ao final. Isso reproduz a semântica de RIGHT: true somente quando emite. A mudança de LEFT, de isReady para isScheduled, é equivalente neste caminho, pois o remove só ocorre quando a condição externa é verdadeira. O estado emitido é o mesmo em todas as versões.

4. CRITÉRIO DE CONFLITO:
   - (A) não se aplica: nenhum valor é igual em BASE, LEFT e RIGHT e diferente em MERGE.
   - (B) o valor de retorno e os demais estados em MERGE são iguais aos de RIGHT para o retorno e aos de LEFT para os efeitos colaterais. Nada é perdido.
   - (C) o código de RIGHT (return e loop em emit()) depende de o método emitir ou não. Essa condição é controlada pelo mesmo predicado que no LEFT, e o comportamento em MERGE é idêntico ao de RIGHT. O código de LEFT não lê o retorno.
   - Há uma pequena diferença em RIGHT, em que `retryService.isReady` é chamado de novo para decidir o remove. Em MERGE a chamada é substituída por isScheduled, como em LEFT. Não há interferência indesejada.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): NO</summary>

1. INTENÇÃO: LEFT extrai a variável isScheduled no else-if final de emitTupleIfNotEmitted. A condição de retryService.remove(msgId) muda de isReady(msgId) para isScheduled. RIGHT muda o retorno do método para boolean (true se emitiu, false caso contrário) e altera emit() para usar esse retorno em um loop.

2. ESTADO: O valor de retorno de emitTupleIfNotEmitted, os conjuntos emitted e retryService (remove), o contador numUncommittedOffsets e o iterador waitingToEmit, que é alterado por emit().

3. TABELA DE ESTADOS:
   - Entrada: record já falhado e agendado para retry, e pronto (isScheduled = true, isReady = true), ainda não emitido nem acked.
   - Retorno: BASE = void | LEFT = void | RIGHT = true | MERGE = true.
   - emitted: BASE = {msgId} | LEFT = {msgId} | RIGHT = {msgId} | MERGE = {msgId}.
   - retryService (remove): BASE = removido | LEFT = removido | RIGHT = removido | MERGE = removido.
   - Entrada 2: record não agendado (isScheduled = false), que será emitido.
   - Retorno: RIGHT = true | MERGE = true.
   - Entrada 3: record já emitido. Retorno: RIGHT = false | MERGE = false.
   - Entrada 4: record agendado mas não pronto. Retorno: RIGHT = false | MERGE = false, pois o return true está dentro do if (!isScheduled || isReady) e o return false final cobre o resto.
   - O merge reestruturou o bloco: o return true foi colocado dentro do if interno e o return false fica no final, após o else. Isso preserva o comportamento do RIGHT em todos os caminhos: acked → false, emitted → false, emissão → true, não pronto → false.
   - Em emit(), o loop é idêntico ao de RIGHT.

4. CRITÉRIO DE CONFLITO:
   - (A) não se aplica: os valores diferem de BASE em pelo menos um dos pais, ou o MERGE é igual a eles.
   - (B) o retorno do MERGE é igual ao de RIGHT em todos os caminhos, e os efeitos de LEFT (remove condicionado a isScheduled) são preservados.
   - (C) o código de RIGHT (returns) não lê as variáveis alteradas por LEFT de forma que mude seu comportamento. O return true só é alcançado quando houve emissão, o que continua valendo no MERGE. O loop em emit() depende do retorno, que tem a mesma semântica de RIGHT. Na prática, a mudança de LEFT (isReady → isScheduled na remoção) não interfere nos returns.

</details>

#### claude-haiku-5-5: YES ❌

<details><summary>Execução 1 (<code>1.csv</code>): YES — Condição C: emitted (conjunto de msgIds, via retorno de emitTupleIfNotEmitted e laço de emit())</summary>

1. INTENÇÃO: Confirmada pelos diffs. LEFT extrai `isScheduled` em `emitTupleIfNotEmitted` (else em vez de else-if) e troca a condição de `retryService.remove` de `isReady` para `isScheduled`. Também altera `initialize()` (remove de `emitted` os msgIds de partições não reatribuídas), `ack()` e `fail()`. RIGHT faz `emitTupleIfNotEmitted` retornar `boolean`, troca `emit()` por um laço `while` que avança enquanto o retorno for `false`, e altera `doSeekRetriableTopicPartitions`, `shutdown`, `OffsetEntry` e `findNextCommitOffset`.

2. ESTADO: Escritos pelo TARGET e pelos trechos alterados:
   - `emitted` (Set de msgIds), escrito por `emitTupleIfNotEmitted` (LEFT e BASE) e por `initialize`, `ack` e `fail` (LEFT).
   - `retryService` (agendamento), escrito por `emitTupleIfNotEmitted` (remove).
   - `numUncommittedOffsets`, escrito por `emitTupleIfNotEmitted`.
   - Valor de retorno de `emitTupleIfNotEmitted` (novo em RIGHT), lido pelo laço de `emit()`.
   - `waitingToEmit`, consumido por `emit()`.

3. TABELA DE ESTADOS: Cenário: o msgId m do registro r foi emitido antes. Depois, a partição de r é revogada e atribuída a outro spout. Então `onPartitionsAssigned` roda sem essa partição, e `r` ainda está em `waitingToEmit`. Em seguida, `nextTuple()` chama `emit()`.
   - `emitted` contém m (antes do emit): BASE = sim | LEFT = não (removido por `initialize`) | RIGHT = sim | MERGE = não
   - Retorno de `emitTupleIfNotEmitted(r)`: BASE = (void) | LEFT = (void) | RIGHT = false (ramo "já emitido") | MERGE = true (emitido)
   - Tupla emitida por `emit()`: BASE = nenhuma | LEFT = r | RIGHT = nenhuma (laço avança para o próximo registro) | MERGE = r
   - `numUncommittedOffsets`: BASE = n | LEFT = n+1 | RIGHT = n | MERGE = n+1
   - `retryService` (m agendado?): BASE = não | LEFT = não | RIGHT = não | MERGE = não

4. CRITÉRIO DE CONFLITO: X = `emitted`.
   - (A) não se aplica: `emitted` difere de BASE em LEFT, e o MERGE é igual a LEFT.
   - (B) `emitted` em LEFT (não contém m) difere de BASE (contém m). O MERGE (não contém m) preserva o valor de LEFT. Não há violação de B.
   - (C) `emitted` difere de BASE em LEFT. O código alterado por RIGHT (o laço `while` de `emit()`) é controlado por esse valor, pois seu fluxo depende do retorno de `emitTupleIfNotEmitted`, que depende de `emitted.contains(msgId)`. Na entrada escolhida, RIGHT isolado não emite r (o laço avança), enquanto no MERGE r é emitido e o laço para. O código de RIGHT se comporta de forma diferente no MERGE do que no pai que o escreveu. Logo, C se aplica.

   Os demais candidatos não geram conflito:
   - `retryService`: LEFT troca a condição de remove. Como a remoção só ocorre dentro do ramo que já exige `!isScheduled || isReady`, a troca é equivalente, e RIGHT não lê esse estado.
   - Valor de retorno: é um valor novo de RIGHT, não escrito por LEFT.
   - `numUncommittedOffsets`: LEFT e RIGHT não se sobrepõem nele, e o MERGE é igual a LEFT (+1).

   Conclusão: existe conflito pela condição C envolvendo `emitted`.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): YES — Condição C: emitted</summary>

1. INTENÇÃO: O resumo de LEFT ("refatoração extraindo uma variável de um IF e alterando outra condição de IF") está incompleto. O diff de LEFT extrai `isScheduled` em `emitTupleIfNotEmitted`, mas também altera o estado de `emitted`: `initialize` remove de `emitted` os msgIds de partições que não estão mais atribuídas, `ack` ignora msgIds não rastreados e `fail` só remove de `emitted` quando há retry. O resumo de RIGHT está correto: muda `emit()` e `emitTupleIfNotEmitted` para retornar `boolean`, com um laço que descarta registros até um ser emitido. Ambos os lados também fazem outras mudanças fora do método alvo, que não entram nesta análise.

2. ESTADO: O TARGET `emitTupleIfNotEmitted` escreve `emitted`, `numUncommittedOffsets`, o agendamento do `retryService` e o valor de retorno (novo em RIGHT e presente no MERGE). Os trechos alterados escrevem `emitted` (LEFT, em `initialize`, `ack`, `fail`), `retryService` (LEFT, em `fail` e no `remove` condicionado a `isScheduled`) e o `waitingToEmit` (RIGHT, em `emit`). Como `emitTupleIfNotEmitted` lê `emitted` (`emitted.contains(msgId)`) e o código de RIGHT depende do retorno desse método, `emitted` é o elemento de estado relevante.

3. TABELA DE ESTADOS:
   Cenário: a partição P0 tem o registro r1 já emitido (`emitted = {r1}`). P0 é revogada e reatribuída ao mesmo spout, e r1 é pollado novamente (`waitingToEmit` contém r1).
   - `emitted` após `initialize(partitions)` sem P0: BASE = {r1} | LEFT = {} | RIGHT = {r1} | MERGE = {}
   - Retorno de `emitTupleIfNotEmitted(r1)` (valor usado pelo laço de `emit()` de RIGHT): BASE = n/a (void) | LEFT = n/a (void) | RIGHT = false (r1 é descartado) | MERGE = true (r1 é emitido)
   - Tuplas emitidas nesse passo: BASE = 0 | LEFT = 1 | RIGHT = 0 | MERGE = 1

   Verificação da equivalência interna de LEFT: `if (isScheduled) remove` equivale a `if (isReady) remove` dentro do ramo, porque `isReady` implica `isScheduled`. Por isso a extração da variável não altera o comportamento de `emitTupleIfNotEmitted` por si só.

4. CRITÉRIO DE CONFLITO: X = `emitted`.
   - (A) Não se aplica: `emitted` muda em LEFT, então não é igual nas três versões de BASE, LEFT e RIGHT.
   - (B) LEFT altera `emitted` ({} ≠ {r1}) e o MERGE ({}) preserva o valor de LEFT. RIGHT não altera `emitted`, então (B) não se aplica a RIGHT. Para LEFT, a condição não é violada.
   - (C) LEFT altera `emitted`, e o código alterado por RIGHT (`emitTupleIfNotEmitted`, via `emitted.contains` e o retorno consumido por `emit()`) lê esse valor. No MERGE, esse código se comporta de forma diferente do pai RIGHT: em RIGHT, r1 é descartado como já emitido; no MERGE, r1 é emitido novamente. A interferência é real, mesmo que a mudança de LEFT pareça intencional, porque o laço de RIGHT deixa de funcionar como o desenvolvedor de RIGHT pretendia.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): YES — Condição C: emitted</summary>

1. INTENÇÃO: LEFT extrai a variável `isScheduled` em `emitTupleIfNotEmitted()`, usa-a para decidir o `retryService.remove()`, e adiciona em `initialize()` a remoção de `emitted` para partições que deixaram de ser atribuídas. RIGHT faz `emitTupleIfNotEmitted()` retornar `boolean` e altera `emit()` para pular registros não emitidos. O resumo de RIGHT não menciona o retorno booleano nem o `emit()`, mas o diff confirma essas mudanças, então confio no diff.

2. ESTADO: Escritos pelo TARGET e pelos trechos alterados:
   - `emitted` (Set de msgId): lido por `emitTupleIfNotEmitted()` (`emitted.contains`) e escrito por `emitted.add` (no target), por `emitted.removeIf` (LEFT, em `initialize()`), por `ack` e `fail` (LEFT).
   - `retryService` (estado de agendamento): lido e escrito pelo target.
   - Valor de retorno de `emitTupleIfNotEmitted()`: void em BASE e LEFT, boolean em RIGHT e MERGE.
   - `waitingToEmit` (iterador): consumido por `emit()` (RIGHT).

3. TABELA DE ESTADOS: Cenário: a partição P é revogada e reatribuída. O registro r (offset 5) já tinha sido emitido antes da revogação e é lido novamente no poll seguinte. Não há retry agendado.
   - `emitted.contains(r)` após `initialize()`: BASE = true | LEFT = false | RIGHT = true | MERGE = false
   - Comportamento de `emitTupleIfNotEmitted(r)`:
     - BASE: pula (já emitido), sem retorno (void)
     - LEFT: emite (não está em `emitted`), void
     - RIGHT: pula, retorna false
     - MERGE: emite, retorna true
   - Retorno de `emitTupleIfNotEmitted` em MERGE = true, não é uma função de `emitted` que RIGHT tenha definido para este cenário.

4. CRITÉRIO DE CONFLITO: X = `emitted` (o conjunto inteiro).
   - (A) não se aplica: `emitted` em LEFT (false) difere de BASE (true), então X não é igual nos três.
   - (B) não se aplica: `emitted` em LEFT difere de BASE, e o MERGE (false) é igual a LEFT, então LEFT é preservado. Para RIGHT, `emitted` é igual a BASE, então não há condição de B para RIGHT.
   - (C) se aplica: `emitted` em LEFT difere de BASE (LEFT escreveu X). O código alterado por RIGHT, `emitTupleIfNotEmitted()`, lê X via `emitted.contains(msgId)`. No MERGE, esse código emite o registro r e retorna true, enquanto no pai RIGHT, que o escreveu, ele pula r e retorna false. Logo, o código alterado por RIGHT se comporta no MERGE de forma diferente do pai que o escreveu.

   Demais elementos (`retryService`, `isScheduled`, retorno booleano, `waitingToEmit`): o refatoramento do `isScheduled` é equivalente, porque `isReady` implica `isScheduled` e nenhum estado muda entre as leituras. A estrutura de retornos do merge está correta. Não há conflito de (A), (B) ou (C) para esses elementos. O conflito é apenas o de (C) sobre `emitted`.

</details>

### 12. `activiti__bf46684b__UserTaskActivityBehavior#execute`

- **Target:** `execute(ActivityExecution)`
- **Esperado:** NO; **acertam:** claude-opus-5-5, claude-sonnet-5-5; **erram:** claude-haiku-5-5
- **Código:** [activiti__bf46684b__UserTaskActivityBehavior](../../data/mergedataset/activiti__bf46684b__UserTaskActivityBehavior)

**LEFT:** Left adds a new IF statement, which may set the field formKey of the local variable formKey, or throws an exception.

**RIGHT:** Right adds a new IF statement, which may call static external methods without using their returns.

**Justificativa do dataset:** There is no locally observable interference as the Right changes do not trhows any exception, otherwise it could represent an interference with Left changes.

#### claude-opus-5-5: NO ✅

<details><summary>Execução 1 (<code>1.csv</code>): NO</summary>

1. INTENÇÃO:
   - **LEFT**: adiciona um bloco que avalia `getFormKeyExpression()`. Se o valor for uma String, grava em `task.formKey`; se for não nulo e de outro tipo, lança `ActivitiIllegalArgumentException`. Também reordena os imports, sem efeito no comportamento.
   - **RIGHT**: antes de `task.fireEvent(EVENTNAME_CREATE)`, despacha um evento `TASK_CREATED` com a entidade `task`, desde que o event dispatcher esteja habilitado.
   - Os diffs confirmam os resumos. O MERGE contém as duas mudanças: o bloco de formKey fica antes de `handleAssignments`, e o dispatch fica depois.

2. ESTADO:
   - `task.formKey`, escrito por LEFT.
   - A exceção lançada por `execute()`, nova em LEFT.
   - O evento despachado pelo dispatcher, ou seja, a fila de eventos (tipo e entidade referenciada), escrito por RIGHT.
   - Os demais campos de `task` (name, description, dueDate, priority, category, assignee, candidatos) não são alterados por nenhum dos lados.

3. TABELA DE ESTADOS:
   - Entrada: `formKeyExpression` resolve para "myForm", dispatcher habilitado.
     - `task.formKey`: BASE = null | LEFT = "myForm" | RIGHT = null | MERGE = "myForm"
     - Eventos despachados: BASE = nenhum | LEFT = nenhum | RIGHT = [TASK_CREATED(task)] | MERGE = [TASK_CREATED(task)]
     - Exceção: nenhuma nas quatro versões.
   - Entrada 2: `formKeyExpression` resolve para um Integer, dispatcher habilitado.
     - Exceção: BASE = nenhuma | LEFT = ActivitiIllegalArgumentException | RIGHT = nenhuma | MERGE = ActivitiIllegalArgumentException
     - Eventos: BASE = nenhum | LEFT = nenhum | RIGHT = [TASK_CREATED] | MERGE = nenhum
     - Na prática essa entrada não ocorre, porque o cast `(String)` lançaria ClassCastException antes do check. Isso vale igualmente em LEFT e em MERGE.

4. CRITÉRIO DE CONFLITO:
   - **(A)** Não se aplica. Nenhum elemento tem o mesmo valor em BASE, LEFT e RIGHT e um valor diferente em MERGE.
   - **(B)** `task.formKey` de LEFT ("myForm") é preservado no MERGE. Os eventos despachados por RIGHT (TASK_CREATED com a entidade `task`) também são preservados: mesmo tipo e mesma entidade. A exceção de LEFT é preservada no MERGE. Na entrada 2, o fato de nenhum evento ser despachado decorre da exceção de LEFT, preservada como LEFT pretendia. Isso já ocorria em BASE com qualquer exceção lançada antes desse ponto.
   - **(C)** O código de RIGHT não lê `formKey`. Ele apenas passa a referência de `task` para o evento, assim como `task.fireEvent` já fazia em BASE e em LEFT. O código de LEFT não lê o estado do dispatcher. O preenchimento de formKey antes da notificação segue a convenção já existente ("All properties set").

</details>

#### claude-sonnet-5-5: NO ✅

<details><summary>Execução 1 (<code>1.csv</code>): NO</summary>

1. INTENÇÃO: LEFT adiciona um bloco que avalia a expressão formKey e chama task.setFormKey(...) com o resultado, ou lança exceção se o valor não for String. RIGHT adiciona, antes de task.fireEvent(CREATE), o despacho de um evento TASK_CREATED pelo event dispatcher, caso ele esteja habilitado. O diff confirma ambos os resumos. O resumo de RIGHT fala em métodos estáticos externos cujo retorno não é usado, mas o diff mostra que a task é passada como argumento ao evento.

2. ESTADO:
   - task.formKey, escrito por setFormKey (LEFT).
   - A exceção lançada se formKey não for String (LEFT).
   - O evento despachado ao event dispatcher, que carrega a task como entidade (RIGHT).
   - Os listeners disparados por task.fireEvent(CREATE), que leem a task (comum).

3. TABELA DE ESTADOS:
   - Entrada: taskDefinition com formKeyExpression = "form1" e dispatcher habilitado.
   - task.formKey: BASE = null | LEFT = "form1" | RIGHT = null | MERGE = "form1"
   - Evento TASK_CREATED despachado: BASE = nenhum | LEFT = nenhum | RIGHT = despachado com task.formKey = null | MERGE = despachado com task.formKey = "form1"
   - Exceção: não há mudança de comportamento em nenhum dos cenários.

4. CRITÉRIO DE CONFLITO:
   - (A) não se aplica: task.formKey muda em LEFT e no MERGE, mas não é igual em BASE, LEFT e RIGHT.
   - (B) o valor de task.formKey em LEFT ("form1") é preservado no MERGE. O evento de RIGHT existe no MERGE. O conteúdo do evento, a task, difere de RIGHT apenas porque agora possui formKey, que é o objetivo de LEFT.
   - (C) o código novo de RIGHT lê a task, que contém formKey, escrito por LEFT. Mas o formKey está definido antes do despacho, que é o comportamento desejado: o evento TASK_CREATED é disparado com a task completamente inicializada, como o comentário "All properties set" indica. Ele não é controlado por formKey, e a leitura apenas observa um estado mais completo, sem interferência indesejada. Nenhum dos lados escreve algo que o outro lê de forma incompatível com a sua intenção. A exceção de LEFT também não interfere no código de RIGHT: ela apenas impede o despacho, o que é coerente com o comportamento de falha de BASE.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): NO</summary>

1. INTENÇÃO: LEFT adiciona um bloco que avalia a expressão formKey e chama task.setFormKey(...) com o resultado, ou lança exceção se o valor não for String. RIGHT adiciona, antes de task.fireEvent(CREATE), o despacho de um evento TASK_CREATED pelo event dispatcher, caso esteja habilitado. O resultado do despacho não é usado. Os diffs confirmam os resumos.

2. ESTADO:
   - task.formKey, escrito por LEFT via task.setFormKey.
   - A exceção lançada por LEFT, quando o formKey não é String.
   - A variável local formKey.
   - O estado interno do event dispatcher e dos listeners, escrito por RIGHT ao despachar TASK_CREATED.
   - O objeto task, lido por RIGHT em createEntityEvent(TASK_CREATED, task).
   - Os efeitos de task.fireEvent(CREATE), que lê o estado de task.

3. TABELA DE ESTADOS:
   - Entrada: formKeyExpression avalia para "form1" e o dispatcher está habilitado.
   - task.formKey: BASE = null | LEFT = "form1" | RIGHT = null | MERGE = "form1"
   - Evento TASK_CREATED despachado: BASE = não | LEFT = não | RIGHT = sim (task.formKey = null no evento) | MERGE = sim (task.formKey = "form1" no evento)
   - Efeitos de fireEvent(CREATE): BASE = task sem formKey | LEFT = task com formKey "form1" | RIGHT = task sem formKey | MERGE = task com formKey "form1"
   - Exceção, com formKey não String: BASE = nenhuma | LEFT = ActivitiIllegalArgumentException | RIGHT = nenhuma | MERGE = ActivitiIllegalArgumentException (lançada antes do despacho, como em LEFT)

4. CRITÉRIO DE CONFLITO:
   - (A) não se aplica: nenhum valor muda no MERGE sem ter mudado em LEFT ou RIGHT.
   - (B) task.formKey em LEFT ("form1") é preservado no MERGE. O evento despachado em RIGHT existe no MERGE. A exceção de LEFT é preservada. Todos os valores são preservados.
   - (C) o código de RIGHT lê task ao criar o evento e dispara listeners, e task.formKey foi alterado por LEFT. No entanto, o código de RIGHT não é controlado por formKey, e o evento é apenas uma notificação de criação da tarefa. No MERGE, o evento carrega a tarefa já com formKey definido, que é justamente o estado completo ("All properties set") que RIGHT pretendia notificar. Não há comportamento divergente do pai que o escreveu: RIGHT não depende do valor de formKey, e LEFT não lê nada escrito por RIGHT. Além disso, o despacho ocorre depois do setFormKey, o que é a ordem desejada.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): NO</summary>

1. INTENÇÃO: LEFT adiciona um bloco que lê a expressão formKey e chama task.setFormKey(...), ou lança uma exceção se o valor não for String. RIGHT adiciona, antes de task.fireEvent(CREATE), o despacho de um evento TASK_CREATED via EventDispatcher, quando este está habilitado. Os diffs confirmam os resumos. O resumo de RIGHT fala em chamadas estáticas sem uso do retorno, e isso coincide com a chamada de dispatchEvent e o uso de ActivitiEventBuilder.createEntityEvent.

2. ESTADO:
   - task.formKey, escrito por LEFT.
   - A exceção lançada por LEFT quando o valor não é String.
   - O estado interno do EventDispatcher (eventos despachados e listeners notificados), escrito por RIGHT.
   - O evento TASK_CREATED, que carrega a referência a task.
   - O estado de task, lido por createEntityEvent e pelos listeners.

3. TABELA DE ESTADOS:
   - Entrada: formKeyExpression retorna "form1" e o dispatcher está habilitado.
   - task.formKey: BASE = null | LEFT = "form1" | RIGHT = null | MERGE = "form1".
   - Evento TASK_CREATED despachado: BASE = não | LEFT = não | RIGHT = sim | MERGE = sim.
   - Estado de task visto pelo evento TASK_CREATED: em RIGHT, formKey = null; no MERGE, formKey = "form1". Os listeners recebem a referência ao objeto task, que já tem o formKey definido.
   - Exceção, com formKey não String: BASE = nenhuma | LEFT = ActivitiIllegalArgumentException | RIGHT = nenhuma | MERGE = ActivitiIllegalArgumentException. O evento não é despachado no MERGE, porque a exceção ocorre antes. Isso é consistente com LEFT.

4. CRITÉRIO DE CONFLITO:
   - (A) não se aplica: nenhum valor muda no MERGE sem ter mudado em LEFT ou RIGHT.
   - (B) o MERGE preserva task.formKey de LEFT, e preserva o evento despachado de RIGHT.
   - (C) o código de RIGHT lê task, mas apenas a passa como referência ao evento. O despacho não depende do formKey para decidir se ocorre, e a lógica de RIGHT se comporta igual. Que os listeners vejam o formKey definido é o comportamento desejável e esperado, porque o evento é disparado depois de todas as propriedades estarem definidas, como diz o comentário "All properties set". Esse formKey adicional no estado de task não faz o código de RIGHT se comportar de modo diferente do que ele pretendia. As escritas de LEFT não são lidas por nenhuma condição de RIGHT, e RIGHT não escreve nada que LEFT leia.
   - Não há interferência indesejada entre as mudanças.

</details>

#### claude-haiku-5-5: YES ❌

<details><summary>Execução 1 (<code>1.csv</code>): YES — Condição C: task.formKey (payload do evento TASK_CREATED)</summary>

1. INTENÇÃO: LEFT adiciona um bloco que lê a expressão de formKey, grava `task.setFormKey(...)` quando o valor não é nulo, e lança exceção quando o tipo não é String. RIGHT adiciona um bloco que, se o dispatcher de eventos estiver habilitado, despacha `TASK_CREATED` com a entidade `task`, antes de `task.fireEvent(...)`. Os diffs confirmam os resumos. Os imports são reorganizados de forma compatível, sem efeito semântico.

2. ESTADO:
   - `task.formKey`, escrito por LEFT via `setFormKey` e lido pelo evento de RIGHT, porque a entidade `task` é o payload de `TASK_CREATED`.
   - O canal de saída do evento `TASK_CREATED`, escrito por RIGHT e cujo conteúdo depende de `task`.
   - A execução do método, pois a exceção lançada por LEFT controla se o dispatch de RIGHT é alcançado.

3. TABELA DE ESTADOS:
   Entrada: `getFormKeyExpression().getValue(execution)` = "form1"; dispatcher habilitado; `getExpressionText()` não é usado no caminho feliz.
   - `task.formKey`: BASE = null | LEFT = "form1" | RIGHT = null | MERGE = "form1"
   - Eventos despachados: BASE = nenhum | LEFT = nenhum | RIGHT = [TASK_CREATED(task com formKey = null)] | MERGE = [TASK_CREATED(task com formKey = "form1")]
   - Caminho com exceção (valor não-String): LEFT lança antes do dispatch; no MERGE o dispatch de RIGHT é ignorado, enquanto em RIGHT isolado ele ocorreria.

4. CRITÉRIO DE CONFLITO: X = `task.formKey` (e o evento `TASK_CREATED` que carrega `task`).
   - (A) não se aplica: X muda em LEFT, então não é igual nos três.
   - (B) o valor de X em LEFT ("form1") difere de BASE (null), e o MERGE preserva LEFT ("form1"). O valor de X em RIGHT (null) difere de BASE e não é preservado no MERGE ("form1"), porém RIGHT não alterou X diretamente, então B se aplica apenas a LEFT, que é preservado. B não é a condição decisiva.
   - (C) o valor de `task.formKey` em LEFT difere de BASE. O código adicionado por RIGHT (o dispatch de `TASK_CREATED`) lê `task`, e seu payload depende de `task.formKey`. No MERGE, o evento carrega formKey = "form1", enquanto em RIGHT isolado ele carrega null. Além disso, a exceção de LEFT controla se o dispatch de RIGHT ocorre. O comportamento do código de RIGHT muda no MERGE em relação ao pai que o escreveu. Logo, C se aplica.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): YES — Condição C: exceção lançada (o bloco de formKey de LEFT pode lançar exceção antes do despacho do evento TASK_CREATED de RIGHT, alterando se esse código executa)</summary>

1. INTENÇÃO: LEFT adiciona um bloco que lê a expressão de formKey, define `task.setFormKey(...)` quando o valor não é nulo e lança `ActivitiIllegalArgumentException` quando o valor não é String. RIGHT adiciona, antes de `task.fireEvent(EVENTNAME_CREATE)`, um despacho do evento `TASK_CREATED` quando o dispatcher está habilitado. Os resumos conferem com os diffs. Observação: o cast `(String)` na linha de LEFT já lança `ClassCastException` para valores não-String, antes do próprio `instanceof`.

2. ESTADO: Elementos escritos pelos trechos alterados:
   - `task.formKey`, escrito por LEFT.
   - A exceção lançada por `execute()`, que LEFT pode produzir.
   - O evento `TASK_CREATED` despachado para o dispatcher, escrito por RIGHT.
   - O estado do próprio `task`, usado pelo evento.

3. TABELA DE ESTADOS:
   Entrada: `formKeyExpression != null`, `getValue(execution)` retorna `Integer 5` (não-String, não-nulo), dispatcher habilitado.
   - Exceção lançada: BASE = nenhuma | LEFT = `ClassCastException` no cast | RIGHT = nenhuma | MERGE = `ClassCastException` no cast
   - `TASK_CREATED` despachado: BASE = não | LEFT = não (LEFT não contém o bloco de dispatch) | RIGHT = sim | MERGE = não
   - `fireEvent(CREATE)` executado: BASE = sim | LEFT = sim (no caso sem exceção, sim; neste caso de entrada a exceção impede a chegada até ele, então não) | RIGHT = sim | MERGE = não
   - `task.formKey`: BASE = não definido | LEFT = não definido (exceção antes do setFormKey) | RIGHT = não definido | MERGE = não definido

   Como LEFT lança a exceção antes de chegar ao ponto onde RIGHT insere o dispatch, o fluxo de controle do código de RIGHT muda no MERGE.

4. CRITÉRIO DE CONFLITO: X = exceção lançada.
   - (A) não se aplica: no MERGE, a exceção só aparece nas entradas em que LEFT a lança, então o valor de X muda em relação a LEFT/RIGHT, não apenas em MERGE.
   - (B) o valor de X em LEFT difere de BASE (LEFT lança exceção, BASE não), e o MERGE é igual a LEFT nesta entrada, então LEFT é preservado. Já o valor de X em RIGHT é igual ao de BASE (nenhuma exceção), e o MERGE não é igual a RIGHT nesta entrada. Isso não gera B para RIGHT porque X em RIGHT não difere de BASE.
   - (C) o valor de X em LEFT difere de BASE, e o código adicionado por RIGHT (o despacho de `TASK_CREATED`) é controlado por X: ele só é alcançado se o bloco de LEFT não lançar exceção. No MERGE, para essa entrada, o despacho não ocorre, enquanto em RIGHT ele ocorre. O código de RIGHT se comporta de forma diferente no MERGE, o que caracteriza interferência de controle.

   Condição C se aplica. Também há uma dependência de dados secundária: o evento é criado a partir de `task`, que LEFT altera com `setFormKey`, mas o caso de exceção já basta para configurar a condição.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): YES — Condição C: task.formKey</summary>

1. INTENÇÃO: LEFT adiciona, antes de handleAssignments(), a leitura da expressão de formKey e chama task.setFormKey(). RIGHT adiciona, após handleAssignments() e antes de fireEvent(create), o disparo de um evento TASK_CREATED com a entidade task. Os diffs confirmam os resumos. No diff de LEFT, a variável formKey é declarada com cast para String, então a exceção ActivitiIllegalArgumentException do ramo else é inalcançável para valores que não sejam String.

2. ESTADO:
   - task.formKey: escrito por task.setFormKey() em LEFT.
   - Exceção lançada por LEFT (ActivitiIllegalArgumentException, ou ClassCastException pelo cast) quando a expressão não resolve para String.
   - Payload do evento TASK_CREATED: construído por RIGHT a partir da entidade task, portanto lê o estado de task, incluindo formKey.
   - Variável local formKey: existe apenas em LEFT.

3. TABELA DE ESTADOS:
   Entrada: formKeyExpression não nula, avalia para "form.html"; dispatcher habilitado.
   - task.formKey: BASE = null | LEFT = "form.html" | RIGHT = null | MERGE = "form.html"
   - Payload de TASK_CREATED (task.formKey no momento do disparo): BASE = evento não existe | LEFT = evento não existe | RIGHT = null | MERGE = "form.html"
   - Exceção: BASE = nenhuma | LEFT = nenhuma (entrada válida) | RIGHT = nenhuma | MERGE = nenhuma (entrada válida)
   - Para a entrada inválida (expressão não resolve para String): LEFT lança exceção; MERGE lança a mesma exceção antes do disparo do evento, então o evento de RIGHT não ocorre no MERGE, enquanto em RIGHT ele ocorreria.

4. CRITÉRIO DE CONFLITO: X = task.formKey.
   - (A) não se aplica: o valor de task.formKey muda em LEFT em relação a BASE.
   - (B) o valor de task.formKey em LEFT ("form.html") difere de BASE, e o MERGE ("form.html") o preserva. Não há violação de B para este X.
   - (C) o valor de task.formKey em LEFT difere de BASE, e o código adicionado por RIGHT (o disparo do evento TASK_CREATED com a entidade task) lê esse estado. Em RIGHT, o evento carrega formKey = null. No MERGE, o mesmo evento carrega formKey = "form.html". O código de RIGHT se comporta de forma diferente no MERGE, então a condição C se aplica.
   - Há um segundo caso de C: a exceção lançada por LEFT controla se o disparo de RIGHT é executado no MERGE, mas o caso principal é o formKey, pois ele já altera o payload de RIGHT em uma entrada válida.

   Conclusão: existe conflito semântico pela condição C, sobre task.formKey.

</details>

### 13. `spring-boot__ea8107b6__UndertowEmbeddedServletContainerFactory#createDeploymentManager`

- **Target:** `createDeploymentManager(ServletContextInitializer)`
- **Esperado:** NO; **acertam:** claude-opus-5-5, claude-sonnet-5-5; **erram:** claude-haiku-5-5
- **Código:** [spring-boot__ea8107b6__UndertowEmbeddedServletContainerFactory](../../data/mergedataset/spring-boot__ea8107b6__UndertowEmbeddedServletContainerFactory)

**LEFT:** Left sets one attribute of object deployment, which is used to create the returned method object manager.

**RIGHT:** Right modifies the way the returned manager object is created; before, it was done by calling the method defaultContainer from Servlets, and now it’s done by calling the method newContainer.

**Justificativa do dataset:** There is no locally observable interference as the changes performed by Right still return an object with same behavior when compared to base.

#### claude-opus-5-5: NO ✅

<details><summary>Execução 1 (<code>1.csv</code>): NO</summary>

1. INTENÇÃO:
   - **LEFT**: em `createDeploymentManager`, LEFT faz três coisas antes de criar o manager:
     - adiciona `deployment.setDisplayName(getDisplayName())`;
     - configura o access log (`addInitialHandlerChainWrapper`) quando `isAccessLogEnabled()`;
     - configura a persistência de sessão (`setSessionPersistenceManager`) quando `isPersistSession()`.
   - O container continua sendo `Servlets.defaultContainer()`.
   - **RIGHT**: troca apenas `Servlets.defaultContainer()` por `Servlets.newContainer()` na criação do manager. O `DeploymentInfo` não é alterado.
   - Os diffs confirmam os dois resumos.

2. ESTADO:
   - O objeto `deployment` (DeploymentInfo). LEFT escreve nele os atributos displayName, initialHandlerChainWrappers e sessionPersistenceManager.
   - O container Servlet ao qual o deployment é adicionado. RIGHT o altera: em vez do container default (singleton compartilhado), passa a usar um container novo.
   - O `manager` retornado, derivado de ambos.
   - O `sessionManager` com o timeout, que nenhum dos lados alterou.

3. TABELA DE ESTADOS:
   - Entrada: displayName = "app", accessLogEnabled = true (diretório válido), persistSession = false, sessionTimeout = 30.
   - deployment.displayName: BASE = null | LEFT = "app" | RIGHT = null | MERGE = "app"
   - deployment.initialHandlerChainWrappers: BASE = [] | LEFT = [AccessLogWrapper] | RIGHT = [] | MERGE = [AccessLogWrapper]
   - container do manager: BASE = defaultContainer (compartilhado) | LEFT = defaultContainer | RIGHT = novo container isolado | MERGE = novo container isolado
   - manager retornado:
     - BASE: deployment sem os novos atributos, no container default;
     - LEFT: deployment com "app" e access log, no container default;
     - RIGHT: deployment sem os novos atributos, em um novo container;
     - MERGE: deployment com "app" e access log, em um novo container.
   - sessionTimeout: 30 em todas as versões.

4. CRITÉRIO DE CONFLITO:
   - **(A)** Não se aplica. Os únicos elementos que mudam no MERGE são os que já mudaram em LEFT ou em RIGHT. O sessionTimeout é igual em todas as versões.
   - **(B)** Não se aplica.
     - Os atributos do deployment alterados por LEFT têm no MERGE os mesmos valores de LEFT.
     - O container alterado por RIGHT tem no MERGE o mesmo valor de RIGHT (newContainer).
   - **(C)** Não se aplica.
     - O código de RIGHT (`newContainer().addDeployment(deployment)`) lê `deployment`. Porém, a escolha entre container novo e container default não depende de displayName, do access log nem da persistência de sessão. O deployment é registrado num container isolado da mesma forma que em RIGHT.
     - O código de LEFT não lê nem é controlado pelo container escolhido, porque roda antes da criação do container.
     - As duas mudanças compõem-se de forma independente.

</details>

#### claude-sonnet-5-5: NO ✅

<details><summary>Execução 1 (<code>1.csv</code>): NO</summary>

1. INTENÇÃO: O resumo de LEFT diz que ele define um atributo do deployment. O diff mostra mais que isso: LEFT adiciona deployment.setDisplayName(getDisplayName()), o bloco de access log, e o bloco setSessionPersistenceManager condicionado a isPersistSession(). Todas essas mudanças ocorrem antes de Servlets.defaultContainer().addDeployment(deployment). RIGHT troca Servlets.defaultContainer() por Servlets.newContainer() na criação do manager.

2. ESTADO: Os elementos escritos são o objeto deployment (displayName, initial handler chain wrapper, sessionPersistenceManager), o manager criado a partir do container e o valor retornado por createDeploymentManager. O sessionManager também é escrito, com o timeout padrão.

3. TABELA DE ESTADOS:
   - Entrada: access log habilitado, persistSession true, displayName "app".
   - deployment.displayName: BASE = null | LEFT = "app" | RIGHT = null | MERGE = "app"
   - deployment.sessionPersistenceManager: BASE = null | LEFT = FileSessionPersistence | RIGHT = null | MERGE = FileSessionPersistence
   - deployment.initialHandlerChainWrapper: BASE = nenhum | LEFT = access log | RIGHT = nenhum | MERGE = access log
   - container que cria o manager: BASE = defaultContainer (compartilhado) | LEFT = defaultContainer | RIGHT = newContainer | MERGE = newContainer
   - manager retornado: BASE = deployment registrado no container default | LEFT = deployment com os atributos extras, no container default | RIGHT = deployment sem os atributos extras, em um container novo | MERGE = deployment com os atributos extras, em um container novo

4. CRITÉRIO DE CONFLITO:
   - (A) não se aplica: nenhum elemento é igual em BASE, LEFT e RIGHT e diferente em MERGE.
   - (B) o MERGE preserva os atributos de deployment de LEFT e o container de RIGHT.
   - (C) o código de RIGHT, addDeployment(deployment) em um novo container, lê o deployment configurado por LEFT. Ele o recebe da mesma forma que no BASE: apenas registra o deployment e o implanta. A diferença entre os containers (compartilhado ou novo) não altera a leitura dos atributos adicionados por LEFT. Do lado de LEFT, a configuração do deployment não lê nenhum estado do container. O retorno é o manager, que combina as duas mudanças de forma independente. Não há dependência de dados ou de controle que mude o comportamento no MERGE em relação ao pai que escreveu o valor.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): NO</summary>

1. INTENÇÃO: Confirmando nos diffs, LEFT faz mais do que o resumo indica. Dentro de createDeploymentManager, adiciona deployment.setDisplayName(getDisplayName()). Também adiciona a configuração do access log (configureAccessLog) e a persistência de sessão (setSessionPersistenceManager), ambas aplicadas ao deployment antes de addDeployment. RIGHT só troca Servlets.defaultContainer() por Servlets.newContainer() na criação do manager.

2. ESTADO: Os elementos escritos são o objeto deployment (displayName, initial handler chain wrapper, sessionPersistenceManager), o container usado em addDeployment, o manager retornado, o estado do deployment após deploy() e o defaultSessionTimeout do sessionManager.

3. TABELA DE ESTADOS (entrada: access log habilitado, persistSession true, displayName "app"):
   - deployment.displayName: BASE = null | LEFT = "app" | RIGHT = null | MERGE = "app"
   - deployment com wrapper de access log e persistence manager: BASE = não | LEFT = sim | RIGHT = não | MERGE = sim
   - container usado: BASE = defaultContainer (singleton compartilhado) | LEFT = defaultContainer | RIGHT = newContainer (novo) | MERGE = newContainer
   - manager retornado: BASE = deployment registrado no container default, sem os atributos extras | LEFT = deployment registrado no container default, com os atributos extras | RIGHT = deployment registrado em um container novo, sem os atributos extras | MERGE = deployment registrado em um container novo, com os atributos extras
   - sessionTimeout: igual em todas as versões, pois depende só de getSessionTimeout().

4. CRITÉRIO DE CONFLITO:
   - (A) não se aplica: o que muda no MERGE já mudou em LEFT ou em RIGHT.
   - (B) o MERGE preserva o valor de LEFT para os atributos de deployment e o valor de RIGHT para o container. Para o manager inteiro, o valor do MERGE combina as duas mudanças, mas nenhum dos lados escreve sobre o que o outro escreveu.
   - (C) a mudança de RIGHT escolhe o container, e esse código lê deployment, que LEFT alterou. addDeployment registra o deployment como está, e o novo container o recebe com os atributos de LEFT. A instância do container é independente dos atributos do deployment, e o resultado é o esperado para ambos os lados: o deployment configurado, registrado em um container novo. Não há dependência de dados que mude o comportamento do código de RIGHT em relação ao pai que o escreveu.

Nenhuma condição se aplica.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): NO</summary>

1. INTENÇÃO: Pelo diff, LEFT faz muito mais do que o resumo diz. Ele adiciona deployment.setDisplayName(getDisplayName()), o bloco de access log (configureAccessLog via addInitialHandlerChainWrapper) e o bloco de persistência de sessão (setSessionPersistenceManager). Também altera construtores e outros métodos. RIGHT só troca Servlets.defaultContainer() por Servlets.newContainer() ao criar o manager.

2. ESTADO: Em createDeploymentManager, os elementos de estado são:
   - o objeto deployment (displayName, initialHandlerChainWrapper, sessionPersistenceManager);
   - o container de servlets usado para addDeployment, isto é, qual container (compartilhado ou novo) registra o deployment;
   - o manager retornado;
   - o sessionTimeout definido no sessionManager.

3. TABELA DE ESTADOS (entrada: access log habilitado, persistSession true, displayName "app"):
   - deployment.displayName: BASE = nulo | LEFT = "app" | RIGHT = nulo | MERGE = "app"
   - deployment.initialHandlerChainWrapper: BASE = nenhum | LEFT = access log | RIGHT = nenhum | MERGE = access log
   - deployment.sessionPersistenceManager: BASE = nulo | LEFT = FileSessionPersistence | RIGHT = nulo | MERGE = FileSessionPersistence
   - container que recebe o deployment: BASE = container padrão compartilhado | LEFT = container padrão compartilhado | RIGHT = novo container | MERGE = novo container
   - manager retornado: BASE = manager do container padrão, com o deployment básico | LEFT = manager do container padrão, com o deployment configurado | RIGHT = manager de um novo container, com o deployment básico | MERGE = manager de um novo container, com o deployment configurado

4. CRITÉRIO DE CONFLITO:
   - (A) não se aplica: cada valor que muda no MERGE já mudou em LEFT ou em RIGHT.
   - (B) o MERGE preserva as mudanças de LEFT no deployment e a mudança de container de RIGHT. Cada atributo do deployment é igual ao de LEFT, e o container é igual ao de RIGHT.
   - (C) as alterações de LEFT só escrevem atributos do deployment, que é o argumento de addDeployment, e RIGHT só muda qual container o recebe. Nenhuma das duas lê um valor que a outra escreve. Além disso, addDeployment recebe o deployment completo em qualquer container, então o código alterado por RIGHT se comporta no MERGE como em RIGHT. As alterações de LEFT são feitas no objeto deployment antes da chamada e independem do container escolhido. Não há interferência de fluxo de dados ou de controle.

</details>

#### claude-haiku-5-5: YES ❌

<details><summary>Execução 1 (<code>1.csv</code>): YES — Condição C: deployment</summary>

1. INTENÇÃO: LEFT configura o `DeploymentInfo` com um `displayName`, um wrapper de access log (`configureAccessLog`) e um `FileSessionPersistence` quando a persistência de sessão está ativa. Também faz outras mudanças fora do target (renomeia `JarResourcemanager`, altera `getDocumentRootResourceManager`, o construtor e o `getUndertowEmbeddedServletContainer`), que não afetam `createDeploymentManager`. RIGHT troca `Servlets.defaultContainer()` por `Servlets.newContainer()` na linha que chama `addDeployment(deployment)`. O diff confirma ambos os resumos.

2. ESTADO:
   - `deployment` (`DeploymentInfo`): escrito por LEFT (`setDisplayName`, `addInitialHandlerChainWrapper`, `setSessionPersistenceManager`) e lido por `addDeployment(deployment)`, que é a linha alterada por RIGHT.
   - O container escolhido (`Servlets.defaultContainer()` ou `Servlets.newContainer()`), que RIGHT altera.
   - `manager` (`DeploymentManager` retornado): resultado de `addDeployment`.

3. TABELA DE ESTADOS (entrada: `getDisplayName()` não nulo, `isAccessLogEnabled()` verdadeiro, `isPersistSession()` verdadeiro):
   - `deployment`:
     - BASE: sem displayName, sem wrapper de access log, sem persistência de sessão
     - LEFT: com displayName, com wrapper de access log, com persistência de sessão
     - RIGHT: sem displayName, sem wrapper de access log, sem persistência de sessão
     - MERGE: com displayName, com wrapper de access log, com persistência de sessão
   - `container usado em addDeployment`:
     - BASE: `defaultContainer()`
     - LEFT: `defaultContainer()`
     - RIGHT: `newContainer()`
     - MERGE: `newContainer()`
   - `manager` (valor retornado):
     - BASE: manager do container padrão, com o deployment de BASE
     - LEFT: manager do container padrão, com o deployment de LEFT
     - RIGHT: manager do novo container, com o deployment de BASE
     - MERGE: manager do novo container, com o deployment de MERGE

4. CRITÉRIO DE CONFLITO:
   - X = `deployment`.
     - (A) não se aplica: o valor de `deployment` em LEFT difere de BASE, e o MERGE preserva o valor de LEFT.
     - (B) não se aplica: o MERGE preserva o valor de LEFT. Em RIGHT, `deployment` não mudou, então RIGHT não tem alteração nele.
     - (C) se aplica: o valor de `deployment` em LEFT difere de BASE, e a linha alterada por RIGHT (`addDeployment(deployment)`) lê esse objeto. No MERGE, essa linha processa um deployment com displayName, wrapper de access log e persistência de sessão, enquanto em RIGHT ela processou um deployment sem esses elementos. Logo, o código alterado por RIGHT se comporta no MERGE de forma diferente de como se comportava no pai que o escreveu. Isso é o mesmo padrão do Exemplo 3, em que a chamada adicionada por RIGHT lê um valor que LEFT alterou.
   - X = container usado em `addDeployment`.
     - (A) não se aplica: o container em MERGE é igual ao de RIGHT, e o de LEFT é igual a BASE.
     - (B) não se aplica: o MERGE preserva o valor de RIGHT (`newContainer`). LEFT não alterou o container.
     - (C) não se aplica: o código de LEFT não lê o container nem é controlado por ele.
   - X = `manager`.
     - (A) não se aplica: LEFT não altera o valor do manager, e RIGHT o altera de forma preservada no MERGE.
     - (B) não se aplica: o MERGE preserva o valor de RIGHT, e LEFT não altera o manager em si.
     - (C) não se aplica: o código de LEFT não lê o manager.

Conclusão: a condição C se aplica a `deployment`.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): YES — Condição B: manager (DeploymentManager retornado por createDeploymentManager)</summary>

1. INTENÇÃO: LEFT não altera a criação do container. Ele configura o objeto `deployment` com displayName, log de acesso (AccessLogHandler), persistência de sessão e os imports e setters associados. RIGHT troca `Servlets.defaultContainer()` por `Servlets.newContainer()` em `createDeploymentManager`. O diff de RIGHT confirma isso. O MERGE contém as duas mudanças.

2. ESTADO: Escritos pelo TARGET e pelos trechos alterados:
   - `manager` (DeploymentManager retornado): escrito pela linha `Servlets.<container>().addDeployment(deployment)`.
   - `deployment` (DeploymentInfo): escrito por `setDisplayName`, `addInitialHandlerChainWrapper` (via `configureAccessLog`) e `setSessionPersistenceManager` (LEFT), antes de `addDeployment`.
   - O container global implícito retornado por `Servlets.defaultContainer()` (singleton compartilhado) ou `Servlets.newContainer()` (instância nova). Este é o estado que RIGHT altera.

3. TABELA DE ESTADOS: Entrada representativa: `isAccessLogEnabled() = true`, `isPersistSession() = true`, `getDisplayName() = "app"`.
   - `deployment` (configuração): BASE = sem displayName, sem access log, sem persistência | LEFT = displayName "app", access log e persistência configurados | RIGHT = igual a BASE | MERGE = igual a LEFT.
   - Container usado: BASE = defaultContainer (singleton) | LEFT = defaultContainer (singleton) | RIGHT = newContainer (instância nova) | MERGE = newContainer (instância nova).
   - `manager` (DeploymentManager retornado): BASE = manager do singleton, com deployment sem extras | LEFT = manager do singleton, com deployment configurado | RIGHT = manager de nova instância, com deployment sem extras | MERGE = manager de nova instância, com deployment configurado.

4. CRITÉRIO DE CONFLITO:
   - X = `deployment`:
     - (A) não se aplica: X muda em LEFT e não é igual em BASE e LEFT.
     - (B) X em LEFT difere de BASE. O MERGE preserva esse valor: a configuração do MERGE é a mesma de LEFT (displayName, access log e persistência).
     - (C) não se aplica como conflito: o código de RIGHT que muda o container não lê nem é controlado pela configuração do `deployment`. Ele só passa o objeto adiante.
   - X = `manager`:
     - (A) não se aplica: X difere de BASE em LEFT e em RIGHT.
     - (B) X em LEFT difere de BASE, porque o manager de LEFT foi criado no container singleton com o deployment configurado. O valor de X no MERGE é um manager de uma nova instância de container. Ou seja, o MERGE não preserva o valor de LEFT (o container muda de singleton para instância nova). Essa condição se aplica.
     - (C) também seria possível pelo código de sessão existente (`sessionManager.setDefaultSessionTimeout`), que lê `manager`. Porém, esse código não foi alterado por LEFT, então não é o caso de (C).
   - Não se usa a intenção de RIGHT para descartar (B): a troca de container é intencional para RIGHT, mas o valor de `manager` que LEFT produziu não é preservado no MERGE.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): YES — Condição C: deployment</summary>

1. INTENÇÃO: LEFT configura o objeto `deployment` dentro de `createDeploymentManager` (define o display name, habilita access log via `addInitialHandlerChainWrapper` e, se a persistência de sessão estiver ativa, define o `SessionPersistenceManager`). RIGHT troca `Servlets.defaultContainer()` por `Servlets.newContainer()` na linha que chama `addDeployment(deployment)`. O resumo de LEFT é coerente com o diff, mas o diff de LEFT é mais amplo (também altera cabeçalho, construtores, `getDocumentRootResourceManager`, `JarResourceManager` etc.), que estão fora do TARGET.

2. ESTADO: Dentro de `createDeploymentManager`, os elementos de estado relevantes são:
   - `deployment` (variável local, objeto `DeploymentInfo`), escrito por LEFT (`setDisplayName`, `addInitialHandlerChainWrapper`, `setSessionPersistenceManager`) e lido por `addDeployment(deployment)`, a linha alterada por RIGHT.
   - `manager` (variável local e valor retornado), escrito pela linha alterada por RIGHT e pela linha de `addDeployment`.

3. TABELA DE ESTADOS:
   Entrada: `isAccessLogEnabled() = true`, `isPersistSession() = true`, `getDisplayName() = "app"`.
   - `deployment` (conteúdo):
     - BASE: sem display name, sem handler wrapper, sem persistência
     - LEFT: display name "app", com access log wrapper, com FileSessionPersistence
     - RIGHT: igual a BASE
     - MERGE: igual a LEFT
   - `manager`:
     - BASE: `defaultContainer().addDeployment(base deployment)`
     - LEFT: `defaultContainer().addDeployment(deployment com extras)`
     - RIGHT: `newContainer().addDeployment(base deployment)`
     - MERGE: `newContainer().addDeployment(deployment com extras)`

4. CRITÉRIO DE CONFLITO: X = `deployment` e X = `manager`.
   - X = `deployment`:
     - (A) não se aplica: o valor de `deployment` em LEFT difere de BASE.
     - (B) não se aplica: RIGHT é igual a BASE em `deployment`, e o MERGE é igual a LEFT, então LEFT é preservado.
     - (C) aplica-se: o valor de `deployment` em LEFT difere de BASE, e a linha alterada por RIGHT (`Servlets.newContainer().addDeployment(deployment)`) lê `deployment`. No pai RIGHT, essa linha processa um deployment sem display name, sem access log e sem persistência de sessão. No MERGE, ela processa um deployment com essas configurações, portanto se comporta de forma diferente da forma como RIGHT a escreveu.
   - X = `manager`:
     - O valor de `manager` em LEFT (container padrão com extras) e em RIGHT (novo container sem extras) difere de BASE, e o MERGE (novo container com extras) não é igual a nenhum dos dois. Essa diferença decorre da combinação de duas mudanças em partes distintas do mesmo objeto, e não de uma interferência nova, então não é tratada como conflito separado. A condição C para `manager` não se aplica porque nenhum código alterado lê `manager` de forma que mude seu comportamento.
   - Conclusão: a condição C se aplica a `deployment`, pois a alteração de RIGHT é controlada por dados escritos por LEFT.

</details>

### 14. `elasticsearch__d8968869__TransportIndexAction#executeIndexRequestOnPrimary`

- **Target:** `executeIndexRequestOnPrimary(org.elasticsearch.action.index.IndexRequest| org.elasticsearch.index.shard.IndexShard| org.elasticsearch.cluster.action.index.MappingUpdatedAction)`
- **Esperado:** NO; **acertam:** claude-opus-5-5, claude-sonnet-5-5; **erram:** claude-haiku-5-5
- **Código:** [elasticsearch__d8968869__TransportIndexAction](../../data/mergedataset/elasticsearch__d8968869__TransportIndexAction)

**LEFT:** Added a call to a set method "seqNo", and passed the value as a parameter to the IndexResponse constructor

**RIGHT:** Extract variable on the object created by the IndexResponse constructor

**Justificativa do dataset:** Right changes were a extract variable refactoring

#### claude-opus-5-5: NO ✅

<details><summary>Execução 1 (<code>1.csv</code>): NO</summary>

1. INTENÇÃO:
   - LEFT: em executeIndexRequestOnPrimary, adiciona `request.seqNo(operation.seqNo())` e passa `request.seqNo()` ao construtor de IndexResponse. Também passa `request.seqNo()` para `prepareIndexOnReplica` na réplica. O diff confirma o resumo.
   - RIGHT: em executeIndexRequestOnPrimary, extrai a criação de IndexResponse para a variável local `response`, sem mudar os argumentos. Também reformata a assinatura e remove o javadoc. Fora do TARGET, migra a classe para TransportWriteAction, com onPrimaryShard e onReplicaShard. Essas mudanças apenas delegam ao método TARGET e a executeIndexRequestOnReplica, sem alterar o que é escrito.
   - MERGE: inclui `request.seqNo(operation.seqNo())`, a variável extraída `response` e o construtor com `request.seqNo()`.

2. ESTADO:
   - Campos do request: version, versionType e seqNo (este último escrito apenas por LEFT e MERGE).
   - A variável local `response` (IndexResponse), presente em RIGHT e MERGE.
   - O WriteResult retornado (response e translog location).
   - O estado do shard, escrito por indexShard.index(operation).

3. TABELA DE ESTADOS:
   - Entrada: request sem atualização de mapeamento. A operação indexa com version = 1, seqNo = 5, created = true, location = L.
   - request.version: BASE = 1 | LEFT = 1 | RIGHT = 1 | MERGE = 1
   - request.seqNo: BASE = não definido (padrão) | LEFT = 5 | RIGHT = não definido | MERGE = 5
   - IndexResponse retornado:
     - BASE = (shardId, type, id, v=1, created=true)
     - LEFT = (shardId, type, id, seqNo=5, v=1, created=true)
     - RIGHT = (shardId, type, id, v=1, created=true)
     - MERGE = (shardId, type, id, seqNo=5, v=1, created=true)
   - WriteResult.location: L nas quatro versões.

4. CRITÉRIO DE CONFLITO:
   - (A) Não se aplica. Os únicos valores que diferem no MERGE (seqNo e o IndexResponse com seqNo) também diferem em LEFT. Os demais elementos são iguais em todas as versões.
   - (B) request.seqNo e o IndexResponse de LEFT diferem de BASE, e o MERGE é igual a LEFT nos dois. RIGHT não altera nenhum valor em relação a BASE, pois a extração de variável é um refactoring sem efeito semântico, e o MERGE coincide com RIGHT nos elementos que RIGHT preserva.
   - (C) O código alterado por RIGHT (a variável `response` e as novas onPrimaryShard e onReplicaShard) apenas repassa o resultado. Ele não lê seqNo de forma que mude seu comportamento: em RIGHT ele já repassava o response inteiro, e no MERGE repassa o response de LEFT intacto. O código de LEFT, por sua vez, não lê nada escrito por RIGHT.

</details>

#### claude-sonnet-5-5: NO ✅

<details><summary>Execução 1 (<code>1.csv</code>): NO</summary>

1. INTENÇÃO: LEFT propaga o seqNo. Na réplica, passa request.seqNo() a prepareIndexOnReplica. Na primária, chama request.seqNo(operation.seqNo()) e passa request.seqNo() ao construtor de IndexResponse. RIGHT apenas extrai a variável local response (new IndexResponse(...) sem seqNo) e a retorna no WriteResult, além de refatorar a classe para TransportWriteAction. Confirmado nos diffs.

2. ESTADO: No target executeIndexRequestOnPrimary, os elementos escritos são request.seqNo (campo do request), a variável local response (o IndexResponse, com seu campo seqNo) e o valor retornado no WriteResult.

3. TABELA DE ESTADOS: entrada com operation.seqNo() = 5.
   - request.seqNo: BASE = não definido (valor padrão) | LEFT = 5 | RIGHT = não definido | MERGE = 5
   - response.seqNo (no IndexResponse retornado): BASE = não existe/padrão | LEFT = 5 | RIGHT = padrão | MERGE = 5
   - Retorno (WriteResult.response): BASE = sem seqNo | LEFT = com seqNo 5 | RIGHT = sem seqNo | MERGE = com seqNo 5

   O MERGE combina `request.seqNo(operation.seqNo())` com a construção de `response` usando `request.seqNo()`, que é a linha de LEFT dentro da variável extraída por RIGHT. O resultado equivale a LEFT, e o return usa response, como RIGHT pretendia.

4. CRITÉRIO DE CONFLITO:
   - (A) não se aplica: os valores diferem em LEFT.
   - (B) o MERGE preserva o valor de LEFT (seqNo 5 no response). RIGHT não alterou o valor observável, só a estrutura, então o MERGE também é equivalente a RIGHT em tudo o que RIGHT mudou.
   - (C) o código de RIGHT (construção e retorno de response) lê request.seqNo, escrito por LEFT, mas se comporta no MERGE como LEFT pretendia. A extração de variável não altera semântica. Não há interferência indesejada.

   Os demais pontos (a réplica passando seqNo) só mudaram em LEFT, e RIGHT mudou a assinatura da classe sem interferir nesse fluxo.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): NO</summary>

1. INTENÇÃO: LEFT propaga o seqNo. Em executeIndexRequestOnPrimary, grava request.seqNo(operation.seqNo()) e passa request.seqNo() ao construtor de IndexResponse. Em executeIndexRequestOnReplica, passa request.seqNo() a prepareIndexOnReplica. RIGHT só extrai a variável local response (new IndexResponse(...) sem seqNo) e devolve new WriteResult&lt;&gt;(response, location). Além disso, RIGHT reestrutura a classe (TransportWriteAction), sem alterar a semântica do target.

2. ESTADO: Os elementos escritos no target são request.seqNo (campo, escrito por LEFT), a variável local response (RIGHT), o seqNo contido em IndexResponse e o retorno WriteResult.

3. TABELA DE ESTADOS:
   - Entrada: operation.seqNo() = 5, request.seqNo inicial = unassigned
   - request.seqNo: BASE = não atribuído | LEFT = 5 | RIGHT = não atribuído | MERGE = 5
   - seqNo em IndexResponse: BASE = não existe/não informado | LEFT = 5 | RIGHT = não informado | MERGE = 5
   - response (local): BASE = não existe | LEFT = não existe | RIGHT = IndexResponse sem seqNo | MERGE = IndexResponse com seqNo 5
   - Retorno WriteResult.response: BASE = sem seqNo | LEFT = seqNo 5 | RIGHT = sem seqNo | MERGE = seqNo 5

4. CRITÉRIO DE CONFLITO:
   - (A) não se aplica: o valor muda em LEFT.
   - (B) o MERGE preserva o valor de LEFT para request.seqNo, para o seqNo da resposta e para o retorno. RIGHT é um refactoring que não altera valores; o valor de response no MERGE é o construtor do LEFT atribuído à variável extraída, o que preserva o comportamento do RIGHT. O merge integrou corretamente a mudança de LEFT dentro da expressão extraída por RIGHT.
   - (C) o código alterado por RIGHT (extração da variável e retorno) lê o resultado do construtor. No MERGE, o construtor recebe seqNo como no LEFT, o que é a intenção de LEFT, e o refactoring de RIGHT não depende do valor de seqNo. A ordem é mantida: request.seqNo(operation.seqNo()) vem antes da criação da resposta. Não há interferência.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): NO</summary>

1. INTENÇÃO: LEFT propaga o seqNo. Em executeIndexRequestOnPrimary, grava request.seqNo(operation.seqNo()) e passa request.seqNo() ao construtor de IndexResponse. Na réplica, passa request.seqNo() a prepareIndexOnReplica. RIGHT apenas extrai a variável local `response` com o IndexResponse (sem seqNo) e retorna new WriteResult&lt;&gt;(response, location), sem mudar o comportamento.

2. ESTADO: Em TARGET (executeIndexRequestOnPrimary), os elementos escritos são request.seqNo (campo do request), o campo seqNo do IndexResponse, a variável local response e o retorno WriteResult (response, location).

3. TABELA DE ESTADOS:
   - Entrada: operation.seqNo() = 5
   - request.seqNo: BASE = não definido (valor padrão) | LEFT = 5 | RIGHT = não definido | MERGE = 5
   - response.seqNo (retorno): BASE = não existe/padrão | LEFT = 5 | RIGHT = padrão | MERGE = 5
   - response (variável local): BASE = não existe | LEFT = não existe | RIGHT = IndexResponse sem seqNo | MERGE = IndexResponse construída com request.seqNo() = 5
   - WriteResult retornado: BASE = resposta sem seqNo | LEFT = resposta com seqNo 5 | RIGHT = igual a BASE | MERGE = resposta com seqNo 5

4. CRITÉRIO DE CONFLITO:
   - (A) não se aplica: os valores em LEFT diferem de BASE.
   - (B) o valor de X em LEFT (response.seqNo = 5, request.seqNo = 5) difere de BASE, e o MERGE o preserva. Em RIGHT, o valor retornado é igual ao de BASE, e a refatoração é preservada semanticamente, já que o retorno do MERGE contém o response extraído com o seqNo de LEFT.
   - (C) o código de RIGHT (a variável response e o return) lê o valor de request.seqNo escrito por LEFT. No MERGE, a mescla integrou as duas mudanças: a linha `new IndexResponse(..., request.seqNo(), ...)` fica na variável extraída, e request.seqNo(operation.seqNo()) vem antes dela. O comportamento é o mesmo que LEFT pretendia, e a extração de variável de RIGHT é só refatoração. O código de RIGHT não se comporta de forma diferente do que RIGHT pretendia.
   - Nenhuma condição se aplica.

</details>

#### claude-haiku-5-5: YES ❌

<details><summary>Execução 1 (<code>1.csv</code>): YES — Condição C: request.seqNo</summary>

1. INTENÇÃO: LEFT passa a propagar o seqNo: define `request.seqNo(operation.seqNo())` após a versão e passa `request.seqNo()` ao construtor de `IndexResponse`. Também altera `executeIndexRequestOnReplica` para usar `request.seqNo()`. RIGHT faz uma refatoração de extração de variável: cria `IndexResponse response = new IndexResponse(shardId, type, id, version, created)` e retorna `new WriteResult<>(response, ...)`, além de trocar `TransportReplicationAction` por `TransportWriteAction` e mover o código de `shardOperationOnPrimary`/`shardOperationOnReplica` para `onPrimaryShard`/`onReplicaShard`. Os resumos conferem com os diffs.

2. ESTADO: No método TARGET, os elementos de estado escritos são:
   - `request.seqNo` (escrito por `request.seqNo(operation.seqNo())`, em LEFT e MERGE);
   - o objeto `IndexResponse` retornado (dentro de `WriteResult`), cujo conteúdo depende dos argumentos do construtor;
   - `request.version` e `request.versionType` (escritos, mas sem alteração entre os pais).

3. TABELA DE ESTADOS: Entrada considerada: primário, `request.version = 1`, `operation.seqNo() = 7`, `created = true`.
   - `request.seqNo`: BASE = não definido | LEFT = 7 | RIGHT = não definido | MERGE = 7
   - `IndexResponse` retornado: BASE = (shardId, type, id, version=1, created=true) | LEFT = (…, seqNo=7, version=1, created=true) | RIGHT = (…, version=1, created=true) | MERGE = (…, seqNo=7, version=1, created=true)
   - Código alterado por RIGHT (a linha extraída que cria `response`): BASE = cria o IndexResponse sem seqNo | RIGHT = idem | MERGE = cria o IndexResponse com `request.seqNo()`, lendo o valor escrito por LEFT.

4. CRITÉRIO DE CONFLITO:
   - X = `request.seqNo`:
     - (A) não se aplica: o valor de X muda em LEFT, então não é igual nos três.
     - (B) o valor de X em LEFT (7) difere de BASE, e o MERGE (7) preserva esse valor. Não viola B.
     - (C) o valor de X em LEFT difere de BASE, e o código alterado por RIGHT (a linha extraída que cria `response`) passa a ler `request.seqNo()` no MERGE. Esse código se comporta no MERGE de forma diferente de como se comportava em RIGHT, onde criava o `IndexResponse` sem seqNo. Logo, a condição C se aplica.
   - X = objeto `IndexResponse`:
     - (A) não se aplica, pois LEFT altera o valor.
     - (B) o valor em LEFT difere de BASE e é preservado no MERGE; o valor em RIGHT é igual ao de BASE, então B não se aplica a RIGHT.
     - (C) já coberta pela análise de `request.seqNo`.

   A junção é textualmente limpa e a intenção de cada lado é mantida: o seqNo é definido antes da criação do objeto e a refatoração de RIGHT não altera a semântica isoladamente. Mesmo assim, a condição C se aplica literalmente: o código de RIGHT, no MERGE, lê um estado alterado por LEFT e se comporta de forma diferente do pai que o escreveu. Não descarto a condição pela intenção de LEFT.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): YES — Condição C: request.seqNo</summary>

1. INTENÇÃO: LEFT grava `request.seqNo(operation.seqNo())` em `executeIndexRequestOnPrimary` e passa `request.seqNo()` ao construtor de `IndexResponse`. Também usa `request.seqNo()` na preparação da réplica. RIGHT apenas extrai a criação do `IndexResponse` para a variável `response`, sem alterar argumentos. Os resumos conferem com os diffs.

2. ESTADO: Escritos pelo TARGET e pelos trechos alterados:
   - `request.seqNo`, escrito por `request.seqNo(operation.seqNo())` (LEFT).
   - O objeto `IndexResponse` criado na linha alterada por RIGHT e por LEFT, cujo campo seqNo é lido de `request.seqNo()`.
   - `response` (variável local introduzida por RIGHT).
   - O `WriteResult` retornado.

3. TABELA DE ESTADOS: Entrada com `request.seqNo` inicial = -1 (não atribuído) e `operation.seqNo()` = 7.
   - `request.seqNo`: BASE = -1 | LEFT = 7 | RIGHT = -1 | MERGE = 7
   - `IndexResponse.seqNo` (criado na linha alterada): BASE = -1 (construtor sem seqNo) | LEFT = 7 | RIGHT = -1 (construtor sem seqNo, apenas extraído para `response`) | MERGE = 7
   - `response` / `WriteResult.response`: BASE = IndexResponse(seqNo -1) | LEFT = IndexResponse(seqNo 7) | RIGHT = IndexResponse(seqNo -1) | MERGE = IndexResponse(seqNo 7)

4. CRITÉRIO DE CONFLITO:
   - X = `request.seqNo`:
     - (A) não se aplica: o valor muda em LEFT.
     - (B) não se aplica: LEFT difere de BASE e o MERGE (7) é igual a LEFT, então está preservado. RIGHT é igual a BASE.
     - (C) se aplica: LEFT escreveu X (difere de BASE). O código alterado por RIGHT, a criação de `IndexResponse` extraída para `response`, passa a ler `request.seqNo()` no MERGE. Em RIGHT, esse mesmo código não lê X e produz `IndexResponse` com seqNo -1. No MERGE, produz seqNo 7. Logo, esse código se comporta no MERGE de forma diferente do pai que o escreveu.
   - X = `IndexResponse.seqNo` / `response`:
     - (A) não se aplica: muda em LEFT.
     - (B) não se aplica: MERGE (7) é igual ao valor de LEFT (7), que é preservado. RIGHT (-1) é igual a BASE.
     - (C) não é necessária, pois X é derivado de `request.seqNo` e C já se aplica a ele.

   Não há conflito do tipo B: o resultado de LEFT é preservado. Há conflito do tipo C: a linha que RIGHT alterou (extração de `response`) passou a depender do valor de `request.seqNo` escrito por LEFT, e isso muda o comportamento que RIGHT tinha.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): YES — Condição C: request.seqNo</summary>

1. INTENÇÃO: LEFT passa a gravar `request.seqNo(operation.seqNo())` e a incluir `request.seqNo()` no `IndexResponse`. RIGHT é uma extração de variável: `IndexResponse response = new IndexResponse(...)` seguido de `new WriteResult<>(response, ...)`, sem mudança de comportamento pretendida. Os diffs confirmam os resumos.

2. ESTADO: Escritos ou lidos pelo TARGET e pelos trechos alterados:
   - `request.seqNo` (campo do request): escrito por LEFT, lido pelo construtor de `IndexResponse` no MERGE.
   - `response` (variável local e objeto `IndexResponse` retornado em `WriteResult`).
   - `operation.seqNo()` (lido por LEFT para escrever em `request.seqNo`).

3. TABELA DE ESTADOS:
   - Entrada: `request.seqNo` inicial = 0, `operation.seqNo()` = 5, `version` = 1, `created` = true.
   - `request.seqNo`: BASE = 0 | LEFT = 5 | RIGHT = 0 | MERGE = 5
   - `response` retornado (conteúdo do IndexResponse): BASE = (sem seqNo, versão 1) | LEFT = (seqNo 5, versão 1) | RIGHT = (sem seqNo, versão 1) | MERGE = (seqNo 5, versão 1)
   - Retorno de `WriteResult.response`: BASE = response sem seqNo | LEFT = response com seqNo 5 | RIGHT = response sem seqNo | MERGE = response com seqNo 5

4. CRITÉRIO DE CONFLITO:
   - X = `response`:
     - (A) não se aplica: o valor difere de BASE em LEFT.
     - (B) LEFT difere de BASE (seqNo 5), e MERGE preserva esse valor (seqNo 5). RIGHT é igual a BASE. Não há violação.
     - (C) não se aplica como dependência, pois RIGHT não lê o `response` alterado por LEFT.
   - X = `request.seqNo`:
     - (A) não se aplica: LEFT difere de BASE.
     - (B) LEFT difere de BASE (5), e MERGE preserva o valor (5). Não há violação.
     - (C) LEFT altera X (0 para 5). A instrução de RIGHT, alterada pelo outro pai, é a construção do `IndexResponse`. Em RIGHT, essa instrução não lê `seqNo`. No MERGE, ela lê `request.seqNo`, valor escrito por LEFT, e produz um resultado diferente do que RIGHT produziu (com seqNo 5 em vez de sem seqNo). A regra manda não descartar a condição pela intenção dos desenvolvedores. Por isso, a condição C se aplica literalmente a `request.seqNo`.
   - Ressalva: a mudança de comportamento na linha vem da própria edição de LEFT sobre essa linha, o que é consistente com a intenção de LEFT. Mesmo assim, a condição C é satisfeita pela definição fornecida.

</details>

### 15. `elasticsearch__d8968869__DocWriteResponse#readFrom`

- **Target:** `readFrom(org.elasticsearch.common.io.stream.StreamInput)`
- **Esperado:** NO; **acertam:** claude-opus-5-5, claude-sonnet-5-5; **erram:** claude-haiku-5-5
- **Código:** [elasticsearch__d8968869__DocWriteResponse](../../data/mergedataset/elasticsearch__d8968869__DocWriteResponse)

**LEFT:** Left adds a call for method readZLong on the in object.

**RIGHT:** Right adds a call for method readBoolean on the object in.

**Justificativa do dataset:** Left and Right changes just added new method calls that returns the byte at the buffer's current position.

#### claude-opus-5-5: NO ✅

<details><summary>Execução 1 (<code>1.csv</code>): NO</summary>

1. INTENÇÃO: Os diffs confirmam os resumos.
   - LEFT adiciona o campo `seqNo`. Ele é serializado em `writeTo` com `out.writeZLong(seqNo)` logo após `version` e desserializado em `readFrom` com `seqNo = in.readZLong()` na mesma posição.
   - RIGHT adiciona o campo `forcedRefresh`. Ele é serializado com `out.writeBoolean(forcedRefresh)` após `version` e desserializado com `forcedRefresh = in.readBoolean()` na mesma posição.
   - O MERGE coloca as duas operações na mesma ordem em `writeTo` e em `readFrom`: primeiro `seqNo`, depois `forcedRefresh`.

2. ESTADO:
   - Campos escritos por `readFrom`: `shardId`, `type`, `id`, `version`, `seqNo` (LEFT) e `forcedRefresh` (RIGHT).
   - A posição de leitura no stream `in`, que cada leitura avança.
   - Esse stream é produzido pelo `writeTo` da mesma versão do código.

3. TABELA DE ESTADOS:
   - Entrada: um objeto com shardId = S, type = "t", id = "1", version = 3, seqNo = 7 (onde existe) e forcedRefresh = true (onde existe). O objeto é serializado pelo `writeTo` de cada versão e lido pelo `readFrom` da mesma versão.
   - Bytes no stream:
     - BASE: [S, "t", "1", 3]
     - LEFT: [S, "t", "1", 3, 7]
     - RIGHT: [S, "t", "1", 3, true]
     - MERGE: [S, "t", "1", 3, 7, true]
   - shardId, type, id, version: S, "t", "1", 3 nas quatro versões.
   - seqNo: BASE = inexistente | LEFT = 7 | RIGHT = inexistente | MERGE = 7
   - forcedRefresh: BASE = inexistente | LEFT = inexistente | RIGHT = true | MERGE = true
   - Posição final do stream: fim do stream nas quatro versões; todos os bytes escritos foram consumidos.

4. CRITÉRIO DE CONFLITO:
   - (A) Não se aplica. Os campos comuns (shardId, type, id, version) têm o mesmo valor em BASE, LEFT, RIGHT e MERGE, e a posição final do stream também é a mesma.
   - (B) Não se aplica.
     - `seqNo` em LEFT (7) difere de BASE, e o MERGE (7) preserva esse valor.
     - `forcedRefresh` em RIGHT (true) difere de BASE, e o MERGE (true) preserva esse valor.
   - (C) Não se aplica.
     - Existe uma dependência real: o `readBoolean` de RIGHT lê a posição do stream, que no MERGE foi avançada antes pelo `readZLong` de LEFT.
     - Porém o `writeTo` do MERGE grava `seqNo` antes de `forcedRefresh`, na mesma ordem da leitura.
     - Por isso o `readBoolean` lê exatamente o booleano gravado, com o mesmo valor (true) que leria em RIGHT.
     - Da mesma forma, o `readZLong` de LEFT lê o mesmo valor (7) que leria em LEFT.
     - Nenhum dos dois códigos se comporta no MERGE de forma diferente de como se comporta no pai que o escreveu.

</details>

#### claude-sonnet-5-5: NO ✅

<details><summary>Execução 1 (<code>1.csv</code>): NO</summary>

1. INTENÇÃO: LEFT adiciona o campo seqNo e o lê em readFrom() com in.readZLong() depois de version. RIGHT adiciona o campo forcedRefresh e o lê com in.readBoolean() depois de version. Os diffs confirmam os resumos. Em writeTo(), LEFT escreve seqNo com writeZLong e RIGHT escreve forcedRefresh com writeBoolean, ambos logo após version.

2. ESTADO: Os campos shardId, type, id, version, seqNo e forcedRefresh, escritos por readFrom(). Também o cursor do stream `in`, que é um estado consumido por cada leitura em ordem. Há ainda o formato de bytes do stream `out` em writeTo().

3. TABELA DE ESTADOS:
   Entrada: stream escrito por writeTo() da mesma versão do código, com version=5, seqNo=7, forcedRefresh=true.
   - BASE: lê shardId, type, id, version=5. seqNo e forcedRefresh não existem.
   - LEFT: escreve version, seqNo. Lê version=5, seqNo=7 (consistente).
   - RIGHT: escreve version, forcedRefresh. Lê version=5, forcedRefresh=true (consistente).
   - MERGE: writeTo escreve version, seqNo, forcedRefresh. readFrom lê version, seqNo, forcedRefresh na mesma ordem. Resultado: version=5, seqNo=7, forcedRefresh=true.

   A ordem de leitura (ZLong, depois Boolean) coincide com a ordem de escrita (ZLong, depois Boolean), então o stream é simétrico.

4. CRITÉRIO DE CONFLITO:
   - (A) não se aplica: seqNo e forcedRefresh mudam em LEFT e RIGHT respectivamente, e nada muda no MERGE sem ter mudado em um dos pais.
   - (B) seqNo em LEFT = 7 e no MERGE = 7. forcedRefresh em RIGHT = true e no MERGE = true. Ambos são preservados.
   - (C) a leitura de forcedRefresh depende da posição do cursor, que em RIGHT vem logo após version. No MERGE vem após seqNo, mas a escrita em writeTo() também foi deslocada de forma equivalente. Os valores lidos são os mesmos que cada pai produziria no contexto do seu próprio formato. Nenhum código alterado por um lado lê um valor que o outro lado tenha alterado de forma incompatível.
   
   O construtor mudou a assinatura em LEFT, mas isso não é target e não afeta o comportamento de readFrom().

</details>

<details><summary>Execução 2 (<code>2.csv</code>): NO</summary>

1. INTENÇÃO: LEFT adiciona o campo seqNo e lê seqNo com in.readZLong() após version em readFrom (e escreve com out.writeZLong(seqNo) em writeTo). RIGHT adiciona o campo forcedRefresh e lê forcedRefresh com in.readBoolean() após version (e escreve com out.writeBoolean em writeTo). Os diffs confirmam os resumos.

2. ESTADO: Os campos seqNo e forcedRefresh e o estado consumido do stream `in` (posição de leitura). Os campos shardId, type, id e version são os mesmos nos três lados. Em writeTo, o stream `out` recebe os bytes escritos.

3. TABELA DE ESTADOS:
   - Entrada: stream escrito pelo writeTo da mesma versão, com seqNo = 5, forcedRefresh = true, version = 1.
   - Ordem de escrita no MERGE: version, seqNo, forcedRefresh. Ordem de leitura no MERGE: version, seqNo, forcedRefresh. As duas ordens são consistentes.
   - seqNo: BASE = inexistente | LEFT = 5 | RIGHT = inexistente (0) | MERGE = 5
   - forcedRefresh: BASE = inexistente | LEFT = inexistente (false) | RIGHT = true | MERGE = true
   - Posição de `in` após readFrom: BASE = depois de version | LEFT = depois de seqNo | RIGHT = depois de forcedRefresh | MERGE = depois de seqNo e forcedRefresh.

   Cada lado lê o que ele mesmo escreve, e o MERGE lê e escreve os dois na mesma ordem. O MERGE preserva o valor de seqNo de LEFT e o de forcedRefresh de RIGHT.

   Há uma questão de compatibilidade de formato de fio com versões antigas de cada lado, mas isso não é uma interferência entre as mudanças dentro do MERGE. Os campos lidos são independentes: nenhum lê o valor do outro, e a ordem é simétrica entre readFrom e writeTo.

4. CRITÉRIO DE CONFLITO:
   - (A) não se aplica: nenhum valor muda no MERGE sem ter mudado em LEFT ou RIGHT.
   - (B) não se aplica: o MERGE preserva seqNo de LEFT e forcedRefresh de RIGHT.
   - (C) a leitura de forcedRefresh depende da posição do stream, que em LEFT avança com seqNo. No MERGE, porém, writeTo escreve seqNo antes de forcedRefresh, então a leitura de forcedRefresh recebe o valor correto, o mesmo comportamento que o pai que o escreveu produziria. Nenhuma dependência é quebrada.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): NO</summary>

1. INTENÇÃO: LEFT adiciona o campo seqNo e lê seqNo com in.readZLong() ao final de readFrom (após version). RIGHT adiciona o campo forcedRefresh e lê forcedRefresh com in.readBoolean() ao final de readFrom (após version). Os diffs confirmam os resumos.

2. ESTADO: Em readFrom, os elementos escritos são os campos shardId, type, id, version, seqNo e forcedRefresh. O stream `in` também é um elemento de estado, pois sua posição de leitura avança a cada read. Os elementos relevantes são seqNo, forcedRefresh e a posição do stream.

3. TABELA DE ESTADOS:
   - Entrada: stream com [shardId, "t", "i", ZLong(5), ZLong(7), true].
   - BASE: version=5, depois não lê mais nada; seqNo e forcedRefresh não existem; posição do stream após o ZLong de version.
   - LEFT: version=5, seqNo=7; forcedRefresh não existe. Ordem de escrita (writeTo): version, seqNo. Consistente.
   - RIGHT: version=5, forcedRefresh=readBoolean() lê o byte do ZLong(7) (interpretado como boolean). Ordem de escrita: version, forcedRefresh. Consistente com seu próprio writeTo.
   - MERGE: readFrom lê version, seqNo=readZLong(), forcedRefresh=readBoolean(). writeTo escreve version, seqNo, forcedRefresh. Na ordem, seqNo=7 e forcedRefresh=true. Leitura e escrita são consistentes entre si, e os valores são os esperados por cada lado.

   Valores:
   - seqNo: BASE = n/a | LEFT = 7 | RIGHT = n/a (0 padrão) | MERGE = 7
   - forcedRefresh: BASE = n/a | LEFT = false (padrão) | RIGHT = true | MERGE = true
   - posição do stream após readFrom: BASE = após version | LEFT = após seqNo | RIGHT = após o boolean | MERGE = após seqNo e boolean.

4. CRITÉRIO DE CONFLITO:
   - (A) não se aplica: nenhum valor é igual em BASE, LEFT e RIGHT e diferente no MERGE.
   - (B) seqNo e forcedRefresh no MERGE são iguais aos valores do pai que os escreveu. A posição do stream difere de cada pai, mas isso é a composição esperada de duas leituras aditivas. Como o writeTo do MERGE escreve na mesma ordem, a serialização é simétrica e consistente.
   - (C) a leitura de forcedRefresh depende da posição do stream, deslocada pela leitura de seqNo do LEFT. Porém, o writeTo mesclado também escreve seqNo antes de forcedRefresh, então o byte lido corresponde ao escrito. Não há comportamento diferente do pretendido.

Não há interferência indesejada.

</details>

#### claude-haiku-5-5: YES ❌

<details><summary>Execução 1 (<code>1.csv</code>): YES — Condição C: in (fluxo StreamInput, posição de leitura consumida por readZLong e readBoolean)</summary>

1. INTENÇÃO: LEFT adiciona a leitura de `seqNo` com `in.readZLong()` logo após `version`. RIGHT adiciona a leitura de `forcedRefresh` com `in.readBoolean()` no mesmo ponto. Os diffs confirmam os resumos.

2. ESTADO: No target `readFrom(StreamInput in)`, são escritos os campos `seqNo` (LEFT) e `forcedRefresh` (RIGHT), além do próprio fluxo `in`, cuja posição de leitura é avançada a cada chamada. O código de `writeTo` espelha essa ordem.

3. TABELA DE ESTADOS (entrada: version = 5, seqNo = 7, forcedRefresh = true):
   - Fluxo gerado pelo `writeTo` de cada pai:
     - BASE: [zlong 5][bool true]
     - LEFT: [zlong 5][zlong 7]
     - RIGHT: [zlong 5][bool true]
     - MERGE: [zlong 5][zlong 7][bool true]
   - seqNo, após `readFrom` com o fluxo do próprio pai:
     - BASE: inexistente (campo não lido)
     - LEFT: 7
     - RIGHT: 0 (default, não lido)
     - MERGE: 7
   - forcedRefresh, após `readFrom` com o fluxo do próprio pai:
     - BASE: inexistente
     - LEFT: 0 (default)
     - RIGHT: true
     - MERGE: true
   - Ao ler o fluxo de RIGHT (`[zlong 5][bool true]`) com o código MERGE, `readZLong()` consome o byte do booleano e `readBoolean()` tenta ler além do que foi escrito. O resultado difere do que RIGHT produz.

4. CRITÉRIO DE CONFLITO:
   - X = seqNo: 
     - (A) não se aplica, pois seqNo não tem valor igual em BASE, LEFT e RIGHT.
     - (B) o valor de LEFT (7) difere de BASE, e o MERGE preserva LEFT (7). Não há violação.
     - (C) não há leitura de seqNo pelo código de RIGHT.
   - X = fluxo `in` (posição de leitura, estado do tipo "fluxo"):
     - (A) não se aplica, pois o fluxo muda em LEFT e em RIGHT.
     - (B) o fluxo em LEFT difere de BASE (consome um zlong a mais), e o MERGE não preserva o consumo de LEFT. O MERGE consome zlong e boolean, enquanto LEFT consome só zlong. Isso se aplica como divergência de estado, mas depende de o fluxo ser comparado entre pais.
     - (C) o código adicionado por LEFT (`readZLong`) avança a posição de `in`, e o código adicionado por RIGHT (`readBoolean`) lê de `in` nessa posição. Esse código de RIGHT se comporta no MERGE de forma diferente de como se comporta em RIGHT: no pai ele lê o booleano logo após `version`, e no MERGE lê depois do zlong. Com um fluxo produzido por RIGHT, o MERGE lê valores errados (ver tabela).
   - Conclusão: a condição C se aplica ao fluxo de entrada `in`. O merge é textualmente limpo, mas as duas leituras disputam a mesma posição do fluxo, e a leitura de RIGHT muda de comportamento no MERGE.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): YES — Condição C: stream de entrada `in` (posição de leitura, lida por readBoolean() após o readZLong() de LEFT)</summary>

1. INTENÇÃO: LEFT passa a ler `seqNo` (`in.readZLong()`) ao final de `readFrom`, e também o escreve em `writeTo`. RIGHT passa a ler `forcedRefresh` (`in.readBoolean()`) ao final de `readFrom`, e também o escreve em `writeTo`. Os resumos conferem com os diffs.

2. ESTADO: O elemento de estado relevante é o stream `in` (StreamInput), um canal de entrada cuja posição de leitura é consumida por `readFrom`. Também são escritos pelo método alvo: `this.version`, `this.type`, `this.id`, `this.shardId`, e os campos novos `this.seqNo` (LEFT) e `this.forcedRefresh` (RIGHT).

3. TABELA DE ESTADOS:
   - Entrada: após ler `version`, o stream contém os bytes `[0x0E, 0x00]`. O byte `0x0E` é um zlong (zigzag) que vale 7. O byte `0x00` é um boolean falso.
   - Stream (posição de leitura de `in` ao sair de `readFrom`):
     - BASE: lê os 4 campos anteriores e para antes de `0x0E`.
     - LEFT: `seqNo = readZLong()` consome `0x0E` e para em `0x00`.
     - RIGHT: `forcedRefresh = readBoolean()` consome `0x0E` (nonzero, então `true`) e para em `0x00`.
     - MERGE: `seqNo = readZLong()` consome `0x0E` (7). Em seguida, `forcedRefresh = readBoolean()` lê `0x00` (`false`).
   - `forcedRefresh`: BASE = indefinido | LEFT = indefinido | RIGHT = true | MERGE = false.
   - `seqNo`: BASE = indefinido | LEFT = 7 | RIGHT = indefinido | MERGE = 7.
   - Observação sobre o `writeTo` do MERGE: ele escreve `zlong seqNo` e depois `boolean forcedRefresh`, na mesma ordem em que o MERGE lê. Assim, a serialização e a desserialização do MERGE são consistentes entre si.

4. CRITÉRIO DE CONFLITO: X = posição de leitura do stream `in` e, em particular, o valor que `readBoolean()` obtém dele.
   - (A) não se aplica: o stream muda em LEFT e em RIGHT em relação a BASE.
   - (B) aplica-se em sentido estrito: a posição de LEFT (após o zlong) difere da posição de MERGE (após zlong e boolean), e o MERGE não preserva o valor de LEFT.
   - (C) aplica-se de forma mais precisa: o código adicionado por RIGHT (`readBoolean()`) lê o stream, e o código adicionado por LEFT (`readZLong()`) altera a posição desse stream antes dele. No pai RIGHT, `readBoolean()` lê `0x0E` e produz `true`. No MERGE, o mesmo `readBoolean()` lê `0x00` e produz `false`. O código de RIGHT se comporta de forma diferente no MERGE do que em RIGHT, por dependência de dados sobre o stream que LEFT consumiu.
   Como C descreve diretamente a interferência entre as leituras sequenciais do mesmo stream, essa é a condição que melhor explica o conflito.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): YES — Condição C: in (posição de leitura do StreamInput)</summary>

1. INTENÇÃO: LEFT adiciona a leitura de `seqNo` (`in.readZLong()`) ao final de `readFrom`, espelhando sua escrita em `writeTo`. RIGHT adiciona a leitura de `forcedRefresh` (`in.readBoolean()`) ao final de `readFrom`, espelhando sua própria escrita. Os diffs confirmam os resumos.

2. ESTADO: Os elementos de estado afetados são:
   - `this.seqNo`, escrito por `readFrom` (apenas em LEFT e MERGE);
   - `this.forcedRefresh`, escrito por `readFrom` (apenas em RIGHT e MERGE);
   - `in` (StreamInput), um canal de entrada cuja posição de leitura é avançada por cada `readX()`. Ele é lido e consumido por `readZLong` (LEFT) e `readBoolean` (RIGHT).

3. TABELA DE ESTADOS:
   Entrada: fluxo serializado pelo writer do MERGE com version = 7, seqNo = 5, forcedRefresh = true. Bytes na ordem: [version][seqNo][forcedRefresh].
   - Posição do fluxo após `version`: BASE = byte de seqNo (BASE não lê seqNo, então para no fim de version) | LEFT = byte de seqNo, consumido por readZLong | RIGHT = byte de seqNo, lido por readBoolean como se fosse forcedRefresh | MERGE = byte de seqNo, consumido por readZLong, depois byte de forcedRefresh, consumido por readBoolean
   - seqNo: BASE = (inexistente/0) | LEFT = 5 | RIGHT = 0 (padrão) | MERGE = 5
   - forcedRefresh: BASE = (inexistente/false) | LEFT = false (padrão) | RIGHT = interpretação do byte de seqNo, que difere do valor real de forcedRefresh | MERGE = true

4. CRITÉRIO DE CONFLITO:
   - X = seqNo.
     - (A) não se aplica: o valor muda em LEFT.
     - (B) o valor em LEFT (5) difere de BASE (inexistente/0), e o MERGE (5) preserva esse valor. Não há conflito por B.
     - (C) não se aplica: o código de RIGHT não lê nem é controlado por seqNo.
   - X = forcedRefresh.
     - (A) não se aplica: o valor muda em RIGHT.
     - (B) o valor em RIGHT difere de BASE, e o MERGE (true) preserva o valor que RIGHT pretendia quando o fluxo tem o formato do MERGE. Não há conflito por B nessa entrada.
     - (C) não se aplica diretamente, pois o código de LEFT não lê forcedRefresh.
   - X = in (posição do fluxo `StreamInput`).
     - O valor de `in` em LEFT difere de BASE, porque LEFT avança a posição de leitura com `readZLong`.
     - O código alterado por RIGHT (`readBoolean`) lê `in`. Em RIGHT isoladamente, ele consome o byte imediatamente após `version`. No MERGE, ele consome o byte depois do `seqNo`. Assim, o mesmo código se comporta de forma diferente no MERGE em relação ao pai que o escreveu.
     - A condição (C) se aplica a `in`.

   O formato do MERGE é internamente consistente: `writeTo` escreve `seqNo` e depois `forcedRefresh`, e `readFrom` lê na mesma ordem. Isso não elimina a condição (C), porque a interferência está na posição compartilhada do fluxo, que é um elemento de estado consumido pelos dois lados. Pela regra, a intenção dos desenvolvedores não descarta a condição.

</details>

### 16. `elasticsearch__d8968869__MetaDataCreateIndexService#createIndex`

- **Target:** `createIndex(org.elasticsearch.action.admin.indices.create.CreateIndexClusterStateUpdateRequest| org.elasticsearch.action.ActionListener<ClusterStateUpdateResponse>)`
- **Esperado:** NO; **acertam:** claude-opus-5-5, claude-sonnet-5-5; **erram:** claude-haiku-5-5
- **Código:** [elasticsearch__d8968869__MetaDataCreateIndexService](../../data/mergedataset/elasticsearch__d8968869__MetaDataCreateIndexService)

**LEFT:** Left adds two new parameters when creating the local variable indexService.

**RIGHT:** Right extracts a local variable (refactoring) and also adds a new local variable routingNumShards.

**Justificativa do dataset:** There is no locally observable interference as the Left changes just add parameters to create a local variable, which does not interfere with the new changes of Right.

#### claude-opus-5-5: NO ✅

<details><summary>Execução 1 (<code>1.csv</code>): NO</summary>

1. INTENÇÃO:
   - LEFT: na chamada `indicesService.createIndex(...)` passa um quarto argumento, `shardId -> {}`. É um callback no-op, presumivelmente um listener de shard. O diff confirma o resumo.
   - RIGHT: introduz `routingNumShards`. O valor inicial é o número de shards das settings. Se for um shrink, passa a ser `getRoutingNumShards()` do índice de origem. Esse valor é aplicado a `tmpImd` (via `tmpImdBuilder`) e a `indexMetaDataBuilder`. RIGHT também permite shrink para N shards: remove o `put("index.number_of_shards", 1)` e troca a validação por `getRoutingFactor`. O diff confirma o resumo, que omite as mudanças de shrink.
   - MERGE: combina as duas mudanças sem alterações adicionais.

2. ESTADO:
   - variável local `routingNumShards` (RIGHT);
   - `tmpImd`, incluindo `routingNumShards` e settings (RIGHT);
   - argumentos passados a `createIndex`, incluindo o novo callback (LEFT);
   - `indexService` retornado e `createdIndex`;
   - `indexMetaData`, incluindo `routingNumShards`;
   - `updatedState` retornado.

3. TABELA DE ESTADOS:
   - Entrada: shrink de índice origem com 8 shards (`routingNumShards` = 8) para `number_of_shards` = 2.
   - `routingNumShards`: BASE = inexistente | LEFT = inexistente | RIGHT = 8 | MERGE = 8
   - `tmpImd.routingNumShards`: BASE = 1 (shards forçado a 1) | LEFT = 1 | RIGHT = 8 | MERGE = 8
   - `tmpImd.number_of_shards`: BASE = 1 | LEFT = 1 | RIGHT = 2 | MERGE = 2
   - callback passado a `createIndex`: BASE = nenhum | LEFT = `shardId -> {}` | RIGHT = nenhum | MERGE = `shardId -> {}`
   - `indexMetaData.routingNumShards`: BASE = 1 | LEFT = 1 | RIGHT = 8 | MERGE = 8
   - `updatedState`: BASE = índice com 1 shard | LEFT = igual a BASE | RIGHT = índice com 2 shards e routing 8 | MERGE = igual a RIGHT

4. CRITÉRIO DE CONFLITO:
   - (A) Não se aplica. Nenhum elemento é igual em BASE, LEFT e RIGHT e diferente no MERGE.
   - (B) Não se aplica.
     - O callback difere de BASE em LEFT, e o MERGE o preserva.
     - `routingNumShards`, `tmpImd`, `indexMetaData` e `updatedState` diferem de BASE em RIGHT, e o MERGE preserva os valores de RIGHT.
   - (C) Não se aplica.
     - O callback de LEFT é um no-op. Ele não lê `routingNumShards` nem `tmpImd`, e o código de RIGHT não lê o callback.
     - Em ambos os pais, `createIndex` recebe o mesmo tipo de `tmpImd`. A única diferença é o `routingNumShards` de RIGHT, que segue igual no MERGE, e o callback vazio não altera o comportamento dependente disso.

</details>

#### claude-sonnet-5-5: NO ✅

<details><summary>Execução 1 (<code>1.csv</code>): NO</summary>

1. INTENÇÃO: LEFT passa a chamar indicesService.createIndex com dois argumentos a mais (um listener lambda `shardId -> {}`), mantendo tmpImd e a lista vazia. RIGHT introduz routingNumShards (calculado a partir das settings, ou do índice de origem no shrink) e o aplica em tmpImdBuilder e indexMetaDataBuilder. RIGHT também altera prepareShrinkIndexSettings (remove o put de number_of_shards=1) e validateShrinkIndex.

2. ESTADO: Em createIndex/execute, os elementos escritos são routingNumShards, tmpImd (com routingNumShards), indexService (resultado da chamada de createIndex, com os novos argumentos), indexMetaDataBuilder e o IndexMetaData final. Nas chamadas, o estado também inclui o listener passado a createIndex.

3. TABELA DE ESTADOS:
   - Entrada: request sem shrink, number_of_shards = 5.
   - routingNumShards: BASE = não existe | LEFT = não existe | RIGHT = 5 | MERGE = 5
   - tmpImd.routingNumShards: BASE = padrão | LEFT = padrão | RIGHT = 5 | MERGE = 5
   - indexService: BASE = createIndex(nsp, tmpImd, []) | LEFT = createIndex(nsp, tmpImd, [], listener) | RIGHT = igual a BASE, mas com tmpImd com routingNumShards | MERGE = createIndex(nsp, tmpImd com routingNumShards, [], listener)
   - indexMetaData final: BASE = sem routingNumShards | LEFT = igual a BASE | RIGHT = com routingNumShards 5 | MERGE = com routingNumShards 5
   
   O MERGE combina as duas mudanças de forma aditiva: a chamada de LEFT usa o tmpImd construído por RIGHT. LEFT não lê routingNumShards nem as settings alteradas, e o lambda `shardId -> {}` não depende do estado de RIGHT. RIGHT, por sua vez, não lê nada que LEFT escreva. O valor de cada elemento no MERGE coincide com o do pai que o alterou.

4. CRITÉRIO DE CONFLITO:
   - (A) não se aplica: nenhum valor muda no MERGE sem ter mudado em LEFT ou RIGHT.
   - (B) o MERGE preserva o valor de cada pai nos elementos que cada um alterou (a assinatura estendida de LEFT e o routingNumShards de RIGHT).
   - (C) o código alterado por um pai não lê nem é controlado por estado escrito pelo outro. A chamada de LEFT consome tmpImd, mas o comportamento relevante dela (o listener) é independente das mudanças de RIGHT.
   
   Não há interferência.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): NO</summary>

1. INTENÇÃO: LEFT passa dois novos argumentos (a lista vazia e o lambda shardId -&gt; {}) na chamada indicesService.createIndex, que ganhou uma sobrecarga ou assinatura nova. RIGHT introduz routingNumShards, calculado a partir de INDEX_NUMBER_OF_SHARDS_SETTING e, no caso de shrink, a partir do índice de origem. Esse valor alimenta tmpImdBuilder e indexMetaDataBuilder. RIGHT também troca o checagem de shrink por getRoutingFactor e remove o put de index.number_of_shards=1.

2. ESTADO: Os elementos escritos são indexService, criado por createIndex, tmpImd, que carrega routingNumShards, indexMetaData, que também carrega routingNumShards, e o estado do cluster resultante. Em RIGHT, a variável routingNumShards é lida por tmpImdBuilder e por indexMetaDataBuilder.

3. TABELA DE ESTADOS:
   - Entrada: criação de índice normal, sem shrink, com 5 shards.
   - routingNumShards: BASE = não existe | LEFT = não existe | RIGHT = 5 | MERGE = 5
   - tmpImd.routingNumShards: BASE = padrão (derivado das settings) | LEFT = igual a BASE | RIGHT = 5 | MERGE = 5
   - indexService: BASE = criado com tmpImd | LEFT = criado com tmpImd e o listener shardId -&gt; {} | RIGHT = criado com tmpImd (routingNumShards = 5) | MERGE = criado com tmpImd (routingNumShards = 5) e o listener
   - indexMetaData: BASE = sem routingNumShards explícito | LEFT = igual a BASE | RIGHT = routingNumShards = 5 | MERGE = routingNumShards = 5

4. CRITÉRIO DE CONFLITO:
   - (A) não se aplica: não há valor que seja igual em BASE, LEFT e RIGHT e diferente em MERGE.
   - (B) o MERGE preserva o valor de LEFT (o listener na chamada) e o valor de RIGHT (routingNumShards em tmpImd e em indexMetaData).
   - (C) a chamada alterada por LEFT lê tmpImd, que RIGHT alterou. No MERGE, porém, essa chamada recebe o mesmo tmpImd que receberia em RIGHT, com a única diferença sendo o argumento novo, que não depende de nenhum valor escrito por RIGHT. O lambda shardId -&gt; {} não lê estado. A variável routingNumShards só é lida pelos builders de RIGHT, e LEFT não a altera. Portanto, não há interferência de dados ou de controle.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): NO</summary>

1. INTENÇÃO: LEFT só adiciona dois argumentos à chamada indicesService.createIndex (a lista vazia e o listener `shardId -> {}`). RIGHT cria routingNumShards, usa-o em tmpImdBuilder e em indexMetaDataBuilder via setRoutingNumShards, e altera a lógica de shrink. Confirmei isso nos diffs.

2. ESTADO: Os elementos escritos no TARGET são:
   - routingNumShards (local);
   - tmpImd (construído com tmpImdBuilder);
   - indexService (retorno de createIndex com a nova assinatura);
   - indexMetaData (via indexMetaDataBuilder).
   O efeito de createIndex em indicesService é um estado externo.

3. TABELA DE ESTADOS:
   - Entrada: criação de um índice normal com 5 shards, sem shrink.
   - routingNumShards: BASE = não existe | LEFT = não existe | RIGHT = 5 | MERGE = 5
   - tmpImd.routingNumShards: BASE = padrão | LEFT = padrão | RIGHT = 5 | MERGE = 5
   - indexService: BASE = criado com tmpImd e sem listener | LEFT = criado com tmpImd e listener | RIGHT = criado com tmpImd(5) e sem listener | MERGE = criado com tmpImd(5) e listener
   - indexMetaData.routingNumShards: BASE = padrão | LEFT = padrão | RIGHT = 5 | MERGE = 5

   O merge é a união das duas mudanças. A chamada de createIndex em LEFT recebe tmpImd, que em RIGHT passa a ser construído de outra forma. O argumento tmpImd é o mesmo em ambos os lados, e o merge reproduz o comportamento de LEFT (listener) e o de RIGHT (tmpImd com routingNumShards).

4. CRITÉRIO DE CONFLITO:
   - (A) não se aplica: nenhum valor muda em MERGE sem ter mudado em LEFT ou RIGHT.
   - (B) o MERGE preserva LEFT (listener adicionado) e RIGHT (routingNumShards em tmpImd e em indexMetaData).
   - (C) o código alterado por LEFT, a chamada com o listener `shardId -> {}`, não lê routingNumShards e não é controlado por ele diretamente. Ele lê tmpImd, que RIGHT alterou. Nesse caso o comportamento depende só da assinatura e do listener vazio, que é um no-op. Assim, a chamada se comporta no MERGE como em LEFT, apenas com o tmpImd mais completo, que é o resultado pretendido por RIGHT. O listener vazio não depende do valor de tmpImd.
   Não há interferência indesejada.

</details>

#### claude-haiku-5-5: YES ❌

<details><summary>Execução 1 (<code>1.csv</code>): YES — Condição C: index.number_of_shards (valor propagado para tmpImd e lido pela chamada indicesService.createIndex)</summary>

1. INTENÇÃO: LEFT altera a chamada `indicesService.createIndex(...)` para passar um argumento extra, `shardId -> {}`. O resumo fala em "dois novos parâmetros", mas o diff adiciona apenas um. Confio no diff. RIGHT adiciona `routingNumShards`, usa `setRoutingNumShards` nos builders, troca a validação de shards do shrink por `getRoutingFactor` e remove `.put("index.number_of_shards", 1)` de `prepareShrinkIndexSettings`. O resumo diz "refatoração", mas o diff muda comportamento. Confio no diff.

2. ESTADO: Elementos escritos pelo target e pelos trechos alterados:
   - `indexSettingsBuilder` / `actualIndexSettings`, em especial a chave `index.number_of_shards`, escrita por `prepareShrinkIndexSettings` (BASE e RIGHT) e lida pelo `tmpImd`.
   - `tmpImd`, lido pela chamada `indicesService.createIndex(...)` que LEFT alterou.
   - `routingNumShards`, `tmpImdBuilder` e `indexMetaDataBuilder`, escritos apenas por RIGHT.
   - `shardId -> {}`, o argumento que LEFT adicionou.

3. TABELA DE ESTADOS:
   Entrada: shrink de um índice de origem com 10 shards, sem `index.number_of_shards` nas settings da requisição. O default de 5 é aplicado antes de `prepareShrinkIndexSettings`.
   - `index.number_of_shards` no `indexSettingsBuilder` antes de `tmpImd`:
     - BASE = 1 (forçado por `.put("index.number_of_shards", 1)`)
     - LEFT = 1
     - RIGHT = 5 (o `put` foi removido, então permanece o default)
     - MERGE = 5
   - `tmpImd.getNumberOfShards()` lido por `indicesService.createIndex(...)`:
     - BASE = 1 | LEFT = 1 | RIGHT = 5 | MERGE = 5
   - Validação com `getRoutingFactor(10, 5)`: passa em RIGHT e MERGE. Em BASE e LEFT essa validação não existe.
   - `routingNumShards`: BASE = não existe | LEFT = não existe | RIGHT = 10 (`sourceMetaData.getRoutingNumShards()`) | MERGE = 10

4. CRITÉRIO DE CONFLITO: X = `index.number_of_shards` (via `tmpImd`).
   - (A) não se aplica: o valor de X muda em RIGHT (1 para 5) e o MERGE reproduz RIGHT.
   - (B) não se aplica: o valor de X em LEFT (1) é igual ao de BASE (1).
   - (C) se aplica: o valor de X em RIGHT (5) difere de BASE (1). O código alterado por LEFT, a chamada `indicesService.createIndex(nodeServicesProvider, tmpImd, ...)`, lê `tmpImd`, que é derivado de X. No MERGE, essa chamada cria o índice temporário com 5 shards, e não com 1 como LEFT produziu e testou. Logo, o código de LEFT se comporta de forma diferente do que se comportava no seu pai.

   Para `routingNumShards`, não há conflito: BASE e LEFT não têm o elemento, e RIGHT é o único pai que o escreve.

</details>

<details><summary>Execução 2 (<code>2.csv</code>): YES — Condição C: tmpImd</summary>

1. INTENÇÃO: LEFT passa um callback no-op (`shardId -> {}`) como argumento extra em `indicesService.createIndex(...)`. O resumo diz "dois parâmetros", mas o diff adiciona apenas um argumento. RIGHT faz mais do que uma extração de variável: adiciona `routingNumShards`, aplica `setRoutingNumShards` em `tmpImd` e no `indexMetaDataBuilder`, remove o `number_of_shards = 1` forçado em `prepareShrinkIndexSettings` e troca a checagem de shards por `getRoutingFactor`. Confio no diff.

2. ESTADO: Elementos de estado escritos pelos trechos alterados:
   - `tmpImd` (escrito por RIGHT e lido pela chamada `indicesService.createIndex` alterada por LEFT);
   - `routingNumShards` (variável local nova de RIGHT);
   - `actualIndexSettings` (afetado por RIGHT via `prepareShrinkIndexSettings`, e alimenta `tmpImd`);
   - `indexMetaDataBuilder` (escrito por RIGHT);
   - o argumento do callback (LEFT), que não é lido por ninguém.

3. TABELA DE ESTADOS: Entrada: índice de origem com 4 shards e `routingNumShards = 4`; request de shrink para 2 shards.
   - `tmpImd.numberOfShards`: BASE = 1 | LEFT = 1 | RIGHT = 2 | MERGE = 2
   - `tmpImd.routingNumShards`: BASE = default derivado de 1 shard | LEFT = default derivado de 1 shard | RIGHT = 4 | MERGE = 4
   - Argumento de `createIndex` no 3º/4º parâmetro: BASE = `emptyList()` | LEFT = `emptyList()` + `shardId -> {}` | RIGHT = `emptyList()` | MERGE = `emptyList()` + `shardId -> {}`
   - `indexMetaDataBuilder.routingNumShards`: BASE = default | LEFT = default | RIGHT = 4 | MERGE = 4

4. CRITÉRIO DE CONFLITO: X = `tmpImd`.
   - (A) não se aplica: o valor de `tmpImd` muda em RIGHT em relação a BASE.
   - (B) `tmpImd` em LEFT é igual a BASE, então LEFT é preservado. Em RIGHT, `tmpImd` difere de BASE, e MERGE é igual a RIGHT (2 shards, routingNumShards 4), então RIGHT também é preservado. Não há violação de B.
   - (C) `tmpImd` difere de BASE em RIGHT, e o código alterado por LEFT (a chamada `indicesService.createIndex(nodeServicesProvider, tmpImd, ...)`) lê `tmpImd`. No pai LEFT, essa chamada recebia `tmpImd` com 1 shard e routing padrão. No MERGE, recebe `tmpImd` com 2 shards e routingNumShards 4. Assim, o código de LEFT se comporta de forma diferente do que seu autor observou. A intenção de RIGHT não remove essa condição, porque a regra é de dependência de dados e ela se aplica.
   - Os demais elementos (`routingNumShards`, `indexMetaDataBuilder`) não são lidos pelo código alterado por LEFT, então não geram conflito.

</details>

<details><summary>Execução 3 (<code>3.csv</code>): YES — Condição C: tmpImd (routingNumShards)</summary>

1. INTENÇÃO: LEFT passa um argumento extra (`shardId -> {}`) à chamada `indicesService.createIndex(...)`. O resumo diz "dois novos parâmetros", mas o diff adiciona apenas um argumento, então confio no diff. RIGHT remove imports não usados, introduz `routingNumShards` (vindo do índice de origem em caso de shrink), passa a construir `tmpImd` com `setRoutingNumShards(routingNumShards)` e remove `index.number_of_shards = 1` de `prepareShrinkIndexSettings`. Também altera a validação em `validateShrinkIndex`, que não é o TARGET.

2. ESTADO: Elementos escritos pelo TARGET e pelos trechos alterados:
   - `tmpImd` (e seu `routingNumShards`), escrito por RIGHT e lido por LEFT na chamada `indicesService.createIndex(...)`.
   - `indexService`, retornado pela chamada alterada por LEFT.
   - `actualIndexSettings` / `number_of_shards`, alterado por RIGHT via `prepareShrinkIndexSettings`.
   - `indexMetaData` / `routingNumShards` do build final, escrito por RIGHT.

3. TABELA DE ESTADOS:
   Entrada: shrink de `logs` (source com 8 shards e routingNumShards = 1024) para um índice com 2 shards, sem `index.number_of_shards` explícito na requisição. Valores simplificados para fins de cálculo.
   - `number_of_shards` (actualIndexSettings): BASE = 1 | LEFT = 1 | RIGHT = 2 | MERGE = 2
   - `tmpImd.routingNumShards` (valor passado para `indicesService.createIndex`): BASE = 2 (default derivado de 2 shards) | LEFT = 2 | RIGHT = 1024 | MERGE = 1024
   - `indexService` (objeto retornado): BASE = serviço criado com tmpImd de routing 2 | LEFT = mesmo serviço com listener no-op | RIGHT = serviço criado com routing 1024 | MERGE = serviço criado com routing 1024 e listener no-op

4. CRITÉRIO DE CONFLITO: X = `tmpImd.routingNumShards`, que é o estado que a chamada alterada por LEFT consome.
   - (A) não se aplica: X difere de BASE em RIGHT (1024 ≠ 2) e a condição exige igualdade em BASE, LEFT e RIGHT.
   - (B) não se aplica: MERGE (1024) preserva o valor de RIGHT (1024).
   - (C) se aplica: RIGHT alterou X, e o código alterado por LEFT (a chamada `indicesService.createIndex(nodeServicesProvider, tmpImd, ..., shardId -> {})`) lê `tmpImd`. Esse código recebe um `tmpImd` com routing 1024 no MERGE e com routing 2 no LEFT, então se comporta de forma diferente do que se comportaria no pai LEFT.
   - Observação: `number_of_shards` também chega ao código de LEFT pela dependência `tmpImd ← actualIndexSettings`, mas a dependência direta e relevante é `tmpImd.routingNumShards`.
   - A intenção de RIGHT (routing do índice de origem no shrink) não descarta a condição C, pois a regra considera apenas a dependência e a diferença de comportamento.

</details>

