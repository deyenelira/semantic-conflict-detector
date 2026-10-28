import csv
import difflib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# Os datasets disponíveis são os diretórios de data/ que contêm um dataset.csv (ex.: toy, mergedataset)
DATASETS = tuple(sorted(p.name for p in DATA.iterdir() if (p / "dataset.csv").is_file()))

SEM_ALTERACOES = "(sem alterações em relação a BASE)"
# linhas inalteradas mostradas ao redor de cada mudança nos diffs (o padrão do git)
CONTEXT_LINES = 3


def load(name):
    """Devolve as linhas do dataset com o código de BASE completo e LEFT/RIGHT/MERGE como diffs.

    Cada linha do dataset.csv tem id, target, label, left_summary e right_summary. O código fica em
    data/<dataset>/<pasta>/{base,left,right,merge}.<extensão>, onde <pasta> é o id até o "#"
    (uma mesma pasta pode ter mais de um alvo).
    """
    if name not in DATASETS:
        raise ValueError(f"Dataset inválido: {name!r}. Opções: {', '.join(DATASETS)}")
    folder = DATA / name
    with open(folder / "dataset.csv", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    for row in rows:
        case = folder / row["id"].split("#")[0]
        files = {v: version_file(case, v) for v in ("base", "left", "right", "merge")}
        base = files["base"].read_text(encoding="utf-8")
        row["base"] = base
        for v in ("left", "right", "merge"):
            row[v] = unified_diff(base, files[v].read_text(encoding="utf-8"),
                                  files["base"].name, files[v].name)
    return rows


def version_file(case, version):
    matches = sorted(case.glob(f"{version}.*"))
    if len(matches) != 1:
        raise FileNotFoundError(f"Esperado um arquivo {version}.* em {case}, encontrados: {matches}")
    return matches[0]


def unified_diff(base, other, base_name, other_name):
    # garante quebra de linha no fim para que a ausência dela não apareça como alteração
    base_lines = (base if base.endswith("\n") else base + "\n").splitlines(keepends=True)
    other_lines = (other if other.endswith("\n") else other + "\n").splitlines(keepends=True)
    diff = "".join(difflib.unified_diff(base_lines, other_lines, base_name, other_name, n=CONTEXT_LINES))
    return diff or SEM_ALTERACOES
