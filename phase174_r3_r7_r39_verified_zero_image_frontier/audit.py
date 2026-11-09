"""Source-first actual ProofStep frontier for the R38 zero-image chain.

Do not promote adopted DB-prior GIVEN to INFERENCE, do not assert a root
completion, and do not modify any production provider, database or renderer.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r39_verified_zero_image_frontier.source_guard import verify_checkout

ROOT = Path(__file__).resolve().parents[1]


def derive_from_expansion(expansion: object, steps: tuple[object, ...]):
    """Use the canonical inference matcher, never construct a fake proof step."""
    from phase165_r3_recursive_search import GoalExpansion
    from proof import ProofRule, ProofStep, find_inference_matches_for_rule
    from phase164_r8_proofstep_factory import derive_inference_proof_step

    if not isinstance(expansion, GoalExpansion):
        raise TypeError("GoalExpansion required")
    if (not isinstance(steps, tuple)
            or any(not isinstance(step, ProofStep) for step in steps)
            or tuple(step.conclusion for step in steps) != expansion.subgoals):
        raise ValueError("ProofStep premises do not match candidate subgoals")
    matches = tuple(
        match for match in find_inference_matches_for_rule(expansion.rule, steps)
        if len(match.premises) == len(steps)
        and all(x is y for x, y in zip(match.premises, steps))
    )
    if len(matches) != 1:
        raise RuntimeError("No unique matching genuine inference")
    result = derive_inference_proof_step(matches[0])
    if (not isinstance(result, ProofStep)
            or result.rule is not ProofRule.INFERENCE
            or result.premises != steps):
        raise RuntimeError("Inference factory produced an invalid proof step")
    return result


def derive_one(goal: object, provider, parents: tuple[object, ...], rule_name: str | None = None):
    """Choose the one requested generic rule; reject ambiguity rather than guess."""
    options = provider(goal)
    chosen = tuple(option for option in options
                   if option.subgoals == tuple(parent.conclusion for parent in parents)
                   and (rule_name is None or option.rule.name == rule_name))
    if len(chosen) != 1:
        raise RuntimeError("Expected one typed inference for " + type(goal).__name__)
    result = derive_from_expansion(chosen[0], parents)
    if result.conclusion != goal:
        raise RuntimeError("Inferred conclusion differs from the intended goal")
    return result


def inspect_proof_frontier() -> dict[str, object]:
    """Prove generator zero from real citation; inspect cyclic DB blocker."""
    from expression import Zero
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
    from map_property_rules import ImageZeroStatement
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from phase169_r10e4_ordered_db_prior.db_prior import (
        admitted_db_step, exact_prior_database_result, verified_db_step,
    )
    from phase169_r10e5_composite_generator_image.rule import (
        component_image_obligations, expand_composite_generator_image,
    )
    from phase169_r10eq_r1_universal_stable_definition.definition import expand_defined_stable_element_image
    from phase174_r3_r7_r12_toda59_annihilator_source.rule import (
        expand_cited_annihilator_specialization,
    )
    from phase174_r3_r7_r12_toda59_annihilator_source.source import CitedFamilyAnnihilator
    from phase174_r3_r7_r38_source_bound_zero_image_public_wiring.provider import (
        left_associated, lifted_stable_composition,
    )
    from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import RULE_NAME as CYCLIC_RULE
    from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    original_fixed = tuple(
        link.step for link in bridge.proof_links
        if isinstance(link.step, ProofStep)
        and link.step.rule is ProofRule.GIVEN
        and bridge.registry.assertion(link.assertion_id).content == link.step.conclusion
    )
    schema_steps = tuple(step for step in original_fixed
                         if type(step.conclusion) is CitedFamilyAnnihilator)
    if len(schema_steps) != 1:
        raise RuntimeError("Expected exactly one cited Toda (5.9) general source")
    source_step = schema_steps[0]
    source_citation = getattr(getattr(source_step, "inference_rule", None), "literature_reference", None)
    if source_citation is None or source_citation.locator != "(5.9)":
        raise RuntimeError("Source attribution is not Toda (5.9)")

    prior = exact_prior_database_result(5, 5)
    if type(prior) is not Relation or prior.relation_type is not RelationType.EQUALITY:
        raise RuntimeError("The reviewed earlier DB group is missing")
    db_step = admitted_db_step(prior, proof_target=root, bridge=bridge)
    if (not isinstance(db_step, ProofStep)
            or db_step.rule is not ProofRule.GIVEN
            or not verified_db_step(db_step, proof_target=root, bridge=bridge)):
        raise RuntimeError("Earlier DB prior failed its existing independent admission gate")
    domain, target = prior.lhs, TodaPrimaryGroup(
        prior.lhs.group_dimension + 1, prior.lhs.sphere_dimension + 1,
    )
    mapping = TodaSuspensionMap(domain, target)
    lift = lifted_stable_composition(prior.rhs.generator)
    if lift is None:
        raise RuntimeError("R38 registered composite generator cannot be suspended")
    left = left_associated(lift)
    if left is None:
        raise RuntimeError("Canonical composition cannot be rebracketed")
    right_goal = GeneratorImage(mapping, prior.rhs.generator, lift)
    left_goal = GeneratorImage(mapping, prior.rhs.generator, left)
    zero_generator_goal = GeneratorImage(mapping, prior.rhs.generator, Zero())
    zero_image_goal = ImageZeroStatement(mapping)
    annihilator_goal = Relation(left.left, Zero(), RelationType.EQUALITY)

    shared = shared_expansion_provider(bridge, proof_target=root)
    public_r38 = tuple(x for x in shared(zero_image_goal) if x.rule.name == CYCLIC_RULE)
    if len(public_r38) != 1 or public_r38[0].subgoals != (prior, zero_generator_goal):
        raise RuntimeError("R38 public cyclic candidate disappeared")

    n6_step = derive_one(
        annihilator_goal,
        lambda goal: expand_cited_annihilator_specialization(goal, (source_step.conclusion,)),
        (source_step,),
    )
    factors = component_image_obligations(right_goal)
    if factors is None or len(factors) != 2:
        raise RuntimeError("Composite generator image does not factor into two typed images")
    stable_steps = tuple(derive_one(fact, expand_defined_stable_element_image, ())
                         for fact in factors)
    right_step = derive_one(right_goal, expand_composite_generator_image, stable_steps)
    from phase174_r3_r7_r9_composition_associativity.rule import expand_generator_image_associativity
    left_step = derive_one(left_goal, expand_generator_image_associativity, (right_step,))
    from phase174_r3_r7_r7_composite_zero_audit.rule import expand_generator_zero_from_composite
    zero_generator_step = derive_one(
        zero_generator_goal,
        lambda goal: expand_generator_zero_from_composite(goal, left_goal),
        (left_step, n6_step),
    )
    if zero_generator_step.rule is not ProofRule.INFERENCE:
        raise RuntimeError("Generator zero has not been inferred")
    if find_inference_matches_for_rule(public_r38[0].rule, (db_step, zero_generator_step)):
        raise RuntimeError("R6 rule accepted adopted DB GIVEN as an inferred presentation")
    if any(step.conclusion in (zero_image_goal, root) for step in original_fixed):
        raise RuntimeError("Forbidden direct zero image/root cited GIVEN")

    return {
        "cited_annihilator_source": "(5.9)",
        "source_general_given_count": 1,
        "adopted_earlier_db_prior_accepted": True,
        "db_prior_is_independent_literature": False,
        "db_presentation_step_rule": db_step.rule.name,
        "n6_annihilator_inferred": True,
        "stable_factor_images_inferred": len(stable_steps),
        "composite_image_inferred": True,
        "associativity_inferred": True,
        "generator_zero_inferred": True,
        "r6_accepts_db_prior_as_inferred_presentation": False,
        "cyclic_presentation_inference_available_in_this_audit": False,
        "zero_suspension_image_proved": False,
        "upper_delta_surjectivity_proved": False,
        "root_complete": False,
        "new_givens": 0,
        "new_public_rules": 0,
        "full_pytest": False,
        "blocker": "Cyclic presentation for the R6 rule is an adopted DB GIVEN, not a verified INFERENCE",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    checkout = verify_checkout()
    observed = None if args.dry_run else inspect_proof_frontier()
    report = {
        "phase": "174-R3-R7-R39",
        "git_state": checkout,
        "observed": observed,
        "gate": (
            "PASS_R39_SOURCE_GUARD_ONLY" if args.dry_run else
            "PASS_R39_CITED_GENERATOR_ZERO_PROVED_DB_PRESENTATION_BARRIER"
        ),
    }
    folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r39"
    )
    folder.mkdir(parents=True, exist_ok=True)
    output = folder / ("preflight.json" if args.dry_run else "zero_image_frontier.json")
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    p = "PHASE174_R3R7R39_"
    for key in ("local_head", "remote_head", "source_guard", "reviewed_r38_upstream_files", "public_r38_installed"):
        print(p + key.upper() + "=" + str(checkout[key]))
    if observed is not None:
        for key, value in observed.items():
            print(p + key.upper() + "=" + str(value))
    print(p + "REPORT=" + str(output))
    print(p + "GATE=" + report["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
