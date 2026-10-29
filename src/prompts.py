DEFINICOES = """<definicoes>
DEFINIÇÃO CONFLITO SEMÂNTICO
Conflito semântico ocorre quando dois commits se juntam sem conflito textual, mas o programa resultante se comporta de forma diferente do que algum dos desenvolvedores queria (interferência indesejada). Isso geralmente ocorre devido à interferência no fluxo de dados ou de controle entre as modificações.

DEFINIÇÃO ELEMENTO DE ESTADO (VARIÁVEL DE ESTADO)
É qualquer posição de memória ou canal de saída que a execução do código pode escrever e depois ler. Inclui: variável local, parâmetro, campo estático ou de instância, posição de array, elemento de coleção, arquivo, fluxo, expressão de um return, exceção lançada e estado temporário.

TARGET é o método que sofreu alteração no merge; centre a análise nele.
</definicoes>"""

PASSOS = """1. INTENÇÃO: Use os resumos de LEFT e RIGHT fornecidos abaixo como ponto de partida e confirme-os nos diffs. Se um resumo contradisser o diff, confie no diff.
2. ESTADO: Liste os elementos de estado escritos pelo método TARGET e pelos trechos alterados.
3. TABELA DE ESTADOS: Escolha uma entrada concreta que exercite as mudanças e calcule, executando o código dos diffs passo a passo, o valor de cada elemento afetado em BASE | LEFT | RIGHT | MERGE. Escreva valores.
@@CRITERIO@@"""

CRITERIO = """4. CRITÉRIO DE CONFLITO: Avalie cada elemento de estado X da tabela. "Valor de X" é o valor final observável do elemento inteiro, e não apenas a parte que um dos lados alterou. O MERGE "preserva" o valor de um pai quando o valor de X no MERGE é igual ao valor de X nesse pai. Existe conflito se, para algum X:
   - (A) o valor de X é igual em BASE, LEFT e RIGHT, mas diferente em MERGE; ou
   - (B) o valor de X em LEFT (ou RIGHT) difere de BASE, e o MERGE não preserva o valor desse pai; ou
   - (C) o valor de X em um dos pais difere de BASE, e o código alterado pelo outro pai lê X ou é controlado por X (dependência de dados ou de controle), de modo que esse código se comporta no MERGE de forma diferente de como se comporta no pai que o escreveu.
   Decida pela aplicação dessas condições aos valores da tabela. Não use a intenção dos desenvolvedores para descartar uma condição que se aplica, nem para criar uma que não se aplica."""

RESULTADO = """Dentro da tag <resultado>, retorne APENAS uma das seguintes linhas, sem texto adicional:
- SIM - Condição <A, B ou C>: <variável de estado que sofreu o conflito>
- NAO"""

CASO = """<caso>
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
</caso>"""

# exemplos sintéticos, de domínios diferentes dos casos avaliados, com SIM e NAO equilibrados
EXEMPLOS = """<exemplos>
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
   - BASE: "HELLO  HELLO  WORLD"
   - LEFT: "HELLO HELLO WORLD"
   - RIGHT: "HELLO    WORLD"
   - MERGE: "HELLO  WORLD"
4. CRITÉRIO DE CONFLITO: X = this.text.
   - (A) não se aplica: o valor de X em LEFT e em RIGHT difere de BASE.
   - (B) o valor de X em LEFT ("HELLO HELLO WORLD") difere de BASE, e o valor no MERGE ("HELLO  WORLD") é diferente dele, então LEFT não é preservado.
   - (C) não é necessária, pois B já se aplica.
</analise>
<resultado>
SIM - Condição B: this.text
</resultado>
</saida_esperada>
</exemplo>

<exemplo numero="2">
<entrada>
RESUMO DAS MUDANÇAS
LEFT: Left changes the timeout constant from 30 to 60 in connect()
RIGHT: Right changes the timeout constant from 30 to 60 in connect()
TARGET: connect()
</entrada>
<saida_esperada>
<analise>
1. INTENÇÃO: LEFT e RIGHT aumentam o timeout para 60.
2. ESTADO: O campo timeout, lido por connect().
3. TABELA DE ESTADOS:
   - timeout: BASE = 30 | LEFT = 60 | RIGHT = 60 | MERGE = 60
4. CRITÉRIO DE CONFLITO: X = timeout.
   - (A) não se aplica: o valor de X em LEFT e em RIGHT difere de BASE.
   - (B) o valor de X em LEFT (60) e em RIGHT (60) difere de BASE, e o MERGE (60) é igual a ambos, então é preservado.
   - (C) nenhum código alterado lê um valor de X diferente do que o pai que o escreveu produziria.
</analise>
<resultado>
NAO
</resultado>
</saida_esperada>
</exemplo>

<exemplo numero="3">
<entrada>
RESUMO DAS MUDANÇAS
LEFT: Left changes the condition in isEligible() from age >= 18 to age >= 21
RIGHT: Right adds a call to sendCoupon(user) inside the if (isEligible(user)) block in notifyUsers()
TARGET: notifyUsers()
</entrada>
<saida_esperada>
<analise>
1. INTENÇÃO: LEFT torna a elegibilidade mais restrita (21 anos). RIGHT envia um cupom para os usuários elegíveis.
2. ESTADO: O resultado de isEligible(user), lido pelo if de notifyUsers(), e a caixa de saída coupons, escrita por sendCoupon().
3. TABELA DE ESTADOS:
   - Entrada: user com age = 19
   - isEligible: BASE = true | LEFT = false | RIGHT = true | MERGE = false
   - coupons: BASE = vazia | LEFT = vazia | RIGHT = 1 cupom | MERGE = vazia
4. CRITÉRIO DE CONFLITO: X = isEligible(user) e X = coupons.
   - (A) não se aplica: nenhum valor muda no MERGE sem ter mudado em LEFT ou RIGHT.
   - (B) o MERGE preserva o valor de isEligible de LEFT. O valor de coupons em RIGHT (1 cupom) difere de BASE e não é preservado no MERGE (vazia).
   - (C) o valor de isEligible em LEFT difere de BASE, e o código adicionado por RIGHT é controlado por esse valor, então se comporta no MERGE de forma diferente de RIGHT.
</analise>
<resultado>
SIM - Condição C: isEligible(user)
</resultado>
</saida_esperada>
</exemplo>

<exemplo numero="4">
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
   - Entrada: pedido de 1 unidade, stock = 10
   - stock: BASE = 10 | LEFT = 9 | RIGHT = 10 | MERGE = 9
   - outbox: BASE = vazia | LEFT = vazia | RIGHT = 1 e-mail | MERGE = 1 e-mail
4. CRITÉRIO DE CONFLITO: X = stock e X = outbox.
   - (A) não se aplica: nenhum valor muda no MERGE sem ter mudado em LEFT ou RIGHT.
   - (B) o valor de stock em LEFT e o de outbox em RIGHT diferem de BASE, e o MERGE é igual a cada um deles.
   - (C) sendEmail() não lê stock, e updateStock() não lê outbox.
</analise>
<resultado>
NAO
</resultado>
</saida_esperada>
</exemplo>

<exemplo numero="5">
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
   - (C) não é necessária, pois A já se aplica.
</analise>
<resultado>
SIM - Condição A: total
</resultado>
</saida_esperada>
</exemplo>

<exemplo numero="6">
<entrada>
RESUMO DAS MUDANÇAS
LEFT: Left changes the text of the exception message thrown in validate()
RIGHT: Right adds a null check on the name parameter at the start of validate(), before the existing checks
TARGET: validate()
</entrada>
<saida_esperada>
<analise>
1. INTENÇÃO: LEFT muda a mensagem de erro de um dos checks existentes. RIGHT rejeita name nulo antes dos demais checks.
2. ESTADO: A exceção lançada por validate() (tipo e mensagem).
3. TABELA DE ESTADOS:
   - Entrada A: name = "x" com o check existente falhando
     - BASE: IllegalArgumentException("invalid") | LEFT: IllegalArgumentException("invalid format") | RIGHT: IllegalArgumentException("invalid") | MERGE: IllegalArgumentException("invalid format")
   - Entrada B: name = null
     - BASE: NullPointerException ao usar name | LEFT: igual a BASE | RIGHT: IllegalArgumentException("name is null") | MERGE: IllegalArgumentException("name is null")
4. CRITÉRIO DE CONFLITO: X = exceção lançada.
   - (A) não se aplica: nenhum valor muda no MERGE sem ter mudado em LEFT ou RIGHT.
   - (B) o MERGE é igual a LEFT na entrada A e igual a RIGHT na entrada B.
   - (C) o novo check de RIGHT não lê nem é controlado pela mensagem alterada por LEFT.
</analise>
<resultado>
NAO
</resultado>
</saida_esperada>
</exemplo>
</exemplos>"""

FECHO = "Analise o caso acima seguindo os passos de <instrucoes> e responda nos blocos <analise> e <resultado>."

CABECALHO = "Você é um desenvolvedor sênior investigando se um merge introduziu um conflito semântico."

INSTRUCOES = """<instrucoes>
Estruture sua resposta obrigatoriamente em dois blocos, nesta ordem: <analise> e <resultado>.

Dentro da tag <analise>, execute os seguintes passos, um após o outro:
{passos}

@@RESULTADO@@
</instrucoes>"""

FORMATO_ENTRADA = """<formato_da_entrada>
BASE contém o código completo. LEFT, RIGHT e MERGE são diffs unificados em relação a BASE.
</formato_da_entrada>"""

# zero-shot e one-shot diferem apenas pela presença dos exemplos
_instrucoes = INSTRUCOES.replace("{passos}", PASSOS)

_zero = "\n\n".join([CABECALHO, DEFINICOES, FORMATO_ENTRADA, _instrucoes, CASO, FECHO])
_one = "\n\n".join([CABECALHO, DEFINICOES, FORMATO_ENTRADA, _instrucoes, EXEMPLOS,
                    "AGORA ANALISE O SEGUINTE CASO:", CASO, FECHO])

PROMPTS = {nome: texto.replace("@@CRITERIO@@", CRITERIO).replace("@@RESULTADO@@", RESULTADO)
           for nome, texto in {"zero_shot_guided": _zero, "one_shot_guided": _one}.items()}
