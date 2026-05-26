from __future__ import annotations

from dataclasses import dataclass
from math import cos, pi, sin
import os
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", str(Path(".matplotlib-cache").resolve()))

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.path import Path as MatplotlibPath
from matplotlib.patches import PathPatch, Wedge

from viz_api_project.charts.common import ensure_columns, prepare_output_path


@dataclass(frozen=True)
class ChordDiagramConfig:
    source: str
    target: str
    value: str
    title: str
    output: str


def create_chord_diagram(dataframe: pd.DataFrame, config: ChordDiagramConfig) -> Path:
    ensure_columns(dataframe, [config.source, config.target, config.value])

    flows = (
        dataframe.groupby([config.source, config.target], as_index=False)[config.value]
        .sum()
        .query(f"{config.value} > 0")
    )
    nodes = sorted(set(flows[config.source]).union(flows[config.target]))
    if not nodes:
        raise ValueError("Nao existem fluxos positivos para gerar o diagrama de cordas.")

    angles = _node_angles(nodes)

    figure, axis = plt.subplots(figsize=(9, 9))
    axis.set_title(config.title)
    axis.set_aspect("equal")
    axis.axis("off")

    _draw_nodes(axis, nodes, angles)
    _draw_chords(axis, flows, angles, config)

    output_path = prepare_output_path(config.output)
    figure.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(figure)

    return output_path


def _node_angles(nodes: list[str]) -> dict[str, float]:
    step = 2 * pi / len(nodes)
    return {node: index * step for index, node in enumerate(nodes)}


def _draw_nodes(axis: plt.Axes, nodes: list[str], angles: dict[str, float]) -> None:
    radius = 1.0
    width = 0.05

    for node in nodes:
        angle = angles[node]
        degrees = angle * 180 / pi
        wedge = Wedge(
            center=(0, 0),
            r=radius,
            theta1=degrees - 7,
            theta2=degrees + 7,
            width=width,
            facecolor="#27ae60",
            edgecolor="white",
        )
        axis.add_patch(wedge)

        label_radius = 1.15
        x = label_radius * cos(angle)
        y = label_radius * sin(angle)
        axis.text(x, y, str(node), ha="center", va="center", fontsize=9)


def _draw_chords(
    axis: plt.Axes,
    flows: pd.DataFrame,
    angles: dict[str, float],
    config: ChordDiagramConfig,
) -> None:
    max_value = float(flows[config.value].max())

    for _, row in flows.iterrows():
        source_angle = angles[row[config.source]]
        target_angle = angles[row[config.target]]
        source = _point_on_circle(source_angle, radius=0.95)
        target = _point_on_circle(target_angle, radius=0.95)
        control = (0.0, 0.0)

        path = MatplotlibPath(
            [source, control, target],
            [MatplotlibPath.MOVETO, MatplotlibPath.CURVE3, MatplotlibPath.CURVE3],
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


def _point_on_circle(angle: float, radius: float) -> tuple[float, float]:
    return radius * cos(angle), radius * sin(angle)
