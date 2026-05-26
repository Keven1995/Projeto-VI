from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd


class ChartStrategy(ABC):
    @abstractmethod
    def create(self, dataframe: pd.DataFrame) -> Path:
        raise NotImplementedError
