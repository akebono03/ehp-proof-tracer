"""Read-only audit: isolate cited Prop. 4.2 inferences from root DFS blocking.

The R45 first-child stop is audited without rewriting the existing search
order, installing inferred steps, or claiming pi_12^7 has been proved.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r46_prop42_dfs_audit.source_guard import verify_checkout


def inspect_prop42_dfs_frontier() -> dict[str, object]:
    """Observe independent real canonical subproofs and the bounded R45 traversal."""
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase163_r4_registry_bridge import RegistryBridgeResult
    from phase165_r12_r11_prop42_unified import (
        TodaProp42GeneralExactnessStatement,
        build_prop42_specialization_provider,
        prop42_exactness_indices,
    )
    from phase165_r12_r12_ehp_consequences import (
        EHPImageEqualsKernelStatement,
        proof_has_general_prop42_ancestor,
    )
    from phase165_r3_recursive_search import (
        RegisteredGoalUnresolved,
        reconstruct_registered_goal,
    )
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
        build_shared_typed_bridge(), goal=root,
    )
    toda59 = screened_general_law(bridge)
    if len(toda59) != 1:
        raise RuntimeError("The R44 independently cited Toda (5.9) source is missing")
    citing_ids = tuple(
        link.assertion_id for link in bridge.proof_links
        if isinstance(link.step, ProofStep)
        and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == toda59[0]
    )
    if len(citing_ids) != 1:
        raise RuntimeError("R44 source must identify precisely one citation")
    citing_id = citing_ids[0]

    universal = TodaProp42GeneralExactnessStatement()
    prop42_sources = tuple(
        link for link in bridge.proof_links
        if isinstance(link.step, ProofStep)
        and link.step.rule is ProofRule.GIVEN
        and not link.step.premises
        and link.step.conclusion == universal
        and bridge.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
        and bridge.registry.assertion(link.assertion_id).content == universal
        and bridge.registry.reference(
            bridge.registry.assertion(link.assertion_id).reference_id
        ).publication_position is not None
        and getattr(
            getattr(link.step.inference_rule, "literature_reference", None),
            "locator", None,
        ) == "Proposition 4.2 (4.4)"
    )
    if len(prop42_sources) != 1:
        raise RuntimeError("An exact, cited Proposition 4.2 universal source is required")

    root_inputs = ehp_zero_inputs(root)
    if root_inputs is None or len(root_inputs) != 4:
        raise RuntimeError("Typed EHP root expansion changed")
    upper = root_inputs[0]
    upper_inputs = upper_delta_surjectivity_inputs(upper)
    if upper_inputs is None or len(upper_inputs) != 4:
        raise RuntimeError("Typed upper-Delta expansion changed")
    hopf = upper_inputs[0]
    hopf_inputs = hopf_injectivity_from_zero_image_inputs(hopf)
    if hopf_inputs is None or len(hopf_inputs) != 2:
        raise RuntimeError("Typed Hopf injection expansion changed")
    zero_image, hopf_exactness = hopf_inputs
    lower_image_kernel = upper_inputs[1]
    if type(lower_image_kernel) is not EHPImageEqualsKernelStatement:
        raise RuntimeError("Lower image-kernel Goal has changed type")
    windows = {
        "root_delta_e": root_inputs[1],
        "root_e_h": root_inputs[2],
        "hopf_e_h": hopf_exactness,
        "lower_h_delta": TodaProp42ExactnessStatement(lower_image_kernel.window),
    }
    expected_indices = {
        "root_delta_e": (6, 12, "delta_e"),
        "root_e_h": (6, 12, "e_h"),
        "hopf_e_h": (5, 11, "e_h"),
        "lower_h_delta": (5, 11, "h_delta"),
    }
    if any(
        prop42_exactness_indices(window) != expected_indices[name]
        for name, window in windows.items()
    ):
        raise RuntimeError("Reviewed four Prop. 4.2 windows changed")

    public = shared_expansion_provider(bridge, proof_target=root)
    def match(goal: object, rule_name: str, subgoals: tuple):
        return tuple(
            option for option in public(goal)
            if option.rule.name == rule_name and option.subgoals == subgoals
        )

    exact_rule = "Toda Proposition 4.2: generic consecutive EHP specialization"
    exact_options = {
        name: match(window, exact_rule, (universal,))
        for name, window in windows.items()
    }
    root_options = match(root, ROOT_RULE, root_inputs)
    upper_options = match(upper, UPPER_RULE, upper_inputs)
    hopf_options = match(hopf, HOPF_RULE, hopf_inputs)
    lower_options = match(
        lower_image_kernel,
        "EHP exactness implies image equals kernel",
        (windows["lower_h_delta"],),
    )
    if any(len(options) != 1 for options in (
        root_options, upper_options, hopf_options, lower_options,
        *exact_options.values(),
    )):
        raise RuntimeError("A reviewed public Prop. 4.2 or EHP proposal was lost")

    # The exact same R45 scope is used, with the zero-image subproof omitted.
    # A trace observes which child goals the real depth-first engine requests.
    traversal: list[str] = []
    def bounded_r45(goal: object):
        for name, comparison, options in (
            ("root", root, root_options),
            ("upper_delta", upper, upper_options),
            ("hopf_injective", hopf, hopf_options),
            ("lower_image_kernel", lower_image_kernel, lower_options),
        ):
            if type(goal) is type(comparison) and goal == comparison:
                traversal.append(name)
                return options
        for name, comparison in windows.items():
            if type(goal) is type(comparison) and goal == comparison:
                traversal.append(name)
                return exact_options[name]
        if type(goal) is type(zero_image) and goal == zero_image:
            traversal.append("zero_image_outside_scope")
            return ()
        traversal.append(type(goal).__name__)
        return ()

    bounded_result = search_registered_partial_proof(
        n=7, k=5, goal=root, bridge=bridge,
        citing_assertion_id=citing_id,
        expansion_provider=bounded_r45, lookup_mode="typed_reference",
    )
    if any(step.conclusion == root for step in bounded_result.proven_steps):
        raise RuntimeError("Restricted R45 traversal unexpectedly proves the target")

    def only_exactness(goal: object):
        for name, statement in windows.items():
            if type(goal) is type(statement) and goal == statement:
                return exact_options[name]
        if type(goal) is type(lower_image_kernel) and goal == lower_image_kernel:
            return lower_options
        return ()

    # Independently start canonical recursive search *at each actual typed
    # obligation*. These proofs are certified subproofs, not the root proof.
    verified: dict[str, dict[str, object]] = {}
    for name, target in (
        *tuple(windows.items()),
        ("lower_image_kernel", lower_image_kernel),
    ):
        observed: list[ProofStep] = []
        def note(kind: str, goal: object, step: ProofStep | None) -> None:
            if kind == "proved" and isinstance(step, ProofStep):
                observed.append(step)
        try:
            step = reconstruct_registered_goal(
                target, bridge, citing_id, only_exactness,
                lookup_mode="typed_reference", progress_observer=note,
            )
        except RegisteredGoalUnresolved as error:
            verified[name] = {
                "status": "unresolved", "inference": False,
                "general_prop42_ancestor": False,
                "accepted_steps": len(observed),
                "diagnostic": str(error)[:300],
            }
            continue
        inference = (
            isinstance(step, ProofStep)
            and step.rule is ProofRule.INFERENCE
            and type(step.conclusion) is type(target)
            and step.conclusion == target
        )
        ancestor = inference and proof_has_general_prop42_ancestor(step)
        if inference and not ancestor:
            raise RuntimeError("Inferred Prop. 4.2 result lacks cited ancestor")
        verified[name] = {
            "status": "proved" if inference else "not_inferred",
            "inference": inference,
            "general_prop42_ancestor": ancestor,
            "accepted_steps": len(observed),
            "premise_rule_types": [s.rule.value for s in step.premises],
        }

    # Screening out the universal source must prevent exactness specialization.
    screened_without_prop42 = RegistryBridgeResult(
        bridge.registry, bridge.records,
        tuple(link for link in bridge.proof_links
              if link.assertion_id != prop42_sources[0].assertion_id),
    )
    missing_source_provider = build_prop42_specialization_provider(screened_without_prop42)
    absent_candidates = {
        name: len(missing_source_provider(window))
        for name, window in windows.items()
    }
    if any(absent_candidates.values()):
        raise RuntimeError("Prop. 4.2 specialization bypassed the source gate")

    open_types = Counter(type(goal).__name__ for goal in bounded_result.open_goals)
    proof_types = Counter(type(step.conclusion).__name__ for step in bounded_result.proven_steps)
    return {
        "root": "pi_12^7 = 0",
        "source_first_universal_count": len(prop42_sources),
        "cited_prop42_source_reference_id": bridge.registry.assertion(
            prop42_sources[0].assertion_id
        ).reference_id,
        "prop42_public_candidates": {name: len(options) for name, options in exact_options.items()},
        "prop42_when_source_removed": absent_candidates,
        "r45_bounded_status": bounded_result.status.value,
        "r45_bounded_verified_steps": len(bounded_result.proven_steps),
        "r45_bounded_proven_types": dict(sorted(proof_types.items())),
        "r45_bounded_open_goal_types": dict(sorted(open_types.items())),
        "r45_public_provider_visit_trace": traversal,
        "r45_first_unexpanded_subgoal_is_zero_image": (
            "zero_image_outside_scope" in traversal
            and not any(name in traversal for name in windows)
        ),
        "isolated_canonical_subproofs": verified,
        "isolated_proofs_not_added_to_root_search": True,
        "r44_zero_image_not_replayed": True,
        "root_complete": False,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "production_files_changed": 0,
        "web_http_checked": False,
        "full_pytest": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = verify_checkout()
    observed = None if args.dry_run else inspect_prop42_dfs_frontier()
    inferred = () if observed is None else tuple(
        data["inference"] and data["general_prop42_ancestor"]
        for data in observed["isolated_canonical_subproofs"].values()
    )
    if args.dry_run:
        gate = "PASS_R46_REVIEWED_R45R1_SOURCE_PREFLIGHT"
    elif all(inferred) and observed["r45_first_unexpanded_subgoal_is_zero_image"]:
        gate = "PASS_R46_CITED_PROP42_SUBPROOFS_VERIFIED_DFS_ROOT_PENDING"
    else:
        gate = "PASS_R46_PROP42_INFERENCE_OR_DFS_GAP_RECORDED"
    folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r46"
    )
    folder.mkdir(parents=True, exist_ok=True)
    destination = folder / ("preflight.json" if args.dry_run else "prop42_dfs_audit.json")
    destination.write_text(json.dumps(
        {"phase": "174-R3-R7-R46", "state": state,
         "observation": observed, "gate": gate},
        ensure_ascii=False, indent=2,
    ) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R46_"
    for key, value in state.items():
        print(prefix + key.upper() + "=" + str(value))
    if observed is not None:
        for key, value in observed.items():
            print(prefix + key.upper() + "=" + str(value))
    print(prefix + "REPORT=" + str(destination))
    print(prefix + "GATE=" + gate)
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
