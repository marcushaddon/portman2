"""Abstractions for a word repository."""

from abc import ABC, abstractmethod
from typing import List

from word import Word

class WordRepo(ABC):
    """An interface for a word repository."""

    @abstractmethod
    def get_random_by_prefix(self, prefix: str) -> Word:
        """Lookup words with a given prefix."""
        pass
    
    @abstractmethod
    def get_random(self) -> Word:
        """Get random word."""
        pass
    
    @abstractmethod
    def lookup(self, word: str) -> Word:
        """Look up a word."""
        pass
