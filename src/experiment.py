"""Roda o experimento completo: cada modelo várias vezes sobre o dataset, e depois gera os relatórios.

Uso: python3 -m src.experiment results/v3
     python3 -m src.experiment results/v3 --models claude-haiku-5-5 claude-sonnet-5-5 --runs 3 --dataset toy

Grava cada execução em <diretório>/<modelo>/<n>.csv, o formato lido por src.reports, e no fim chama src.reports.
Execuções que já têm CSV são puladas, então basta rodar o mesmo comando de novo para continuar
um experimento interrompido.
"""
import argparse
import csv
from pathlib import Path

from src.conflict_detector import run
from src.datasets import DATASETS
from src.providers import PROVIDERS, get_provider
from src.reports import gerar_relatorios

MODELS = ["claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5"]


def resumo_status(caminho):
    """Conta as chamadas por status (ok, skipped, error), para avisar de execuções com muitos erros."""
    with open(caminho, newline="", encoding="utf-8-sig") as f:
        status = [row["status"].split(":")[0] for row in csv.DictReader(f)]
    return {s: status.count(s) for s in sorted(set(status))}


def main():
    parser = argparse.ArgumentParser(description="Roda cada modelo várias vezes e gera os relatórios.")
    parser.add_argument("diretorio", type=Path, help="diretório de saída, ex.: results/v3")
    parser.add_argument("--provider", choices=PROVIDERS, default="anthropic")
    parser.add_argument("--models", nargs="+", default=MODELS, help=f"padrão: {' '.join(MODELS)}")
    parser.add_argument("--runs", type=int, default=3, help="execuções por modelo (padrão: 3)")
    parser.add_argument("--dataset", choices=DATASETS, default="mergedataset")
    parser.add_argument("--cache", action="store_true",
                        help="cache de 1h da parte fixa do prompt (só provedores com SUPPORTS_PREFIX_CACHE)")
    args = parser.parse_args()

    for model in args.models:
        provider = get_provider(args.provider, model)
        if args.cache and not getattr(provider, "SUPPORTS_PREFIX_CACHE", False):
            parser.error(f"--cache não é suportado pelo provedor {args.provider!r}")
        pasta = args.diretorio / model.replace("/", "-").replace(":", "-")
        pasta.mkdir(parents=True, exist_ok=True)
        for n in range(1, args.runs + 1):
            destino = pasta / f"{n}.csv"
            if destino.exists():
                print(f"=== {model} | execução {n}/{args.runs}: {destino} já existe, pulando")
                continue
            print(f"=== {model} | execução {n}/{args.runs} -> {destino}")
            # grava em um arquivo temporário e só renomeia no fim, para que uma execução interrompida
            # não seja confundida com uma completa ao rodar o comando de novo
            parcial = destino.with_suffix(".csv.partial")
            run(provider, args.dataset, parcial, cache=args.cache)
            parcial.rename(destino)
            print(f"=== {model} | execução {n}/{args.runs} concluída: {resumo_status(destino)}")

    gerar_relatorios(args.diretorio)


if __name__ == "__main__":
    main()
