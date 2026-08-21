"""Base interface for lookup providers."""
from typing import Optional, Dict, Any


class BaseLookupProvider:
    """Abstract base class for all character and dictionary lookup providers."""

    def lookup(self, char: str) -> Optional[Dict[str, Any]]:
        """Look up information for a single character."""
        raise NotImplementedError
