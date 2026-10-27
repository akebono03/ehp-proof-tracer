"""Targeted, read-only search audit for newly composed generator images."""
from __future__ import annotations

import json
from pathlib import Path

from homotopy_groups import TodaPrimaryGroup
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase169_r10e5_composite_generator_image.rule import (
    component_image_obligations,
)
from phase165_r14_r6_generic_iso import GeneratorImage


OUTPUT = Path(__file__).resolve().parent / "output"
CASES = (
    (14, 6),
    (15, 8),
    (15, 9),
    (14, 7),
    (8, 4),
    (13, 3),
)


def main() -> None:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    bridge = build_shared_typed_bridge()
    results = []
    for n, k in CASES:
        result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
        composite_inferences = tuple(
            step for step in result.proven_steps
            if (step.rule.value == "inference"
                and isinstance(step.conclusion, GeneratorImage)
                and component_image_obligations(step.conclusion) is not None)
        )
        info = {
            "n": n,
            "k": k,
            "status": result.status.value,
            "composite_image_inferences": len(composite_inferences),
            "diagnostics": list(result.diagnostics),
            "unresolved_goal_types": [type(x).__name__ for x in result.open_goals],
        }
        results.append(info)
        print(f"R10E5_pi_{n+k}^{n}_STATUS={info['status']}")
        print(f"R10E5_pi_{n+k}^{n}_COMPOSITE_IMAGES={info['composite_image_inferences']}")
        print(f"R10E5_pi_{n+k}^{n}_OPEN_GOALS={','.join(info['unresolved_goal_types'])}")
    OUTPUT.mkdir(exist_ok=True)
    file = OUTPUT / "audit.json"
    file.write_text(json.dumps({
        "phase": "169 R10E5",
        "cases": results,
        "full_pytest_run": False,
    }, ensure_ascii=False, indent=2) + '\n', encoding="utf-8")
    print("R10E5_AUDIT=" + str(file))
    print("R10E5_FULL_PYTEST_RUN=False")


if __name__ == "__main__":
    main()
