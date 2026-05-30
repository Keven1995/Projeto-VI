from __future__ import annotations

import argparse
import sys

from viz_api_project.config import load_config
from viz_api_project.env import load_dotenv
from viz_api_project.facades.visualization_facade import VisualizationFacade


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Gera visualizacoes a partir de dados consumidos de API."
    )
    parser.add_argument(
        "--config",
        default="configs/tmdb_top_rated_2025.json",
        help="Caminho do arquivo JSON de configuracao.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    load_dotenv()
    config = load_config(args.config)

    try:
        generated_files = VisualizationFacade().generate_from_config(config)
    except RuntimeError as error:
        print(f"Erro: {error}", file=sys.stderr)
        raise SystemExit(1) from error

    for file_path in generated_files:
        print(f"Grafico gerado: {file_path}")


if __name__ == "__main__":
    main()
