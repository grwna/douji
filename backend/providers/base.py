"""Base interface for lookup providers."""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class BaseLookupProvider(ABC):
    """Abstract base class for all character and dictionary lookup providers."""

    @abstractmethod
    def lookup(self, char: str) -> Optional[Dict[str, Any]]:
        """Look up information for a single character."""
