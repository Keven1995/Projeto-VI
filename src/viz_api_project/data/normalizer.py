from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import pandas as pd


def extract_records(payload: Any, records_path: str = "") -> list[dict[str, Any]]:
    data = _resolve_path(payload, records_path)

    if isinstance(data, dict):
        return [data]

    if not isinstance(data, list):
        raise ValueError("O caminho informado nao aponta para uma lista de registros.")

    if not all(isinstance(item, dict) for item in data):
        raise ValueError("Todos os registros precisam ser objetos JSON.")

    return data


def normalize_records(records: Iterable[dict[str, Any]]) -> pd.DataFrame:
    dataframe = pd.json_normalize(list(records))

    if dataframe.empty:
        raise ValueError("O dataset retornado esta vazio.")

    return dataframe


def _resolve_path(payload: Any, path: str) -> Any:
    if not path:
        return payload

    current = payload
    for part in path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
            continue

        raise KeyError(f"Caminho nao encontrado no JSON: {path}")

    return current
