import pandas as pd

from viz_api_project.dtos.clean_dataset_dto import CleanDatasetDTO


def test_clean_dataset_dto_from_dataframe_carries_metadata() -> None:
    dataframe = pd.DataFrame([{"title": "Example", "vote_average": 8.5}])

    dto = CleanDatasetDTO.from_dataframe(
        dataframe,
        source="tmdb",
        metadata={"raw_movies_count": 1},
    )

    assert dto.records_count == 1
    assert dto.columns == ("title", "vote_average")
    assert dto.metadata["raw_movies_count"] == 1
