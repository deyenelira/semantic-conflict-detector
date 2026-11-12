"""Gera todos os relatórios de um diretório com uma pasta por modelo e um CSV de resultados por execução.

Uso: python3 -m src.reports results/v2

Escreve, dentro do diretório:
- <modelo>/<execução>_report.md: o relatório de src.metrics para cada execução;
- <modelo>/report.md: o resumo das execuções do modelo;
- report.md: a comparação entre os modelos.
"""
import argparse
from pathlib import Path

from src.comparison import relatorio_comparativo, relatorio_modelo
from src.metrics import carregar, relatorio


def carregar_modelos(diretorio):
    modelos = {}
    for pasta in sorted(p for p in diretorio.iterdir() if p.is_dir()):
        csvs = sorted(pasta.glob("*.csv"))
        if csvs:
            modelos[pasta.name] = [carregar(csv) for csv in csvs]
    return modelos


def conferir_casos_e_prompts(modelos):
    """As execuções só podem ser comparadas se todas têm os mesmos casos e prompts."""
    execucoes = [(f"{nome}/{r.arquivo}", r) for nome, rs in modelos.items() for r in rs]
    nome_referencia, referencia = execucoes[0]
    for nome, r in execucoes:
        if set(r.casos) != set(referencia.casos) or set(r.prompts) != set(referencia.prompts):
            raise SystemExit(f"{nome} não tem os mesmos casos e prompts que {nome_referencia}")


def escrever(caminho, conteudo):
    caminho.write_text(conteudo, encoding="utf-8")
    print(caminho)


def main():
    parser = argparse.ArgumentParser(description="Gera os relatórios por execução, por modelo e entre modelos.")
    parser.add_argument("diretorio", type=Path, help="diretório com uma pasta de CSVs por modelo, ex.: results/v2")
    args = parser.parse_args()

    modelos = carregar_modelos(args.diretorio)
    if not modelos:
        raise SystemExit(f"nenhum CSV encontrado em {args.diretorio}/<modelo>/")
    conferir_casos_e_prompts(modelos)

    for nome, execucoes in modelos.items():
        pasta = args.diretorio / nome
        for r in execucoes:
            escrever(pasta / f"{Path(r.arquivo).stem}_report.md", relatorio(r, titulo=f"{nome}/{r.arquivo}"))
        escrever(pasta / "report.md", relatorio_modelo(nome, execucoes))
    escrever(args.diretorio / "report.md", relatorio_comparativo(modelos, args.diretorio.name))


if __name__ == "__main__":
    main()
