"""Post-patch typed 9-stem search audit; observation never creates evidence."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase169_r10e5_composite_generator_image.rule import component_image_obligations
from phase165_r14_r6_generic_iso import GeneratorImage
from proof import ProofRule

HERE = Path(__file__).resolve().parent
TARGETS = ((13, 9), (15, 9), (15, 8))


def _describe_open(goal: object) -> dict:
    obj = {"type": type(goal).__name__, "repr": repr(goal)}
    if isinstance(goal, GeneratorImage):
        obj["source_generator"] = repr(goal.source_generator)
        obj["target_generator"] = repr(goal.target_generator)
        factors = component_image_obligations(goal)
        if factors is not None:
            obj["factor_obligations"] = [{
                "source": repr(f.source_generator),
                "target": repr(f.target_generator),
            } for f in factors]
    return obj


def audit_case(bridge, n: int, k: int) -> dict:
    result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
    images = [step for step in result.proven_steps
              if step.rule is ProofRule.INFERENCE
              and isinstance(step.conclusion, GeneratorImage)]
    return {
        "target": f"pi_{n+k}^{n}",
        "status": result.status.value,
        "open_goals": [_describe_open(x) for x in result.open_goals],
        "inferred_generator_images": len(images),
        "proven_steps": len(result.proven_steps),
        "complete_claim_from_audit": False,
    }


def main() -> None:
    bridge = build_shared_typed_bridge()
    cases = [audit_case(bridge, n, k) for n, k in TARGETS]
    document = {
        "phase": "169 R10E9", "mode": "FOCUSED_PATCH_AUDIT",
        "source_equations_added": False,
        "mathematical_inference_rules_added": False,
        "csv_names_as_proof": False,
        "full_pytest_run": False,
        "cases": cases,
    }
    output = HERE / "output" / "audit.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for case in cases:
        prefix = "R10E9_" + case["target"]
        print(prefix + "_STATUS=" + case["status"])
        print(prefix + "_OPEN=" + ",".join(x["type"] for x in case["open_goals"]))
        print(prefix + "_INFERRED_GENERATOR_IMAGES=" + str(case["inferred_generator_images"]))
        for x in case["open_goals"]:
            if x["type"] == "GeneratorImage":
                print(prefix + "_OPEN_IMAGE=" + x["source_generator"] + " => " + x["target_generator"])
    print("R10E9_AUDIT_JSON=" + str(output))
    print("R10E9_FULL_PYTEST_RUN=False")


if __name__ == "__main__":
    main()
