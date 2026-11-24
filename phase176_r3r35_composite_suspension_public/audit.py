"""Read-only, source-screened public frontier and local inference replay."""
from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import tempfile

PACKAGE = "phase176_r3r35_composite_suspension_public"
RULE_NAME = "proved composite suspension image yields typed element equality"


def probe() -> dict:
    from expression import Composition, GeneratorSymbol, HomotopyElement, Suspension
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase176_r3r34_composite_suspension_isolated.source import (
        composite_suspension_equality_input,
    )
    from proof import Relation, RelationType, ProofRule, find_inference_match, apply_inference_match

    eta5 = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    eta6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    eta7 = HomotopyElement("η₇", 7, 8, 7, GeneratorSymbol("η", index=7))
    goal = Relation(
        Suspension(Composition(eta5, eta6)),
        Composition(eta6, eta7), RelationType.EQUALITY,
    )
    image = composite_suspension_equality_input(goal)
    if image is None:
        raise RuntimeError("INVALID_TYPED_COMPOSITE_SUSPENSION_GOAL")
    bridge = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(bridge, n=3, k=5)
    if len(roots) != 1:
        raise RuntimeError("ROOT_NOT_UNIQUE")
    screened = screen_independent_sources_for_derived_goal(bridge, goal=roots[0])
    provider = shared_expansion_provider(screened, proof_target=roots[0])
    candidates = tuple(item for item in provider(goal) if item.rule.name == RULE_NAME)
    if len(candidates) != 1 or candidates[0].subgoals != (image,):
        raise RuntimeError("PUBLIC_COMPOSITE_SUSPENSION_CANDIDATE_NOT_CONNECTED")

    # Explicitly replay only the locally available definitional inference chain.
    # This is not an assertion that DFS's source-order/citation gate has passed.
    image_options = provider(image)
    replayed = False
    replay_rules = []
    for option in image_options:
        if option.subgoals:
            continue
        first_match = find_inference_match(option.rule, ())
        if first_match is None:
            continue
        first_step = apply_inference_match(first_match)
        if first_step.rule is not ProofRule.INFERENCE or first_step.conclusion != image:
            continue
        second_match = find_inference_match(candidates[0].rule, (first_step,))
        if second_match is None:
            continue
        second_step = apply_inference_match(second_match)
        if (second_step.rule is ProofRule.INFERENCE
                and second_step.conclusion == goal
                and second_step.premises == (first_step,)):
            replayed = True
            replay_rules = [option.rule.name, candidates[0].rule.name]
            break
    return {
        "gate": "PASS_R3R35_PUBLIC_BRANCH_CONNECTED",
        "public_candidate_count": len(candidates),
        "public_subgoal_count": len(candidates[0].subgoals),
        "image_candidate_rules": [item.rule.name for item in image_options],
        "isolated_inference_replayed": replayed,
        "isolated_replay_rules": replay_rules,
        "source_screened_context_used": True,
        "shared_dfs_source_order_gate_verified": False,
        "hopf_image_proved": False,
        "root_group_proved": False,
        "new_given": 0,
        "full_pytest": "NOT_RUN",
    }


def main() -> int:
    try:
        result = probe()
    except Exception as error:
        result = {
            "gate": "FAIL_R3R35_PUBLIC_AUDIT",
            "error": type(error).__name__ + ": " + str(error),
            "full_pytest": "NOT_RUN",
        }
    folder = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
              / "EHPProofTracerAudit" / PACKAGE)
    folder.mkdir(parents=True, exist_ok=True)
    destination = folder / "public_report.json"
    destination.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    for key, value in result.items():
        print("PHASE176_R3R35_" + key.upper() + "=" + str(value))
    print("REPORT=" + str(destination))
    return 0 if result["gate"].startswith("PASS_") else 1


if __name__ == "__main__":
    sys.exit(main())
