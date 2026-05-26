from __future__ import annotations

from pathlib import Path

import pandas as pd


def ensure_columns(dataframe: pd.DataFrame, columns: list[str]) -> None:
    missing = [column for column in columns if column not in dataframe.columns]
    if missing:
        available = ", ".join(dataframe.columns)
        raise ValueError(
            f"Colunas ausentes: {', '.join(missing)}. Colunas disponiveis: {available}"
        )


def prepare_output_path(path: str | Path) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return output_path
