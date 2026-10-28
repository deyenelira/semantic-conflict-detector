PROMPTS = {
    "prompt_intencao_estado": """Você é um desenvolvedor sênior investigando se um merge introduziu um conflito semântico.

DEFINIÇÃO CONFLITO SEMÂNTICO
Conflito semântico é quando dois commits se juntam sem conflito textual, mas o programa
resultante se comporta de forma diferente do que algum dos desenvolvedores queria.

DEFINIÇÃO ELEMENTO DE ESTADO (VARIÁVEL DE ESTADO)
É qualquer posição de memória ou canal de saída que a execução do código pode escrever e
depois ler. Inclui: variável local, parâmetro, campo estático ou de instância, posição de
array, elemento de coleção, arquivo, fluxo, expressão de um return, exceção lançada e
estado temporário.

Siga estas etapas:
1. INTENÇÃO: resuma em uma frase o que LEFT mudou em relação a BASE e o que RIGHT mudou,
   ou seja, o comportamento que cada desenvolvedor quis introduzir.
2. ESTADO: liste os elementos de estado (conforme a definição acima) lidos ou escritos pelos
   trechos alterados. Considere também métodos diferentes que acessam o mesmo elemento e a
   ordem em que são executados.
3. TABELA: para cada elemento de estado X, descreva o valor/comportamento em BASE | LEFT | RIGHT | MERGE.
4. CRITÉRIO: há conflito se existir um X tal que
   (a) X é igual em BASE, LEFT e RIGHT, mas diferente em MERGE; ou
   (b) X em LEFT (ou RIGHT) difere de BASE, e o MERGE não preserva o valor desse pai.
5. Ignore refatorações sem efeito no comportamento e mudanças em elementos de estado independentes.

Responda SIM ou NAO na primeira linha, depois mostre as etapas.

BASE contém o código completo. LEFT, RIGHT e MERGE são diffs unificados em relação a BASE
(linhas iniciadas com - foram removidas e linhas iniciadas com + foram adicionadas).

BASE:
{base}

LEFT:
{left}

RIGHT:
{right}

MERGE:
{merge}""",

    "prompt_one_shot_cleantext": """Você é um desenvolvedor sênior investigando se um merge introduziu um conflito semântico.

DEFINIÇÃO CONFLITO SEMÂNTICO
Conflito semântico é quando dois commits se juntam sem conflito textual, mas o programa
resultante se comporta de forma diferente do que algum dos desenvolvedores queria.

DEFINIÇÃO ELEMENTO DE ESTADO (VARIÁVEL DE ESTADO)
É qualquer posição de memória ou canal de saída que a execução do código pode escrever e
depois ler. Inclui: variável local, parâmetro, campo estático ou de instância, posição de
array, elemento de coleção, arquivo, fluxo, expressão de um return, exceção lançada e
estado temporário.


EXEMPLOS DE ELEMENTOS DE ESTADO
Considere uma classe Text com os campos "String text", "int fixes" e "int comments".
- Campo de instância: this.fixes (contador de correções) e this.comments (contador de comentários).
  São elementos diferentes: um método que só escreve em comments não interfere em fixes.
- Campo de instância reescrito por vários métodos: this.text, que normalizeWhiteSpace(),
  removeComments() e removeDuplicateWords() leem e reescrevem. Se LEFT e RIGHT adicionam
  chamadas que reescrevem this.text, ambos escrevem no mesmo elemento.
- Variável local: em "Settings settings = builder.build();", a variável settings.
  Se LEFT e RIGHT atribuem a settings, há escrita no mesmo elemento.
- Elemento de coleção / estado de uma lista: a lista retornada por getAllEventTypes().
  Se LEFT adiciona 5 itens e RIGHT adiciona outros 3 a ela, o tamanho final depende de ambos.
- Valor retornado: a expressão em "return x + y;". Se LEFT e RIGHT alteram essa expressão,
  alteram o mesmo elemento.
- Exceção lançada: se LEFT faz o método lançar uma exceção em certo caso e RIGHT
  muda esse caso, ambos afetam o mesmo elemento.
- Posição de array: a[0] e a[1] não interferem; já a = new int[3] interfere com a[0] = 1.
- Atribuição de BASE no meio: se BASE já escreve em fixes entre a escrita de LEFT e a de
  RIGHT, a de RIGHT sobrescreve a de BASE, e não há interferência.

Siga estas etapas:
1. INTENÇÃO: resuma em uma frase o que LEFT mudou em relação a BASE e o que RIGHT mudou,
   ou seja, o comportamento que cada desenvolvedor quis introduzir.
2. ESTADO: liste os elementos de estado (conforme a definição e os exemplos acima) lidos ou
   escritos pelos trechos alterados. Considere também métodos diferentes que acessam o mesmo
   elemento e a ordem em que são executados.
3. TABELA: para cada elemento X, descreva o valor/comportamento em BASE | LEFT | RIGHT | MERGE.
4. CRITÉRIO: há conflito se existir um X tal que
   (a) X é igual em BASE, LEFT e RIGHT, mas diferente em MERGE; ou
   (b) X em LEFT (ou RIGHT) difere de BASE, e o MERGE não preserva o valor desse pai.
5. Ignore refatorações sem efeito no comportamento e mudanças em elementos de estado independentes.

Responda SIM ou NAO na primeira linha, depois mostre as etapas.

BASE contém o código completo. LEFT, RIGHT e MERGE são diffs unificados em relação a BASE
(linhas iniciadas com - foram removidas e linhas iniciadas com + foram adicionadas).

EXEMPLO
BASE:
cleanText() {{
    removeComments();
}}

LEFT:
--- base.java
+++ left.java
@@ -1,3 +1,4 @@
 cleanText() {{
+    normalizeWhiteSpace();
     removeComments();
 }}

RIGHT:
--- base.java
+++ right.java
@@ -1,3 +1,4 @@
 cleanText() {{
     removeComments();
+    removeDuplicateWords();
 }}

MERGE:
--- base.java
+++ merge.java
@@ -1,3 +1,5 @@
 cleanText() {{
+    normalizeWhiteSpace();
     removeComments();
+    removeDuplicateWords();
 }}

Análise:
- Intenção LEFT: colapsar espaços múltiplos. Intenção RIGHT: remover palavras duplicadas consecutivas.
- Estado: o campo text da instância, que cada método chamado em cleanText lê e reescreve
  (a ordem das operações importa).
- Entrada "HELLO  HELLO  WORLD" (dois espaços entre as palavras):
  LEFT -> "HELLO HELLO WORLD"; RIGHT -> "HELLO    WORLD"; MERGE -> "HELLO  WORLD".
- O resultado do MERGE mantém espaços duplicados que LEFT queria colapsar em um só.
Resposta: SIM

AGORA ANALISE:

BASE:
{base}

LEFT:
{left}

RIGHT:
{right}

MERGE:
{merge}""",

"prompt_teste_mental": """Você é um desenvolvedor sênior investigando se um merge introduziu um conflito semântico.

DEFINIÇÃO CONFLITO SEMÂNTICO
Conflito semântico é quando dois commits se juntam sem conflito textual, mas o programa
resultante se comporta de forma diferente do que algum dos desenvolvedores queria.

Investigue como um desenvolvedor faria, nesta ordem:

PASSO 1 - ENTENDER O CÓDIGO
Explique em poucas frases o que o código faz em BASE. Depois diga o que LEFT mudou e o que
RIGHT mudou em relação a BASE, e qual comportamento cada desenvolvedor provavelmente queria
obter. Por fim, descreva como o MERGE combinou as duas mudanças (inclusive a ordem em que
as operações passaram a executar).

PASSO 2 - IDENTIFICAR AS VARIÁVEIS DE ESTADO
Variável de estado (ou elemento de estado) é qualquer posição de memória ou canal de saída
que a execução do código pode escrever e depois ler. Inclui: variável local, parâmetro,
campo estático ou de instância, posição de array, elemento de coleção, arquivo, fluxo,
expressão de um return, exceção lançada e estado temporário.

PASSO 3 - SIMULAR UM CASO QUE SATISFAÇA OS CRITÉRIOS
Para cada variável X do passo 2, tente imaginar uma entrada ou um estado inicial concreto
em que X se comporte de acordo com um dos critérios abaixo:
  (a) X tem o mesmo valor/comportamento em BASE, LEFT e RIGHT, mas diferente em MERGE; ou
  (b) X em LEFT (ou RIGHT) difere de BASE, e o MERGE não preserva o valor desse pai.
Execute mentalmente BASE, LEFT, RIGHT e MERGE com essa entrada, passo a passo, e anote o
valor de X em cada versão (BASE | LEFT | RIGHT | MERGE).

PASSO 4 - CONCLUIR
Se você encontrou uma entrada e uma variável que satisfazem (a) ou (b), há conflito: diga
qual desenvolvedor teve a intenção violada. Se, depois de tentar, nenhuma variável
satisfaz os critérios, não há conflito. Refatorações sem efeito no comportamento e
mudanças em variáveis independentes não são conflito.

Na primeira linha responda SIM ou NAO. Depois mostre o raciocínio de cada passo.

BASE contém o código completo. LEFT, RIGHT e MERGE são diffs unificados em relação a BASE
(linhas iniciadas com - foram removidas e linhas iniciadas com + foram adicionadas).

BASE:
{base}

LEFT:
{left}

RIGHT:
{right}

MERGE:
{merge}""",
}
