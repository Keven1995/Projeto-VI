from __future__ import annotations

from pathlib import Path

from viz_api_project.config import ProjectConfig
from viz_api_project.facades.visualization_facade import VisualizationFacade


def run_pipeline(config: ProjectConfig) -> list[Path]:
    return VisualizationFacade().generate_from_config(config)
