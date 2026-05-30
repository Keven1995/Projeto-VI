from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", str(Path(".matplotlib-cache").resolve()))

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.path import Path as MatplotlibPath
from matplotlib.patches import Circle, PathPatch

from viz_api_project.charts.common import ensure_columns, prepare_output_path


@dataclass(frozen=True)
class ChordDiagramConfig:
    source: str
    target: str
    value: str
    title: str
    output: str
    top_n: int | None = None


def create_chord_diagram(dataframe: pd.DataFrame, config: ChordDiagramConfig) -> Path:
    ensure_columns(dataframe, [config.source, config.target, config.value])

    flows = (
        dataframe.groupby([config.source, config.target], as_index=False)[config.value]
        .sum()
        .query(f"{config.value} > 0")
        .sort_values(config.value, ascending=False)
    )
    if config.top_n:
        flows = flows.head(config.top_n)

    if flows.empty:
        raise ValueError("Nao existem fluxos positivos para gerar o diagrama de cordas.")

    sources = _ordered_nodes(flows, config.source, config.value)
    targets = _ordered_nodes(flows, config.target, config.value)
    source_positions = _node_positions(sources, x=-0.85)
    target_positions = _node_positions(targets, x=0.85)

    figure_height = max(7, max(len(sources), len(targets)) * 0.45)
    figure, axis = plt.subplots(figsize=(12, figure_height))
    axis.set_title(config.title)
    axis.axis("off")

    _draw_column_title(axis, "Idiomas", x=-0.85)
    _draw_column_title(axis, "Generos", x=0.85)
    _draw_nodes(axis, source_positions, align="right", color="#2f80ed")
    _draw_nodes(axis, target_positions, align="left", color="#27ae60")
    _draw_chords(axis, flows, source_positions, target_positions, config)

    axis.set_xlim(-1.45, 1.45)
    axis.set_ylim(-1.15, 1.15)

    output_path = prepare_output_path(config.output)
    figure.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(figure)

    return output_path


def _ordered_nodes(flows: pd.DataFrame, column: str, value_column: str) -> list[str]:
    totals = flows.groupby(column)[value_column].sum().sort_values(ascending=False)
    return [str(node) for node in totals.index]


def _node_positions(nodes: list[str], x: float) -> dict[str, tuple[float, float]]:
    if len(nodes) == 1:
        return {nodes[0]: (x, 0.0)}

    step = 1.8 / (len(nodes) - 1)
    return {node: (x, 0.9 - index * step) for index, node in enumerate(nodes)}


def _draw_column_title(axis: plt.Axes, title: str, x: float) -> None:
    axis.text(x, 1.08, title, ha="center", va="bottom", fontsize=11, fontweight="bold")


def _draw_nodes(
    axis: plt.Axes,
    positions: dict[str, tuple[float, float]],
    *,
    align: str,
    color: str,
) -> None:
    text_offset = -0.05 if align == "right" else 0.05

    for node, (x, y) in positions.items():
        axis.add_patch(Circle((x, y), radius=0.018, facecolor=color, edgecolor="white"))
        axis.text(
            x + text_offset,
            y,
            node,
            ha=align,
            va="center",
            fontsize=9,
        )


def _draw_chords(
    axis: plt.Axes,
    flows: pd.DataFrame,
    source_positions: dict[str, tuple[float, float]],
    target_positions: dict[str, tuple[float, float]],
    config: ChordDiagramConfig,
) -> None:
    max_value = float(flows[config.value].max())

    for _, row in flows.iterrows():
        source = source_positions[str(row[config.source])]
        target = target_positions[str(row[config.target])]
        source_control = (-0.2, source[1])
        target_control = (0.2, target[1])

        path = MatplotlibPath(
            [source, source_control, target_control, target],
            [
                MatplotlibPath.MOVETO,
                MatplotlibPath.CURVE4,
                MatplotlibPath.CURVE4,
                MatplotlibPath.CURVE4,
            ],
        )
        linewidth = 0.75 + 6 * (float(row[config.value]) / max_value)
        patch = PathPatch(
            path,
            facecolor="none",
            edgecolor="#9b51e0",
            linewidth=linewidth,
            alpha=0.35,
        )
        axis.add_patch(patch)
