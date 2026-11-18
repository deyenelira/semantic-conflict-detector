"""Relatório para análise manual dos casos em que os modelos divergem em um prompt.

Um modelo é estável em um caso quando todas as suas execuções deram a mesma resposta YES/NO. Entram no relatório
os casos em que todos os modelos são estáveis, ao menos um responde YES e ao menos um responde NO. Para cada caso,
o relatório traz os resumos das mudanças e a justificativa do dataset, além da resposta e da análise de cada execução.
"""
import csv
import html
import os
import re

from src.datasets import DATA, DATASETS
from src.metrics import tabela

PROMPT = "few_shot_guided_both"

# trechos de código (```...``` ou `...`), onde < e > aparecem literalmente
CODIGO_RE = re.compile(r"(```.*?```|`[^`\n]*`)", re.DOTALL)


def carregar_dataset(casos):
    """Linhas do dataset que contém todos os casos dos resultados, e a pasta desse dataset."""
    for nome in DATASETS:
        with open(DATA / nome / "dataset.csv", newline="", encoding="utf-8") as f:
            linhas = {linha["id"]: linha for linha in csv.DictReader(f)}
        if set(casos) <= set(linhas):
            return linhas, DATA / nome
    raise SystemExit("nenhum dataset em data/ contém todos os casos dos resultados")


def escapar_fora_do_codigo(texto):
    """Escapa < e > fora dos trechos de código, para que tipos como Map<String, Long> não sumam como tags HTML."""
    partes = CODIGO_RE.split(texto)
    return "".join(parte if i % 2 else parte.replace("<", "&lt;").replace(">", "&gt;") for i, parte in enumerate(partes))


def chamada(execucao, caso, prompt):
    return next(c for c in execucao.por_prompt[prompt] if c["id"] == caso)


def resposta_estavel(execucoes, caso, prompt):
    """YES/NO se todas as execuções deram essa resposta, senão None."""
    respostas = {r.resposta.get((caso, prompt)) for r in execucoes}
    return respostas.pop() if len(respostas) == 1 and None not in respostas else None


def casos_divergentes(modelos, prompt, esperado):
    """Casos com a resposta esperada em que todos os modelos são estáveis e ao menos um responde YES e outro NO."""
    r = next(iter(modelos.values()))[0]
    selecionados = []
    for caso in r.casos:
        if r.esperado[caso] != esperado:
            continue
        respostas = {nome: resposta_estavel(execucoes, caso, prompt) for nome, execucoes in modelos.items()}
        if None not in respostas.values() and {"YES", "NO"} <= set(respostas.values()):
            selecionados.append((caso, respostas))
    return selecionados


def secao_caso(numero, caso, respostas, modelos, prompt, dataset, pasta_dataset, destino):
    linha = dataset[caso]
    pasta_caso = pasta_dataset / caso.split("#")[0]
    esperado = linha["label"].upper()
    certos = [nome for nome, resposta in respostas.items() if resposta == esperado]
    errados = [nome for nome, resposta in respostas.items() if resposta != esperado]

    saida = [
        f"### {numero}. `{caso}`\n",
        f"- **Target:** `{linha['target']}`",
        f"- **Esperado:** {esperado}; **acertam:** {', '.join(certos)}; **erram:** {', '.join(errados)}",
        f"- **Código:** [{pasta_caso.name}]({os.path.relpath(pasta_caso, destino)})\n",
        f"**LEFT:** {linha['left_summary'] or '—'}\n",
        f"**RIGHT:** {linha['right_summary'] or '—'}\n",
        f"**Justificativa do dataset:** {linha.get('justification') or '—'}\n",
    ]
    # quem acerta primeiro, para ler as análises certas e erradas em sequência
    for nome in certos + errados:
        marca = "✅" if nome in certos else "❌"
        saida.append(f"#### {nome}: {respostas[nome]} {marca}\n")
        for i, execucao in enumerate(modelos[nome]):
            c = chamada(execucao, caso, prompt)
            detalhe = f" — Condição {c['violated condition']}: {c['state variable']}" if c["violated condition"] else ""
            saida.append(f"<details><summary>Execução {i + 1} (<code>{html.escape(execucao.arquivo)}</code>): "
                         f"{html.escape(c['model answer'] + detalhe)}</summary>\n")
            saida.append(escapar_fora_do_codigo((c.get("analysis") or "(análise não registrada)").strip()))
            saida.append("\n</details>\n")
    return "\n".join(saida)


def secao_grupo(titulo, descricao, selecionados, modelos, prompt, dataset, pasta_dataset, destino, inicio):
    saida = [f"## {titulo}\n", f"{descricao} {len(selecionados)} casos.\n"]
    if selecionados:
        linhas = [[f"`{caso}`", *respostas.values()] for caso, respostas in selecionados]
        saida += [tabela(["Caso", *modelos], linhas), ""]
    for numero, (caso, respostas) in enumerate(selecionados, inicio):
        saida.append(secao_caso(numero, caso, respostas, modelos, prompt, dataset, pasta_dataset, destino))
    return "\n".join(saida)


def relatorio_casos_divergentes(modelos, titulo, destino, prompt=PROMPT):
    """modelos: nome do modelo -> lista de execuções; destino: diretório onde o relatório será salvo (para os links)."""
    r = next(iter(modelos.values()))[0]
    if prompt not in r.prompts:
        return f"# Casos divergentes — `{titulo}`\n\nO prompt `{prompt}` não está nos resultados.\n"
    dataset, pasta_dataset = carregar_dataset(r.casos)
    execucoes = ", ".join(f"`{nome}` ({len(rs)})" for nome, rs in modelos.items())
    conflitos = casos_divergentes(modelos, prompt, "YES")
    sem_conflito = casos_divergentes(modelos, prompt, "NO")

    saida = [
        f"# Casos divergentes — `{titulo}`\n",
        f"- **Prompt:** `{prompt}`",
        f"- **Modelos (execuções):** {execucoes}",
        "- Entram os casos em que cada modelo deu a mesma resposta em todas as suas execuções, e ao menos um modelo "
        "respondeu YES e outro NO. Um modelo com uma única execução é sempre considerado estável.",
        "- Em cada caso, os modelos que acertam vêm primeiro. A análise de cada execução começa recolhida; clique na execução para abri-la.\n",
        secao_grupo("1. Conflitos detectados só por parte dos modelos",
                    "Casos com conflito (YES) em que algum modelo detecta o conflito e outro não:",
                    conflitos, modelos, prompt, dataset, pasta_dataset, destino, 1),
        secao_grupo("2. Falsos positivos de parte dos modelos",
                    "Casos sem conflito (NO) em que algum modelo responde YES e outro acerta:",
                    sem_conflito, modelos, prompt, dataset, pasta_dataset, destino, len(conflitos) + 1),
    ]
    return "\n".join(saida) + "\n"
