"""Run R9 in the local project; does not edit production files."""
from __future__ import annotations

import json

from phase165_r12_r9_ehp_connection import (
    classify_ehp_exactness_windows,
    collect_screened_exactness_windows,
)
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_prop51_claim_order import pi4_3_goal


def main() -> None:
    goal = pi4_3_goal()
    bridge = build_shared_typed_bridge()
    target_ids = (
        a.assertion_id for a in bridge.registry._assertions.values()
        if a.content == goal and "prop5.1:pi4_3" in a.assertion_id
    )
    target_ids = tuple(target_ids)
    if len(target_ids) != 1:
        raise RuntimeError("registered Proposition 5.1 goal is not unique")
    screened = screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=target_ids[0],
    )
    # R7 must be applied by the installed search pipeline, not reconstructed
    # by a permissive local heuristic. These are candidate windows only.
    windows = collect_screened_exactness_windows(screened)
    groups = classify_ehp_exactness_windows(windows)
    result = {
        "phase": "165 R12-R9",
        "mode": "READ_ONLY_EHP_EXACTNESS_WINDOW_AUDIT",
        "citation_screened_window_count": len(windows),
        "window_counts": {k: len(v) for k, v in groups.items()},
        "windows": {
            k: [
                {
                    "assertion_id": w.assertion_id,
                    "source_term": repr(w.source_term),
                    "middle_term": repr(w.middle_term),
                    "target_term": repr(w.target_term),
                } for w in v
            ] for k, v in groups.items()
        },
        "r7_dependency_guard_applied_in_this_audit": False,
        "im_delta_equals_kernel_e_derived": False,
        "im_e_equals_kernel_h_derived": False,
        "specific_kernel_multiple_derived": False,
        "surjectivity_derived": False,
        "pi43_proof_certified": False,
        "full_pytest_run": False,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
