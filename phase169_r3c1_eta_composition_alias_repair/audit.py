"""R3C1: print actual citation-traced composite-image derivation or its blocker."""
from __future__ import annotations

import json
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "output"


def audit() -> dict:
    from homotopy_groups import TodaSuspensionIsomorphismStatement
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, shared_expansion_provider,
    )
    from phase165_r55_nk_only_goal import (
        registered_group_goal_candidates, search_group_from_registered_goal,
    )
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r12_r21_eta_generator_chain import expand_cited_eta_generator
    from phase165_r3_recursive_search import (
        RegisteredGoalUnresolved, reconstruct_registered_goal,
    )
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from proof import ProofRule

    bridge = build_shared_typed_bridge()
    contexts = []
    lower = search_group_from_registered_goal(n=2, k=2, bridge=bridge)
    upper = search_group_from_registered_goal(
        n=3, k=2, bridge=bridge, context_sink=contexts.append,
    )
    if not contexts:
        raise AssertionError("missing original screened pi5^3 context")
    context = contexts[-1]
    candidate_goals = registered_group_goal_candidates(bridge, n=3, k=2)
    if len(candidate_goals) != 1:
        raise AssertionError("pi5^3 unique registered group goal required")
    target = candidate_goals[0]
    citing_id = resolve_specialized_goal_citing_id(bridge, target)
    if citing_id is None:
        raise AssertionError("pi5^3 citation boundary not available")
    proposals = shared_expansion_provider(context, proof_target=target)(target)
    transport = tuple(item for item in proposals if item.rule.name ==
                      "finite cyclic presentation transported by proved suspension isomorphism")
    if len(transport) != 1:
        raise AssertionError("R3B unique transport candidate missing")
    source_goal, iso_goal, image_goal = transport[0].subgoals
    if not isinstance(image_goal, GeneratorImage):
        raise AssertionError("missing typed image goal")
    image_options = expand_cited_eta_generator(image_goal)
    result = {
        "lower_status": lower.status.value,
        "upper_status": upper.status.value,
        "upper_proven_steps": len(upper.proven_steps),
        "upper_open_goals": [type(g).__name__ for g in upper.open_goals],
        "source_goal": repr(source_goal),
        "iso_goal": repr(iso_goal),
        "image_goal": repr(image_goal),
        "composite_image_proposals": len(image_options),
        "component_witness_types": [type(x).__name__ for x in image_options[0].subgoals] if image_options else [],
        "target_citing_assertion": citing_id,
        "image_search_status": "not_searched",
        "image_search_diagnostic": None,
        "image_ancestor_given_types": [],
        "image_ancestor_inference_types": [],
    }
    if len(image_options) != 1 or len(image_options[0].subgoals) != 2:
        from toda_rules import toda_eta_family_definition_statement
        if hasattr(image_goal.source_generator, "left"):
            f = image_goal.source_generator.left
            expected = toda_eta_family_definition_statement(2).element
            result["actual_eta2_repr"] = repr(f)
            result["canonical_eta2_repr"] = repr(expected)
        return result
    observations = []
    try:
        proof = reconstruct_registered_goal(
            image_goal, context, citing_id,
            shared_expansion_provider(context, proof_target=image_goal),
            lookup_mode="typed_reference_publication",
            progress_observer=lambda event, goal, step: observations.append((event, goal, step)),
        )
    except RegisteredGoalUnresolved as error:
        result["image_search_status"] = "unresolved"
        result["image_search_diagnostic"] = str(error)
    else:
        if proof.conclusion != image_goal or proof.rule is not ProofRule.INFERENCE:
            raise AssertionError("composite image was not actually inferred")
        proven = [step for event, _, step in observations if event == "proved" and step is not None]
        if proof not in proven:
            raise AssertionError("final image proof missing from verified progress")
        if any(step.rule is ProofRule.GIVEN and
               isinstance(step.conclusion, (GeneratorImage, TodaSuspensionIsomorphismStatement))
               for step in proven):
            raise AssertionError("image or isomorphism was accepted as GIVEN")
        result["image_search_status"] = "proved"
        result["image_ancestor_given_types"] = [
            type(step.conclusion).__name__ for step in proven if step.rule is ProofRule.GIVEN
        ]
        result["image_ancestor_inference_types"] = [
            type(step.conclusion).__name__ for step in proven if step.rule is ProofRule.INFERENCE
        ]
    if lower.status is not ProofSearchStatus.COMPLETE:
        raise AssertionError("pi4^2 completed result regressed")
    return result


def main() -> int:
    result = audit()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    file = OUTPUT / "composite_image.json"
    file.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for key, value in result.items():
        print(f"{key.upper()}={value!r}")
    print("REPORT:", file)
    success = (result["composite_image_proposals"] == 1
               and result["component_witness_types"] == ["GeneratorSuspension", "GeneratorSuspension"]
               and result["image_search_status"] == "proved")
    print("R3C1_ACCEPTED_PROOF=" + str(success))
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
