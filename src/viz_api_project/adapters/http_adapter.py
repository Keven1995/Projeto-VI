from __future__ import annotations

from typing import Any

import requests


class HttpAdapter:
    def get_json(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        params: dict[str, str | int | float | bool] | None = None,
        timeout_seconds: int = 30,
    ) -> Any:
        response = requests.get(
            url,
            headers=headers or {},
            params=params or {},
            timeout=timeout_seconds,
        )
        response.raise_for_status()
        return response.json()
