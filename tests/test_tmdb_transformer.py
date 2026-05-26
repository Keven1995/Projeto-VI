from viz_api_project.data.tmdb_transformer import build_tmdb_movie_dataframe


def test_build_tmdb_movie_dataframe_maps_primary_genre() -> None:
    movies = [
        {
            "id": 1,
            "title": "Example",
            "release_date": "2026-01-01",
            "genre_ids": [28, 12],
            "popularity": 10.5,
            "vote_average": 7.2,
            "vote_count": 100,
            "original_language": "en",
        }
    ]

    dataframe = build_tmdb_movie_dataframe(movies, {28: "Acao", 12: "Aventura"})

    assert dataframe.loc[0, "primary_genre"] == "Acao"
    assert dataframe.loc[0, "genre_names"] == ["Acao", "Aventura"]
