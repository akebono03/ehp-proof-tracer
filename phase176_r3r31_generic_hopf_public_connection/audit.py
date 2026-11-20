"""Read-only proof-search probe after the additive R3R31 public hookup."""
from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import tempfile

from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication, Suspension
from map_facts import EHP_H_MAP
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase165_r3_recursive_search import RegisteredGoalUnresolved, reconstruct_registered_goal
from proof import ProofRule, Relation, RelationType
from phase176_r3r30_generic_hopf_substitution_isolated.source import generic_hopf_substitution_inputs


def probe() -> dict:
    nu = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    eta5 = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    eta6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    alpha = Composition(nu, eta6)
    suspension = Suspension(eta6)
    goal = Relation(
        MapApplication(EHP_H_MAP, Composition(alpha, suspension)),
        Composition(Composition(eta5, eta6), suspension),
        RelationType.EQUALITY,
    )
    bridge = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(bridge, n=3, k=5)
    if len(roots) != 1:
        raise RuntimeError("ROOT_NOT_UNIQUE")
    context = screen_independent_sources_for_derived_goal(bridge, goal=roots[0])
    provider = shared_expansion_provider(context, proof_target=roots[0])
    expansions = tuple(x for x in provider(goal)
                       if x.rule.name ==
                       "substitute independently proved Hopf value into cited right formula")
    if len(expansions) != 1:
        raise RuntimeError("EXPECTED_ONE_GENERAL_HOPF_SUBSTITUTION_CANDIDATE")
    inputs = generic_hopf_substitution_inputs(goal)
    if inputs is None or expansions[0].subgoals != inputs:
        raise RuntimeError("INCORRECT_HOPF_SUBGOALS")
    result = {
        "gate": "PASS_R3R31_PUBLIC_CANDIDATE_CONNECTED",
        "candidate_count": len(expansions),
        "subgoal_count": len(inputs),
        "subgoal_rule_names": [
            [item.rule.name for item in provider(child)]
            for child in inputs
        ],
        "root_rule_names": [item.rule.name for item in provider(roots[0])],
        "hopf_image_complete_claimed": False,
        "root_group_complete_claimed": False,
        "new_given": 0,
        "full_pytest": "NOT_RUN",
    }
    # A source ID provides a search context, not a forged group citation.
    matching_ids = [
        a.assertion_id for a in context.registry._assertions.values()
        if a.origin.value == "fixed_statement"
        and a.content in tuple(
            link.step.conclusion for link in context.proof_links if link.step is not None
        )
        and isinstance(a.assertion_id, str)
        and "right_hopf_formula" in a.assertion_id
    ]
    if matching_ids:
        try:
            step = reconstruct_registered_goal(
                goal, context, matching_ids[0], provider,
                lookup_mode="typed_reference",
            )
            result["complete_proof"] = step.rule is ProofRule.INFERENCE
            result["proved_step_rule"] = step.rule.value
        except RegisteredGoalUnresolved as exc:
            result["complete_proof"] = False
            result["unresolved_reason"] = str(exc)[:400]
    else:
        result["complete_proof"] = False
        result["unresolved_reason"] = "NO_SOURCE_CONTEXT_ID"
    return result


def main() -> int:
    try:
        result = probe()
    except Exception as exc:
        result = {"gate": "FAIL_R3R31_PUBLIC_AUDIT",
                  "error": type(exc).__name__ + ": " + str(exc),
                  "full_pytest": "NOT_RUN"}
    path = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
            / "EHPProofTracerAudit" / "phase176_r3r31_generic_hopf_public_connection")
    path.mkdir(parents=True, exist_ok=True)
    file = path / "public_report.json"
    file.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")
    for k,v in result.items():
        print("PHASE176_R3R31_" + k.upper() + "=" + str(v))
    print("PHASE176_R3R31_PUBLIC_REPORT=" + str(file))
    print("(END)")
    return 0 if result["gate"].startswith("PASS_") else 1


if __name__ == "__main__":
    sys.exit(main())
