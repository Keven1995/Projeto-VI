from __future__ import annotations

from pathlib import Path

import pandas as pd

from viz_api_project.charts.chord import ChordDiagramConfig, create_chord_diagram
from viz_api_project.strategies.chart_strategy import ChartStrategy


class ChordChartStrategy(ChartStrategy):
    def __init__(self, config: ChordDiagramConfig) -> None:
        self._config = config

    def create(self, dataframe: pd.DataFrame) -> Path:
        return create_chord_diagram(dataframe, self._config)
