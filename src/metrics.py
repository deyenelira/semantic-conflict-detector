"""Gera um relatório em Markdown com as métricas de um CSV de resultados, agrupadas por prompt.

Uso: python3 -m src.metrics results/<arquivo>_response.csv > relatorio.md
"""
import argparse
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

# "<tipo>_shot_guided_<contexto>", ex.: few_shot_guided_target
PROMPT_RE = re.compile(r"(zero|few)_shot_guided_(none|summaries|target|both)$")
ARQUIVO_RE = re.compile(r"(?P<dataset>[^_]+)_(?P<provider>[^_]+)_(?P<data>\d{8}-\d{6})_response\.csv$")


def pct(valor):
    return "—" if valor is None else f"{valor * 100:.1f}%".replace(".", ",")


def dec(valor):
    return "—" if valor is None else f"{valor:.2f}".replace(".", ",")


def div(a, b):
    return a / b if b else None


def tabela(cabecalho, linhas):
    saida = ["| " + " | ".join(cabecalho) + " |", "|" + "---|" * len(cabecalho)]
    saida += ["| " + " | ".join(str(c) for c in linha) + " |" for linha in linhas]
    return "\n".join(saida)


def sem_resposta(linha):
    """Motivo de a chamada não ter resposta YES/NO, ou None se ela tem."""
    if linha["model answer"] in ("YES", "NO"):
        return None
    status = linha["status"]
    if status.startswith("skipped"):
        return "ignorada"
    if "refusal" in status:
        return "recusa"
    if status.startswith("error"):
        return "erro"
    return "fora do formato"  # status ok, mas a resposta não segue "SIM - Condição X: ..." / "NAO"


def metricas(linhas):
    """Métricas da classe YES, calculadas só sobre as chamadas com resposta YES/NO."""
    m = Counter()
    for linha in linhas:
        if sem_resposta(linha):
            m["sem"] += 1
            continue
        esperado, resposta = linha["expected answer"] == "YES", linha["model answer"] == "YES"
        m[("T" if esperado == resposta else "F") + ("P" if resposta else "N")] += 1
    tp, tn, fp, fn = m["TP"], m["TN"], m["FP"], m["FN"]
    precisao, recall = div(tp, tp + fp), div(tp, tp + fn)
    f1 = div(2 * precisao * recall, precisao + recall) if precisao is not None and recall is not None else None
    return {"acuracia": div(tp + tn, tp + tn + fp + fn), "precisao": precisao, "recall": recall, "f1": f1,
            "especificidade": div(tn, tn + fp), "TP": tp, "TN": tn, "FP": fp, "FN": fn, "sem": m["sem"],
            "total": len(linhas)}


CAB_METRICAS = ["Acurácia", "Precisão", "Recall", "F1", "Especificidade", "TP", "TN", "FP", "FN", "Sem resposta"]


def linha_metricas(m):
    return [pct(m["acuracia"]), pct(m["precisao"]), pct(m["recall"]), dec(m["f1"]), pct(m["especificidade"]),
            m["TP"], m["TN"], m["FP"], m["FN"], m["sem"]]


def tabela_metricas(titulo_grupo, grupos):
    return tabela([titulo_grupo] + CAB_METRICAS, [[nome] + linha_metricas(metricas(ls)) for nome, ls in grupos.items()])


def relatorio(caminho):
    with open(caminho, newline="", encoding="utf-8-sig") as f:
        linhas = list(csv.DictReader(f))
    prompts = list(dict.fromkeys(l["prompt"] for l in linhas))
    por_prompt = {p: [l for l in linhas if l["prompt"] == p] for p in prompts}
    casos = list(dict.fromkeys(l["id"] for l in linhas))
    esperado = {l["id"]: l["expected answer"] for l in linhas}
    resposta = {(l["id"], l["prompt"]): l["model answer"] for l in linhas if not sem_resposta(l)}
    n_yes = sum(esperado[c] == "YES" for c in casos)

    s = []
    nome = Path(caminho).name
    info = ARQUIVO_RE.search(nome)
    s.append(f"# Relatório por prompt — `{nome}`\n")
    if info:
        s.append(f"- **Dataset:** `{info['dataset']}` — {len(casos)} casos ({n_yes} YES, {len(casos) - n_yes} NO)")
        s.append(f"- **Provedor:** `{info['provider']}`")
    else:
        s.append(f"- **Casos:** {len(casos)} ({n_yes} YES, {len(casos) - n_yes} NO)")
    s.append(f"- **Prompts:** {len(prompts)}; **chamadas:** {len(linhas)}")
    motivos = Counter(m for m in map(sem_resposta, linhas) if m)
    s.append("- **Sem resposta YES/NO:** " + (", ".join(f"{k}: {v}" for k, v in motivos.items()) or "nenhuma"))
    s.append("- As métricas consideram só as chamadas com resposta YES/NO; as demais aparecem em \"Sem resposta\".\n")

    # 1. geral
    s.append("## 1. Resultado geral\n")
    s.append(tabela_metricas("Chamadas", {"todas": linhas}))
    yes_reais = sum(l["expected answer"] == "YES" for l in linhas)
    s.append(f"\nBaseline: sempre responder \"NO\" daria {pct(div(len(linhas) - yes_reais, len(linhas)))} de acurácia "
             f"({len(linhas) - yes_reais}/{len(linhas)}). Proporção real de YES nas chamadas: {pct(div(yes_reais, len(linhas)))}.\n")

    # 2. por prompt
    s.append("## 2. Resultado por prompt\n")
    s.append(tabela_metricas("Prompt", por_prompt))
    s.append("")
    distrib = []
    for p, ls in por_prompt.items():
        c = Counter(l["model answer"] for l in ls if not sem_resposta(l))
        respondidas = c["YES"] + c["NO"]
        distrib.append([p, c["YES"], c["NO"], len(ls) - respondidas, pct(div(c["YES"], respondidas))])
    s.append(tabela(["Prompt", "Respostas YES", "Respostas NO", "Sem resposta", "% YES (das respondidas)"], distrib))
    s.append("")

    # 3. efeito de cada fator, quando os nomes seguem <tipo>_shot_guided_<contexto>
    fatores = {p: PROMPT_RE.match(p) for p in prompts}
    if all(fatores.values()):
        s.append("## 3. Efeito de cada fator\n")
        s.append("### Zero-shot vs. few-shot (somando as variantes de contexto)\n")
        por_tipo = defaultdict(list)
        por_contexto = defaultdict(list)
        for p, m in fatores.items():
            por_tipo[m[1] + "-shot"] += por_prompt[p]
            por_contexto[m[2]] += por_prompt[p]
        s.append(tabela_metricas("Tipo", por_tipo))
        s.append("\n### Contexto fornecido (somando zero-shot e few-shot)\n")
        s.append(tabela_metricas("Contexto", por_contexto))
        s.append("")

    # 4. concordância entre os prompts
    s.append("## 4. Concordância entre os prompts\n")
    s.append(f"Votos \"YES\" por caso, somando os {len(prompts)} prompts (chamadas sem resposta não contam como YES):\n")
    votos = {c: sum(resposta.get((c, p)) == "YES" for p in prompts) for c in casos}
    s.append(tabela([f"Votos YES (de {len(prompts)})", "Casos YES reais", "Casos NO reais"],
                    [[k, sum(votos[c] == k and esperado[c] == "YES" for c in casos),
                      sum(votos[c] == k and esperado[c] == "NO" for c in casos)] for k in range(len(prompts) + 1)]))
    s.append(f"\n- YES reais que nenhum prompt detectou: {sum(votos[c] == 0 and esperado[c] == 'YES' for c in casos)}/{n_yes}")
    s.append(f"- NO reais marcados como YES por ≥1 prompt: "
             f"{sum(votos[c] > 0 and esperado[c] == 'NO' for c in casos)}/{len(casos) - n_yes}\n")

    s.append(f"Ensemble por voto (por caso, {len(casos)} casos):\n")
    ensemble = []
    for k in range(1, len(prompts) + 1):
        votado = [{"expected answer": esperado[c], "model answer": "YES" if votos[c] >= k else "NO", "status": "ok"}
                  for c in casos]
        m = metricas(votado)
        ensemble.append([f"≥{k} de {len(prompts)}", pct(m["acuracia"]), pct(m["precisao"]), pct(m["recall"]),
                         dec(m["f1"]), m["TP"], m["FP"]])
    s.append(tabela(["Regra (YES se…)", "Acurácia", "Precisão", "Recall", "F1", "TP", "FP"], ensemble))

    s.append("\nConcordância par a par (mesma resposta, sobre os casos respondidos pelos dois prompts):\n")
    pares = []
    for a in prompts:
        linha = [f"**{a}**"]
        for b in prompts:
            comuns = [c for c in casos if (c, a) in resposta and (c, b) in resposta]
            linha.append(pct(div(sum(resposta[(c, a)] == resposta[(c, b)] for c in comuns), len(comuns))))
        pares.append(linha)
    s.append(tabela([""] + prompts, pares))
    s.append("")

    # 5. condição violada
    s.append("## 5. Condição violada (A/B/C) nas respostas YES\n")
    cond = []
    for p, ls in por_prompt.items():
        yes = [l for l in ls if l["model answer"] == "YES"]
        tp = [l for l in yes if l["expected answer"] == "YES"]
        c, ctp = Counter(l["violated condition"] for l in yes), Counter(l["violated condition"] for l in tp)
        cond.append([p, c["A"], c["B"], c["C"], len(yes) - c["A"] - c["B"] - c["C"], ctp["A"], ctp["B"], ctp["C"]])
    s.append(tabela(["Prompt", "A", "B", "C", "outra/vazia", "Entre os TP: A", "B", "C"], cond))
    s.append("\nO dataset não traz a condição esperada, então não é possível medir a acurácia dessa classificação.\n")

    # 6. por projeto (o id do mergedataset começa com <projeto>__; no toy, cada caso é seu próprio "projeto")
    s.append("## 6. Resultado por projeto (acertos / chamadas, contando chamadas sem resposta como incorretas)\n")
    projetos = defaultdict(list)
    for c in casos:
        projetos[c.split("__")[0].split("#")[0]].append(c)
    proj = []
    for nome_proj, cs in sorted(projetos.items(), key=lambda x: -len(x[1])):
        y = sum(esperado[c] == "YES" for c in cs)
        linha = [nome_proj, f"{len(cs)} ({y}/{len(cs) - y})"]
        for p in prompts:
            acertos = sum(resposta.get((c, p)) == esperado[c] for c in cs)
            linha.append(f"{acertos}/{len(cs)}")
        proj.append(linha)
    s.append(tabela(["Projeto", "Casos (YES/NO)"] + prompts, proj))
    s.append("")

    # 7. chamadas sem resposta
    s.append("## 7. Chamadas sem resposta YES/NO\n")
    tipos = ["ignorada", "erro", "recusa", "fora do formato"]
    sem = []
    for p, ls in por_prompt.items():
        c = Counter(sem_resposta(l) for l in ls)
        faltas = [l for l in ls if sem_resposta(l)]
        sem.append([p] + [c[t] for t in tipos] + [sum(l["expected answer"] == "YES" for l in faltas),
                                                  sum(l["expected answer"] == "NO" for l in faltas)])
    s.append(tabela(["Prompt", "Ignoradas (prompt grande demais)", "Erros", "Recusas", "Fora do formato",
                     "Em casos YES", "Em casos NO"], sem))
    s.append("\n## Observações\n")
    s.append("- Precisão, recall, F1 e especificidade são da classe YES (conflito semântico).")
    s.append("- Cada caso foi avaliado uma única vez por prompt, sem repetições, então não há medida de variância.")
    return "\n".join(s) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Gera um relatório em Markdown com métricas por prompt.")
    parser.add_argument("csv", help="arquivo de resultados gerado por src.conflict_detector")
    args = parser.parse_args()
    print(relatorio(args.csv), end="")


if __name__ == "__main__":
    main()
