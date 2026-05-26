from __future__ import annotations

from pathlib import Path

from viz_api_project.dtos.clean_dataset_dto import CleanDatasetDTO
from viz_api_project.strategies.chart_strategy import ChartStrategy


class VisualizationService:
    def __init__(self, strategies: list[ChartStrategy]) -> None:
        self._strategies = strategies

    def generate(self, dataset: CleanDatasetDTO) -> list[Path]:
        return [strategy.create(dataset.dataframe) for strategy in self._strategies]
