"""Register context-bound shared expansion providers without altering their mathematical rules."""
from __future__ import annotations

from typing import Callable

from phase165_r6_2_unified_registry_r3_r3.provider_registry import UnifiedExpansionProviderRegistry


def build_context_expansion_provider_registry(
    *, available: tuple[object, ...], prior_conclusions: tuple[object, ...],
    expand_registered_toda45_finite_cyclic_goal: Callable,
    expand_registered_eta_specialization: Callable,
    expand_registered_delta_image_goal: Callable,
    expand_cited_general_specialization: Callable,
) -> UnifiedExpansionProviderRegistry:
    """Preserve the four existing call signatures, order, and citation context."""
    if not isinstance(available, tuple) or not isinstance(prior_conclusions, tuple):
        raise TypeError("context statements must be tuples")
    registry = UnifiedExpansionProviderRegistry()
    specifications = (
        ("phase165_r57_r7_stable_expansion.expand_registered_toda45_finite_cyclic_goal",
         expand_registered_toda45_finite_cyclic_goal, available + prior_conclusions),
        ("phase165_r57_r8_eta_specialization.expand_registered_eta_specialization",
         expand_registered_eta_specialization, available),
        ("phase165_r57_r19_delta_image_backward.expand_registered_delta_image_goal",
         expand_registered_delta_image_goal, available),
        ("phase165_r57_r20_general_specialization.expand_cited_general_specialization",
         expand_cited_general_specialization, available),
    )
    for provider_id, function, statements in specifications:
        if not callable(function):
            raise TypeError("context expansion provider must be callable")
        def bound(goal: object, *, _function=function, _statements=statements):
            return _function(goal, _statements)
        registry.register(provider_id, bound, origin="SHARED_CITED_CONTEXT")
    return registry
