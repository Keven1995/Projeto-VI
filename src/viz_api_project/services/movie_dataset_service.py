from __future__ import annotations

from viz_api_project.data.tmdb_transformer import build_tmdb_movie_dataframe
from viz_api_project.dtos.clean_dataset_dto import CleanDatasetDTO
from viz_api_project.repositories.movie_repository import MovieRepository


class MovieDatasetService:
    def __init__(self, repository: MovieRepository) -> None:
        self._repository = repository

    def build_dataset(self) -> CleanDatasetDTO:
        movies = self._repository.get_movies()
        genre_names_by_id = self._repository.get_genres()
        dataframe = build_tmdb_movie_dataframe(movies, genre_names_by_id)
        return CleanDatasetDTO.from_dataframe(
            dataframe,
            source="tmdb",
            metadata={
                "raw_movies_count": len(movies),
                "genres_count": len(genre_names_by_id),
            },
        )
