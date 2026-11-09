"""R45: read-only source-first audit of open Proposition 4.2/EHP obligations.

This deliberately scoped canonical search does not replay R44's entire
zero-image branch and cannot certify the final pi_12^7 group. It determines
whether already-registered general EHP exactness rules are actually usable.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r45_ehp_open_obligation_audit.source_guard import verify_checkout


def inspect_open_ehp_obligations() -> dict[str, object]:
    """Trace real public proposals and a constrained canonical proof search."""
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from map_property_rules import ImageZeroStatement
    from phase165_r12_r11_prop42_unified import (
        TodaProp42GeneralExactnessStatement,
        prop42_exactness_indices,
    )
    from phase165_r12_r12_ehp_consequences import (
        EHPImageEqualsKernelStatement,
        proof_has_general_prop42_ancestor,
    )
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r2_search_adapter import search_registered_partial_proof
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge,
        shared_expansion_provider,
    )
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase174_r3_r7_r3_ehp_zero_rule.rule import (
        RULE_NAME as ROOT_RULE,
        ehp_zero_inputs,
    )
    from phase174_r3_r7_r5_zero_image_hopf_injective.rule import (
        RULE_NAME as HOPF_RULE,
        hopf_injectivity_from_zero_image_inputs,
    )
    from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import (
        RULE_NAME as UPPER_RULE,
        upper_delta_surjectivity_inputs,
    )
    from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.provider import (
        screened_general_law,
    )
    from proof import ProofRule, ProofStep
    from toda_rules import TodaProp42ExactnessStatement
    from unified_statement_registry import AssertionOrigin

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(
        build_shared_typed_bridge(), goal=root
    )
    r44_source = screened_general_law(bridge)
    if len(r44_source) != 1:
        raise RuntimeError("R44 Toda (5.9) source was lost")
    source_ids = tuple(
        link.assertion_id for link in bridge.proof_links
        if isinstance(link.step, ProofStep)
        and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == r44_source[0]
    )
    if len(source_ids) != 1:
        raise RuntimeError("The R44 source link is no longer unique")

    universal = TodaProp42GeneralExactnessStatement()
    cited_universal = tuple(
        link for link in bridge.proof_links
        if isinstance(link.step, ProofStep)
        and link.step.rule is ProofRule.GIVEN
        and not link.step.premises
        and link.step.conclusion == universal
        and bridge.registry.assertion(link.assertion_id).origin
        is AssertionOrigin.FIXED_STATEMENT
        and bridge.registry.assertion(link.assertion_id).content == universal
        and bridge.registry.reference(
            bridge.registry.assertion(link.assertion_id).reference_id
        ).publication_position is not None
        and getattr(
            getattr(link.step.inference_rule, "literature_reference", None),
            "locator", None,
        ) == "Proposition 4.2 (4.4)"
    )
    if len(cited_universal) > 1:
        raise RuntimeError("Duplicated screened Prop. 4.2 source")

    root_inputs = ehp_zero_inputs(root)
    if root_inputs is None or len(root_inputs) != 4:
        raise RuntimeError("R3 zero-root obligation shape changed")
    upper = root_inputs[0]
    upper_inputs = upper_delta_surjectivity_inputs(upper)
    if upper_inputs is None or len(upper_inputs) != 4:
        raise RuntimeError("R37 Delta-surjectivity obligation shape changed")
    hopf = upper_inputs[0]
    lower_image_kernel = upper_inputs[1]
    hopf_inputs = hopf_injectivity_from_zero_image_inputs(hopf)
    if hopf_inputs is None or len(hopf_inputs) != 2:
        raise RuntimeError("R5 Hopf-injectivity obligation shape changed")
    zero_image, hopf_exactness = hopf_inputs
    if (type(zero_image) is not ImageZeroStatement
            or type(lower_image_kernel) is not EHPImageEqualsKernelStatement):
        raise RuntimeError("Typed zero-image or lower EHP obligation changed")

    windows = {
        "root_delta_e": root_inputs[1],
        "root_e_h": root_inputs[2],
        "hopf_e_h": hopf_exactness,
        "lower_h_delta": TodaProp42ExactnessStatement(lower_image_kernel.window),
    }
    expected = {
        "root_delta_e": (6, 12, "delta_e"),
        "root_e_h": (6, 12, "e_h"),
        "hopf_e_h": (5, 11, "e_h"),
        "lower_h_delta": (5, 11, "h_delta"),
    }
    for name, statement in windows.items():
        if (type(statement) is not TodaProp42ExactnessStatement
                or prop42_exactness_indices(statement) != expected[name]):
            raise RuntimeError("The reviewed Prop. 4.2 window changed: " + name)
    values = tuple(windows.values())
    if any(first == second for index, first in enumerate(values)
           for second in values[index + 1:]):
        raise RuntimeError("Distinct EHP windows unexpectedly overlap")

    public = shared_expansion_provider(bridge, proof_target=root)
    exactness_rule_name = "Toda Proposition 4.2: generic consecutive EHP specialization"
    image_kernel_rule_name = "EHP exactness implies image equals kernel"

    def matching(goal: object, name: str, subgoals: tuple):
        return tuple(
            expansion for expansion in public(goal)
            if expansion.rule.name == name and expansion.subgoals == subgoals
        )

    exact_options = {
        name: matching(statement, exactness_rule_name, (universal,))
        for name, statement in windows.items()
    }
    root_options = matching(root, ROOT_RULE, root_inputs)
    upper_options = matching(upper, UPPER_RULE, upper_inputs)
    hopf_options = matching(hopf, HOPF_RULE, hopf_inputs)
    lower_options = matching(
        lower_image_kernel, image_kernel_rule_name,
        (windows["lower_h_delta"],),
    )
    for name, options in (
        ("EHP root", root_options),
        ("upper Delta", upper_options),
        ("Hopf injectivity", hopf_options),
        ("lower image-kernel", lower_options),
    ):
        if len(options) != 1:
            raise RuntimeError("Reviewed public conditional rule changed: " + name)
    if any(len(options) > 1 for options in exact_options.values()):
        raise RuntimeError("Duplicated public Prop. 4.2 specialization candidate")

    # Deliberately exclude the R44 zero-image branch and unexamined providers.
    # The only source leaves remain the actual screened bridge proof links.
    def scoped(goal: object):
        if goal == root:
            return root_options
        if goal == upper:
            return upper_options
        if goal == hopf:
            return hopf_options
        if goal == lower_image_kernel:
            return lower_options
        for name, statement in windows.items():
            if goal == statement:
                return exact_options[name]
        return ()

    result = search_registered_partial_proof(
        n=7, k=5, goal=root, bridge=bridge,
        citing_assertion_id=source_ids[0],
        expansion_provider=scoped, lookup_mode="typed_reference",
    )
    if result.status is ProofSearchStatus.COMPLETE:
        raise RuntimeError("The intentionally restricted R45 proof unexpectedly completed")
    if any(step.conclusion == root for step in result.proven_steps):
        raise RuntimeError("Root was claimed without proving zero image and other goals")
    inferred = {
        name: tuple(
            step for step in result.proven_steps
            if step.conclusion == statement and step.rule is ProofRule.INFERENCE
        )
        for name, statement in windows.items()
    }
    if any(len(steps) > 1 for steps in inferred.values()):
        raise RuntimeError("Duplicate certified exactness steps in bounded proof")
    ancestry = {
        name: (
            len(steps) == 1 and proof_has_general_prop42_ancestor(steps[0])
        )
        for name, steps in inferred.items()
    }
    if any(len(inferred[name]) == 1 and not ancestry[name] for name in windows):
        raise RuntimeError("Inferred exactness has no cited universal source ancestor")
    lower_derived = any(
        step.conclusion == lower_image_kernel and step.rule is ProofRule.INFERENCE
        for step in result.proven_steps
    )
    hopf_derived = any(
        step.conclusion == hopf and step.rule is ProofRule.INFERENCE
        for step in result.proven_steps
    )
    upper_derived = any(
        step.conclusion == upper and step.rule is ProofRule.INFERENCE
        for step in result.proven_steps
    )
    opened = Counter(type(goal).__name__ for goal in result.open_goals)
    return {
        "root": "pi_12^7 = 0",
        "r44_zero_image_inference_is_prior_evidence_not_replayed": True,
        "toda59_screened_source_count": len(r44_source),
        "prop42_cited_universal_source_count": len(cited_universal),
        "prop42_source_reference_ids": [
            bridge.registry.assertion(link.assertion_id).reference_id
            for link in cited_universal
        ],
        "prop42_window_indices": {
            key: list(value) for key, value in expected.items()
        },
        "prop42_public_specialization_candidates": {
            name: len(options) for name, options in exact_options.items()
        },
        "public_root_candidates": len(root_options),
        "public_upper_delta_candidates": len(upper_options),
        "public_hopf_injective_candidates": len(hopf_options),
        "public_lower_image_kernel_candidates": len(lower_options),
        "canonical_scoped_search_status": result.status.value,
        "canonical_scoped_proven_steps": len(result.proven_steps),
        "canonical_scoped_prop42_inference_steps": {
            name: len(steps) for name, steps in inferred.items()
        },
        "canonical_scoped_prop42_has_cited_ancestor": ancestry,
        "canonical_scoped_lower_image_kernel_inferred": lower_derived,
        "canonical_scoped_hopf_injectivity_inferred": hopf_derived,
        "canonical_scoped_upper_delta_surjectivity_inferred": upper_derived,
        "canonical_scoped_open_goal_types": dict(sorted(opened.items())),
        "canonical_scoped_unresolved_goals": len(result.open_goals),
        "zero_image_deliberately_outside_r45_scoped_proof": True,
        "new_givens": 0,
        "production_files_changed": 0,
        "root_complete": False,
        "web_http_checked": False,
        "full_pytest": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    git_state = verify_checkout()
    observation = None if args.dry_run else inspect_open_ehp_obligations()
    if args.dry_run:
        gate = "PASS_R45_R44_MERGE_SOURCE_PREFLIGHT"
    elif (observation["prop42_cited_universal_source_count"] == 1
          and all(value == 1 for value in observation[
              "canonical_scoped_prop42_inference_steps"
          ].values())):
        gate = "PASS_R45_CITED_PROP42_CANONICAL_INFERENCE_ROOT_PENDING"
    elif (observation["prop42_cited_universal_source_count"] == 1
          and all(value == 1 for value in observation[
              "prop42_public_specialization_candidates"
          ].values())):
        gate = "PASS_R45_PUBLIC_PROP42_AVAILABLE_CANONICAL_INFERENCE_PENDING"
    else:
        gate = "PASS_R45_PROP42_SOURCE_OR_PROVIDER_GAP_RECORDED"
    directory = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r45"
    )
    directory.mkdir(parents=True, exist_ok=True)
    filename = "preflight.json" if args.dry_run else "ehp_open_obligations.json"
    report = {"phase": "174-R3-R7-R45", "git": git_state,
              "observation": observation, "gate": gate}
    output = directory / filename
    output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    prefix = "PHASE174_R3R7R45_"
    for key, value in git_state.items():
        print(prefix + key.upper() + "=" + str(value))
    if observation is not None:
        for key, value in observation.items():
            print(prefix + key.upper() + "=" + str(value))
    print(prefix + "REPORT=" + str(output))
    print(prefix + "GATE=" + gate)
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
