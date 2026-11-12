"""Gera um relatório em Markdown com as métricas de um CSV de resultados, agrupadas por prompt.

Uso: python3 -m src.metrics results/<arquivo>_response.csv > relatorio.md
"""
import argparse
import csv
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

# "<tipo>_shot_guided_<contexto>", ex.: few_shot_guided_target
PROMPT_RE = re.compile(r"(zero|few)_shot_guided_(none|summaries|target|both)$")
ARQUIVO_RE = re.compile(r"(?P<dataset>[^_]+)_(?P<provider>[^_]+)_(?P<data>\d{8}-\d{6})_response\.csv$")

MOTIVOS_SEM_RESPOSTA = ["ignorada", "erro", "recusa", "fora do formato"]
CONDICOES = "ABC"

CAB_METRICAS = ["Acurácia", "Precisão", "Recall", "F1", "Especificidade", "TP", "TN", "FP", "FN", "Sem resposta"]

OBSERVACOES = """
## Observações

- Precisão, recall, F1 e especificidade são da classe YES (conflito semântico).
- Cada caso foi avaliado uma única vez por prompt, sem repetições, então não há medida de variância."""


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


def sem_resposta(chamada):
    """Motivo de a chamada não ter resposta YES/NO, ou None se ela tem."""
    if chamada["model answer"] in ("YES", "NO"):
        return None
    status = chamada["status"]
    if status.startswith("skipped"):
        return "ignorada"
    if "refusal" in status:
        return "recusa"
    if status.startswith("error"):
        return "erro"
    return "fora do formato"  # status ok, mas a resposta não segue "SIM - Condição X: ..." / "NAO"


def metricas_das_respostas(pares):
    """Métricas da classe YES a partir de pares (resposta esperada, resposta do modelo), ambas YES/NO."""
    pares = [(esperado == "YES", resposta == "YES") for esperado, resposta in pares]
    tp = sum(esperado and resposta for esperado, resposta in pares)
    tn = sum(not esperado and not resposta for esperado, resposta in pares)
    fp = sum(not esperado and resposta for esperado, resposta in pares)
    fn = sum(esperado and not resposta for esperado, resposta in pares)
    precisao, recall = div(tp, tp + fp), div(tp, tp + fn)
    if precisao is None or recall is None:
        f1 = None
    else:
        f1 = div(2 * precisao * recall, precisao + recall)
    return {"acuracia": div(tp + tn, len(pares)), "precisao": precisao, "recall": recall, "f1": f1,
            "especificidade": div(tn, tn + fp), "TP": tp, "TN": tn, "FP": fp, "FN": fn}


def metricas(chamadas):
    """Métricas da classe YES, calculadas só sobre as chamadas com resposta YES/NO."""
    respondidas = [c for c in chamadas if not sem_resposta(c)]
    m = metricas_das_respostas((c["expected answer"], c["model answer"]) for c in respondidas)
    m["sem"] = len(chamadas) - len(respondidas)
    return m


def linha_metricas(m):
    return [pct(m["acuracia"]), pct(m["precisao"]), pct(m["recall"]), dec(m["f1"]), pct(m["especificidade"]),
            m["TP"], m["TN"], m["FP"], m["FN"], m["sem"]]


def tabela_metricas(titulo_grupo, grupos):
    return tabela([titulo_grupo] + CAB_METRICAS, [[nome] + linha_metricas(metricas(cs)) for nome, cs in grupos.items()])


@dataclass
class Resultados:
    arquivo: str
    chamadas: list
    prompts: list
    por_prompt: dict
    casos: list
    esperado: dict  # caso -> YES/NO
    resposta: dict  # (caso, prompt) -> YES/NO, só das chamadas com resposta

    def n_yes(self, casos):
        return sum(self.esperado[caso] == "YES" for caso in casos)

    def chamadas_dos_prompts(self, prompts):
        return [chamada for prompt in prompts for chamada in self.por_prompt[prompt]]


def carregar(caminho):
    with open(caminho, newline="", encoding="utf-8-sig") as f:
        chamadas = list(csv.DictReader(f))
    prompts = list(dict.fromkeys(c["prompt"] for c in chamadas))
    return Resultados(
        arquivo=Path(caminho).name,
        chamadas=chamadas,
        prompts=prompts,
        por_prompt={p: [c for c in chamadas if c["prompt"] == p] for p in prompts},
        casos=list(dict.fromkeys(c["id"] for c in chamadas)),
        esperado={c["id"]: c["expected answer"] for c in chamadas},
        resposta={(c["id"], c["prompt"]): c["model answer"] for c in chamadas if not sem_resposta(c)},
    )


def prompts_por_fator(prompts):
    """({tipo: prompts}, {contexto: prompts}), ou None se algum nome não segue <tipo>_shot_guided_<contexto>."""
    fatores = {p: PROMPT_RE.match(p) for p in prompts}
    if not all(fatores.values()):
        return None
    por_tipo, por_contexto = defaultdict(list), defaultdict(list)
    for prompt, match in fatores.items():
        tipo, contexto = match.groups()
        por_tipo[f"{tipo}-shot"].append(prompt)
        por_contexto[contexto].append(prompt)
    return por_tipo, por_contexto


def projeto(caso):
    """No mergedataset o id começa com <projeto>__; no toy, cada caso é seu próprio projeto."""
    return caso.split("__")[0].split("#")[0]


def concordancia(r, prompt_a, prompt_b):
    """Fração dos casos respondidos pelos dois prompts em que eles deram a mesma resposta."""
    comuns = [caso for caso in r.casos if (caso, prompt_a) in r.resposta and (caso, prompt_b) in r.resposta]
    iguais = sum(r.resposta[(caso, prompt_a)] == r.resposta[(caso, prompt_b)] for caso in comuns)
    return div(iguais, len(comuns))


def secao_cabecalho(r, titulo):
    n_yes = r.n_yes(r.casos)
    yes_no = f"({n_yes} YES, {len(r.casos) - n_yes} NO)"
    motivos = Counter(filter(None, map(sem_resposta, r.chamadas)))
    saida = [f"# Relatório por prompt — `{titulo}`\n"]
    info = ARQUIVO_RE.search(r.arquivo)
    if info:
        saida.append(f"- **Dataset:** `{info['dataset']}` — {len(r.casos)} casos {yes_no}")
        saida.append(f"- **Provedor:** `{info['provider']}`")
    else:
        saida.append(f"- **Casos:** {len(r.casos)} {yes_no}")
    saida.append(f"- **Prompts:** {len(r.prompts)}; **chamadas:** {len(r.chamadas)}")
    saida.append("- **Sem resposta YES/NO:** " + (", ".join(f"{k}: {v}" for k, v in motivos.items()) or "nenhuma"))
    saida.append("- As métricas consideram só as chamadas com resposta YES/NO; as demais aparecem em \"Sem resposta\".\n")
    return "\n".join(saida)


def secao_geral(r):
    total = len(r.chamadas)
    yes_reais = sum(c["expected answer"] == "YES" for c in r.chamadas)
    no_reais = total - yes_reais
    return "\n".join([
        "## 1. Resultado geral\n",
        tabela_metricas("Chamadas", {"todas": r.chamadas}),
        f"\nBaseline: sempre responder \"NO\" daria {pct(div(no_reais, total))} de acurácia ({no_reais}/{total}). "
        f"Proporção real de YES nas chamadas: {pct(div(yes_reais, total))}.\n",
    ])


def secao_por_prompt(r):
    distribuicao = []
    for prompt, chamadas in r.por_prompt.items():
        respostas = Counter(c["model answer"] for c in chamadas if not sem_resposta(c))
        respondidas = respostas["YES"] + respostas["NO"]
        distribuicao.append([prompt, respostas["YES"], respostas["NO"], len(chamadas) - respondidas,
                             pct(div(respostas["YES"], respondidas))])
    return "\n".join([
        "## 2. Resultado por prompt\n",
        tabela_metricas("Prompt", r.por_prompt),
        "",
        tabela(["Prompt", "Respostas YES", "Respostas NO", "Sem resposta", "% YES (das respondidas)"], distribuicao),
        "",
    ])


def secao_fatores(r):
    fatores = prompts_por_fator(r.prompts)
    if fatores is None:
        return None
    por_tipo, por_contexto = fatores
    return "\n".join([
        "## 3. Efeito de cada fator\n",
        "### Zero-shot vs. few-shot (somando as variantes de contexto)\n",
        tabela_metricas("Tipo", {tipo: r.chamadas_dos_prompts(ps) for tipo, ps in por_tipo.items()}),
        "\n### Contexto fornecido (somando zero-shot e few-shot)\n",
        tabela_metricas("Contexto", {contexto: r.chamadas_dos_prompts(ps) for contexto, ps in por_contexto.items()}),
        "",
    ])


def secao_concordancia(r):
    n = len(r.prompts)
    votos = {caso: sum(r.resposta.get((caso, p)) == "YES" for p in r.prompts) for caso in r.casos}
    yes_reais = [caso for caso in r.casos if r.esperado[caso] == "YES"]
    no_reais = [caso for caso in r.casos if r.esperado[caso] == "NO"]

    distribuicao_votos = [[k, sum(votos[caso] == k for caso in yes_reais), sum(votos[caso] == k for caso in no_reais)]
                          for k in range(n + 1)]
    nao_detectados = sum(votos[caso] == 0 for caso in yes_reais)
    falsos_alarmes = sum(votos[caso] > 0 for caso in no_reais)

    ensemble = []
    for k in range(1, n + 1):
        m = metricas_das_respostas((r.esperado[caso], "YES" if votos[caso] >= k else "NO") for caso in r.casos)
        ensemble.append([f"≥{k} de {n}", pct(m["acuracia"]), pct(m["precisao"]), pct(m["recall"]), dec(m["f1"]),
                         m["TP"], m["FP"]])

    pares = [[f"**{a}**"] + [pct(concordancia(r, a, b)) for b in r.prompts] for a in r.prompts]

    return "\n".join([
        "## 4. Concordância entre os prompts\n",
        f"Votos \"YES\" por caso, somando os {n} prompts (chamadas sem resposta não contam como YES):\n",
        tabela([f"Votos YES (de {n})", "Casos YES reais", "Casos NO reais"], distribuicao_votos),
        f"\n- YES reais que nenhum prompt detectou: {nao_detectados}/{len(yes_reais)}",
        f"- NO reais marcados como YES por ≥1 prompt: {falsos_alarmes}/{len(no_reais)}\n",
        f"Ensemble por voto (por caso, {len(r.casos)} casos):\n",
        tabela(["Regra (YES se…)", "Acurácia", "Precisão", "Recall", "F1", "TP", "FP"], ensemble),
        "\nConcordância par a par (mesma resposta, sobre os casos respondidos pelos dois prompts):\n",
        tabela([""] + r.prompts, pares),
        "",
    ])


def secao_condicao(r):
    linhas = []
    for prompt, chamadas in r.por_prompt.items():
        yes = [c for c in chamadas if c["model answer"] == "YES"]
        condicoes = Counter(c["violated condition"] for c in yes)
        condicoes_tp = Counter(c["violated condition"] for c in yes if c["expected answer"] == "YES")
        outras = len(yes) - sum(condicoes[x] for x in CONDICOES)
        linhas.append([prompt, *[condicoes[x] for x in CONDICOES], outras, *[condicoes_tp[x] for x in CONDICOES]])
    return "\n".join([
        "## 5. Condição violada (A/B/C) nas respostas YES\n",
        tabela(["Prompt", "A", "B", "C", "outra/vazia", "Entre os TP: A", "B", "C"], linhas),
        "\nO dataset não traz a condição esperada, então não é possível medir a acurácia dessa classificação.\n",
    ])


def secao_por_projeto(r):
    projetos = defaultdict(list)
    for caso in r.casos:
        projetos[projeto(caso)].append(caso)
    linhas = []
    for nome, casos in sorted(projetos.items(), key=lambda item: -len(item[1])):
        n_yes = r.n_yes(casos)
        acertos = [sum(r.resposta.get((caso, p)) == r.esperado[caso] for caso in casos) for p in r.prompts]
        linhas.append([nome, f"{len(casos)} ({n_yes}/{len(casos) - n_yes})"] + [f"{a}/{len(casos)}" for a in acertos])
    return "\n".join([
        "## 6. Resultado por projeto (acertos / chamadas, contando chamadas sem resposta como incorretas)\n",
        tabela(["Projeto", "Casos (YES/NO)"] + r.prompts, linhas),
        "",
    ])


def secao_sem_resposta(r):
    linhas = []
    for prompt, chamadas in r.por_prompt.items():
        motivos = Counter(map(sem_resposta, chamadas))
        faltas = [c for c in chamadas if sem_resposta(c)]
        em_yes = sum(c["expected answer"] == "YES" for c in faltas)
        em_no = sum(c["expected answer"] == "NO" for c in faltas)
        linhas.append([prompt, *[motivos[m] for m in MOTIVOS_SEM_RESPOSTA], em_yes, em_no])
    return "\n".join([
        "## 7. Chamadas sem resposta YES/NO\n",
        tabela(["Prompt", "Ignoradas (prompt grande demais)", "Erros", "Recusas", "Fora do formato",
                "Em casos YES", "Em casos NO"], linhas),
    ])


def relatorio(r, titulo=None):
    secoes = [secao_cabecalho(r, titulo or r.arquivo), secao_geral(r), secao_por_prompt(r), secao_fatores(r), secao_concordancia(r),
              secao_condicao(r), secao_por_projeto(r), secao_sem_resposta(r), OBSERVACOES]
    return "\n".join(s for s in secoes if s is not None) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Gera um relatório em Markdown com métricas por prompt.")
    parser.add_argument("csv", help="arquivo de resultados gerado por src.conflict_detector")
    args = parser.parse_args()
    print(relatorio(carregar(args.csv)), end="")


if __name__ == "__main__":
    main()
