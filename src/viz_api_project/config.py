from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from viz_api_project.api.client import ApiConfig
from viz_api_project.api.tmdb_client import TmdbConfig
from viz_api_project.charts.bar import BarChartConfig
from viz_api_project.charts.chord import ChordDiagramConfig
from viz_api_project.charts.line import LineChartConfig


@dataclass(frozen=True)
class ProjectConfig:
    source: str
    api: ApiConfig | None
    tmdb: TmdbConfig | None
    records_path: str
    local_data_path: Path | None
    line: LineChartConfig
    bar: BarChartConfig
    chord: ChordDiagramConfig


def load_config(path: str | Path) -> ProjectConfig:
    config_path = Path(path)
    raw_config = json.loads(config_path.read_text(encoding="utf-8"))

    source = raw_config.get("source", "generic")
    api_config = _build_api_config(raw_config.get("api", {}))
    tmdb_config = _build_tmdb_config(raw_config.get("tmdb", {})) if source == "tmdb" else None
    local_data_path = raw_config.get("local_data_path")
    charts = raw_config["charts"]

    return ProjectConfig(
        source=source,
        api=api_config,
        tmdb=tmdb_config,
        records_path=raw_config.get("records_path", ""),
        local_data_path=Path(local_data_path) if local_data_path else None,
        line=LineChartConfig(**charts["line"]),
        bar=BarChartConfig(**charts["bar"]),
        chord=ChordDiagramConfig(**charts["chord"]),
    )


def _build_api_config(raw_api: dict[str, Any]) -> ApiConfig | None:
    url = raw_api.get("url")
    if not url:
        return None

    return ApiConfig(
        url=url,
        timeout_seconds=raw_api.get("timeout_seconds", 30),
        headers=raw_api.get("headers", {}),
        params=raw_api.get("params", {}),
    )


def _build_tmdb_config(raw_tmdb: dict[str, Any]) -> TmdbConfig:
    return TmdbConfig(
        base_url=raw_tmdb.get("base_url", "https://api.themoviedb.org/3"),
        language=raw_tmdb.get("language", "pt-BR"),
        region=raw_tmdb.get("region", "BR"),
        pages=raw_tmdb.get("pages", 3),
        movie_source=raw_tmdb.get("movie_source", "popular"),
        discover_params=raw_tmdb.get("discover_params", {}),
        timeout_seconds=raw_tmdb.get("timeout_seconds", 30),
        read_token_env=raw_tmdb.get("read_token_env", "TMDB_READ_TOKEN"),
        api_key_env=raw_tmdb.get("api_key_env", "TMDB_API_KEY"),
    )
