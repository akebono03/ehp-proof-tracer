"""Read-only actual search/proposal audit of the current Phase 169 R3B frontier."""
from __future__ import annotations

import json
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "output"


def audit() -> dict:
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase166_r3aj_structured_generator import database_structured_group_goal_candidates
    from homotopy_groups import TodaSuspensionIsomorphismStatement
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r12_r24_web_search_connection import expand_finite_cyclic_relation

    bridge = build_shared_typed_bridge()
    lower_candidates = database_structured_group_goal_candidates(n=2, k=2)
    upper_candidates = database_structured_group_goal_candidates(n=3, k=2)
    if len(lower_candidates) != 1 or len(upper_candidates) != 1:
        raise AssertionError("unique lower/upper 2-stem goal metadata required")
    lower, upper = lower_candidates[0], upper_candidates[0]
    lower_contexts = []
    upper_contexts = []
    lower_result = search_group_from_registered_goal(
        n=2, k=2, bridge=bridge, context_sink=lower_contexts.append,
    )
    upper_result = search_group_from_registered_goal(
        n=3, k=2, bridge=bridge, context_sink=upper_contexts.append,
    )
    if not upper_contexts:
        raise AssertionError("actual upper Proof Search context missing")
    proposals = shared_expansion_provider(upper_contexts[-1], proof_target=upper)(upper)
    transport = tuple(
        option for option in proposals
        if option.rule.name == "finite cyclic presentation transported by proved suspension isomorphism"
    )
    source_proposal = expand_finite_cyclic_relation(upper)
    record = dict(
        lower_status=lower_result.status.value,
        upper_status=upper_result.status.value,
        upper_proven_steps=len(upper_result.proven_steps),
        upper_open_goals=[type(g).__name__ for g in upper_result.open_goals],
        upper_diagnostics=list(upper_result.diagnostics),
        source_goal_candidates=len(source_proposal),
        root_candidate_rules=[p.rule.name for p in proposals],
        transport_candidates=len(transport),
        transport_subgoals=[
            {"type": type(v).__name__, "repr": repr(v)}
            for option in transport for v in option.subgoals
        ],
        cited_iso_as_given=any(
            isinstance(link.step.conclusion, TodaSuspensionIsomorphismStatement)
            and bool(transport)
            and link.step.conclusion == transport[0].subgoals[1]
            for link in upper_contexts[-1].proof_links
            if link.step is not None
        ),
        cited_generator_image_as_given=any(
            isinstance(link.step.conclusion, GeneratorImage)
            and bool(transport)
            and link.step.conclusion == transport[0].subgoals[2]
            for link in upper_contexts[-1].proof_links
            if link.step is not None
        ),
    )
    if lower_result.status is not ProofSearchStatus.COMPLETE:
        raise AssertionError("previously completed lower group regressed")
    if upper_result.status is ProofSearchStatus.COMPLETE:
        raise AssertionError("this frontier-only phase must not claim full pi5^3 completion")
    if len(transport) != 1 or len(transport[0].subgoals) != 3:
        raise AssertionError("verified three-obligation transport candidate missing")
    if transport[0].subgoals[0] != lower:
        raise AssertionError("the lower group must remain a separately proved goal")
    if record["cited_iso_as_given"] or record["cited_generator_image_as_given"]:
        raise AssertionError("isomorphism or generator image must not be given facts")
    return record


def main() -> int:
    result = audit()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "frontier.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
    )
    for k, v in result.items():
        print(str(k).upper() + "=" + repr(v))
    print("REPORT: " + str(OUTPUT / "frontier.json"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
