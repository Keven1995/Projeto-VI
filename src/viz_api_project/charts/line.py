from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", str(Path(".matplotlib-cache").resolve()))

import matplotlib.pyplot as plt
import pandas as pd
from pandas.api.types import is_object_dtype

from viz_api_project.charts.common import ensure_columns, prepare_output_path


@dataclass(frozen=True)
class LineChartConfig:
    x: str
    y: str
    title: str
    output: str
    group_by: str | None = None
    aggregation: str | None = None


def create_line_chart(dataframe: pd.DataFrame, config: LineChartConfig) -> Path:
    required_columns = [config.x, config.y]
    if config.group_by:
        required_columns.append(config.group_by)
    ensure_columns(dataframe, required_columns)

    plot_data = dataframe.copy()
    if is_object_dtype(plot_data[config.x]):
        converted_x = pd.to_datetime(plot_data[config.x], errors="coerce")
        if converted_x.notna().all():
            plot_data[config.x] = converted_x

    if config.aggregation:
        plot_data = _aggregate_line_data(plot_data, config)

    plot_data = plot_data.sort_values(config.x)

    figure, axis = plt.subplots(figsize=(11, 6))

    if config.group_by:
        for label, group in plot_data.groupby(config.group_by):
            axis.plot(group[config.x], group[config.y], marker="o", linewidth=2, label=str(label))
        axis.legend(title=config.group_by)
    else:
        axis.plot(plot_data[config.x], plot_data[config.y], marker="o", linewidth=2)

    axis.set_title(config.title)
    axis.set_xlabel(config.x)
    axis.set_ylabel(config.y)
    axis.grid(True, alpha=0.25)
    figure.autofmt_xdate()
    figure.tight_layout()

    output_path = prepare_output_path(config.output)
    figure.savefig(output_path, dpi=150)
    plt.close(figure)

    return output_path


def _aggregate_line_data(
    dataframe: pd.DataFrame,
    config: LineChartConfig,
) -> pd.DataFrame:
    group_columns = [config.x]
    if config.group_by:
        group_columns.append(config.group_by)

    if config.aggregation not in {"sum", "mean", "median", "max", "min"}:
        raise ValueError(f"Agregacao invalida para grafico de linha: {config.aggregation}")

    return (
        dataframe.groupby(group_columns, as_index=False)[config.y]
        .agg(config.aggregation)
        .sort_values(config.x)
    )
