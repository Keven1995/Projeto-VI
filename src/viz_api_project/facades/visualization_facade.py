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
        release_year = _extract_release_year(config.tmdb.discover_params)
        return MovieDatasetService(repository, release_year=release_year).build_dataset()

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


def _extract_release_year(
    discover_params: dict[str, str | int | float | bool] | None,
) -> int | None:
    if not discover_params:
        return None

    release_year = discover_params.get("primary_release_year")
    if isinstance(release_year, int):
        return release_year

    if isinstance(release_year, str) and release_year.isdigit():
        return int(release_year)

    return None
