from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from viz_api_project.api.client import ApiClient
from viz_api_project.config import ProjectConfig
from viz_api_project.data.normalizer import extract_records


class GenericRepository:
    def __init__(self, config: ProjectConfig) -> None:
        self._config = config

    def get_records(self) -> list[dict[str, Any]]:
        payload = self._load_payload()
        return extract_records(payload, self._config.records_path)

    def _load_payload(self) -> object:
        if self._config.api:
            return ApiClient(self._config.api).fetch_json()

        if self._config.local_data_path:
            path = Path(self._config.local_data_path)
            return json.loads(path.read_text(encoding="utf-8"))

        raise ValueError("Informe uma API ou um arquivo local de dados no config.")
