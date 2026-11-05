"""Read-only post-patch gate: real screened proposals, not invented evidence."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile

from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase174_r3_r5_finite_cyclic_extension.patch import (
    SHARED, TEST, PREFLIGHT, insert_shared, replace_r3r4_test,
    replace_preflight_provider_guard, git,
)
from proof import ProofRule
from toda_rules import TodaDeltaZeroStatement


def audit() -> dict[str, object]:
    """A proposal route is not a completed proof; preserve this distinction."""
    if (Path(SHARED).read_bytes() != insert_shared(git("show", "HEAD:" + SHARED))
            or Path(TEST).read_bytes() != replace_r3r4_test(git("show", "HEAD:" + TEST))
            or Path(PREFLIGHT).read_bytes() != replace_preflight_provider_guard(Path(PREFLIGHT).read_bytes())):
        raise ValueError("Production source or regression test is not reviewed")
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=5, k=3)
    if len(goals) != 1:
        raise ValueError("Unexpected public target count")
    target = goals[0]
    citing = resolve_specialized_goal_citing_id(bridge, target)
    if citing is None:
        raise ValueError("Publication position is missing")
    screened = prefer_universal_prop42_derivation(screen_shared_proof_context(
        bridge, goal=target, citing_assertion_id=citing,
        explicit_publication_target=True,
    ))
    provider = shared_expansion_provider(screened, proof_target=target)
    cyclic = CyclicStructureStatement(target.lhs, target.rhs.generator, target.rhs.order)
    cyclic_options = tuple(
        x for x in provider(cyclic)
        if x.rule.name == "finite cyclic extension by an index-two injective image"
    )
    if len(cyclic_options) != 1:
        raise ValueError("Typed cyclic root is not uniquely expanded")
    index, prior, doubled = cyclic_options[0].subgoals
    index_options = tuple(
        x for x in provider(index)
        if x.rule.name == "Toda (4.8) conditional index-two double suspension"
    )
    if len(index_options) != 1:
        raise ValueError("Conditional Toda (4.8) expansion is missing")
    delta, theorem = index_options[0].subgoals
    expected = TodaDeltaZeroStatement(TodaDeltaMap(
        TodaPrimaryGroup(7, 7), TodaPrimaryGroup(5, 3),
    ))
    if delta != expected:
        raise ValueError("Root branch is not the reviewed Delta-zero condition")
    if any(
        link.step is not None and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == theorem
        for link in screened.proof_links
    ):
        raise ValueError("The unaudited general theorem was directly GIVEN")
    # Prove Delta by the ordinary citation-screened provider, independently
    # of whether all sibling obligations can be proved in this R3-R5 stage.
    inferred_delta = reconstruct_registered_goal(
        delta, screened, citing, provider, lookup_mode="typed_reference",
    )
    if inferred_delta.rule is not ProofRule.INFERENCE or inferred_delta.conclusion != delta:
        raise ValueError("An inferred Delta-zero ProofStep was not reconstructed")
    from phase165_r52_r2_search_adapter import search_registered_partial_proof
    partial = search_registered_partial_proof(
        n=5, k=3, goal=target, bridge=screened,
        citing_assertion_id=citing, expansion_provider=provider,
        lookup_mode="typed_reference",
    )
    rooted_delta = any(s.conclusion == delta and s.rule is ProofRule.INFERENCE
                       for s in partial.proven_steps)
    return {
        "phase": "174-R3-R5-IMPL",
        "mode": "SOURCE_CONDITIONAL_CYCLIC_BACKWARD_EXPANSION",
        "root_goal_type": type(target).__name__,
        "cyclic_goal_type": type(cyclic).__name__,
        "root_to_cyclic_proposals": len(cyclic_options),
        "cyclic_to_toda48_proposals": len(index_options),
        "delta_proposal_count": len(provider(delta)),
        "public_delta_independently_proved": True,
        "root_search_status": partial.status.value,
        "root_proven_steps": len(partial.proven_steps),
        "rooted_delta_in_partial_steps": rooted_delta,
        "new_source_theorem_registered": False,
        "root_group_completed_by_this_stage": partial.status.value == "complete",
        "source_citation_registration_missing": True,
        "double_relation_inference_still_required": True,
        "new_given": 0,
        "full_pytest_performed": False,
        "existing_files_modified": [SHARED, TEST, PREFLIGHT],
    }


def main() -> int:
    result = audit()
    if result["root_group_completed_by_this_stage"]:
        raise ValueError("Unexpected conclusion: unregistered source theorem supplied")
    folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    folder = folder / "EHPProofTracerAudit" / "phase174_r3_r5_impl"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "audit.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE174_R3R5_IMPL_CYCLIC_PROPOSALS=" + str(result["root_to_cyclic_proposals"]))
    print("PHASE174_R3R5_IMPL_TODA48_PROPOSALS=" + str(result["cyclic_to_toda48_proposals"]))
    print("PHASE174_R3R5_IMPL_DELTA_INFERRED=" + str(result["public_delta_independently_proved"]))
    print("PHASE174_R3R5_IMPL_ROOT_STATUS=" + result["root_search_status"])
    print("PHASE174_R3R5_IMPL_ROOT_PROVEN_STEPS=" + str(result["root_proven_steps"]))
    print("PHASE174_R3R5_IMPL_ROOTED_DELTA=" + str(result["rooted_delta_in_partial_steps"]))
    print("PHASE174_R3R5_IMPL_NEW_GIVEN=0")
    print("PHASE174_R3R5_IMPL_GROUP_COMPLETE=False")
    print("PHASE174_R3R5_IMPL_REPORT=" + str(path))
    print("PHASE174_R3R5_IMPL_MATH_GATE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
