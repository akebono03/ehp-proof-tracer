"""Verify live R3-R6 source-ancestry, independent inferences, root status."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile

from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r3_recursive_search import RegisteredGoalUnresolved, reconstruct_registered_goal
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r2_search_adapter import search_registered_partial_proof
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase174_r3_r5_finite_cyclic_extension.rule import Toda48UniversalConditionalStatement
from phase174_r3_r6_source_extension.patch import (
    PREFLIGHT,
    R3R4_TEST,
    R3R5_TEST,
    SHARED,
    connect_shared,
    replace_preflight_audit,
    replace_r3r4_test,
    replace_r3r5_test,
    reviewed_originals,
)
from phase174_r3_r6_source_extension.source import (
    Toda55UniversalDoubleStatement,
    verify_extension_texts,
)
from proof import ProofRule


def _leaves(step) -> tuple[object, ...]:
    """Return all cited GIVEN conclusions under a proved inference step."""
    if step.rule is ProofRule.GIVEN:
        return (step.conclusion,)
    result = []
    for premise in step.premises:
        result.extend(_leaves(premise))
    return tuple(result)


def audit() -> dict[str, object]:
    reviewed = reviewed_originals()
    changes = {
        SHARED: connect_shared,
        R3R4_TEST: replace_r3r4_test,
        R3R5_TEST: replace_r3r5_test,
        PREFLIGHT: replace_preflight_audit,
    }
    if any(Path(path).read_bytes() != transform(reviewed[path])
           for path, transform in changes.items()):
        raise ValueError("Unexpected source patch or test content")
    positions = dict(verify_extension_texts())
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=5, k=3)
    if len(goals) != 1:
        raise ValueError("Public target is not uniquely registered")
    target = goals[0]
    citing = resolve_specialized_goal_citing_id(bridge, target)
    if citing is None:
        raise ValueError("Target source order is missing")
    screened = prefer_universal_prop42_derivation(screen_shared_proof_context(
        bridge, goal=target, citing_assertion_id=citing,
        explicit_publication_target=True,
    ))
    available = tuple(link.step.conclusion for link in screened.proof_links
                      if link.step is not None and link.step.rule is ProofRule.GIVEN)
    if available.count(Toda48UniversalConditionalStatement()) != 1:
        raise ValueError("Toda (4.8) general reference missing or duplicated")
    if available.count(Toda55UniversalDoubleStatement()) != 1:
        raise ValueError("Toda (5.5) general reference missing or duplicated")
    provider = shared_expansion_provider(screened, proof_target=target)
    cyclic = CyclicStructureStatement(target.lhs, target.rhs.generator, target.rhs.order)
    proposals = tuple(p for p in provider(cyclic) if p.rule.name ==
                      "finite cyclic extension by an index-two injective image")
    if len(proposals) != 1:
        raise ValueError("R3-R5 generic cyclic extension proposal changed")
    index, prior, doubled = proposals[0].subgoals
    if index in available or prior in available and prior == target or doubled in available or target in available:
        raise ValueError("A derived conclusion was promoted to a direct reference")
    index_step = reconstruct_registered_goal(
        index, screened, citing, provider, lookup_mode="typed_reference",
    )
    if index_step.rule is not ProofRule.INFERENCE or (
        Toda48UniversalConditionalStatement() not in _leaves(index_step)
    ):
        raise ValueError("Toda (4.8) index-two claim lacks certified source ancestry")
    doubled_step = reconstruct_registered_goal(
        doubled, screened, citing, provider, lookup_mode="typed_reference",
    )
    if doubled_step.rule is not ProofRule.INFERENCE or (
        Toda55UniversalDoubleStatement() not in _leaves(doubled_step)
    ):
        raise ValueError("Toda (5.5) double lacks independently certified source ancestry")
    try:
        prior_step = reconstruct_registered_goal(
            prior, screened, citing, provider, lookup_mode="typed_reference",
        )
    except RegisteredGoalUnresolved:
        prior_step = None
    partial = search_registered_partial_proof(
        n=5, k=3, goal=target, bridge=screened,
        citing_assertion_id=citing, expansion_provider=provider,
        lookup_mode="typed_reference",
    )
    certified = partial.status.value == "complete"
    if certified and not any(
        s.rule is ProofRule.INFERENCE and s.conclusion == target
        for s in partial.proven_steps
    ):
        raise ValueError("Complete status without a verified group root")
    if any(link.step is not None and link.step.rule is ProofRule.GIVEN
           and link.step.conclusion == target for link in screened.proof_links):
        raise ValueError("The target was incorrectly registered as GIVEN")
    return {
        "phase": "174-R3-R6",
        "reviewed_source_positions": positions,
        "registered_universal_source_given": 2,
        "registered_direct_group_given": 0,
        "toda48_index_two_step": "INFERENCE",
        "toda48_ancestry_cited": True,
        "toda55_double_step": "INFERENCE",
        "toda55_ancestry_cited": True,
        "prior_group_obligation_proved": prior_step is not None,
        "prior_group_proof_rule": prior_step.rule.value if prior_step is not None else None,
        "root_search_status": partial.status.value,
        "root_proven_step_count": len(partial.proven_steps),
        "root_open_goal_types": [type(g).__name__ for g in partial.open_goals],
        "root_complete_verified": certified,
        "web_narrative_complete_checked": False,
        "new_group_specific_rules": 0,
        "full_pytest_performed": False,
    }


def main() -> int:
    result = audit()
    folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    folder = folder / "EHPProofTracerAudit" / "phase174_r3_r6"
    folder.mkdir(parents=True, exist_ok=True)
    destination = folder / "audit.json"
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print("PHASE174_R3R6_CITED_UNIVERSAL_GIVENS=2")
    print("PHASE174_R3R6_NEW_GROUP_GIVEN=0")
    print("PHASE174_R3R6_TODA48_INDEX_INFERRED=True")
    print("PHASE174_R3R6_TODA55_DOUBLE_INFERRED=True")
    print("PHASE174_R3R6_PRIOR_PROVED=" + str(result["prior_group_obligation_proved"]))
    print("PHASE174_R3R6_ROOT_STATUS=" + result["root_search_status"])
    print("PHASE174_R3R6_ROOT_PROVEN_STEPS=" + str(result["root_proven_step_count"]))
    print("PHASE174_R3R6_ROOT_COMPLETE=" + str(result["root_complete_verified"]))
    print("PHASE174_R3R6_REPORT=" + str(destination))
    print("PHASE174_R3R6_SOURCE_ANCESTRY_GATE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
