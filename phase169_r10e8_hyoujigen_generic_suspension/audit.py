"""Observe group search and cited source scope; never infer proofs from names."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase169_r10e8_hyoujigen_generic_suspension.chapter_vi_reference import (
    build_cited_chapter_vi_family_definitions,
    verified_chapter_vi_source_positions,
)
from proof import ProofRule

HERE = Path(__file__).resolve().parent
CASES = ((15, 8), (15, 9))


def make_report() -> dict:
    """Run only the two formerly partial goals, under the current source bridge."""
    positions = dict(verified_chapter_vi_source_positions())
    cited = build_cited_chapter_vi_family_definitions()
    bridge = build_shared_typed_bridge()
    results = []
    for n, k in CASES:
        result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
        image_steps = tuple(
            step for step in result.proven_steps
            if step.rule is ProofRule.INFERENCE
            and type(step.conclusion).__name__ == "GeneratorImage"
        )
        results.append({
            "target": f"pi_{n+k}^{n}",
            "status": result.status.value,
            "open_goals": [type(goal).__name__ for goal in result.open_goals],
            "inferred_generator_images": len(image_steps),
            "proof_step_count": len(result.proven_steps),
        })
    return {
        "phase": "169 R10E8",
        "source": "Toda Chapter VI adopted transcription, original edition unverified",
        "chapter_vi_checked_positions": positions,
        "registered_chapter_vi_fixed_sources": len(cited.proof_links),
        "inference_engine_changed": False,
        "csv_proves_generator_image": False,
        "full_pytest_run": False,
        "results": results,
    }


def main() -> None:
    result = make_report()
    path = HERE / "output" / "audit.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")
    for case in result["results"]:
        prefix = "R10E8_" + case["target"]
        print(prefix + "_STATUS=" + case["status"])
        print(prefix + "_OPEN=" + ",".join(case["open_goals"]))
        print(prefix + "_INFERRED_GENERATOR_IMAGES="
              + str(case["inferred_generator_images"]))
    print("R10E8_SOURCE_DEFINITIONS="
          + str(result["registered_chapter_vi_fixed_sources"]))
    print("R10E8_INFERENCE_ENGINE_CHANGED=False")
    print("R10E8_CSV_PROVES_GENERATOR_IMAGE=False")
    print("R10E8_AUDIT_JSON=" + str(path))
    print("R10E8_FULL_PYTEST_RUN=False")


if __name__ == "__main__":
    main()
