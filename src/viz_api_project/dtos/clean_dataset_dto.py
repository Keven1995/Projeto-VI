from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd


@dataclass(frozen=True)
class CleanDatasetDTO:
    dataframe: pd.DataFrame
    source: str
    records_count: int
    columns: tuple[str, ...]
    metadata: dict[str, str | int | float | bool] = field(default_factory=dict)

    @classmethod
    def from_dataframe(
        cls,
        dataframe: pd.DataFrame,
        *,
        source: str,
        metadata: dict[str, str | int | float | bool] | None = None,
    ) -> "CleanDatasetDTO":
        return cls(
            dataframe=dataframe,
            source=source,
            records_count=len(dataframe),
            columns=tuple(dataframe.columns),
            metadata=metadata or {},
        )
