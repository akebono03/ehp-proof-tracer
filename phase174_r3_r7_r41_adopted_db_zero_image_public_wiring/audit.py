"""Read-only R41 public provider and source-bound zero-image frontier audit."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.source_guard import verified_state


def inspect_public_r41() -> dict[str, object]:
    """Inspect actual public proposals; never label proposals as root proofs."""
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
    from map_property_rules import ImageZeroStatement
    from phase163_r4_registry_bridge import RegistryBridgeResult
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase174_r3_r7_r40_adopted_db_zero_image_isolated.audit import inspect_isolated_zero_image
    from phase174_r3_r7_r40_adopted_db_zero_image_isolated.rule import RULE_NAME
    from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.provider import (
        build_public_adopted_zero_image_provider, screened_general_law,
    )
    from proof import ProofRule, ProofStep, Relation

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    screened = screened_general_law(bridge)
    if len(screened) != 1:
        raise RuntimeError("Cited Toda (5.9) root-scoped source was not screened")
    prior = exact_prior_database_result(5, 5)
    if not isinstance(prior, Relation):
        raise RuntimeError("Reviewed prior cyclic relation unavailable")
    source = prior.lhs
    mapping = TodaSuspensionMap(source, TodaPrimaryGroup(
        source.group_dimension + 1, source.sphere_dimension + 1,
    ))
    zero_image_goal = ImageZeroStatement(mapping)
    public = shared_expansion_provider(bridge, proof_target=root)
    selected = tuple(x for x in public(zero_image_goal) if x.rule.name == RULE_NAME)
    if len(selected) != 1:
        raise RuntimeError("One R40-based R41 public option required")
    if selected[0].subgoals[0] != prior or len(selected[0].subgoals) != 2:
        raise RuntimeError("R41 lost exact earlier DB presentation/zero-generator obligations")
    isolated = build_public_adopted_zero_image_provider(bridge=bridge, proof_target=root)
    direct = isolated(zero_image_goal)
    if tuple((x.rule.name, x.subgoals) for x in direct) != tuple(
        (x.rule.name, x.subgoals) for x in selected
    ):
        raise RuntimeError("R41 public option differs from isolated source-screened adapter")
    # Changing a target or stripping cited proof links must fail closed.
    naked = RegistryBridgeResult(bridge.registry, bridge.records, ())
    if build_public_adopted_zero_image_provider(
        bridge=naked, proof_target=root,
    )(zero_image_goal):
        raise RuntimeError("R41 accepted a bridge without cited source steps")
    if build_public_adopted_zero_image_provider(
        bridge=bridge, proof_target=TodaPrimaryGroupZeroStatement(source),
    )(zero_image_goal):
        raise RuntimeError("R41 admitted a self-citing/earlier root")
    if build_public_adopted_zero_image_provider(
        bridge=bridge, proof_target=None,
    )(zero_image_goal):
        raise RuntimeError("R41 admitted an untyped target")
    cited_steps = tuple(x.step for x in bridge.proof_links if isinstance(x.step, ProofStep))
    if any(s.conclusion in (zero_image_goal, root) for s in cited_steps):
        raise RuntimeError("Forbidden direct zero-image or final-root GIVEN")
    if any(s.rule is not ProofRule.GIVEN for s in cited_steps):
        raise RuntimeError("Source registration contains improper inference leaf")
    preserved = inspect_isolated_zero_image()
    if (preserved["isolated_zero_image_proved"] is not True
            or preserved["db_given_preserved_inside_proof_tree"] is not True
            or preserved["root_complete"] is not False):
        raise RuntimeError("R40 genuine proof ancestry not preserved")
    return {
        "screened_cited_source_locator": "(5.9)",
        "screened_source_leaves": len(screened),
        "public_r41_zero_image_proposals": len(selected),
        "public_r41_subgoals": len(selected[0].subgoals),
        "source_bound_prior_group_matches": True,
        "r40_isolated_zero_image_verified": True,
        "r40_db_given_preserved": True,
        "source_missing_rejected": True,
        "self_citing_root_rejected": True,
        "untyped_root_rejected": True,
        "new_given_statements": 0,
        "new_mathematical_rules": 0,
        "new_root_given_statements": 0,
        "public_provider_connected": True,
        "public_zero_image_root_verified_by_this_audit": False,
        "upper_delta_surjectivity_verified": False,
        "root_complete": False,
        "web_http_checked": False,
        "full_pytest": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = verified_state()
    observed = None if args.dry_run else inspect_public_r41()
    gate = ("PASS_R41_REVIEWED_SOURCE_PREFLIGHT" if args.dry_run else
            "PASS_R41_VERIFIED_ADOPTED_DB_ZERO_IMAGE_PUBLIC_PROVIDER_CONNECTED_ROOT_PENDING")
    result = {"phase": "174-R3-R7-R41", "source_guard": state,
              "observations": observed, "gate": gate}
    folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r41"
    )
    folder.mkdir(parents=True, exist_ok=True)
    output = folder / ("preflight.json" if args.dry_run else "public_zero_image_provider.json")
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    p = "PHASE174_R3R7R41_"
    for key, value in state.items():
        print(p + key.upper() + "=" + str(value))
    if observed is not None:
        for key, value in observed.items():
            print(p + key.upper() + "=" + str(value))
    print(p + "REPORT=" + str(output))
    print(p + "GATE=" + gate)
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
