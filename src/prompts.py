PROMPTS = {
    "prompt_direto": """Existe conflito semântico nesses commits?

BASE:
{base}

LEFT:
{left}

RIGHT:
{right}

MERGE:
{merge}""",

    "prompt_com_definicao": """Conflito semântico é quando dois commits se juntam sem conflito textual, mas o programa
resultante se comporta de forma diferente do que algum dos desenvolvedores queria.
Existe conflito semântico nesse merge? Responda SIM ou NAO e explique em uma frase.

BASE:
{base}

LEFT:
{left}

RIGHT:
{right}

MERGE:
{merge}""",
}