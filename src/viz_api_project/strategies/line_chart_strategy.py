from __future__ import annotations

from pathlib import Path

import pandas as pd

from viz_api_project.charts.line import LineChartConfig, create_line_chart
from viz_api_project.strategies.chart_strategy import ChartStrategy


class LineChartStrategy(ChartStrategy):
    def __init__(self, config: LineChartConfig) -> None:
        self._config = config

    def create(self, dataframe: pd.DataFrame) -> Path:
        return create_line_chart(dataframe, self._config)
