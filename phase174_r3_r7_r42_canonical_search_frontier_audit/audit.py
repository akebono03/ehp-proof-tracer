"""Trace genuine R41 candidates versus the still-open EHP root in canonical search.

This is a read-only scoped search probe, NOT an HTTP request or a source proof.
Never substitute R40's manually reconstructed result for a canonical result.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r42_canonical_search_frontier_audit.source_guard import verify_checkout


def inspect_search_frontier() -> dict[str, object]:
    """Explain exactly which typed public branch is absent, without adding rules."""
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r2_search_adapter import search_registered_partial_proof
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase169_r10e4_ordered_db_prior.db_prior import admitted_db_step, verified_db_step
    from phase174_r3_r7_r3_ehp_zero_rule.rule import (
        RULE_NAME as EHP_ZERO_RULE, ehp_zero_inputs,
    )
    from phase174_r3_r7_r5_zero_image_hopf_injective.rule import (
        RULE_NAME as HOPF_RULE, hopf_injectivity_from_zero_image_inputs,
    )
    from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import (
        RULE_NAME as UPPER_RULE, expand_upper_delta_surjectivity,
        upper_delta_surjectivity_inputs,
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
    sources = screened_general_law(bridge)
    if len(sources) != 1:
        raise RuntimeError("Required cited general source is missing")
    citing_ids = tuple(
        link.assertion_id for link in bridge.proof_links
        if isinstance(link.step, ProofStep)
        and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == sources[0]
    )
    if len(citing_ids) != 1:
        raise RuntimeError("Missing unique cited registry link for Toda (5.9)")
    public = shared_expansion_provider(bridge, proof_target=root)
    zero_inputs = ehp_zero_inputs(root)
    if zero_inputs is None:
        raise RuntimeError("Invalid general EHP zero root contract")
    upper = zero_inputs[0]
    upper_inputs = upper_delta_surjectivity_inputs(upper)
    if upper_inputs is None:
        raise RuntimeError("Upper EHP Delta general rule no longer applies")
    hopf = upper_inputs[0]
    hopf_inputs = hopf_injectivity_from_zero_image_inputs(hopf)
    if hopf_inputs is None:
        raise RuntimeError("Hopf injectivity has invalid typed subgoals")
    zero_image = hopf_inputs[0]
    root_candidates = tuple(x for x in public(root) if x.rule.name == EHP_ZERO_RULE)
    public_upper = tuple(x for x in public(upper) if x.rule.name == UPPER_RULE)
    public_hopf = tuple(x for x in public(hopf) if x.rule.name == HOPF_RULE)
    public_zero_image = tuple(x for x in public(zero_image) if x.rule.name == ZERO_IMAGE_RULE)
    isolated_upper = expand_upper_delta_surjectivity(upper)
    if (len(root_candidates) != 1
            or root_candidates[0].subgoals != zero_inputs
            or len(isolated_upper) != 1
            or isolated_upper[0].subgoals != upper_inputs
            or public_upper
            or len(public_zero_image) != 1):
        raise RuntimeError("Observed EHP/R37/R41 provider frontier changed")
    presentation, generator_zero = public_zero_image[0].subgoals
    db = admitted_db_step(presentation, proof_target=root, bridge=bridge)
    if (not isinstance(db, ProofStep)
            or not verified_db_step(db, proof_target=root, bridge=bridge)
            or db.rule is not ProofRule.GIVEN):
        raise RuntimeError("Earlier DB prior admission contract changed")
    # The canonical recursive search currently admits a DB prior using its
    # top-level `goal`, which for a direct ImageZero probe is not a group.
    # This is checked as a boundary and is NOT papered over by a fake step.
    if admitted_db_step(presentation, proof_target=zero_image, bridge=bridge) is not None:
        raise RuntimeError("The direct zero-image DB admission scope changed")

    def scoped_root(candidate):
        if candidate == root:
            return root_candidates
        if candidate == upper:
            return public_upper
        return ()

    partial = search_registered_partial_proof(
        n=7, k=5, goal=root, bridge=bridge,
        citing_assertion_id=citing_ids[0],
        expansion_provider=scoped_root,
        lookup_mode="typed_reference",
    )
    if (partial.status is not ProofSearchStatus.SEARCH_FAILED
            or partial.proven_steps or partial.conclusion is not None
            or not any(x == upper for x in partial.open_goals)
            or not any(x == root for x in partial.open_goals)):
        raise RuntimeError("Scoped canonical search no longer has expected open upper Delta")

    def scoped_zero(candidate):
        return public_zero_image if candidate == zero_image else ()

    zero_probe = search_registered_partial_proof(
        n=7, k=5, goal=zero_image, bridge=bridge,
        citing_assertion_id=citing_ids[0],
        expansion_provider=scoped_zero,
        lookup_mode="typed_reference",
    )
    if (zero_probe.status is not ProofSearchStatus.SEARCH_FAILED
            or zero_probe.proven_steps or zero_probe.conclusion is not None):
        raise RuntimeError("Direct typed-zero probe unexpectedly bypassed its DB boundary")
    return {
        "screened_toda59_sources": len(sources),
        "public_root_ehp_candidates": len(root_candidates),
        "public_upper_delta_r37_candidates": len(public_upper),
        "isolated_upper_delta_r37_candidates": len(isolated_upper),
        "public_hopf_r5_candidates": len(public_hopf),
        "public_zero_image_r41_candidates": len(public_zero_image),
        "zero_image_typed_subgoals": len(public_zero_image[0].subgoals),
        "adopted_db_prior_verified_for_group_root": True,
        "direct_zero_image_goal_admits_db_prior": False,
        "canonical_root_scoped_search_status": partial.status.value,
        "canonical_root_scoped_verified_steps": len(partial.proven_steps),
        "canonical_root_scoped_open_upper_delta": True,
        "canonical_zero_image_scoped_status": zero_probe.status.value,
        "canonical_zero_image_scoped_verified_steps": len(zero_probe.proven_steps),
        "scoped_probe_not_full_web_search": True,
        "new_given_statements": 0,
        "new_math_rules": 0,
        "production_files_changed": 0,
        "upper_delta_surjectivity_proved": False,
        "root_complete": False,
        "web_http_checked": False,
        "full_pytest": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = verify_checkout()
    observed = None if args.dry_run else inspect_search_frontier()
    gate = (
        "PASS_R42_REVIEWED_R41_SOURCE_PREFLIGHT" if args.dry_run else
        "PASS_R42_CANONICAL_SCOPED_SEARCH_UPPER_DELTA_PROVIDER_AND_DB_SCOPE_PENDING"
    )
    report = {"phase": "174-R3-R7-R42", "git_state": state,
              "observed": observed, "gate": gate}
    folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r42"
    )
    folder.mkdir(parents=True, exist_ok=True)
    output = folder / ("preflight.json" if args.dry_run else "canonical_frontier.json")
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R42_"
    for key, value in state.items():
        print(prefix + key.upper() + "=" + str(value))
    if observed is not None:
        for key, value in observed.items():
            print(prefix + key.upper() + "=" + str(value))
    print(prefix + "REPORT=" + str(output))
    print(prefix + "GATE=" + gate)
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
