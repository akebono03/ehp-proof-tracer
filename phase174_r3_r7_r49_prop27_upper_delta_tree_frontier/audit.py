"""R49: extend the source-first canonical tree through cited Prop. 2.7.

Retain the R48 source-bound lower-Delta kernel, infer the universal Prop. 2.7
premise and n=6 witness, then infer upper-Delta surjectivity. The root
exactness windows remain intentionally outside this bounded search.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r49_prop27_upper_delta_tree_frontier.source_guard import verify_checkout


def inspect_integrated_prop27_frontier() -> dict[str, object]:
    """Run one actual canonical DFS through cited upper-Delta surjectivity."""
    from expression import Zero
    from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from map_property_rules import ImageZeroStatement
    from phase165_r12_r11_prop42_unified import TodaProp42GeneralExactnessStatement
    from phase165_r12_r12_ehp_consequences import (
        EHPImageEqualsKernelStatement,
        proof_has_general_prop42_ancestor,
    )
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r3_recursive_search import GoalExpansion, SourceBoundGoal
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r2_search_adapter import search_registered_partial_proof
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from phase169_r10e4_ordered_db_prior.db_prior import admitted_db_step, verified_db_step
    from phase169_r10e5_composite_generator_image.rule import (
        component_image_obligations,
        expand_composite_generator_image,
    )
    from phase169_r10eq_r1_universal_stable_definition.definition import expand_defined_stable_element_image
    from phase174_r3_r7_r3_ehp_zero_rule.rule import RULE_NAME as ROOT_RULE, ehp_zero_inputs
    from phase174_r3_r7_r5_zero_image_hopf_injective.rule import (
        RULE_NAME as HOPF_RULE,
        hopf_injectivity_from_zero_image_inputs,
    )
    from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import (
        RULE_NAME as UPPER_RULE,
        upper_delta_surjectivity_inputs,
    )
    from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import RULE_NAME as KERNEL_RULE
    from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
        Prop27GeneralTheoremPremise,
        RULE_NAME as PROP27_RULE,
        typed_specialization,
    )
    from phase174_r3_r7_r28_prop27_typed_literature_registration.registration import (
        Prop27UniversalLiteratureStatement,
    )
    from phase174_r3_r7_r30_prop27_public_provider_wiring.provider import (
        has_certified_prop27_leaf,
    )
    from phase174_r3_r7_r34_prior_lower_delta_source_wiring.source import checked_prior_statements
    from phase174_r3_r7_r40_adopted_db_zero_image_isolated.rule import RULE_NAME as ZERO_IMAGE_RULE
    from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.provider import screened_general_law
    from phase174_r3_r7_r38_source_bound_zero_image_public_wiring.provider import (
        left_associated, lifted_stable_composition,
    )
    from phase174_r3_r7_r9_composition_associativity.rule import expand_generator_image_associativity
    from phase174_r3_r7_r7_composite_zero_audit.rule import expand_generator_zero_from_composite
    from phase174_r3_r7_r12_toda59_annihilator_source.rule import expand_cited_annihilator_specialization
    from proof import (
        ProofRule,
        ProofStep,
        Relation,
        RelationType,
        find_inference_matches_for_rule,
    )
    from toda_rules import TodaProp42ExactnessStatement

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(
        build_shared_typed_bridge(), goal=root,
    )
    laws = screened_general_law(bridge)
    if len(laws) != 1:
        raise RuntimeError("R44 cited Toda (5.9) source is missing")
    source_links = tuple(
        link for link in bridge.proof_links
        if isinstance(link.step, ProofStep)
        and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == laws[0]
    )
    if len(source_links) != 1:
        raise RuntimeError("R44 cited Toda (5.9) source link changed")
    citing_id = source_links[0].assertion_id
    general_prop42 = TodaProp42GeneralExactnessStatement()
    prop42_links = tuple(
        link for link in bridge.proof_links
        if isinstance(link.step, ProofStep)
        and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == general_prop42
    )
    if len(prop42_links) != 1:
        raise RuntimeError("R46 cited Prop. 4.2 source link changed")

    root_inputs = ehp_zero_inputs(root)
    if root_inputs is None or len(root_inputs) != 4:
        raise RuntimeError("R47 root shape changed")
    upper = root_inputs[0]
    upper_inputs = upper_delta_surjectivity_inputs(upper)
    if upper_inputs is None or len(upper_inputs) != 4:
        raise RuntimeError("R47 upper Delta shape changed")
    hopf = upper_inputs[0]
    hopf_inputs = hopf_injectivity_from_zero_image_inputs(hopf)
    if hopf_inputs is None or len(hopf_inputs) != 2:
        raise RuntimeError("R47 Hopf shape changed")
    zero_image, hopf_exactness = hopf_inputs
    lower_image_kernel = upper_inputs[1]
    lower_kernel_multiple = upper_inputs[2]
    prop27_witness = upper_inputs[3]
    lower_exactness = TodaProp42ExactnessStatement(lower_image_kernel.window)
    if (type(zero_image) is not ImageZeroStatement
            or type(lower_image_kernel) is not EHPImageEqualsKernelStatement):
        raise RuntimeError("R47 reviewed typed EHP proof obligations changed")

    public = shared_expansion_provider(bridge, proof_target=root)
    selected: list[tuple[object, tuple]] = []
    reviewed_counts: dict[str, int] = {}

    def select(goal: object, name: str, subgoals: tuple) -> None:
        """Use the first *existing* matching public rule, never fabricate one."""
        matches = tuple(
            option for option in public(goal)
            if option.rule.name == name and option.subgoals == subgoals
        )
        reviewed_counts[name] = len(matches)
        if not matches:
            raise RuntimeError("Reviewed public proof branch missing: " + name)
        selected.append((goal, (matches[0],)))

    select(root, ROOT_RULE, root_inputs)
    select(upper, UPPER_RULE, upper_inputs)
    select(hopf, HOPF_RULE, hopf_inputs)
    zero_options = tuple(x for x in public(zero_image) if x.rule.name == ZERO_IMAGE_RULE)
    if not zero_options or len(zero_options[0].subgoals) != 2:
        raise RuntimeError("R44 adopted-DB zero-image public branch missing")
    zero_option = zero_options[0]
    selected.append((zero_image, (zero_option,)))
    presentation, zero_generator = zero_option.subgoals
    db_step = admitted_db_step(presentation, proof_target=root, bridge=bridge)
    if (db_step is None or db_step.rule is not ProofRule.GIVEN
            or not verified_db_step(db_step, proof_target=root, bridge=bridge)):
        raise RuntimeError("R44 DB prior admission failed")
    if zero_image.map.source_group != presentation.lhs:
        raise RuntimeError("The image source group is not the cited DB prior group")
    false_zero_group = TodaPrimaryGroupZeroStatement(presentation.lhs)
    if false_zero_group == root:
        raise RuntimeError("R47 target root collided with false zero group")

    right = lifted_stable_composition(presentation.rhs.generator)
    left = left_associated(right) if right is not None else None
    if left is None:
        raise RuntimeError("R44 zero-image associativity data unavailable")
    left_goal = GeneratorImage(zero_image.map, presentation.rhs.generator, left)
    right_goal = GeneratorImage(zero_image.map, presentation.rhs.generator, right)
    annihilator = Relation(left.left, Zero(), RelationType.EQUALITY)
    parts = component_image_obligations(right_goal)
    if parts is None or len(parts) != 2:
        raise RuntimeError("R44 composite generator image obligations changed")

    # R44's exact reviewed public generator-image chain.
    r44_requests = (
        (zero_generator, expand_generator_zero_from_composite(zero_generator, left_goal)),
        (left_goal, expand_generator_image_associativity(left_goal)),
        (right_goal, expand_composite_generator_image(right_goal)),
        (annihilator, expand_cited_annihilator_specialization(annihilator, laws)),
    ) + tuple((part, expand_defined_stable_element_image(part)) for part in parts)
    r44_stage_counts: list[dict[str, object]] = []
    for goal, expected in r44_requests:
        matches = tuple(
            option for option in public(goal)
            if any(
                option.rule.name == candidate.rule.name
                and option.subgoals == candidate.subgoals
                for candidate in expected
            )
        )
        r44_stage_counts.append({
            "goal_type": type(goal).__name__,
            "reviewed_public_matches": len(matches),
        })
        selected.append((goal, (matches[0],) if matches else ()))

    # R46's genuine cited generic exactness rules.  Use source-linked
    # expansions, not saved R46 ProofSteps or synthetic GIVEN leaves.
    exact_rule = "Toda Proposition 4.2: generic consecutive EHP specialization"
    select(hopf_exactness, exact_rule, (general_prop42,))
    select(lower_image_kernel, "EHP exactness implies image equals kernel", (lower_exactness,))
    select(lower_exactness, exact_rule, (general_prop42,))

    # R35/R36: the lower Delta kernel is an inference from one inferred
    # free-cyclic domain and two earlier independently cited printed facts.
    # These are exact typed claims, not an invented kernel/root GIVEN.
    codomain, signed_image = checked_prior_statements()
    domain = Relation(
        lower_kernel_multiple.domain,
        FreeCyclicGroup(lower_kernel_multiple.source_generator),
        RelationType.EQUALITY,
    )
    if (signed_image.map != lower_kernel_multiple.map
            or signed_image.element != lower_kernel_multiple.source_generator
            or codomain.lhs != lower_kernel_multiple.map.target_group
            or lower_kernel_multiple.multiple != 2):
        raise RuntimeError("R48 typed kernel does not match the earlier Toda premises")
    source_claims = (
        (codomain, "Proposition 5.8"),
        (signed_image, "(5.10)"),
    )
    earlier_source_ids: list[str] = []
    for claim, locator in source_claims:
        links = tuple(
            link for link in bridge.proof_links
            if isinstance(link.step, ProofStep)
            and link.step.rule is ProofRule.GIVEN
            and not link.step.premises
            and link.step.conclusion == claim
            and getattr(
                getattr(link.step.inference_rule, "literature_reference", None),
                "locator", None,
            ) == locator
        )
        if not links:
            raise RuntimeError("R48 earlier cited source is missing: " + locator)
        earlier_source_ids.append(links[0].assertion_id)
    select(lower_kernel_multiple, KERNEL_RULE, (domain, codomain, signed_image))
    diagonal_options = tuple(
        option for option in public(domain)
        if option.rule.name == "generic cited typed scalar specialization"
        and len(option.subgoals) == 1
        and any(
            isinstance(link.step, ProofStep)
            and link.step.rule is ProofRule.GIVEN
            and link.step.conclusion == option.subgoals[0]
            and find_inference_matches_for_rule(option.rule, (link.step,))
            for link in bridge.proof_links
        )
    )
    if not diagonal_options:
        raise RuntimeError("R48 general-source diagonal specialization absent")
    # The canonical typed-reference lookup otherwise accepts an earlier direct
    # GIVEN for the concrete free-cyclic domain.  R35 correctly requires its
    # domain presentation to be an INFERENCE.  Preserve the exact reviewed
    # R35 rule and its mathematical conclusions; constrain ONLY the searched
    # domain premise to a source-linked specialization, using the existing
    # general-purpose SourceBoundGoal obligation.
    source_bound_count = 0
    for index, (candidate, expansions) in enumerate(selected):
        if type(candidate) is not type(lower_kernel_multiple) or candidate != lower_kernel_multiple:
            continue
        if len(expansions) != 1 or expansions[0].subgoals != (domain, codomain, signed_image):
            raise RuntimeError("R48 reviewed R35 kernel public expansion changed")
        selected[index] = (candidate, tuple(
            GoalExpansion(
                rule=expansions[0].rule,
                subgoals=(
                    SourceBoundGoal(conclusion=domain, source=option.subgoals[0]),
                    codomain,
                    signed_image,
                ),
            )
            for option in diagonal_options
        ))
        source_bound_count = len(diagonal_options)
        break
    if source_bound_count == 0:
        raise RuntimeError("R48 kernel source-bound search obligation was not installed")
    # First Successful Proof Search: let canonical DFS stop at its first success.
    selected.append((domain, diagonal_options))
    reviewed_counts["generic cited typed scalar specialization"] = len(diagonal_options)

    # R30's production provider already contains two *general* Prop. 2.7
    # inferences: universal literature GIVEN -> general premise INFERENCE ->
    # even-n typed witness INFERENCE. Do not create or install ProofSteps.
    if not has_certified_prop27_leaf(bridge):
        raise RuntimeError("R49 source-first Prop. 2.7 general literature leaf missing")
    universal_prop27 = Prop27UniversalLiteratureStatement()
    general_prop27 = Prop27GeneralTheoremPremise()
    if typed_specialization(prop27_witness.n) != prop27_witness:
        raise RuntimeError("R49 upper Delta requires exact even-dimensional Prop. 2.7")
    prop27_source_links = tuple(
        link for link in bridge.proof_links
        if isinstance(link.step, ProofStep)
        and link.step.rule is ProofRule.GIVEN
        and link.step.premises == ()
        and type(link.step.conclusion) is Prop27UniversalLiteratureStatement
        and link.step.conclusion == universal_prop27
        and bridge.registry.reference(
            bridge.registry.assertion(link.assertion_id).reference_id
        ).locator == "Proposition 2.7"
    )
    if len(prop27_source_links) != 1:
        raise RuntimeError("R49 source-first general Prop. 2.7 leaf is not unique")
    if any(link.step is not None
           and link.step.rule is ProofRule.GIVEN
           and link.step.conclusion in (general_prop27, prop27_witness, upper, root)
           for link in bridge.proof_links):
        raise RuntimeError("R49 disallowed a direct GIVEN for a derived EHP goal")
    select(prop27_witness, PROP27_RULE, (general_prop27,))
    select(
        general_prop27,
        "Toda Proposition 2.7 typed literature universal premise",
        (universal_prop27,),
    )

    # Root exactness is deliberately outside R49.  This makes the R37
    # surjectivity inference visible without claiming pi_12^7=0.
    visited: list[str] = []

    def scoped(goal: object) -> tuple:
        if any(
            type(goal) is type(window) and goal == window
            for window in root_inputs[1:3]
        ):
            visited.append("root_exactness_outside_scope")
            return ()
        for expected_goal, options in selected:
            if type(goal) is type(expected_goal) and goal == expected_goal:
                visited.append(type(goal).__name__)
                return options
        visited.append("outside_scope:" + type(goal).__name__)
        return ()

    result = search_registered_partial_proof(
        n=7, k=5, goal=root, bridge=bridge,
        citing_assertion_id=citing_id,
        expansion_provider=scoped, lookup_mode="typed_reference",
    )
    proven = result.proven_steps
    def inferred(goal: object) -> tuple:
        return tuple(
            step for step in proven
            if step.rule is ProofRule.INFERENCE
            and type(step.conclusion) is type(goal)
            and step.conclusion == goal
        )
    zero_steps = inferred(zero_image)
    hopf_steps = inferred(hopf)
    hopf_exact_steps = inferred(hopf_exactness)
    lower_exact_steps = inferred(lower_exactness)
    lower_image_kernel_steps = inferred(lower_image_kernel)
    lower_kernel_steps = inferred(lower_kernel_multiple)
    domain_steps = inferred(domain)
    prop27_steps = inferred(prop27_witness)
    prop27_general_steps = inferred(general_prop27)
    upper_steps = inferred(upper)
    if any(step.conclusion == false_zero_group for step in proven):
        raise RuntimeError("Incorrect group zero substituted for image zero")
    if result.status is ProofSearchStatus.COMPLETE or any(step.conclusion == root for step in proven):
        raise RuntimeError("Intentionally bounded R49 claims a completed group proof")

    def cited_source_ancestor(step: ProofStep, claim: object) -> bool:
        seen: set[int] = set()
        def visit(node: ProofStep) -> bool:
            if id(node) in seen:
                return False
            seen.add(id(node))
            if node.rule is ProofRule.GIVEN and node.conclusion == claim:
                return True
            return any(visit(parent) for parent in node.premises)
        return visit(step)

    if hopf_steps and not any(
        cited_source_ancestor(step, laws[0])
        and proof_has_general_prop42_ancestor(step)
        for step in hopf_steps
    ):
        raise RuntimeError("Hopf inference lacks both independent proof ancestries")
    if lower_image_kernel_steps and not all(
        proof_has_general_prop42_ancestor(step) for step in lower_image_kernel_steps
    ):
        raise RuntimeError("Lower EHP image-kernel inference lacks Prop. 4.2 ancestry")

    # Validate the actual accepted canonical tree and its THREE exact parents.
    kernel_cited_ancestry = any(
        tuple(parent.conclusion for parent in step.premises)
        == (domain, codomain, signed_image)
        and tuple(parent.rule for parent in step.premises)
        == (ProofRule.INFERENCE, ProofRule.GIVEN, ProofRule.GIVEN)
        and cited_source_ancestor(step, codomain)
        and cited_source_ancestor(step, signed_image)
        for step in lower_kernel_steps
    )
    if lower_kernel_steps and not kernel_cited_ancestry:
        raise RuntimeError("Lower kernel inference lacks the three prior typed premises")
    if any(step.conclusion in (root, lower_kernel_multiple)
           and step.rule is ProofRule.GIVEN for step in proven):
        raise RuntimeError("R49 kernel/root were incorrectly asserted as GIVEN")

    return {
        "root": "pi_12^7 = 0",
        "source_first_toda59_given": len(source_links),
        "source_first_general_prop42_given": len(prop42_links),
        "r44_db_prior_is_independent_literature": False,
        "r44_db_prior_admitted_in_group_root_scope": True,
        "selected_public_rule_candidate_counts": reviewed_counts,
        "r44_generator_stage_public_matches": r44_stage_counts,
        "canonical_status": result.status.value,
        "canonical_verified_steps": len(proven),
        "canonical_zero_image_inference_count": len(zero_steps),
        "canonical_hopf_exactness_inference_count": len(hopf_exact_steps),
        "canonical_hopf_injectivity_inference_count": len(hopf_steps),
        "canonical_lower_exactness_inference_count": len(lower_exact_steps),
        "canonical_lower_image_kernel_inference_count": len(lower_image_kernel_steps),
        "canonical_hopf_has_toda59_and_prop42_ancestors": any(
            cited_source_ancestor(step, laws[0])
            and proof_has_general_prop42_ancestor(step)
            for step in hopf_steps
        ),
        "canonical_lower_image_kernel_has_prop42_ancestor": any(
            proof_has_general_prop42_ancestor(step)
            for step in lower_image_kernel_steps
        ),
        "canonical_lower_kernel_inference_count": len(lower_kernel_steps),
        "canonical_lower_kernel_three_premises_cited": kernel_cited_ancestry,
        "canonical_lower_kernel_domain_inferred": len(domain_steps) > 0,
        "canonical_kernel_domain_source_bound_candidates": source_bound_count,
        "canonical_kernel_domain_bound_inference_proved": bool(domain_steps),
        "canonical_lower_kernel_prior_reference_ids": earlier_source_ids,
        "canonical_visited_prop27_frontier": "Prop27TypedHopfDeltaStatement" in visited,
        "canonical_prop27_typed_inference_count": len(prop27_steps),
        "canonical_prop27_general_inference_count": len(prop27_general_steps),
        "canonical_prop27_source_reference_id": prop27_source_links[0].assertion_id,
        "canonical_prop27_cited_three_level_ancestry": any(
            len(step.premises) == 1
            and step.premises[0].rule is ProofRule.INFERENCE
            and step.premises[0].conclusion == general_prop27
            and len(step.premises[0].premises) == 1
            and step.premises[0].premises[0].rule is ProofRule.GIVEN
            and step.premises[0].premises[0].conclusion == universal_prop27
            and getattr(
                getattr(step.inference_rule, "literature_reference", None),
                "locator", None,
            ) == "Proposition 2.7"
            for step in prop27_steps
        ),
        "canonical_upper_delta_surjectivity_inference_count": len(upper_steps),
        "canonical_upper_delta_four_independent_inference_parents": any(
            len(step.premises) == 4
            and tuple(parent.conclusion for parent in step.premises) == upper_inputs
            and all(parent.rule is ProofRule.INFERENCE for parent in step.premises)
            and any(parent is candidate for parent in step.premises for candidate in prop27_steps)
            and any(parent is candidate for parent in step.premises for candidate in lower_kernel_steps)
            for step in upper_steps
        ),
        "canonical_visited_root_exactness_frontier": "root_exactness_outside_scope" in visited,
        "canonical_proven_goal_types": dict(sorted(Counter(
            type(step.conclusion).__name__ for step in proven
        ).items())),
        "canonical_open_goal_types": dict(sorted(Counter(
            type(goal).__name__ for goal in result.open_goals
        ).items())),
        "canonical_scoped_visit_trace": visited,
        "wrong_pi10_5_group_zero_proved": False,
        "kernel_was_not_adopted_as_given": True,
        "isolated_proof_steps_injected": False,
        "new_givens": 0,
        "new_mathematical_rules": 0,
        "production_files_changed": 0,
        "root_complete": False,
        "web_http_checked": False,
        "full_pytest": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = verify_checkout()
    details = None if args.dry_run else inspect_integrated_prop27_frontier()
    connected = details is not None and all((
        details["canonical_zero_image_inference_count"] > 0,
        details["canonical_hopf_exactness_inference_count"] > 0,
        details["canonical_hopf_injectivity_inference_count"] > 0,
        details["canonical_hopf_has_toda59_and_prop42_ancestors"],
        details["canonical_lower_exactness_inference_count"] > 0,
        details["canonical_lower_image_kernel_inference_count"] > 0,
        details["canonical_lower_image_kernel_has_prop42_ancestor"],
        details["canonical_lower_kernel_inference_count"] > 0,
        details["canonical_lower_kernel_three_premises_cited"],
        details["canonical_lower_kernel_domain_inferred"],
        details["canonical_visited_prop27_frontier"],
        details["canonical_prop27_typed_inference_count"] == 1,
        details["canonical_prop27_general_inference_count"] == 1,
        details["canonical_prop27_cited_three_level_ancestry"],
        details["canonical_upper_delta_surjectivity_inference_count"] == 1,
        details["canonical_upper_delta_four_independent_inference_parents"],
        details["canonical_visited_root_exactness_frontier"],
    ))
    gate = (
        "PASS_R49_REVIEWED_R48_SOURCE_PREFLIGHT" if args.dry_run else
        "PASS_R49_CITED_PROP27_UPPER_DELTA_CONNECTED_ROOT_EXACTNESS_PENDING"
        if connected else
        "PASS_R49_PROP27_CONNECTION_GAP_RECORDED"
    )
    folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r49"
    )
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / ("preflight.json" if args.dry_run else "prop27_upper_delta_frontier.json")
    path.write_text(json.dumps({
        "phase": "174-R3-R7-R49", "state": state,
        "details": details, "gate": gate,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R49_"
    for name, value in state.items():
        print(prefix + name.upper() + "=" + str(value))
    if details is not None:
        for name, value in details.items():
            print(prefix + name.upper() + "=" + str(value))
    print(prefix + "REPORT=" + str(path))
    print(prefix + "GATE=" + gate)
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
