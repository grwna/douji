"""Lookup engine coordinating pluggable lookup providers."""
from typing import Optional, Dict, Any, List
from .providers.base import BaseLookupProvider
from .providers.variant_provider import VariantMappingProvider


class LookupEngine:
    """Main lookup coordinator supporting multiple pluggable data providers."""

    def __init__(self, providers: Optional[List[BaseLookupProvider]] = None):
        if providers is None:
            self.providers: List[BaseLookupProvider] = [VariantMappingProvider()]
        else:
            self.providers = list(providers)

    def register_provider(self, provider: BaseLookupProvider) -> None:
        self.providers.append(provider)

    def lookup(self, char: str) -> Optional[Dict[str, Any]]:
        if not char:
            return None

        result: Optional[Dict[str, Any]] = None

        for provider in self.providers:
            res = provider.lookup(char)
            if res:
                if result is None:
                    result = dict(res)
                else:
                    # Merge auxiliary fields if returned by extra providers
                    for k, v in res.items():
                        if k not in result or not result[k]:
                            result[k] = v

        return result
