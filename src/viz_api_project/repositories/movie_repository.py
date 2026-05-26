from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class MovieRepository(ABC):
    @abstractmethod
    def get_movies(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def get_genres(self) -> dict[int, str]:
        raise NotImplementedError
