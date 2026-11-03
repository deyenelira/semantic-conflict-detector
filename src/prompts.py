from src.datasets import unified_diff

CABECALHO = "Você é um desenvolvedor sênior investigando se um merge introduziu um conflito semântico."


def definicoes(com_target):
    texto = """<definicoes>
DEFINIÇÃO CONFLITO SEMÂNTICO
Conflito semântico ocorre quando dois commits se juntam sem conflito textual, mas o programa resultante se comporta de forma diferente do que algum dos desenvolvedores queria (interferência indesejada). Isso geralmente ocorre devido à interferência no fluxo de dados ou de controle entre as modificações.

DEFINIÇÃO ELEMENTO DE ESTADO (VARIÁVEL DE ESTADO)
É qualquer posição de memória ou canal de saída que a execução do código pode escrever e depois ler. Inclui: variável local, parâmetro, campo estático ou de instância, posição de array, elemento de coleção, arquivo, fluxo, expressão de um return, exceção lançada e estado temporário."""
    if com_target:
        texto += "\n\nTARGET é o método que sofreu alteração no merge; centre a análise nele."
    return texto + "\n</definicoes>"


FORMATO_ENTRADA = """<formato_da_entrada>
BASE contém o código completo. LEFT, RIGHT e MERGE são diffs unificados em relação a BASE.
</formato_da_entrada>"""

CRITERIO = """4. CRITÉRIO DE CONFLITO: Avalie cada elemento de estado X da tabela. "Valor de X" é o valor final observável do elemento inteiro, e não apenas a parte que um dos lados alterou. O MERGE "preserva" o valor de um pai quando o valor de X no MERGE é igual ao valor de X nesse pai. Existe conflito se, para algum X:
   - (A) o valor de X é igual em BASE, LEFT e RIGHT, mas diferente em MERGE; ou
   - (B) o valor de X em LEFT (ou RIGHT) difere de BASE, e o MERGE não preserva o valor desse pai; ou
   - (C) o valor de X em um dos pais difere de BASE, e o código alterado pelo outro pai lê X ou é controlado por X (dependência de dados ou de controle), de modo que esse código se comporta no MERGE de forma diferente de como se comporta no pai que o escreveu.
   Decida pela aplicação dessas condições aos valores da tabela. Não use a intenção dos desenvolvedores para descartar uma condição que se aplica, nem para criar uma que não se aplica."""


def passos(com_target, com_resumos):
    if com_resumos:
        intencao = "1. INTENÇÃO: Use os resumos de LEFT e RIGHT fornecidos abaixo como ponto de partida e confirme-os nos diffs. Se um resumo contradisser o diff, confie no diff."
    else:
        intencao = "1. INTENÇÃO: A partir dos diffs, resuma o que LEFT e o que RIGHT mudaram em relação a BASE."
    escritos_por = "pelo método TARGET e pelos trechos alterados" if com_target else "pelos trechos alterados"
    return f"""{intencao}
2. ESTADO: Liste os elementos de estado escritos {escritos_por}.
3. TABELA DE ESTADOS: Escolha uma entrada concreta que exercite as mudanças e calcule, executando o código dos diffs passo a passo, o valor de cada elemento afetado em BASE | LEFT | RIGHT | MERGE. Escreva valores.
{CRITERIO}"""


RESULTADO = """Dentro da tag <resultado>, retorne APENAS uma das seguintes linhas, sem texto adicional:
- SIM - Condição <A, B ou C>: <variável de estado que sofreu o conflito>
- NAO"""


def instrucoes(com_target, com_resumos):
    return f"""<instrucoes>
Estruture sua resposta obrigatoriamente em dois blocos, nesta ordem: <analise> e <resultado>.

Dentro da tag <analise>, execute os seguintes passos, um após o outro:
{passos(com_target, com_resumos)}

{RESULTADO}
</instrucoes>"""


def entrada(com_target, com_resumos):
    """Template da entrada de um caso, preenchido com .format(**linha_do_dataset)."""
    blocos = []
    if com_resumos:
        blocos.append("<resumo_das_mudancas>\nLEFT: {left_summary}\nRIGHT: {right_summary}\n</resumo_das_mudancas>")
    if com_target:
        blocos.append("<target>\n{target}\n</target>")
    blocos += [f"<{v}>\n{{{v}}}\n</{v}>" for v in ("base", "left", "right", "merge")]
    return "\n\n".join(blocos)


FECHO = "Analise o caso acima seguindo os passos de <instrucoes> e responda nos blocos <analise> e <resultado>."

# Exemplos sintéticos, de domínios diferentes dos casos avaliados, com SIM e NAO equilibrados.
# O código é completo em cada versão; na entrada do exemplo LEFT/RIGHT/MERGE viram diffs, como nos casos.
EXEMPLOS = [
    {
        "left_summary": "Left adds a call to normalizeWhiteSpace() in cleanText()",
        "right_summary": "Right adds a call to removeDuplicateWords() in cleanText()",
        "target": "cleanText()",
        "base": r"""class Text {
    private String text;

    Text(String text) {
        this.text = text;
    }

    void cleanText() {
        removeComments();
    }

    void removeComments() {
        text = text.replaceAll("//.*", "");
    }

    void normalizeWhiteSpace() {
        text = text.replaceAll(" +", " ");
    }

    // remove a segunda ocorrência de uma palavra repetida, mantendo os espaços
    void removeDuplicateWords() {
        text = text.replaceAll("\\b(\\w+)( +)\\1\\b", "$1$2");
    }
}
""",
        "left": [("    void cleanText() {\n", "    void cleanText() {\n        normalizeWhiteSpace();\n")],
        "right": [("        removeComments();\n    }\n\n    void removeComments",
                   "        removeComments();\n        removeDuplicateWords();\n    }\n\n    void removeComments")],
        "analise": """1. INTENÇÃO: LEFT colapsa espaços. RIGHT remove duplicatas.
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
   - (C) não é necessária, pois B já se aplica.""",
        "resultado": "SIM - Condição B: this.text",
    },
    {
        "left_summary": "Left changes the timeout constant from 30 to 60 in connect()",
        "right_summary": "Right changes the timeout constant from 30 to 60 in connect()",
        "target": "connect(String host)",
        "base": """class Client {
    private final Socket socket = new Socket();

    void connect(String host) {
        int timeout = 30;
        socket.connect(host, timeout);
    }
}
""",
        "left": [("int timeout = 30;", "int timeout = 60;")],
        "right": [("int timeout = 30;", "int timeout = 60;")],
        "analise": """1. INTENÇÃO: LEFT e RIGHT aumentam o timeout para 60.
2. ESTADO: A variável local timeout, lida por socket.connect().
3. TABELA DE ESTADOS:
   - timeout: BASE = 30 | LEFT = 60 | RIGHT = 60 | MERGE = 60
4. CRITÉRIO DE CONFLITO: X = timeout.
   - (A) não se aplica: o valor de X em LEFT e em RIGHT difere de BASE.
   - (B) o valor de X em LEFT (60) e em RIGHT (60) difere de BASE, e o MERGE (60) é igual a ambos, então é preservado.
   - (C) nenhum código alterado lê um valor de X diferente do que o pai que o escreveu produziria.""",
        "resultado": "NAO",
    },
    {
        "left_summary": "Left changes the condition in isEligible() from age >= 18 to age >= 21",
        "right_summary": "Right adds a call to sendCoupon(user) inside the if (isEligible(user)) block in notifyUsers()",
        "target": "notifyUsers(List<User> users)",
        "base": """class Notifier {
    private final List<String> coupons = new ArrayList<>();

    boolean isEligible(User user) {
        return user.getAge() >= 18;
    }

    void notifyUsers(List<User> users) {
        for (User user : users) {
            if (isEligible(user)) {
                sendNewsletter(user);
            }
        }
    }

    void sendNewsletter(User user) {
        System.out.println("Newsletter sent to " + user.getName());
    }

    void sendCoupon(User user) {
        coupons.add(user.getName());
    }
}
""",
        "left": [("user.getAge() >= 18", "user.getAge() >= 21")],
        "right": [("                sendNewsletter(user);\n",
                   "                sendNewsletter(user);\n                sendCoupon(user);\n")],
        "analise": """1. INTENÇÃO: LEFT torna a elegibilidade mais restrita (21 anos). RIGHT envia um cupom para os usuários elegíveis.
2. ESTADO: O resultado de isEligible(user), lido pelo if de notifyUsers(), e a lista coupons, escrita por sendCoupon().
3. TABELA DE ESTADOS:
   - Entrada: user com age = 19
   - isEligible: BASE = true | LEFT = false | RIGHT = true | MERGE = false
   - coupons: BASE = vazia | LEFT = vazia | RIGHT = 1 cupom | MERGE = vazia
4. CRITÉRIO DE CONFLITO: X = isEligible(user) e X = coupons.
   - (A) não se aplica: nenhum valor muda no MERGE sem ter mudado em LEFT ou RIGHT.
   - (B) o MERGE preserva o valor de isEligible de LEFT. O valor de coupons em RIGHT (1 cupom) difere de BASE e não é preservado no MERGE (vazia).
   - (C) o valor de isEligible em LEFT difere de BASE, e o código adicionado por RIGHT é controlado por esse valor, então se comporta no MERGE de forma diferente de RIGHT.""",
        "resultado": "SIM - Condição C: isEligible(user)",
    },
    {
        "left_summary": "Left adds a call to updateStock() in processOrder()",
        "right_summary": "Right adds a call to sendEmail() in processOrder()",
        "target": "processOrder(Order order)",
        "base": """class OrderService {
    private int stock = 10;
    private final List<Order> orders = new ArrayList<>();
    private final List<String> outbox = new ArrayList<>();

    void processOrder(Order order) {
        validate(order);
        save(order);
    }

    void save(Order order) {
        orders.add(order);
    }

    void validate(Order order) {
        if (order.getQuantity() <= 0) {
            throw new IllegalArgumentException("invalid quantity");
        }
    }

    void updateStock(Order order) {
        stock -= order.getQuantity();
    }

    void sendEmail(Order order) {
        outbox.add("Order confirmed: " + order.getId());
    }
}
""",
        "left": [("        validate(order);\n", "        validate(order);\n        updateStock(order);\n")],
        "right": [("        save(order);\n", "        save(order);\n        sendEmail(order);\n")],
        "analise": """1. INTENÇÃO: LEFT atualiza o estoque. RIGHT envia um e-mail de confirmação.
2. ESTADO: O campo stock, escrito por updateStock() (LEFT), e a lista outbox, escrita por sendEmail() (RIGHT).
3. TABELA DE ESTADOS:
   - Entrada: pedido de 1 unidade, stock = 10
   - stock: BASE = 10 | LEFT = 9 | RIGHT = 10 | MERGE = 9
   - outbox: BASE = vazia | LEFT = vazia | RIGHT = 1 e-mail | MERGE = 1 e-mail
4. CRITÉRIO DE CONFLITO: X = stock e X = outbox.
   - (A) não se aplica: nenhum valor muda no MERGE sem ter mudado em LEFT ou RIGHT.
   - (B) o valor de stock em LEFT e o de outbox em RIGHT diferem de BASE, e o MERGE é igual a cada um deles.
   - (C) sendEmail() não lê stock, e updateStock() não lê outbox.""",
        "resultado": "NAO",
    },
    {
        "left_summary": "Left doubles price at the start of computePrice() and halves total after computing it",
        "right_summary": "Right adds 10 to price before computing total and subtracts 10 from total at the end of computePrice()",
        "target": "computePrice(int price)",
        "base": """class PriceCalculator {
    int computePrice(int price) {
        int fee = 0;
        int total = price + fee;
        total = Math.max(total, 0);
        return total;
    }
}
""",
        "left": [("    int computePrice(int price) {\n", "    int computePrice(int price) {\n        price = price * 2;\n"),
                 ("        int total = price + fee;\n", "        int total = price + fee;\n        total = total / 2;\n")],
        "right": [("        int fee = 0;\n", "        int fee = 0;\n        price = price + 10;\n"),
                  ("        total = Math.max(total, 0);\n", "        total = Math.max(total, 0);\n        total = total - 10;\n")],
        "analise": """1. INTENÇÃO: LEFT dobra price e divide total por 2, e RIGHT soma 10 a price e subtrai 10 de total; cada lado compensa o próprio ajuste.
2. ESTADO: A variável local total, retornada por computePrice().
3. TABELA DE ESTADOS:
   - Entrada: price = 100
   - BASE: total = 100
   - LEFT: price = 200, total = 200 / 2 = 100
   - RIGHT: price = 110, total = 110 - 10 = 100
   - MERGE: price = 200 + 10 = 210, total = 210 / 2 = 105, total = 105 - 10 = 95
4. CRITÉRIO DE CONFLITO: X = total.
   - (A) o valor de X é 100 em BASE, LEFT e RIGHT, mas 95 em MERGE.
   - (B) não se aplica: o valor de X em LEFT e RIGHT é igual ao de BASE.
   - (C) não é necessária, pois A já se aplica.""",
        "resultado": "SIM - Condição A: total",
    },
    {
        "left_summary": "Left changes the text of the exception message thrown in validate()",
        "right_summary": "Right adds a null check on the name parameter at the start of validate(), before the existing checks",
        "target": "validate(String name)",
        "base": """class Validator {
    void validate(String name) {
        if (name.length() < 2) {
            throw new IllegalArgumentException("invalid");
        }
    }
}
""",
        "left": [('"invalid"', '"name too short"')],
        "right": [("    void validate(String name) {\n",
                   "    void validate(String name) {\n        if (name == null) {\n"
                   "            throw new IllegalArgumentException(\"name is null\");\n        }\n")],
        "analise": """1. INTENÇÃO: LEFT muda a mensagem de erro do check existente. RIGHT rejeita name nulo antes do check existente.
2. ESTADO: A exceção lançada por validate() (tipo e mensagem).
3. TABELA DE ESTADOS:
   - Entrada A: name = "x" (falha no check existente)
     - BASE: IllegalArgumentException("invalid") | LEFT: IllegalArgumentException("name too short") | RIGHT: IllegalArgumentException("invalid") | MERGE: IllegalArgumentException("name too short")
   - Entrada B: name = null
     - BASE: NullPointerException em name.length() | LEFT: igual a BASE | RIGHT: IllegalArgumentException("name is null") | MERGE: IllegalArgumentException("name is null")
4. CRITÉRIO DE CONFLITO: X = exceção lançada.
   - (A) não se aplica: nenhum valor muda no MERGE sem ter mudado em LEFT ou RIGHT.
   - (B) o MERGE é igual a LEFT na entrada A e igual a RIGHT na entrada B.
   - (C) o novo check de RIGHT não lê nem é controlado pela mensagem alterada por LEFT.""",
        "resultado": "NAO",
    },
]


def _aplica(codigo, trocas):
    for antigo, novo in trocas:
        assert codigo.count(antigo) == 1, antigo
        codigo = codigo.replace(antigo, novo)
    return codigo


def _versoes(exemplo):
    """Código completo de BASE e LEFT/RIGHT/MERGE como diffs, no mesmo formato dos casos do dataset."""
    base = exemplo["base"]
    left = _aplica(base, exemplo["left"])
    right = _aplica(base, exemplo["right"])
    # MERGE = mudanças de LEFT + mudanças de RIGHT (quando são iguais, aplicadas uma vez)
    merge = left if exemplo["left"] == exemplo["right"] else _aplica(left, exemplo["right"])
    return {"base": base,
            "left": unified_diff(base, left, "base.java", "left.java"),
            "right": unified_diff(base, right, "base.java", "right.java"),
            "merge": unified_diff(base, merge, "base.java", "merge.java")}


def exemplos(com_target, com_resumos):
    partes = []
    for numero, exemplo in enumerate(EXEMPLOS, 1):
        texto = entrada(com_target, com_resumos).format(**{**exemplo, **_versoes(exemplo)})
        # o prompt final passa por .format(**linha), então as chaves do código do exemplo são escapadas
        texto = texto.replace("{", "{{").replace("}", "}}")
        partes.append(f"""<exemplo numero="{numero}">
<entrada>
{texto}
</entrada>
<saida_esperada>
<analise>
{exemplo["analise"]}
</analise>
<resultado>
{exemplo["resultado"]}
</resultado>
</saida_esperada>
</exemplo>""")
    return "<exemplos>\n" + "\n\n".join(partes) + "\n</exemplos>"


def montar(few_shot, com_target, com_resumos):
    partes = [CABECALHO, definicoes(com_target), FORMATO_ENTRADA, instrucoes(com_target, com_resumos)]
    if few_shot:
        partes += [exemplos(com_target, com_resumos), "AGORA ANALISE O SEGUINTE CASO:"]
    partes += [f"<caso>\n{entrada(com_target, com_resumos)}\n</caso>", FECHO]
    return "\n\n".join(partes)


# 2 x 4 variantes: zero-shot ou few-shot, cada uma sem contexto, só com resumos, só com target ou com ambos
VARIANTES = {"none": (False, False), "summaries": (False, True), "target": (True, False), "both": (True, True)}

PROMPTS = {f"{tipo}_shot_guided_{nome}": montar(tipo == "few", com_target, com_resumos)
           for tipo in ("zero", "few")
           for nome, (com_target, com_resumos) in VARIANTES.items()}
