from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from viz_api_project.adapters.http_adapter import HttpAdapter


@dataclass(frozen=True)
class ApiConfig:
    url: str
    timeout_seconds: int = 30
    headers: dict[str, str] = field(default_factory=dict)
    params: dict[str, str] = field(default_factory=dict)


class ApiClient:
    """Small HTTP client focused on JSON APIs."""

    def __init__(self, config: ApiConfig, http_adapter: HttpAdapter | None = None) -> None:
        self._config = config
        self._http_adapter = http_adapter or HttpAdapter()

    def fetch_json(self) -> Any:
        return self._http_adapter.get_json(
            self._config.url,
            headers=self._config.headers,
            params=self._config.params,
            timeout_seconds=self._config.timeout_seconds,
        )
