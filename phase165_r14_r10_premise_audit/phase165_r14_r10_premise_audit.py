"""R14-R10: source-backed proof-obligation audit, not a proof-leaf promoter."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

from homotopy_groups import TodaPrimaryGroupZeroStatement
from phase165_r14_r9_ehp_exactness import (
    expand_generic_ehp_hopf_goal,
)
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase165_r2_registry_lookup import find_eligible_goal_candidates
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from homotopy_groups import TodaPrimaryGroup, TodaHopfInvariantMap

@dataclass(frozen=True)
class ObligationAudit:
    label: str
    statement: object
    expected_reference: str
    source_text_found: bool
    registered_exact_matches: int
    proof_eligible: bool
    reason: str

def audit_pi32_premises(bridge=None) -> tuple[ObligationAudit, ...]:
    if bridge is None:
        bridge, _ = build_phase165_r5_manifest_bridge()
    h = TodaHopfInvariantMap(TodaPrimaryGroup(3,2), TodaPrimaryGroup(3,3))
    inj = expand_generic_ehp_hopf_goal(MapInjective(h))
    surj = expand_generic_ehp_hopf_goal(MapSurjective(h))
    if len(inj) != 1 or len(surj) != 1:
        raise ValueError("expected unique R14-R9 expansions")
    inj_zero, ehp_inj = inj[0].subgoals
    delta_zero, ehp_surj = surj[0].subgoals
    if not isinstance(inj_zero, TodaPrimaryGroupZeroStatement):
        raise TypeError("missing typed zero group")
    assertions = tuple(bridge.registry._assertions.values())
    source51 = tuple(a for a in assertions if a.reference_id == "phase163:archive:toda:(5.1)")
    source51_text = "\n".join(
        a.content.get("source_text", "")
        for a in source51 if isinstance(a.content, dict)
    )
    # The adopted TeX archive includes the numbered (5.1) environment.
    # No original-edition semantics are inferred from this token check.
    has_pi1 = "\\pi^{1}_{i}=0" in source51_text
    obligations = (
        ("pi2_1_zero", inj_zero, "(5.1)", has_pi1,
         "Typed specialization i=2>1 is available only as source candidate; no certified ProofStepLink"),
        ("ehp_e_h_exactness", ehp_inj, "Proposition 4.2", False,
         "E-H exactness window not certified or connected to reviewed source"),
        ("delta_zero", delta_zero, "UNRESOLVED", False,
         "Delta=0 is NOT implied by pi_1^1=Z; requires independent argument"),
        ("ehp_h_delta_exactness", ehp_surj, "Proposition 4.2", False,
         "H-Delta exactness window not certified or connected to reviewed source"),
    )
    results = []
    for label, statement, ref, evidence, reason in obligations:
        exact = tuple(
            a for a in assertions if type(a.content) is type(statement) and a.content == statement
        )
        results.append(ObligationAudit(
            label, statement, ref, evidence, len(exact), False, reason
        ))
    return tuple(results)

def audit_summary(bridge=None) -> dict:
    results = audit_pi32_premises(bridge)
    return {
        "phase": "165 R14-R10",
        "goal": "pi_3^2 = Z{eta_2}",
        "obligations": [
            {
                "label": r.label,
                "statement": repr(r.statement),
                "reference_candidate": r.expected_reference,
                "source_text_found": r.source_text_found,
                "exact_registry_matches": r.registered_exact_matches,
                "proof_eligible": r.proof_eligible,
                "reason": r.reason,
            } for r in results
        ],
        "certified_new_leaves": 0,
        "proof_steps_created": 0,
        "legacy_proof_used": False,
        "full_pytest_run": False,
        "status": "FOUR_PREMISES_AUDITED_NOT_CERTIFIED",
    }
