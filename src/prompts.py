PROMPTS = {
    "zero_shot_autonomous": """Você é um desenvolvedor sênior investigando se um merge introduziu um conflito semântico.

DEFINIÇÃO CONFLITO SEMÂNTICO
Conflito semântico ocorre quando dois commits se juntam sem conflito textual, mas o programa resultante se comporta de forma diferente do que algum dos desenvolvedores queria. Isso geralmente ocorre devido à interferência no fluxo de dados ou controle entre as modificações.

DEFINIÇÃO ELEMENTO DE ESTADO (VARIÁVEL DE ESTADO)
É qualquer posição de memória ou canal de saída que a execução do código pode escrever e depois ler. Inclui: variável local, parâmetro, campo estático ou de instância, posição de array, elemento de coleção, arquivo, fluxo, expressão de um return, exceção lançada e estado temporário.

Você deve estruturar sua resposta OBRIGATORIAMENTE em dois blocos: <analise> e <resultado>.

Dentro da tag <analise>, execute os seguintes passos:
1. INTENÇÃO: Resuma o que LEFT mudou em relação a BASE e o que RIGHT mudou.
2. ESTADO: Liste os elementos de estado lidos ou escritos pelos trechos alterados de LEFT e RIGHT.
3. TABELA DE ESTADOS: Descreva o comportamento/valor final esperado para os elementos afetados em BASE | LEFT | RIGHT | MERGE.
4. CRITÉRIO DE CONFLITO: Avalie se existe algum elemento X onde:
   - (A) LEFT e RIGHT escrevem/modificam elementos de estado dependentes e o MERGE não reconcilia essa dependência.
   - (B) O valor ou comportamento introduzido por LEFT (ou RIGHT) é sobrescrito, ignorado ou quebrado pelas alterações do outro no MERGE.

Dentro da tag <resultado>, retorne APENAS uma das seguintes linhas, sem texto adicional:
- SIM - Condição <A ou B>: <variável de estado que sofreu o conflito>
- NAO

BASE contém o código completo. LEFT, RIGHT e MERGE são diffs unificados em relação a BASE.

BASE:
{base}

LEFT:
{left}

RIGHT:
{right}

MERGE:
{merge}""",

    "one_shot_autonomous": """Você é um desenvolvedor sênior investigando se um merge introduziu um conflito semântico.

DEFINIÇÃO CONFLITO SEMÂNTICO
Conflito semântico ocorre quando dois commits se juntam sem conflito textual, mas o programa resultante se comporta de forma diferente do que algum dos desenvolvedores queria. Isso geralmente ocorre devido à interferência no fluxo de dados ou controle entre as modificações.

DEFINIÇÃO ELEMENTO DE ESTADO (VARIÁVEL DE ESTADO)
É qualquer posição de memória ou canal de saída que a execução do código pode escrever e depois ler. Inclui: variável local, parâmetro, campo estático ou de instância, posição de array, elemento de coleção, arquivo, fluxo, expressão de um return, exceção lançada e estado temporário.

EXEMPLOS DE ELEMENTOS DE ESTADO
- Campo de instância reescrito por vários métodos: this.text, que normalizeWhiteSpace() e removeDuplicateWords() leem e reescrevem.
- Variável local: em "Settings settings = builder.build();". Se LEFT e RIGHT atribuem a settings, há escrita no mesmo elemento.
- Elemento de coleção / estado de uma lista: se LEFT adiciona 5 itens e RIGHT adiciona outros 3, o tamanho final depende de ambos.
- Valor retornado: a expressão em "return x + y;".
- Posição de array: a[0] e a[1] não interferem; já a = new int[3] interfere com a[0] = 1.

Você deve estruturar sua resposta OBRIGATORIAMENTE em dois blocos: <analise> e <resultado>.

Dentro da tag <analise>, execute os seguintes passos:
1. INTENÇÃO: Resuma o que LEFT mudou em relação a BASE e o que RIGHT mudou.
2. ESTADO: Liste os elementos de estado lidos ou escritos pelos trechos alterados de LEFT e RIGHT.
3. TABELA DE ESTADOS: Descreva o comportamento/valor final esperado para os elementos afetados em BASE | LEFT | RIGHT | MERGE.
4. CRITÉRIO DE CONFLITO: Avalie se existe algum elemento X onde:
   - (A) LEFT e RIGHT escrevem/modificam elementos de estado dependentes e o MERGE não reconcilia essa dependência.
   - (B) O valor ou comportamento introduzido por LEFT (ou RIGHT) é sobrescrito, ignorado ou quebrado pelas alterações do outro no MERGE.

Dentro da tag <resultado>, retorne APENAS uma das seguintes linhas, sem texto adicional:
- SIM - Condição <A ou B>: <variável de estado que sofreu o conflito>
- NAO

BASE contém o código completo. LEFT, RIGHT e MERGE são diffs unificados em relação a BASE.

EXEMPLO DE ENTRADA:
BASE:
cleanText() {{
    removeComments();
}}
LEFT: (adiciona normalizeWhiteSpace antes)
RIGHT: (adiciona removeDuplicateWords depois)
MERGE: (adiciona os dois)

EXEMPLO DE SAÍDA ESPERADA:
<analise>
1. INTENÇÃO: LEFT colapsa espaços múltiplos. RIGHT remove palavras duplicadas consecutivas.
2. ESTADO: O campo `text` da instância, que cada método chamado em `cleanText` lê e reescreve (a ordem importa).
3. TABELA DE ESTADOS: 
   - Entrada: "HELLO  HELLO  WORLD"
   - BASE: "HELLO  HELLO  WORLD" (sem comentários)
   - LEFT: "HELLO HELLO WORLD"
   - RIGHT: "HELLO    WORLD"
   - MERGE: "HELLO  WORLD"
4. CRITÉRIO DE CONFLITO: O resultado do MERGE executa RIGHT depois de LEFT. A intenção de LEFT (colapso total de espaços) é quebrada pelas inserções de espaços de RIGHT ou pela falta de normalização final.
</analise>
<resultado>
SIM - Condição B: this.text
</resultado>

AGORA ANALISE O SEGUINTE CASO:

BASE:
{base}

LEFT:
{left}

RIGHT:
{right}

MERGE:
{merge}""",

    "zero_shot_guided": """Você é um desenvolvedor sênior investigando se um merge introduziu um conflito semântico.

DEFINIÇÃO CONFLITO SEMÂNTICO
Conflito semântico ocorre quando dois commits se juntam sem conflito textual, mas o programa resultante se comporta de forma diferente do que algum dos desenvolvedores queria. 

DEFINIÇÃO ELEMENTO DE ESTADO (VARIÁVEL DE ESTADO)
É qualquer posição de memória ou canal de saída que a execução do código pode escrever e depois ler. Inclui: variável local, parâmetro, campo estático ou de instância, posição de array, elemento de coleção, arquivo, fluxo, expressão de um return, exceção lançada e estado temporário.

TARGET é o método que sofreu alteração no merge; centre a análise nele.

Você deve estruturar sua resposta OBRIGATORIAMENTE em dois blocos: <analise> e <resultado>.

Dentro da tag <analise>, execute os seguintes passos:
1. INTENÇÃO: Use os resumos de LEFT e RIGHT fornecidos abaixo como o comportamento que cada desenvolvedor quis introduzir.
2. ESTADO: Liste os elementos de estado lidos ou escritos pelo método TARGET e pelos trechos alterados.
3. TABELA DE ESTADOS: Descreva o comportamento/valor final esperado para os elementos afetados em BASE | LEFT | RIGHT | MERGE.
4. CRITÉRIO DE CONFLITO: Avalie se existe algum elemento X onde:
   - (A) LEFT e RIGHT escrevem/modificam elementos de estado dependentes e o MERGE não reconcilia essa dependência.
   - (B) O valor ou comportamento introduzido por LEFT (ou RIGHT) difere de BASE, e o MERGE não preserva o efeito dessa mudança.

Dentro da tag <resultado>, retorne APENAS uma das seguintes linhas, sem texto adicional:
- SIM - Condição <A ou B>: <variável de estado que sofreu o conflito>
- NAO

BASE contém o código completo. LEFT, RIGHT e MERGE são diffs unificados em relação a BASE.

RESUMO DAS MUDANÇAS (fornecido)
LEFT: {left_summary}
RIGHT: {right_summary}
TARGET: {target}

BASE:
{base}

LEFT:
{left}

RIGHT:
{right}

MERGE:
{merge}""",

    "one_shot_guided": """Você é um desenvolvedor sênior investigando se um merge introduziu um conflito semântico.

DEFINIÇÃO CONFLITO SEMÂNTICO
Conflito semântico ocorre quando dois commits se juntam sem conflito textual, mas o programa resultante se comporta de forma diferente do que algum dos desenvolvedores queria.

DEFINIÇÃO ELEMENTO DE ESTADO (VARIÁVEL DE ESTADO)
É qualquer posição de memória ou canal de saída que a execução do código pode escrever e depois ler.

TARGET é o método que sofreu alteração no merge; centre a análise nele.

Você deve estruturar sua resposta OBRIGATORIAMENTE em dois blocos: <analise> e <resultado>.

Dentro da tag <analise>, execute os seguintes passos:
1. INTENÇÃO: Use os resumos de LEFT e RIGHT fornecidos abaixo.
2. ESTADO: Liste os elementos de estado lidos ou escritos pelo método TARGET.
3. TABELA DE ESTADOS: Descreva o comportamento esperado em BASE | LEFT | RIGHT | MERGE.
4. CRITÉRIO DE CONFLITO: Avalie se existe algum elemento X onde:
   - (A) LEFT e RIGHT escrevem/modificam elementos dependentes não reconciliados no MERGE.
   - (B) O MERGE quebra/sobrescreve o efeito introduzido por um dos lados.

Dentro da tag <resultado>, retorne APENAS uma das seguintes linhas, sem texto adicional:
- SIM - Condição <A ou B>: <variável de estado que sofreu o conflito>
- NAO

EXEMPLO DE ENTRADA:
RESUMO DAS MUDANÇAS
LEFT: Left adds a call to normalizeWhiteSpace() in cleanText()
RIGHT: Right adds a call to removeDuplicateWords() in cleanText()
TARGET: cleanText()

EXEMPLO DE SAÍDA ESPERADA:
<analise>
1. INTENÇÃO: LEFT colapsa espaços. RIGHT remove duplicatas.
2. ESTADO: this.text, lido e modificado pelas chamadas na ordem em que aparecem.
3. TABELA DE ESTADOS: 
   - Entrada: "HELLO  HELLO  WORLD"
   - LEFT: "HELLO HELLO WORLD"
   - RIGHT: "HELLO    WORLD"
   - MERGE: "HELLO  WORLD"
4. CRITÉRIO DE CONFLITO: O MERGE não preserva o colapso de espaços de LEFT.
</analise>
<resultado>
SIM - Condição B: this.text
</resultado>

AGORA ANALISE O SEGUINTE CASO:

RESUMO DAS MUDANÇAS (fornecido)
LEFT: {left_summary}
RIGHT: {right_summary}
TARGET: {target}

BASE:
{base}

LEFT:
{left}

RIGHT:
{right}

MERGE:
{merge}"""
}