from __future__ import annotations

from pathlib import Path

from viz_api_project.api.tmdb_client import TmdbClient
from viz_api_project.config import ProjectConfig
from viz_api_project.dtos.clean_dataset_dto import CleanDatasetDTO
from viz_api_project.repositories.generic_repository import GenericRepository
from viz_api_project.repositories.tmdb_movie_repository import TmdbMovieRepository
from viz_api_project.services.generic_dataset_service import GenericDatasetService
from viz_api_project.services.movie_dataset_service import MovieDatasetService
from viz_api_project.services.visualization_service import VisualizationService
from viz_api_project.strategies.bar_chart_strategy import BarChartStrategy
from viz_api_project.strategies.chord_chart_strategy import ChordChartStrategy
from viz_api_project.strategies.line_chart_strategy import LineChartStrategy


class VisualizationFacade:
    def generate_from_config(self, config: ProjectConfig) -> list[Path]:
        dataset = self.build_clean_dataset(config)
        visualization_service = self._build_visualization_service(config)
        return visualization_service.generate(dataset)

    def build_clean_dataset(self, config: ProjectConfig) -> CleanDatasetDTO:
        if config.source == "tmdb":
            return self._build_tmdb_dataset(config)

        repository = GenericRepository(config)
        return GenericDatasetService(repository).build_dataset()

    def _build_tmdb_dataset(self, config: ProjectConfig) -> CleanDatasetDTO:
        if not config.tmdb:
            raise ValueError("Configuracao do TMDB ausente.")

        repository = TmdbMovieRepository(TmdbClient(config.tmdb))
        return MovieDatasetService(repository).build_dataset()

    def _build_visualization_service(
        self,
        config: ProjectConfig,
    ) -> VisualizationService:
        return VisualizationService(
            [
                LineChartStrategy(config.line),
                BarChartStrategy(config.bar),
                ChordChartStrategy(config.chord),
            ]
        )
