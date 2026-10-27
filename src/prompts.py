PROMPTS = {
    "prompt_intencao_estado": """Você é um desenvolvedor sênior investigando se um merge introduziu um conflito semântico.

Conflito semântico é quando dois commits se juntam sem conflito textual, mas o programa
resultante se comporta de forma diferente do que algum dos desenvolvedores queria.

Siga estas etapas:
1. INTENÇÃO: resuma em uma frase o que LEFT mudou em relação a BASE e o que RIGHT mudou,
   ou seja, o comportamento que cada desenvolvedor quis introduzir.
2. ESTADO: liste os elementos de estado (campos, variáveis, coleções, valores retornados)
   lidos ou escritos pelos trechos alterados. Considere também métodos diferentes que
   acessam o mesmo elemento e a ordem em que são executados.
3. TABELA: para cada elemento X, descreva o valor/comportamento em BASE | LEFT | RIGHT | MERGE.
4. CRITÉRIO: há conflito se existir um X tal que
   (a) X é igual em BASE, LEFT e RIGHT, mas diferente em MERGE; ou
   (b) X em LEFT (ou RIGHT) difere de BASE, e o MERGE não preserva o valor desse pai.
5. Ignore refatorações sem efeito no comportamento e mudanças em elementos de estado independentes.

Responda SIM ou NAO na primeira linha, depois mostre as etapas.

BASE:
{base}

LEFT:
{left}

RIGHT:
{right}

MERGE:
{merge}""",

    "prompt_one_shot_cleantext": """Você é um desenvolvedor sênior investigando se um merge introduziu um conflito semântico.

Conflito semântico é quando dois commits se juntam sem conflito textual, mas o programa
resultante se comporta de forma diferente do que algum dos desenvolvedores queria.

Siga estas etapas:
1. INTENÇÃO: resuma em uma frase o que LEFT mudou em relação a BASE e o que RIGHT mudou,
   ou seja, o comportamento que cada desenvolvedor quis introduzir.
2. ESTADO: liste os elementos de estado (campos, variáveis, coleções, valores retornados)
   lidos ou escritos pelos trechos alterados. Considere também métodos diferentes que
   acessam o mesmo elemento e a ordem em que são executados.
3. TABELA: para cada elemento X, descreva o valor/comportamento em BASE | LEFT | RIGHT | MERGE.
4. CRITÉRIO: há conflito se existir um X tal que
   (a) X é igual em BASE, LEFT e RIGHT, mas diferente em MERGE; ou
   (b) X em LEFT (ou RIGHT) difere de BASE, e o MERGE não preserva o valor desse pai.
5. Ignore refatorações sem efeito no comportamento e mudanças em elementos de estado independentes.

Responda SIM ou NAO na primeira linha, depois mostre as etapas.

EXEMPLO
BASE:
cleanText() {{ removeComments(); }}

LEFT:
cleanText() {{ normalizeWhiteSpace(); removeComments(); }}

RIGHT:
cleanText() {{ removeComments(); removeDuplicateWords(); }}

MERGE:
cleanText() {{ normalizeWhiteSpace(); removeComments(); removeDuplicateWords(); }}

Análise:
- Intenção LEFT: colapsar espaços múltiplos. Intenção RIGHT: remover palavras duplicadas consecutivas.
- Estado: o texto resultante de cleanText (a ordem das operações importa).
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

Conflito semântico é quando dois commits se juntam sem conflito textual, mas o programa
resultante se comporta de forma diferente do que algum dos desenvolvedores queria.

Investigue como um desenvolvedor faria, nesta ordem:

PASSO 1 - ENTENDER O CÓDIGO
Explique em poucas frases o que o código faz em BASE. Depois diga o que LEFT mudou e o que
RIGHT mudou em relação a BASE, e qual comportamento cada desenvolvedor provavelmente queria
obter. Por fim, descreva como o MERGE combinou as duas mudanças (inclusive a ordem em que
as operações passaram a executar).

PASSO 2 - IDENTIFICAR AS VARIÁVEIS DE ESTADO
Liste as variáveis de estado (campos, variáveis, coleções, valores retornados) lidas ou
escritas pelos trechos alterados em LEFT e em RIGHT, inclusive em métodos diferentes.
Dê prioridade às que são afetadas pelas mudanças dos DOIS desenvolvedores.

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

BASE:
{base}

LEFT:
{left}

RIGHT:
{right}

MERGE:
{merge}""",
}
