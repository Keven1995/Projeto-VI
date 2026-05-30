from typing import Any

from viz_api_project.repositories.movie_repository import MovieRepository
from viz_api_project.services.movie_dataset_service import MovieDatasetService


class FakeMovieRepository(MovieRepository):
    def get_movies(self) -> list[dict[str, Any]]:
        return [
            {
                "id": 1,
                "title": "Movie 2025",
                "release_date": "2025-03-10",
                "genre_ids": [18],
                "popularity": 10,
                "vote_average": 8,
                "vote_count": 100,
                "original_language": "pt",
            },
            {
                "id": 2,
                "title": "Movie 2026",
                "release_date": "2026-01-10",
                "genre_ids": [18],
                "popularity": 12,
                "vote_average": 9,
                "vote_count": 200,
                "original_language": "en",
            },
        ]

    def get_genres(self) -> dict[int, str]:
        return {18: "Drama"}


def test_movie_dataset_service_filters_expected_release_year() -> None:
    dataset = MovieDatasetService(
        FakeMovieRepository(),
        release_year=2025,
    ).build_dataset()

    assert dataset.records_count == 1
    assert dataset.dataframe["release_year"].tolist() == [2025]
