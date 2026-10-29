"""Verify source-only R2E link in the current pi_6^3 citation screen.

This audit does not claim or construct a completed proof of pi_6^3.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
import traceback

from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase171_r2e_toda53_double_reference import ASSERTION_ID
from proof import ProofRule


def audit() -> int:
    bridge = build_shared_typed_bridge()
    goal_candidates = registered_group_goal_candidates(bridge, n=3, k=3)
    if len(goal_candidates) != 1:
        raise RuntimeError("pi_6^3 must have exactly one typed DB goal")
    goal = goal_candidates[0]
    citing = resolve_specialized_goal_citing_id(bridge, goal)
    if citing != "shared:0:boundary:Proposition 5.6:pi6_3_group_relation":
        raise RuntimeError("unexpected citing goal identity")
    screened = screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    source_id = "shared:12:" + ASSERTION_ID
    assertion = bridge.registry.assertion(source_id)
    reference = bridge.registry.reference(assertion.reference_id)
    steps = tuple(link.step for link in screened.proof_links
                  if link.assertion_id == source_id and link.step is not None)
    if len(steps) != 1 or steps[0].rule is not ProofRule.GIVEN or steps[0].premises:
        raise RuntimeError("R2E double identity not uniquely screened as GIVEN")
    if (steps[0].conclusion != assertion.content
            or reference.locator != "(5.3)"
            or reference.publication_position != 8100):
        raise RuntimeError("R2E source provenance mismatch")
    if any(link.step is not None and link.step.conclusion == goal
           for link in screened.proof_links):
        raise RuntimeError("target group was incorrectly installed as a GIVEN")
    print("PHASE171_R2E_SOURCE=" + json.dumps({
        "locator": reference.locator,
        "assertion_id": source_id,
        "source_position": reference.publication_position,
        "screened_given_count": len(steps),
        "proof_of_target": False,
    }, ensure_ascii=False))
    print("PHASE171_R2E_NO_DIRECT_GROUP_PROOF=True")
    return 0


def main() -> int:
    try:
        return audit()
    except Exception as exc:
        print(f"PHASE171_R2E_AUDIT_ERROR={type(exc).__name__}: {exc}", file=sys.stderr)
        print(traceback.format_exc()[-2200:], file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
