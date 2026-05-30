from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from textwrap import wrap

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

    labels = plot_data[config.x].astype(str)

    if _should_use_horizontal_bars(labels):
        output_path = _create_horizontal_bar_chart(plot_data, labels, config)
        return output_path

    figure, axis = plt.subplots(figsize=(11, 6))
    axis.bar(labels, plot_data[config.y], color="#2f80ed")
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


def _create_horizontal_bar_chart(
    plot_data: pd.DataFrame,
    labels: pd.Series,
    config: BarChartConfig,
) -> Path:
    sorted_data = plot_data.assign(_label=labels).sort_values(config.y, ascending=True)
    wrapped_labels = [_wrap_label(label) for label in sorted_data["_label"]]
    figure_height = max(6, len(sorted_data) * 0.48)

    figure, axis = plt.subplots(figsize=(12, figure_height))
    bars = axis.barh(wrapped_labels, sorted_data[config.y], color="#2f80ed")

    axis.set_title(config.title)
    axis.set_xlabel(config.y)
    axis.set_ylabel(config.x)
    axis.grid(axis="x", alpha=0.25)
    axis.bar_label(bars, fmt="%.2f", padding=4, fontsize=8)
    axis.margins(x=0.12)
    figure.tight_layout()

    output_path = prepare_output_path(config.output)
    figure.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(figure)

    return output_path


def _should_use_horizontal_bars(labels: pd.Series) -> bool:
    return len(labels) > 8 or labels.str.len().max() > 18


def _wrap_label(label: str, width: int = 32) -> str:
    return "\n".join(wrap(label, width=width, break_long_words=False))
