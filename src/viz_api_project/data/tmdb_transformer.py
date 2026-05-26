from __future__ import annotations

from typing import Any

import pandas as pd


def build_tmdb_movie_dataframe(
    movies: list[dict[str, Any]],
    genre_names_by_id: dict[int, str],
) -> pd.DataFrame:
    dataframe = pd.DataFrame(movies)

    if dataframe.empty:
        raise ValueError("A API do TMDB nao retornou filmes.")

    dataframe["release_date"] = pd.to_datetime(
        dataframe.get("release_date"), errors="coerce"
    )
    dataframe["release_year"] = dataframe["release_date"].dt.year
    dataframe["release_month"] = dataframe["release_date"].dt.to_period("M").astype(str)
    dataframe["primary_genre"] = dataframe["genre_ids"].apply(
        lambda genre_ids: _primary_genre_name(genre_ids, genre_names_by_id)
    )
    dataframe["genre_names"] = dataframe["genre_ids"].apply(
        lambda genre_ids: _genre_names(genre_ids, genre_names_by_id)
    )
    dataframe["popularity"] = pd.to_numeric(dataframe["popularity"], errors="coerce")
    dataframe["vote_average"] = pd.to_numeric(dataframe["vote_average"], errors="coerce")
    dataframe["vote_count"] = pd.to_numeric(dataframe["vote_count"], errors="coerce")

    return dataframe.dropna(subset=["release_date", "popularity"])


def _primary_genre_name(
    genre_ids: list[int] | float,
    genre_names_by_id: dict[int, str],
) -> str:
    names = _genre_names(genre_ids, genre_names_by_id)
    if not names:
        return "Sem genero"
    return names[0]


def _genre_names(
    genre_ids: list[int] | float,
    genre_names_by_id: dict[int, str],
) -> list[str]:
    if not isinstance(genre_ids, list):
        return []

    return [genre_names_by_id.get(genre_id, f"Genero {genre_id}") for genre_id in genre_ids]
