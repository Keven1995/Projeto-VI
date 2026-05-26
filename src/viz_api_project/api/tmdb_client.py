from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from viz_api_project.adapters.http_adapter import HttpAdapter


@dataclass(frozen=True)
class TmdbConfig:
    base_url: str = "https://api.themoviedb.org/3"
    language: str = "pt-BR"
    region: str = "BR"
    pages: int = 3
    movie_source: str = "popular"
    discover_params: dict[str, str | int | float | bool] | None = None
    timeout_seconds: int = 30
    read_token_env: str = "TMDB_READ_TOKEN"
    api_key_env: str = "TMDB_API_KEY"


class TmdbClient:
    def __init__(self, config: TmdbConfig, http_adapter: HttpAdapter | None = None) -> None:
        self._config = config
        self._http_adapter = http_adapter or HttpAdapter()

    def fetch_movies(self) -> list[dict[str, Any]]:
        if self._config.movie_source == "popular":
            return self.fetch_popular_movies()

        if self._config.movie_source == "discover":
            return self.fetch_discovered_movies()

        raise ValueError(f"Fonte de filmes TMDB invalida: {self._config.movie_source}")

    def fetch_popular_movies(self) -> list[dict[str, Any]]:
        movies: list[dict[str, Any]] = []

        for page in range(1, self._config.pages + 1):
            payload = self._get(
                "/movie/popular",
                {
                    "language": self._config.language,
                    "region": self._config.region,
                    "page": page,
                },
            )
            movies.extend(payload.get("results", []))

        return movies

    def fetch_discovered_movies(self) -> list[dict[str, Any]]:
        movies: list[dict[str, Any]] = []
        discover_params = self._config.discover_params or {}

        for page in range(1, self._config.pages + 1):
            payload = self._get(
                "/discover/movie",
                {
                    "language": self._config.language,
                    "region": self._config.region,
                    "page": page,
                    **discover_params,
                },
            )
            movies.extend(payload.get("results", []))

        return movies

    def fetch_movie_genres(self) -> dict[int, str]:
        payload = self._get("/genre/movie/list", {"language": self._config.language})
        genres = payload.get("genres", [])
        return {genre["id"]: genre["name"] for genre in genres}

    def _get(self, path: str, params: dict[str, str | int]) -> Any:
        request_params = dict(params)
        headers: dict[str, str] = {}

        read_token = os.getenv(self._config.read_token_env)
        api_key = os.getenv(self._config.api_key_env)

        if read_token:
            headers["Authorization"] = f"Bearer {read_token}"
        elif api_key:
            request_params["api_key"] = api_key
        else:
            raise RuntimeError(
                "Configure TMDB_READ_TOKEN ou TMDB_API_KEY antes de consumir a API."
            )

        return self._http_adapter.get_json(
            f"{self._config.base_url}{path}",
            headers=headers,
            params=request_params,
            timeout_seconds=self._config.timeout_seconds,
        )
