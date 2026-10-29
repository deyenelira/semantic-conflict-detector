PROMPTS = {
    "zero_shot_autonomous": """Você é um desenvolvedor sênior investigando se um merge introduziu um conflito semântico.

<definicoes>
DEFINIÇÃO CONFLITO SEMÂNTICO
Conflito semântico ocorre quando dois commits se juntam sem conflito textual, mas o programa resultante se comporta de forma diferente do que algum dos desenvolvedores queria (interferência indesejada). Isso geralmente ocorre devido à interferência no fluxo de dados ou controle entre as modificações.

DEFINIÇÃO ELEMENTO DE ESTADO (VARIÁVEL DE ESTADO)
É qualquer posição de memória ou canal de saída que a execução do código pode escrever e depois ler. Inclui: variável local, parâmetro, campo estático ou de instância, posição de array, elemento de coleção, arquivo, fluxo, expressão de um return, exceção lançada e estado temporário.
</definicoes>

<formato_da_entrada>
BASE contém o código completo. LEFT, RIGHT e MERGE são diffs unificados em relação a BASE.
</formato_da_entrada>

<instrucoes>
Estruture sua resposta obrigatoriamente em dois blocos, nesta ordem: <analise> e <resultado>.

Dentro da tag <analise>, execute os seguintes passos, um após o outro:
1. INTENÇÃO: Resuma o que LEFT mudou em relação a BASE e o que RIGHT mudou.
2. ESTADO: Liste os elementos de estado escritos pelos trechos alterados de LEFT e RIGHT.
3. TABELA DE ESTADOS: Descreva o comportamento/valor final esperado para os elementos afetados em BASE | LEFT | RIGHT | MERGE.
4. CRITÉRIO DE CONFLITO: Avalie se existe algum elemento de estado X onde:
   - (A) o valor de X é igual em BASE, LEFT e RIGHT, mas diferente em MERGE; ou
   - (B) o valor de X em LEFT (ou RIGHT) difere de BASE, e o MERGE não preserva o valor desse pai.

Dentro da tag <resultado>, retorne APENAS uma das seguintes linhas, sem texto adicional:
- SIM - Condição <A ou B>: <variável de estado que sofreu o conflito>
- NAO
</instrucoes>

<caso>
<base>
{base}
</base>

<left>
{left}
</left>

<right>
{right}
</right>

<merge>
{merge}
</merge>
</caso>

Analise o caso acima seguindo os passos de <instrucoes> e responda nos blocos <analise> e <resultado>.""",

    "one_shot_autonomous": """Você é um desenvolvedor sênior investigando se um merge introduziu um conflito semântico.

<definicoes>
DEFINIÇÃO CONFLITO SEMÂNTICO
Conflito semântico ocorre quando dois commits se juntam sem conflito textual, mas o programa resultante se comporta de forma diferente do que algum dos desenvolvedores queria (interferência indesejada). Isso geralmente ocorre devido à interferência no fluxo de dados ou controle entre as modificações.

DEFINIÇÃO ELEMENTO DE ESTADO (VARIÁVEL DE ESTADO)
É qualquer posição de memória ou canal de saída que a execução do código pode escrever e depois ler. Inclui: variável local, parâmetro, campo estático ou de instância, posição de array, elemento de coleção, arquivo, fluxo, expressão de um return, exceção lançada e estado temporário.

EXEMPLOS DE ELEMENTOS DE ESTADO
- Campo de instância reescrito por vários métodos: this.text, que normalizeWhiteSpace() e removeDuplicateWords() reescrevem.
- Variável local: em "Settings settings = builder.build();". Se LEFT e RIGHT atribuem a settings, há escrita no mesmo elemento.
- Elemento de coleção / estado de uma lista: se LEFT adiciona 5 itens e RIGHT adiciona outros 3, o tamanho final depende de ambos.
- Valor retornado: a expressão em "return x + y;".
- Posição de array: a[0] e a[1] não interferem; já a = new int[3] interfere com a[0] = 1.
</definicoes>

<formato_da_entrada>
BASE contém o código completo. LEFT, RIGHT e MERGE são diffs unificados em relação a BASE.
</formato_da_entrada>

<instrucoes>
Estruture sua resposta obrigatoriamente em dois blocos, nesta ordem: <analise> e <resultado>.

Dentro da tag <analise>, execute os seguintes passos, um após o outro:
1. INTENÇÃO: Resuma o que LEFT mudou em relação a BASE e o que RIGHT mudou.
2. ESTADO: Liste os elementos de estado escritos pelos trechos alterados de LEFT e RIGHT.
3. TABELA DE ESTADOS: Descreva o comportamento/valor final esperado para os elementos afetados em BASE | LEFT | RIGHT | MERGE.
4. CRITÉRIO DE CONFLITO: Avalie se existe algum elemento de estado X onde:
   - (A) o valor de X é igual em BASE, LEFT e RIGHT, mas diferente em MERGE; ou
   - (B) o valor de X em LEFT (ou RIGHT) difere de BASE, e o MERGE não preserva o valor desse pai.

Dentro da tag <resultado>, retorne APENAS uma das seguintes linhas, sem texto adicional:
- SIM - Condição <A ou B>: <variável de estado que sofreu o conflito>
- NAO
</instrucoes>

<exemplos>
<exemplo numero="1">
<entrada>
BASE:
cleanText() {{
    removeComments();
}}
LEFT: (adiciona normalizeWhiteSpace antes)
RIGHT: (adiciona removeDuplicateWords depois)
MERGE: (adiciona os dois)
</entrada>
<saida_esperada>
<analise>
1. INTENÇÃO: LEFT colapsa espaços múltiplos. RIGHT remove palavras duplicadas consecutivas.
2. ESTADO: O campo `text` da instância, que cada método chamado em `cleanText` reescreve.
3. TABELA DE ESTADOS:
   - Entrada: "HELLO  HELLO  WORLD"
   - BASE: "HELLO  HELLO  WORLD" (sem comentários)
   - LEFT: "HELLO HELLO WORLD"
   - RIGHT: "HELLO    WORLD"
   - MERGE: "HELLO  WORLD"
4. CRITÉRIO DE CONFLITO: X = this.text.
   - (A) não se aplica: o valor de X em LEFT e em RIGHT difere de BASE.
   - (B) o valor de X em LEFT ("HELLO HELLO WORLD") difere de BASE, e o MERGE ("HELLO  WORLD") não preserva esse valor.
</analise>
<resultado>
SIM - Condição B: this.text
</resultado>
</saida_esperada>
</exemplo>

<exemplo numero="2">
<entrada>
BASE:
computePrice(price) {{
    total = price;
}}
LEFT: (soma 10 a price antes e subtrai 10 de total depois)
RIGHT: (soma 5 a price antes e subtrai 5 de total depois)
MERGE: (mantém os dois ajustes antes, mas só a subtração de 10 depois)
</entrada>
<saida_esperada>
<analise>
1. INTENÇÃO: LEFT ajusta price em 10 e compensa em total. RIGHT ajusta price em 5 e compensa em total.
2. ESTADO: A variável local `total`, escrita em `computePrice`.
3. TABELA DE ESTADOS:
   - Entrada: price = 100
   - BASE: total = 100
   - LEFT: total = 100
   - RIGHT: total = 100
   - MERGE: total = 105
4. CRITÉRIO DE CONFLITO: X = total.
   - (A) o valor de X é 100 em BASE, LEFT e RIGHT, mas 105 em MERGE.
   - (B) não se aplica: o valor de X em LEFT e RIGHT é igual ao de BASE.
</analise>
<resultado>
SIM - Condição A: total
</resultado>
</saida_esperada>
</exemplo>

<exemplo numero="3">
<entrada>
BASE:
processOrder() {{
    validate();
}}
LEFT: (adiciona updateStock() depois de validate)
RIGHT: (adiciona sendEmail() depois de validate)
MERGE: (adiciona as duas chamadas)
</entrada>
<saida_esperada>
<analise>
1. INTENÇÃO: LEFT atualiza o estoque. RIGHT envia um e-mail de confirmação.
2. ESTADO: O campo `stock`, escrito por updateStock() (LEFT), e a caixa de saída `outbox`, escrita por sendEmail() (RIGHT).
3. TABELA DE ESTADOS:
   - stock: BASE = inalterado | LEFT = decrementado | RIGHT = inalterado | MERGE = decrementado
   - outbox: BASE = vazia | LEFT = vazia | RIGHT = 1 e-mail | MERGE = 1 e-mail
4. CRITÉRIO DE CONFLITO: X = stock e X = outbox.
   - (A) não se aplica: nenhum valor muda no MERGE sem ter mudado em LEFT ou RIGHT.
   - (B) o valor de stock em LEFT e o de outbox em RIGHT diferem de BASE, e o MERGE preserva ambos.
</analise>
<resultado>
NAO
</resultado>
</saida_esperada>
</exemplo>
</exemplos>

AGORA ANALISE O SEGUINTE CASO:

<caso>
<base>
{base}
</base>

<left>
{left}
</left>

<right>
{right}
</right>

<merge>
{merge}
</merge>
</caso>

Analise o caso acima seguindo os passos de <instrucoes> e responda nos blocos <analise> e <resultado>.""",

    "zero_shot_guided": """Você é um desenvolvedor sênior investigando se um merge introduziu um conflito semântico.

<definicoes>
DEFINIÇÃO CONFLITO SEMÂNTICO
Conflito semântico ocorre quando dois commits se juntam sem conflito textual, mas o programa resultante se comporta de forma diferente do que algum dos desenvolvedores queria (interferência indesejada).

DEFINIÇÃO ELEMENTO DE ESTADO (VARIÁVEL DE ESTADO)
É qualquer posição de memória ou canal de saída que a execução do código pode escrever e depois ler. Inclui: variável local, parâmetro, campo estático ou de instância, posição de array, elemento de coleção, arquivo, fluxo, expressão de um return, exceção lançada e estado temporário.

TARGET é o método que sofreu alteração no merge; centre a análise nele.
</definicoes>

<formato_da_entrada>
BASE contém o código completo. LEFT, RIGHT e MERGE são diffs unificados em relação a BASE.
</formato_da_entrada>

<instrucoes>
Estruture sua resposta obrigatoriamente em dois blocos, nesta ordem: <analise> e <resultado>.

Dentro da tag <analise>, execute os seguintes passos, um após o outro:
1. INTENÇÃO: Use os resumos de LEFT e RIGHT fornecidos abaixo como o comportamento que cada desenvolvedor quis introduzir.
2. ESTADO: Liste os elementos de estado escritos pelo método TARGET e pelos trechos alterados.
3. TABELA DE ESTADOS: Descreva o comportamento/valor final esperado para os elementos afetados em BASE | LEFT | RIGHT | MERGE.
4. CRITÉRIO DE CONFLITO: Avalie se existe algum elemento de estado X onde:
   - (A) o valor de X é igual em BASE, LEFT e RIGHT, mas diferente em MERGE; ou
   - (B) o valor de X em LEFT (ou RIGHT) difere de BASE, e o MERGE não preserva o valor desse pai.

Dentro da tag <resultado>, retorne APENAS uma das seguintes linhas, sem texto adicional:
- SIM - Condição <A ou B>: <variável de estado que sofreu o conflito>
- NAO
</instrucoes>

<caso>
<resumo_das_mudancas>
RESUMO DAS MUDANÇAS (fornecido)
LEFT: {left_summary}
RIGHT: {right_summary}
TARGET: {target}
</resumo_das_mudancas>

<base>
{base}
</base>

<left>
{left}
</left>

<right>
{right}
</right>

<merge>
{merge}
</merge>
</caso>

Analise o caso acima seguindo os passos de <instrucoes> e responda nos blocos <analise> e <resultado>.""",

    "one_shot_guided": """Você é um desenvolvedor sênior investigando se um merge introduziu um conflito semântico.

<definicoes>
DEFINIÇÃO CONFLITO SEMÂNTICO
Conflito semântico ocorre quando dois commits se juntam sem conflito textual, mas o programa resultante se comporta de forma diferente do que algum dos desenvolvedores queria (interferência indesejada).

DEFINIÇÃO ELEMENTO DE ESTADO (VARIÁVEL DE ESTADO)
É qualquer posição de memória ou canal de saída que a execução do código pode escrever e depois ler.

TARGET é o método que sofreu alteração no merge; centre a análise nele.
</definicoes>

<instrucoes>
Estruture sua resposta obrigatoriamente em dois blocos, nesta ordem: <analise> e <resultado>.

Dentro da tag <analise>, execute os seguintes passos, um após o outro:
1. INTENÇÃO: Use os resumos de LEFT e RIGHT fornecidos abaixo.
2. ESTADO: Liste os elementos de estado escritos pelo método TARGET.
3. TABELA DE ESTADOS: Descreva o comportamento esperado em BASE | LEFT | RIGHT | MERGE.
4. CRITÉRIO DE CONFLITO: Avalie se existe algum elemento de estado X onde:
   - (A) o valor de X é igual em BASE, LEFT e RIGHT, mas diferente em MERGE; ou
   - (B) o valor de X em LEFT (ou RIGHT) difere de BASE, e o MERGE não preserva o valor desse pai.

Dentro da tag <resultado>, retorne APENAS uma das seguintes linhas, sem texto adicional:
- SIM - Condição <A ou B>: <variável de estado que sofreu o conflito>
- NAO
</instrucoes>

<exemplos>
<exemplo numero="1">
<entrada>
RESUMO DAS MUDANÇAS
LEFT: Left adds a call to normalizeWhiteSpace() in cleanText()
RIGHT: Right adds a call to removeDuplicateWords() in cleanText()
TARGET: cleanText()
</entrada>
<saida_esperada>
<analise>
1. INTENÇÃO: LEFT colapsa espaços. RIGHT remove duplicatas.
2. ESTADO: this.text, reescrito pelas chamadas na ordem em que aparecem.
3. TABELA DE ESTADOS:
   - Entrada: "HELLO  HELLO  WORLD"
   - LEFT: "HELLO HELLO WORLD"
   - RIGHT: "HELLO    WORLD"
   - MERGE: "HELLO  WORLD"
4. CRITÉRIO DE CONFLITO: X = this.text.
   - (A) não se aplica: o valor de X em LEFT e em RIGHT difere de BASE.
   - (B) o valor de X em LEFT ("HELLO HELLO WORLD") difere de BASE, e o MERGE ("HELLO  WORLD") não preserva esse valor.
</analise>
<resultado>
SIM - Condição B: this.text
</resultado>
</saida_esperada>
</exemplo>

<exemplo numero="2">
<entrada>
RESUMO DAS MUDANÇAS
LEFT: Left adds 10 to price before computing and subtracts 10 from total afterwards in computePrice()
RIGHT: Right adds 5 to price before computing and subtracts 5 from total afterwards in computePrice()
TARGET: computePrice()
</entrada>
<saida_esperada>
<analise>
1. INTENÇÃO: LEFT ajusta price em 10 e compensa em total. RIGHT ajusta price em 5 e compensa em total.
2. ESTADO: A variável local total, escrita em computePrice().
3. TABELA DE ESTADOS:
   - Entrada: price = 100
   - BASE: total = 100
   - LEFT: total = 100
   - RIGHT: total = 100
   - MERGE: total = 105
4. CRITÉRIO DE CONFLITO: X = total.
   - (A) o valor de X é 100 em BASE, LEFT e RIGHT, mas 105 em MERGE.
   - (B) não se aplica: o valor de X em LEFT e RIGHT é igual ao de BASE.
</analise>
<resultado>
SIM - Condição A: total
</resultado>
</saida_esperada>
</exemplo>

<exemplo numero="3">
<entrada>
RESUMO DAS MUDANÇAS
LEFT: Left adds a call to updateStock() in processOrder()
RIGHT: Right adds a call to sendEmail() in processOrder()
TARGET: processOrder()
</entrada>
<saida_esperada>
<analise>
1. INTENÇÃO: LEFT atualiza o estoque. RIGHT envia um e-mail de confirmação.
2. ESTADO: O campo stock, escrito por updateStock() (LEFT), e a caixa de saída outbox, escrita por sendEmail() (RIGHT).
3. TABELA DE ESTADOS:
   - stock: BASE = inalterado | LEFT = decrementado | RIGHT = inalterado | MERGE = decrementado
   - outbox: BASE = vazia | LEFT = vazia | RIGHT = 1 e-mail | MERGE = 1 e-mail
4. CRITÉRIO DE CONFLITO: X = stock e X = outbox.
   - (A) não se aplica: nenhum valor muda no MERGE sem ter mudado em LEFT ou RIGHT.
   - (B) o valor de stock em LEFT e o de outbox em RIGHT diferem de BASE, e o MERGE preserva ambos.
</analise>
<resultado>
NAO
</resultado>
</saida_esperada>
</exemplo>
</exemplos>

AGORA ANALISE O SEGUINTE CASO:

<caso>
<resumo_das_mudancas>
RESUMO DAS MUDANÇAS (fornecido)
LEFT: {left_summary}
RIGHT: {right_summary}
TARGET: {target}
</resumo_das_mudancas>

<base>
{base}
</base>

<left>
{left}
</left>

<right>
{right}
</right>

<merge>
{merge}
</merge>
</caso>

Analise o caso acima seguindo os passos de <instrucoes> e responda nos blocos <analise> e <resultado>."""
}
