"""Rebuild real cited zero-generator ancestry and audited adopted-prior zero image."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r40_adopted_db_zero_image_isolated.source_guard import verify_checkout


def inspect_isolated_zero_image() -> dict[str, object]:
    """Re-run cited R39 steps and infer E(image)=0 without changing any GIVEN."""
    from expression import Zero
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
    from map_property_rules import ImageZeroStatement
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from phase169_r10e4_ordered_db_prior.db_prior import (
        admitted_db_step, exact_prior_database_result, verified_db_step,
    )
    from phase169_r10e5_composite_generator_image.rule import (
        component_image_obligations, expand_composite_generator_image,
    )
    from phase169_r10eq_r1_universal_stable_definition.definition import (
        expand_defined_stable_element_image,
    )
    from phase174_r3_r7_r12_toda59_annihilator_source.rule import (
        expand_cited_annihilator_specialization,
    )
    from phase174_r3_r7_r12_toda59_annihilator_source.source import CitedFamilyAnnihilator
    from phase174_r3_r7_r38_source_bound_zero_image_public_wiring.provider import (
        left_associated, lifted_stable_composition,
    )
    from phase174_r3_r7_r39_verified_zero_image_frontier.audit import derive_one, derive_from_expansion
    from phase174_r3_r7_r40_adopted_db_zero_image_isolated.rule import (
        RULE_NAME, expand_adopted_prior_zero_image,
    )
    from proof import ProofRule, ProofStep, Relation, RelationType

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(
        build_shared_typed_bridge(), goal=root,
    )
    cited = tuple(
        link.step for link in bridge.proof_links
        if isinstance(link.step, ProofStep)
        and link.step.rule is ProofRule.GIVEN
        and type(link.step.conclusion) is CitedFamilyAnnihilator
        and bridge.registry.assertion(link.assertion_id).content == link.step.conclusion
        and link.step.inference_rule is not None
        and link.step.inference_rule.literature_reference is not None
        and link.step.inference_rule.literature_reference.locator == "(5.9)"
    )
    if len(cited) != 1:
        raise RuntimeError("Exactly one independently cited Toda (5.9) general law required")
    prior = exact_prior_database_result(5, 5)
    db = admitted_db_step(prior, proof_target=root, bridge=bridge)
    if (db is None or db.rule is not ProofRule.GIVEN
            or not verified_db_step(db, proof_target=root, bridge=bridge)):
        raise RuntimeError("Actual earlier adopted database prior not verified")
    domain = prior.lhs
    suspension = TodaSuspensionMap(
        domain, TodaPrimaryGroup(domain.group_dimension + 1, domain.sphere_dimension + 1),
    )
    lifted = lifted_stable_composition(prior.rhs.generator)
    left = left_associated(lifted) if lifted is not None else None
    if left is None or type(left.left) is not type(left):
        raise RuntimeError("Canonical composition or parenthesization invalid")
    right_goal = GeneratorImage(suspension, prior.rhs.generator, lifted)
    left_goal = GeneratorImage(suspension, prior.rhs.generator, left)
    zero_goal = GeneratorImage(suspension, prior.rhs.generator, Zero())
    zero_image = ImageZeroStatement(suspension)
    annihilator = Relation(left.left, Zero(), RelationType.EQUALITY)

    annihilator_step = derive_one(
        annihilator,
        lambda goal: expand_cited_annihilator_specialization(goal, (cited[0].conclusion,)),
        (cited[0],),
    )
    parts = component_image_obligations(right_goal)
    if parts is None or len(parts) != 2:
        raise RuntimeError("Factor-image obligations changed")
    factor_steps = tuple(derive_one(goal, expand_defined_stable_element_image, ()) for goal in parts)
    right_step = derive_one(right_goal, expand_composite_generator_image, factor_steps)
    from phase174_r3_r7_r9_composition_associativity.rule import expand_generator_image_associativity
    left_step = derive_one(left_goal, expand_generator_image_associativity, (right_step,))
    from phase174_r3_r7_r7_composite_zero_audit.rule import expand_generator_zero_from_composite
    zero_step = derive_one(
        zero_goal,
        lambda goal: expand_generator_zero_from_composite(goal, left_goal),
        (left_step, annihilator_step),
    )
    if (zero_step.rule is not ProofRule.INFERENCE
            or zero_step.conclusion != zero_goal):
        raise RuntimeError("Cited generator-zero inference incomplete")

    options = expand_adopted_prior_zero_image(
        zero_image, prior, proof_target=root, bridge=bridge,
    )
    if len(options) != 1 or options[0].rule.name != RULE_NAME:
        raise RuntimeError("Isolated adopted-DB zero-image inference not proposed")
    if options[0].subgoals != (prior, zero_goal):
        raise RuntimeError("A premise was replaced or reordered")
    final = derive_from_expansion(options[0], (db, zero_step))
    if (final.rule is not ProofRule.INFERENCE or final.conclusion != zero_image
            or final.premises != (db, zero_step)):
        raise RuntimeError("Actual inferred zero image did not retain its DB provenance")
    if (db.rule is not ProofRule.GIVEN
            or db.note != "ADOPTED_DATABASE_PRIOR; independent reference not asserted"
            or any(step.conclusion in (zero_image, root) for step in (db, cited[0]))):
        raise RuntimeError("Database or result was laundered into a cited conclusion")

    return {
        "source_locator": "(5.9)",
        "cited_general_source_givens": 1,
        "earlier_adopted_db_prior_verified": True,
        "db_prior_rule": db.rule.name,
        "db_prior_is_independent_literature": False,
        "inferred_stable_factor_images": len(factor_steps),
        "inferred_generator_zero": True,
        "isolated_zero_image_proved": True,
        "isolated_zero_image_rule": final.rule.name,
        "db_given_preserved_inside_proof_tree": final.premises[0] is db,
        "isolated_not_public_provider": True,
        "upper_delta_surjectivity_proved": False,
        "root_complete": False,
        "new_givens": 0,
        "new_direct_root_givens": 0,
        "public_production_files_changed": 0,
        "full_pytest": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = verify_checkout()
    result = None if args.dry_run else inspect_isolated_zero_image()
    gate = (
        "PASS_R40_SOURCE_GUARD_ONLY" if args.dry_run else
        "PASS_R40_VERIFIED_ADOPTED_DB_CYCLIC_ZERO_IMAGE_ISOLATED_PUBLIC_PENDING"
    )
    report = {"phase": "174-R3-R7-R40", "git_state": state,
              "observations": result, "gate": gate}
    directory = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r40"
    )
    directory.mkdir(parents=True, exist_ok=True)
    file = directory / ("preflight.json" if args.dry_run else "adopted_db_zero_image.json")
    file.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R40_"
    for name, value in state.items():
        print(prefix + name.upper() + "=" + str(value))
    if result is not None:
        for name, value in result.items():
            print(prefix + name.upper() + "=" + str(value))
    print(prefix + "REPORT=" + str(file))
    print(prefix + "GATE=" + gate)
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
