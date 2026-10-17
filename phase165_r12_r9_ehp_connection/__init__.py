"""R12-R9 read-only exactness source audit.

No document, proof leaf, inference rule, or target structure is created.
The caller must supply an already R7-screened bridge.
"""
from __future__ import annotations

from dataclasses import dataclass

from phase163_r4_registry_bridge import RegistryBridgeResult
from proof import ProofRule
from toda_rules import TodaProp42ExactnessStatement
from unified_statement_registry import AssertionOrigin


@dataclass(frozen=True)
class ExactnessWindowWitness:
    assertion_id: str
    first_map: object
    second_map: object
    source_term: object
    middle_term: object
    target_term: object


def collect_screened_exactness_windows(
    bridge: RegistryBridgeResult,
) -> tuple[ExactnessWindowWitness, ...]:
    """Inspect exactly the existing, citation-screened typed GIVEN steps.

    Never infer that a window is exact from its maps alone; the typed,
    provenance-consistent citation must already be in the passed bridge.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    results: list[ExactnessWindowWitness] = []
    seen: set[str] = set()
    for link in bridge.proof_links:
        if link.assertion_id in seen:
            raise ValueError("ambiguous repeated proof link")
        seen.add(link.assertion_id)
        assertion = bridge.registry.assertion(link.assertion_id)
        step = link.step
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        if step is None or step.rule is not ProofRule.GIVEN:
            continue
        if step.conclusion != assertion.content or step.premises:
            raise ValueError("inconsistent fixed source proof link")
        if not isinstance(step.conclusion, TodaProp42ExactnessStatement):
            continue
        window = step.conclusion.window
        results.append(ExactnessWindowWitness(
            assertion_id=link.assertion_id,
            first_map=window.first_map,
            second_map=window.second_map,
            source_term=window.source_term,
            middle_term=window.middle_term,
            target_term=window.target_term,
        ))
    return tuple(results)


def classify_ehp_exactness_windows(
    witnesses: tuple[ExactnessWindowWitness, ...],
) -> dict[str, tuple[ExactnessWindowWitness, ...]]:
    """Classify cited windows by their actual pair of typed map symbols."""
    if not isinstance(witnesses, tuple) or any(
        not isinstance(item, ExactnessWindowWitness) for item in witnesses
    ):
        raise TypeError("witnesses must be typed exactness windows")
    from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP

    delta_e = tuple(w for w in witnesses if
                    w.first_map == EHP_DELTA_MAP and w.second_map == EHP_E_MAP)
    e_h = tuple(w for w in witnesses if
                w.first_map == EHP_E_MAP and w.second_map == EHP_H_MAP)
    h_delta = tuple(w for w in witnesses if
                    w.first_map == EHP_H_MAP and w.second_map == EHP_DELTA_MAP)
    return {"delta_e": delta_e, "e_h": e_h, "h_delta": h_delta}
