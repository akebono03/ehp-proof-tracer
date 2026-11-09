"""Read-only public R5/R37/EHP/zero-image frontier, with scoped real search."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r43_public_ehp_map_property_wiring.source_guard import (
    verify_checkout,
)


def inspect_public_ehp_frontier() -> dict[str, object]:
    """Verify the public proposals; do not claim a complete root proof."""
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r2_search_adapter import search_registered_partial_proof
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase169_r10e4_ordered_db_prior.db_prior import admitted_db_step, verified_db_step
    from phase174_r3_r7_r3_ehp_zero_rule.rule import (
        RULE_NAME as ROOT_RULE, ehp_zero_inputs,
    )
    from phase174_r3_r7_r5_zero_image_hopf_injective.rule import (
        RULE_NAME as HOPF_RULE, hopf_injectivity_from_zero_image_inputs,
    )
    from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import (
        RULE_NAME as UPPER_RULE, upper_delta_surjectivity_inputs,
    )
    from phase174_r3_r7_r40_adopted_db_zero_image_isolated.rule import (
        RULE_NAME as ZERO_IMAGE_RULE,
    )
    from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.provider import (
        screened_general_law,
    )
    from proof import ProofRule, ProofStep

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(
        build_shared_typed_bridge(), goal=root,
    )
    source_laws = screened_general_law(bridge)
    if len(source_laws) != 1:
        raise RuntimeError("The cited source law from Toda (5.9) is missing")
    identifiers = tuple(
        link.assertion_id for link in bridge.proof_links
        if (isinstance(link.step, ProofStep)
            and link.step.rule is ProofRule.GIVEN
            and link.step.conclusion == source_laws[0])
    )
    if len(identifiers) != 1:
        raise RuntimeError("The Toda (5.9) source must have one cited assertion")

    root_subgoals = ehp_zero_inputs(root)
    if root_subgoals is None:
        raise RuntimeError("The typed EHP root contract disappeared")
    upper = root_subgoals[0]
    upper_subgoals = upper_delta_surjectivity_inputs(upper)
    if upper_subgoals is None:
        raise RuntimeError("The R37 generic surjectivity rule is not applicable")
    hopf = upper_subgoals[0]
    hopf_subgoals = hopf_injectivity_from_zero_image_inputs(hopf)
    if hopf_subgoals is None:
        raise RuntimeError("The R5 generic injectivity rule is not applicable")
    zero_image = hopf_subgoals[0]
    provider = shared_expansion_provider(bridge, proof_target=root)

    def one(goal: object, rule_name: str, expected: tuple[object, ...]):
        options = tuple(x for x in provider(goal)
                        if x.rule.name == rule_name)
        if len(options) != 1 or options[0].subgoals != expected:
            raise RuntimeError("Public conditional expansion differs: " + rule_name)
        return options[0]

    root_expansion = one(root, ROOT_RULE, root_subgoals)
    upper_expansion = one(upper, UPPER_RULE, upper_subgoals)
    hopf_expansion = one(hopf, HOPF_RULE, hopf_subgoals)
    zero_options = tuple(x for x in provider(zero_image)
                         if x.rule.name == ZERO_IMAGE_RULE)
    if len(zero_options) != 1 or len(zero_options[0].subgoals) != 2:
        raise RuntimeError("R41 adopted DB zero-image rule was lost")
    zero_expansion = zero_options[0]
    db_presentation, generator_zero = zero_expansion.subgoals
    db_step = admitted_db_step(db_presentation, proof_target=root, bridge=bridge)
    if (not isinstance(db_step, ProofStep)
            or db_step.rule is not ProofRule.GIVEN
            or not verified_db_step(db_step, proof_target=root, bridge=bridge)):
        raise RuntimeError("The existing adopted DB prior trust boundary failed")
    if admitted_db_step(db_presentation, proof_target=zero_image, bridge=bridge) is not None:
        raise RuntimeError("Direct map-root DB scope unexpectedly changed")
    if any(link.step is not None
           and link.step.conclusion in (root, upper, hopf, zero_image)
           for link in bridge.proof_links):
        raise RuntimeError("A forbidden direct GIVEN shortcuts the proof chain")

    # A bounded canonical probe observes actual DB admission within the GROUP
    # root scope, but intentionally does not pretend that omitted generator
    # proof branches are a completed proof. No web requests are performed.
    def scoped(candidate: object):
        if candidate == root:
            return (root_expansion,)
        if candidate == upper:
            return (upper_expansion,)
        if candidate == hopf:
            return (hopf_expansion,)
        if candidate == zero_image:
            return (zero_expansion,)
        return ()

    partial = search_registered_partial_proof(
        n=7, k=5, goal=root, bridge=bridge,
        citing_assertion_id=identifiers[0],
        expansion_provider=scoped, lookup_mode="typed_reference",
    )
    if (partial.status not in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)
            or partial.conclusion is not None
            or not any(step.conclusion == db_presentation
                       and step.rule is ProofRule.GIVEN
                       for step in partial.proven_steps)
            or not any(x == generator_zero for x in partial.open_goals)
            or not any(x == upper for x in partial.open_goals)
            or not any(x == root for x in partial.open_goals)):
        raise RuntimeError("Unexpected bounded canonical search observation")

    return {
        "screened_toda59_source_leaves": len(source_laws),
        "public_ehp_root_candidates": 1,
        "public_upper_delta_r37_candidates": 1,
        "public_hopf_injectivity_r5_candidates": 1,
        "public_adopted_db_zero_image_r41_candidates": 1,
        "r37_independent_subgoals": len(upper_subgoals),
        "r5_independent_subgoals": len(hopf_subgoals),
        "root_scoped_db_prior_admitted_by_actual_search": True,
        "direct_zero_image_scope_db_prior_admitted": False,
        "scoped_canonical_search_status": partial.status.value,
        "scoped_canonical_verified_db_prior_steps": sum(
            1 for step in partial.proven_steps
            if step.conclusion == db_presentation and step.rule is ProofRule.GIVEN
        ),
        "scoped_canonical_generator_zero_open": True,
        "r40_isolated_result_not_promoted_to_public_proof": True,
        "new_given_statements": 0,
        "new_mathematical_rules": 0,
        "upper_delta_surjectivity_verified": False,
        "root_complete": False,
        "web_http_checked": False,
        "full_pytest": False,
        "gate": "PASS_R43_PUBLIC_R5_R37_CONDITIONAL_EHP_WIRING_ROOT_PENDING",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    state = verify_checkout()
    details = None if args.dry_run else inspect_public_ehp_frontier()
    folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r43"
    )
    folder.mkdir(parents=True, exist_ok=True)
    dest = folder / ("preflight.json" if args.dry_run else "public_ehp_map_frontier.json")
    gate = "PASS_R43_REVIEWED_R42_PREFLIGHT" if args.dry_run else details["gate"]
    report = {
        "phase": "174-R3-R7-R43", "git_state": state,
        "observed": details, "gate": gate,
    }
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    p = "PHASE174_R3R7R43_"
    for key, value in state.items():
        print(p + key.upper() + "=" + str(value))
    if details is not None:
        for key, value in details.items():
            if key != "gate":
                print(p + key.upper() + "=" + str(value))
    print(p + "REPORT=" + str(dest))
    print(p + "GATE=" + gate)
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
