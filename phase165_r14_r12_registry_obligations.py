"""R14-R12: typed exactness source candidates and missing E-iso derivation.

No citations or proof leaves are approved by mapping alone.
"""
from __future__ import annotations
from dataclasses import dataclass
from homotopy_groups import (
    TodaDeltaMap, TodaPrimaryGroup, TodaSuspensionMap,
    TodaSuspensionIsomorphismStatement,
)
from phase165_r14_r11_delta_zero import expand_delta_zero_from_suspension_iso
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from unified_statement_registry import AssertionInstantiation


@dataclass(frozen=True)
class UncertifiedPremiseBinding:
    label: str
    goal: object
    source_locator: str | None
    source_assertion_ids: tuple[str, ...]
    origin: str
    status: str = "NOT_PROOF_ELIGIBLE"


def bind_delta_zero_obligations(bridge) -> tuple[UncertifiedPremiseBinding, ...]:
    delta = TodaDeltaMap(TodaPrimaryGroup(3, 3), TodaPrimaryGroup(1, 1))
    expansions = expand_delta_zero_from_suspension_iso(
        __import__('toda_rules').TodaDeltaZeroStatement(delta)
    )
    if len(expansions) != 1:
        raise ValueError("expected one delta zero expansion")
    e_iso, delta_e_exact = expansions[0].subgoals
    expected = TodaSuspensionIsomorphismStatement(
        TodaSuspensionMap(TodaPrimaryGroup(1, 1), TodaPrimaryGroup(2, 2))
    )
    if e_iso != expected:
        raise ValueError("unexpected E isomorphism")
    reference_candidates = tuple(
        ref for ref in bridge.registry._references.values()
        if ref.locator in ("Proposition 4.2", "Prop.4.2", "(4.2)")
    )
    ids = tuple(
        a.assertion_id for a in bridge.registry._assertions.values()
        if a.reference_id in {ref.reference_id for ref in reference_candidates}
        and a.assertion_id.startswith("phase163:archive:")
    )
    return (
        UncertifiedPremiseBinding(
            "E_pi11_pi22_isomorphism", e_iso, None, (),
            "DERIVED_GOAL_REQUIRES_INDEPENDENT_SUSPENSION_THEOREM",
        ),
        UncertifiedPremiseBinding(
            "Delta_E_exactness", delta_e_exact,
            "Proposition 4.2", ids,
            "TODA_ARCHIVE_SOURCE_ONLY" if ids else "NO_ARCHIVED_SOURCE_MATCH",
        ),
    )


def audit_r12(bridge=None) -> dict:
    if bridge is None:
        bridge, _ = build_phase165_r5_manifest_bridge()
    rows = bind_delta_zero_obligations(bridge)
    return {
        "phase": "165 R14-R12",
        "status": "TYPED_OBLIGATIONS_BOUND_BUT_NOT_CERTIFIED",
        "obligation_count": len(rows),
        "obligations": [
            {"label": item.label, "goal": repr(item.goal),
             "source_locator": item.source_locator,
             "source_assertion_ids": list(item.source_assertion_ids),
             "origin": item.origin, "status": item.status}
            for item in rows
        ],
        "registered_proof_eligible": 0,
        "toda_proof_steps_created": 0,
        "pi32_proved": False,
        "full_pytest_run": False,
    }
