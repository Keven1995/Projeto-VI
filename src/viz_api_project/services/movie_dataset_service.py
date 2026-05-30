from __future__ import annotations

from viz_api_project.data.tmdb_transformer import build_tmdb_movie_dataframe
from viz_api_project.dtos.clean_dataset_dto import CleanDatasetDTO
from viz_api_project.repositories.movie_repository import MovieRepository


class MovieDatasetService:
    def __init__(self, repository: MovieRepository, release_year: int | None = None) -> None:
        self._repository = repository
        self._release_year = release_year

    def build_dataset(self) -> CleanDatasetDTO:
        movies = self._repository.get_movies()
        genre_names_by_id = self._repository.get_genres()
        dataframe = build_tmdb_movie_dataframe(movies, genre_names_by_id)
        if self._release_year:
            dataframe = dataframe[dataframe["release_year"] == self._release_year]

        return CleanDatasetDTO.from_dataframe(
            dataframe,
            source="tmdb",
            metadata={
                "raw_movies_count": len(movies),
                "clean_movies_count": len(dataframe),
                "genres_count": len(genre_names_by_id),
                "release_year": self._release_year or "",
            },
        )
