"""Abstractions for a word repository."""

from abc import ABC, abstractmethod
from typing import List

from word import Word

class WordRepo(ABC):
    """An interface for a word repository."""

    @abstractmethod
    def get_by_prefix(self, prefix: str) -> List[Word]:
        """Lookup words with a given prefix."""
        pass
