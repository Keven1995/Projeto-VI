from __future__ import annotations

from typing import Any

from viz_api_project.api.tmdb_client import TmdbClient
from viz_api_project.repositories.movie_repository import MovieRepository


class TmdbMovieRepository(MovieRepository):
    def __init__(self, client: TmdbClient) -> None:
        self._client = client

    def get_movies(self) -> list[dict[str, Any]]:
        return self._client.fetch_movies()

    def get_genres(self) -> dict[int, str]:
        return self._client.fetch_movie_genres()
