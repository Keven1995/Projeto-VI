from viz_api_project.api.tmdb_client import TmdbClient, TmdbConfig


def test_fetch_movies_rejects_invalid_source() -> None:
    client = TmdbClient(TmdbConfig(movie_source="invalid"))

    try:
        client.fetch_movies()
    except ValueError as error:
        assert "Fonte de filmes TMDB invalida" in str(error)
    else:
        raise AssertionError("Expected invalid movie source to raise ValueError.")
