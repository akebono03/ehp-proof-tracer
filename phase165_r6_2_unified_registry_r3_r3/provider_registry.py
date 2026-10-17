"""Registry of callable expansion providers; no mathematical certification implied."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class RegisteredExpansionProvider:
    provider_id: str
    provider: Callable
    origin: str
    status: str = "CONNECTED_NOT_PROOF_VERIFIED"


class UnifiedExpansionProviderRegistry:
    def __init__(self) -> None:
        self._entries: dict[str, RegisteredExpansionProvider] = {}

    def register(self, provider_id: str, provider: Callable, *, origin: str,
                 status: str = "CONNECTED_NOT_PROOF_VERIFIED") -> None:
        if not isinstance(provider_id, str) or not provider_id:
            raise ValueError("provider_id must be nonempty")
        if not callable(provider):
            raise TypeError("provider must be callable")
        if not isinstance(origin, str) or not origin:
            raise ValueError("origin must be nonempty")
        if provider_id in self._entries:
            raise ValueError("duplicate provider_id: " + provider_id)
        self._entries[provider_id] = RegisteredExpansionProvider(provider_id, provider, origin, status)

    def entries(self) -> tuple[RegisteredExpansionProvider, ...]:
        return tuple(self._entries.values())

    def providers(self) -> tuple[Callable, ...]:
        return tuple(entry.provider for entry in self._entries.values())


def build_shared_expansion_provider_registry(
    *, expand_generic_iso_goal: Callable,
    expand_generic_ehp_hopf_goal: Callable,
    expand_delta_zero_from_suspension_iso: Callable,
    expand_diagonal_suspension: Callable,
    extra_providers: tuple = (),
) -> UnifiedExpansionProviderRegistry:
    if not isinstance(extra_providers, tuple):
        raise TypeError("extra_providers must be tuple")
    registry = UnifiedExpansionProviderRegistry()
    fixed = (
        ("phase165_r14_r6_generic_iso.expand_generic_iso_goal", expand_generic_iso_goal),
        ("phase165_r14_r9_ehp_exactness.expand_generic_ehp_hopf_goal", expand_generic_ehp_hopf_goal),
        ("phase165_r14_r11_delta_zero.expand_delta_zero_from_suspension_iso", expand_delta_zero_from_suspension_iso),
        ("phase165_r14_r14_diagonal_and_prop42.expand_diagonal_suspension", expand_diagonal_suspension),
    )
    for provider_id, provider in fixed:
        registry.register(provider_id, provider, origin="SHARED_FIXED")
    for index, provider in enumerate(extra_providers):
        registry.register("caller.extra_provider.{}".format(index), provider, origin="CALLER_EXPLICIT")
    return registry
