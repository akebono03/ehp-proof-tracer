"""Read-only canonical-search audit of E(pi_10^5)=0 versus pi_10^5=0.

This probe deliberately restricts the search to an inspected R43/R41/R38
backward branch. It never claims to exercise every Web branch or the HTTP UI.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r44_public_zero_image_tree_frontier.source_guard import verify_checkout


def inspected_frontier() -> dict[str, object]:
    """Observe genuine canonical steps, without manually installing a proof."""
    from expression import Zero
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from map_property_rules import ImageZeroStatement
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r2_search_adapter import search_registered_partial_proof
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from phase169_r10e4_ordered_db_prior.db_prior import admitted_db_step, verified_db_step
    from phase169_r10e5_composite_generator_image.rule import (
        component_image_obligations, expand_composite_generator_image,
    )
    from phase169_r10eq_r1_universal_stable_definition.definition import expand_defined_stable_element_image
    from phase174_r3_r7_r3_ehp_zero_rule.rule import RULE_NAME as EHP_RULE, ehp_zero_inputs
    from phase174_r3_r7_r5_zero_image_hopf_injective.rule import RULE_NAME as HOPF_RULE, hopf_injectivity_from_zero_image_inputs
    from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import RULE_NAME as UPPER_RULE, upper_delta_surjectivity_inputs
    from phase174_r3_r7_r40_adopted_db_zero_image_isolated.rule import RULE_NAME as ZERO_IMAGE_RULE
    from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.provider import screened_general_law
    from phase174_r3_r7_r38_source_bound_zero_image_public_wiring.provider import (
        left_associated, lifted_stable_composition,
    )
    from phase174_r3_r7_r9_composition_associativity.rule import expand_generator_image_associativity
    from phase174_r3_r7_r7_composite_zero_audit.rule import expand_generator_zero_from_composite
    from phase174_r3_r7_r12_toda59_annihilator_source.rule import expand_cited_annihilator_specialization
    from phase165_r14_r6_generic_iso import GeneratorImage
    from proof import ProofRule, ProofStep, Relation, RelationType

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    laws = screened_general_law(bridge)
    if len(laws) != 1:
        raise RuntimeError("Required independently cited Toda (5.9) source not screened")
    citation_ids = tuple(
        link.assertion_id for link in bridge.proof_links
        if isinstance(link.step, ProofStep)
        and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == laws[0]
    )
    if len(citation_ids) != 1:
        raise RuntimeError("Cited source lacks exactly one concrete proof link")
    public = shared_expansion_provider(bridge, proof_target=root)
    root_inputs = ehp_zero_inputs(root)
    upper = root_inputs[0]
    upper_inputs = upper_delta_surjectivity_inputs(upper)
    hopf = upper_inputs[0]
    hopf_inputs = hopf_injectivity_from_zero_image_inputs(hopf)
    zero_image = hopf_inputs[0]
    if type(zero_image) is not ImageZeroStatement:
        raise RuntimeError("Hopf injectivity requires zero-image, not zero-group")

    def single_public(goal, name, expected):
        options = tuple(
            item for item in public(goal)
            if item.rule.name == name and item.subgoals == expected
        )
        if len(options) != 1:
            raise RuntimeError("Reviewed R43 public provider disappeared or became ambiguous: " + name)
        return options[0]

    root_exp = single_public(root, EHP_RULE, root_inputs)
    upper_exp = single_public(upper, UPPER_RULE, upper_inputs)
    hopf_exp = single_public(hopf, HOPF_RULE, hopf_inputs)
    candidates = tuple(x for x in public(zero_image) if x.rule.name == ZERO_IMAGE_RULE)
    if len(candidates) != 1 or len(candidates[0].subgoals) != 2:
        raise RuntimeError("R41 source-bound zero-image option missing")
    image_exp = candidates[0]
    prior, zero_generator_goal = image_exp.subgoals
    db_step = admitted_db_step(prior, proof_target=root, bridge=bridge)
    if (db_step is None or db_step.rule is not ProofRule.GIVEN
            or not verified_db_step(db_step, proof_target=root, bridge=bridge)):
        raise RuntimeError("Source-first DB prior trust boundary did not validate")
    if zero_image.map.source_group != prior.lhs:
        raise RuntimeError("Cyclic prior group does not match suspension domain")
    false_zero_group = TodaPrimaryGroupZeroStatement(prior.lhs)
    if false_zero_group == zero_image:
        raise RuntimeError("A zero-group and zero-image statement were conflated")
    if any(step.conclusion == false_zero_group for step in (db_step,)):
        raise RuntimeError("DB adopted prior incorrectly asserts group is zero")
    if any(false_zero_group in item.subgoals for item in (root_exp, upper_exp, hopf_exp, image_exp)):
        raise RuntimeError("The selected R41 chain acquired an incorrect zero-group premise")
    right = lifted_stable_composition(prior.rhs.generator)
    left = left_associated(right) if right is not None else None
    if left is None:
        raise RuntimeError("R38 composite cannot be lifted and reassociated")
    left_goal = GeneratorImage(zero_image.map, prior.rhs.generator, left)
    right_goal = GeneratorImage(zero_image.map, prior.rhs.generator, right)
    annihilator = Relation(left.left, Zero(), RelationType.EQUALITY)
    parts = component_image_obligations(right_goal)
    if parts is None or len(parts) != 2:
        raise RuntimeError("Wrong number of defined composition-image obligations")

    requested = (
        (zero_generator_goal, expand_generator_zero_from_composite(zero_generator_goal, left_goal)),
        (left_goal, expand_generator_image_associativity(left_goal)),
        (right_goal, expand_composite_generator_image(right_goal)),
        (annihilator, expand_cited_annihilator_specialization(annihilator, laws)),
    ) + tuple((part, expand_defined_stable_element_image(part)) for part in parts)
    selected = [(root, (root_exp,)), (upper, (upper_exp,)),
                (hopf, (hopf_exp,)), (zero_image, (image_exp,))]
    stages = {}
    for typed_goal, expected_options in requested:
        seen = public(typed_goal)
        matches = tuple(
            item for item in seen
            if any(item.rule.name == expected.rule.name
                   and item.subgoals == expected.subgoals
                   for expected in expected_options)
        )
        name = type(typed_goal).__name__
        stages[name] = stages.get(name, []) + [{
            "matching_public_options": len(matches),
            "isolated_options": len(expected_options),
        }]
        # An absent or ambiguous stage is a reported open goal, not a proof.
        selected.append((typed_goal, matches if len(matches) == 1 else ()))

    def scoped(goal):
        for candidate, options in selected:
            if type(goal) is type(candidate) and goal == candidate:
                return options
        return ()

    result = search_registered_partial_proof(
        n=7, k=5, goal=root, bridge=bridge,
        citing_assertion_id=citation_ids[0],
        expansion_provider=scoped, lookup_mode="typed_reference",
    )
    proven = result.proven_steps
    inferred_zero_image = tuple(
        step for step in proven
        if step.conclusion == zero_image and step.rule is ProofRule.INFERENCE
    )
    false_zero_proved = any(step.conclusion == false_zero_group for step in proven)
    if false_zero_proved:
        raise RuntimeError("The canonical scoped search produced an incorrect zero-group claim")
    if result.status is ProofSearchStatus.COMPLETE:
        raise RuntimeError("The intentionally bounded R44 search unexpectedly completed the final root")
    return {
        "reviewed_root": "pi_12^7 = 0",
        "screened_toda59_sources": len(laws),
        "public_r43_ehp_root_options": 1,
        "public_r43_upper_delta_options": 1,
        "public_r43_hopf_options": 1,
        "public_r41_zero_image_options": 1,
        "r41_prior_adopted_as_db_given": True,
        "r41_prior_is_independent_literature": False,
        "zero_image_is_not_domain_zero_group": True,
        "wrong_pi10_5_zero_group_is_r41_direct_premise": False,
        "wrong_pi10_5_zero_group_was_proved": False,
        "source_bound_stage_public_options": stages,
        "canonical_bounded_search_status": result.status.value,
        "canonical_bounded_verified_steps": len(proven),
        "canonical_bounded_zero_image_inferred": len(inferred_zero_image) > 0,
        "canonical_bounded_zero_image_steps": len(inferred_zero_image),
        "canonical_bounded_open_goal_types": [type(x).__name__ for x in result.open_goals],
        "canonical_bounded_proven_step_types": [type(s.conclusion).__name__ for s in proven],
        "probe_is_not_full_web_search": True,
        "web_http_checked": False,
        "root_complete": False,
        "new_givens": 0,
        "production_files_changed": 0,
        "full_pytest": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    state = verify_checkout()
    details = None if arguments.dry_run else inspected_frontier()
    gate = (
        "PASS_R44_R43_MERGE_SOURCE_PREFLIGHT" if arguments.dry_run else
        "PASS_R44_TYPED_ZERO_IMAGE_VERSUS_ZERO_GROUP_CANONICAL_FRONTIER_AUDITED"
    )
    directory = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r44"
    )
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / ("preflight.json" if arguments.dry_run else "zero_image_tree_frontier.json")
    output.write_text(json.dumps({"phase": "174-R3-R7-R44", "state": state,
                                  "details": details, "gate": gate},
                                 ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R44_"
    for key, value in state.items():
        print(prefix + key.upper() + "=" + str(value))
    if details is not None:
        for key, value in details.items():
            print(prefix + key.upper() + "=" + str(value))
    print(prefix + "REPORT=" + str(output))
    print(prefix + "GATE=" + gate)
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
