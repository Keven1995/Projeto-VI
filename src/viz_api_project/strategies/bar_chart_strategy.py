from __future__ import annotations

from pathlib import Path

import pandas as pd

from viz_api_project.charts.bar import BarChartConfig, create_bar_chart
from viz_api_project.strategies.chart_strategy import ChartStrategy


class BarChartStrategy(ChartStrategy):
    def __init__(self, config: BarChartConfig) -> None:
        self._config = config

    def create(self, dataframe: pd.DataFrame) -> Path:
        return create_bar_chart(dataframe, self._config)
