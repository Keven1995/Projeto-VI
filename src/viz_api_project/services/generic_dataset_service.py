from __future__ import annotations

from viz_api_project.data.normalizer import normalize_records
from viz_api_project.dtos.clean_dataset_dto import CleanDatasetDTO
from viz_api_project.repositories.generic_repository import GenericRepository


class GenericDatasetService:
    def __init__(self, repository: GenericRepository) -> None:
        self._repository = repository

    def build_dataset(self) -> CleanDatasetDTO:
        records = self._repository.get_records()
        dataframe = normalize_records(records)
        return CleanDatasetDTO.from_dataframe(
            dataframe,
            source="generic",
            metadata={"raw_records_count": len(records)},
        )
