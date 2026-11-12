"""Relatórios que comparam as execuções de um mesmo modelo e os modelos entre si.

As execuções de um modelo são uma lista de Resultados (src.metrics) com os mesmos casos e prompts.
"""
from collections import Counter
from statistics import mean

from src.metrics import (CAB_METRICAS, MOTIVOS_SEM_RESPOSTA, dec, div, linha_metricas, metricas,
                         metricas_das_respostas, pct, prompts_por_fator, sem_resposta, tabela, tabela_metricas)

COLUNAS_RESUMO = [("acuracia", pct), ("precisao", pct), ("recall", pct), ("f1", dec), ("especificidade", pct)]
CAB_RESUMO = ["Acurácia", "Precisão", "Recall", "F1", "Especificidade", "Sem resposta (soma)"]
CAB_SEM_RESPOSTA = ["Ignoradas (prompt grande demais)", "Erros", "Recusas", "Fora do formato"]
MAX_CASOS_INSTAVEIS = 10

NOTA_METRICAS = ("- As métricas aparecem como média entre as execuções, com o intervalo (mín–máx) entre parênteses, "
                 "e consideram só as chamadas com resposta YES/NO.\n")


def media(valores):
    valores = [v for v in valores if v is not None]
    return mean(valores) if valores else None


def resumo(valores, formato):
    """Média e intervalo dos valores definidos, ex.: 62,0% (55,0%–70,0%)."""
    valores = [v for v in valores if v is not None]
    if not valores:
        return "—"
    if min(valores) == max(valores):
        return formato(valores[0])
    return f"{formato(mean(valores))} ({formato(min(valores))}–{formato(max(valores))})"


def metricas_por_execucao(execucoes, prompts=None):
    return [metricas(r.chamadas_dos_prompts(prompts or r.prompts)) for r in execucoes]


def linha_resumo(metricas_das_execucoes):
    medias = [resumo([m[chave] for m in metricas_das_execucoes], formato) for chave, formato in COLUNAS_RESUMO]
    return medias + [sum(m["sem"] for m in metricas_das_execucoes)]


def tabela_resumo(titulo_grupo, execucoes, grupos):
    """Uma linha por grupo de prompts, com as métricas resumidas entre as execuções."""
    linhas = [[nome, *linha_resumo(metricas_por_execucao(execucoes, prompts))] for nome, prompts in grupos.items()]
    return tabela([titulo_grupo, *CAB_RESUMO], linhas)


def respostas_das_execucoes(execucoes, caso, prompt):
    return [r.resposta.get((caso, prompt)) for r in execucoes]


def estabilidade(execucoes, prompts):
    """(chamadas respondidas em todas as execuções, quantas delas tiveram a mesma resposta em todas)."""
    respondidas = iguais = 0
    for caso in execucoes[0].casos:
        for prompt in prompts:
            respostas = respostas_das_execucoes(execucoes, caso, prompt)
            if None in respostas:
                continue
            respondidas += 1
            iguais += len(set(respostas)) == 1
    return respondidas, iguais


def prompts_divergentes(execucoes, caso):
    """Prompts em que as execuções responderam YES e NO para o caso."""
    return [p for p in execucoes[0].prompts
            if len(set(filter(None, respostas_das_execucoes(execucoes, caso, p)))) > 1]


def resposta_da_maioria(execucoes, caso, prompt):
    """YES/NO dado pela maioria das execuções, ou None em caso de empate ou sem respostas."""
    votos = Counter(respostas_das_execucoes(execucoes, caso, prompt))
    if votos["YES"] > votos["NO"]:
        return "YES"
    if votos["NO"] > votos["YES"]:
        return "NO"
    return None


def metricas_da_maioria(execucoes, prompts):
    esperado = execucoes[0].esperado
    pares = [(esperado[caso], resposta_da_maioria(execucoes, caso, p)) for caso in execucoes[0].casos for p in prompts]
    respondidos = [(e, resposta) for e, resposta in pares if resposta]
    m = metricas_das_respostas(respondidos)
    m["sem"] = len(pares) - len(respondidos)
    return m


def taxa_de_acerto(execucoes, caso):
    """Fração das chamadas do caso, somando prompts e execuções, com a resposta esperada (sem resposta é erro)."""
    esperado = execucoes[0].esperado[caso]
    respostas = [r.resposta.get((caso, p)) for r in execucoes for p in r.prompts]
    return div(sum(resposta == esperado for resposta in respostas), len(respostas))


def descricao_casos(r):
    n_yes = r.n_yes(r.casos)
    return (f"- **Casos:** {len(r.casos)} ({n_yes} YES, {len(r.casos) - n_yes} NO); **prompts:** {len(r.prompts)}; "
            f"**chamadas por execução:** {len(r.chamadas)}")


def cabecalho_modelo(nome, execucoes):
    arquivos = ", ".join(f"`{r.arquivo}`" for r in execucoes)
    return "\n".join([
        f"# Relatório do modelo — `{nome}`\n",
        f"- **Execuções:** {len(execucoes)} ({arquivos})",
        descricao_casos(execucoes[0]),
        NOTA_METRICAS,
    ])


def secao_execucoes(execucoes):
    return "\n".join([
        "## 1. Resultado por execução\n",
        tabela_metricas("Execução", {r.arquivo: r.chamadas for r in execucoes}),
        "",
        tabela(["", *CAB_RESUMO], [["média", *linha_resumo(metricas_por_execucao(execucoes))]]),
        "",
    ])


def secao_prompts_modelo(execucoes):
    prompts = execucoes[0].prompts
    return "\n".join([
        "## 2. Resultado por prompt\n",
        tabela_resumo("Prompt", execucoes, {p: [p] for p in prompts}),
        "",
    ])


def secao_fatores_modelo(execucoes):
    fatores = prompts_por_fator(execucoes[0].prompts)
    if fatores is None:
        return None
    por_tipo, por_contexto = fatores
    return "\n".join([
        "## 3. Efeito de cada fator\n",
        "### Zero-shot vs. few-shot (somando as variantes de contexto)\n",
        tabela_resumo("Tipo", execucoes, por_tipo),
        "\n### Contexto fornecido (somando zero-shot e few-shot)\n",
        tabela_resumo("Contexto", execucoes, por_contexto),
        "",
    ])


def secao_estabilidade(execucoes):
    r = execucoes[0]
    grupos = {p: [p] for p in r.prompts} | {"todos": r.prompts}
    linhas = []
    for nome, prompts in grupos.items():
        respondidas, iguais = estabilidade(execucoes, prompts)
        linhas.append([nome, respondidas, iguais, pct(div(iguais, respondidas))])

    divergencias = {caso: prompts_divergentes(execucoes, caso) for caso in r.casos}
    instaveis = sorted((caso for caso in r.casos if divergencias[caso]), key=lambda caso: -len(divergencias[caso]))
    linhas_instaveis = [[caso, r.esperado[caso], f"{len(divergencias[caso])}/{len(r.prompts)}"]
                        for caso in instaveis[:MAX_CASOS_INSTAVEIS]]

    saida = [
        "## 4. Estabilidade entre as execuções\n",
        "Chamadas (caso e prompt) respondidas em todas as execuções e quantas delas tiveram a mesma resposta em todas:\n",
        tabela(["Prompt", "Respondidas em todas", "Mesma resposta", "Estabilidade"], linhas),
        "",
    ]
    if instaveis:
        saida += [
            f"Casos com respostas YES e NO entre as execuções: {len(instaveis)}/{len(r.casos)}. "
            f"Os {len(linhas_instaveis)} com mais prompts divergentes:\n",
            tabela(["Caso", "Esperado", "Prompts divergentes"], linhas_instaveis),
            "",
        ]
    else:
        saida.append("Nenhum caso teve respostas diferentes entre as execuções.\n")
    return "\n".join(saida)


def secao_maioria(execucoes):
    prompts = execucoes[0].prompts
    grupos = {p: [p] for p in prompts} | {"todos": prompts}
    linhas = [[nome, *linha_metricas(metricas_da_maioria(execucoes, ps))] for nome, ps in grupos.items()]
    return "\n".join([
        "## 5. Resposta da maioria das execuções\n",
        "Para cada caso e prompt, a resposta dada pela maioria das execuções. Empates (ex.: uma execução sem resposta "
        "e as outras divergindo) contam como \"Sem resposta\".\n",
        tabela(["Prompt", *CAB_METRICAS], linhas),
        "",
    ])


def secao_sem_resposta_execucoes(execucoes):
    linhas = []
    for r in execucoes:
        motivos = Counter(map(sem_resposta, r.chamadas))
        linhas.append([r.arquivo, *[motivos[m] for m in MOTIVOS_SEM_RESPOSTA]])
    return "\n".join([
        "## 6. Chamadas sem resposta YES/NO por execução\n",
        tabela(["Execução", *CAB_SEM_RESPOSTA], linhas),
    ])


def relatorio_modelo(nome, execucoes):
    secoes = [cabecalho_modelo(nome, execucoes), secao_execucoes(execucoes), secao_prompts_modelo(execucoes),
              secao_fatores_modelo(execucoes), secao_estabilidade(execucoes), secao_maioria(execucoes),
              secao_sem_resposta_execucoes(execucoes)]
    return "\n".join(s for s in secoes if s is not None) + "\n"


def tabela_por_grupo(modelos, titulo_grupo, grupos, chave, formato):
    """Uma linha por grupo de prompts e uma coluna por modelo, com a média de uma métrica entre as execuções."""
    linhas = []
    for nome, prompts in grupos.items():
        valores = [media(m[chave] for m in metricas_por_execucao(execucoes, prompts)) for execucoes in modelos.values()]
        linhas.append([nome, *map(formato, valores)])
    return tabela([titulo_grupo, *modelos], linhas)


def cabecalho_comparativo(modelos, titulo):
    lista = ", ".join(f"`{nome}` ({len(execucoes)} execuções)" for nome, execucoes in modelos.items())
    return "\n".join([
        f"# Comparação entre modelos — `{titulo}`\n",
        f"- **Modelos:** {lista}",
        descricao_casos(next(iter(modelos.values()))[0]),
        NOTA_METRICAS,
    ])


def secao_geral_modelos(modelos):
    linhas, linhas_maioria = [], []
    for nome, execucoes in modelos.items():
        prompts = execucoes[0].prompts
        respondidas, iguais = estabilidade(execucoes, prompts)
        linhas.append([nome, *linha_resumo(metricas_por_execucao(execucoes)), pct(div(iguais, respondidas))])
        linhas_maioria.append([nome, *linha_metricas(metricas_da_maioria(execucoes, prompts))])
    return "\n".join([
        "## 1. Resultado geral por modelo\n",
        tabela(["Modelo", *CAB_RESUMO, "Estabilidade"], linhas),
        "\nEstabilidade: fração das chamadas respondidas em todas as execuções que tiveram a mesma resposta em todas.\n",
        "Usando a resposta da maioria das execuções para cada caso e prompt:\n",
        tabela(["Modelo", *CAB_METRICAS], linhas_maioria),
        "",
    ])


def secao_prompts_modelos(modelos):
    prompts = next(iter(modelos.values()))[0].prompts
    grupos = {p: [p] for p in prompts}
    return "\n".join([
        "## 2. Resultado por prompt (média entre as execuções)\n",
        "### F1\n",
        tabela_por_grupo(modelos, "Prompt", grupos, "f1", dec),
        "\n### Recall\n",
        tabela_por_grupo(modelos, "Prompt", grupos, "recall", pct),
        "\n### Precisão\n",
        tabela_por_grupo(modelos, "Prompt", grupos, "precisao", pct),
        "",
    ])


def secao_fatores_modelos(modelos):
    fatores = prompts_por_fator(next(iter(modelos.values()))[0].prompts)
    if fatores is None:
        return None
    por_tipo, por_contexto = fatores
    return "\n".join([
        "## 3. Efeito de cada fator (F1 médio entre as execuções)\n",
        "### Zero-shot vs. few-shot (somando as variantes de contexto)\n",
        tabela_por_grupo(modelos, "Tipo", por_tipo, "f1", dec),
        "\n### Contexto fornecido (somando zero-shot e few-shot)\n",
        tabela_por_grupo(modelos, "Contexto", por_contexto, "f1", dec),
        "",
    ])


def secao_casos_dificeis(modelos):
    r = next(iter(modelos.values()))[0]
    taxas = {caso: [taxa_de_acerto(execucoes, caso) for execucoes in modelos.values()] for caso in r.casos}
    dificeis = sorted((caso for caso in r.casos if all(t < 0.5 for t in taxas[caso])), key=lambda caso: mean(taxas[caso]))
    yes_reais = [caso for caso in r.casos if r.esperado[caso] == "YES"]
    nunca_detectados = [caso for caso in yes_reais if all(t == 0 for t in taxas[caso])]

    saida = [
        "## 4. Casos difíceis\n",
        "Taxa de acerto de cada caso: fração das chamadas, somando prompts e execuções, com a resposta esperada "
        "(chamadas sem resposta contam como erro).\n",
        f"Casos em que todos os modelos acertaram menos da metade das chamadas: {len(dificeis)}/{len(r.casos)}\n",
    ]
    if dificeis:
        linhas = [[caso, r.esperado[caso], *map(pct, taxas[caso])] for caso in dificeis]
        saida += [tabela(["Caso", "Esperado", *modelos], linhas), ""]
    saida.append(f"Conflitos (YES) que nenhuma chamada de nenhum modelo detectou: {len(nunca_detectados)}/{len(yes_reais)}")
    saida += [f"- `{caso}`" for caso in nunca_detectados]
    return "\n".join(saida)


def relatorio_comparativo(modelos, titulo):
    """modelos: nome do modelo -> lista de execuções."""
    secoes = [cabecalho_comparativo(modelos, titulo), secao_geral_modelos(modelos), secao_prompts_modelos(modelos),
              secao_fatores_modelos(modelos), secao_casos_dificeis(modelos)]
    return "\n".join(s for s in secoes if s is not None) + "\n"
