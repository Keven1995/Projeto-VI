from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", str(Path(".matplotlib-cache").resolve()))

import matplotlib.pyplot as plt
import pandas as pd

from viz_api_project.charts.common import ensure_columns, prepare_output_path


@dataclass(frozen=True)
class BarChartConfig:
    x: str
    y: str
    title: str
    output: str
    top_n: int = 10


def create_bar_chart(dataframe: pd.DataFrame, config: BarChartConfig) -> Path:
    ensure_columns(dataframe, [config.x, config.y])

    plot_data = (
        dataframe.groupby(config.x, as_index=False)[config.y]
        .sum()
        .sort_values(config.y, ascending=False)
        .head(config.top_n)
    )

    figure, axis = plt.subplots(figsize=(11, 6))
    axis.bar(plot_data[config.x].astype(str), plot_data[config.y], color="#2f80ed")
    axis.set_title(config.title)
    axis.set_xlabel(config.x)
    axis.set_ylabel(config.y)
    axis.tick_params(axis="x", rotation=35)
    axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()

    output_path = prepare_output_path(config.output)
    figure.savefig(output_path, dpi=150)
    plt.close(figure)

    return output_path
