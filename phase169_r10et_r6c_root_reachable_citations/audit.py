"""R6C complete-proof root citations / common Definition / Trust audit."""
from __future__ import annotations

import json
from pathlib import Path

from phase169_r10et_r6_residual_definition_dependency_audit.audit import (
    R2_BASELINE, PROBES, REQUIRED, STABLE_TRANSPORT, summarize_dependency,
)
from phase169_r10et_r1_definition_reference_dependency_audit.audit import inspect_case


def audit_real_cases(root: Path, output: Path) -> dict:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge

    baseline_path = root / R2_BASELINE
    base = json.loads(baseline_path.read_text(encoding="utf-8"))
    if base.get("mode") != "AUDIT_ONLY_SHADOW" or not base.get("all_complete_trusted"):
        raise RuntimeError("R2 baseline is not a verified shadow proof")
    reference = {item["group"]: item for item in base["cases"]}
    output.mkdir(parents=True, exist_ok=False)
    bridge = build_shared_typed_bridge()
    cases = []
    for n, k in REQUIRED + PROBES:
        target = f"pi_{n+k}^{n}"
        case = inspect_case(bridge, n, k, output)
        judgment = summarize_dependency(
            case, reference.get(target),
            stable_transport=(n, k) in STABLE_TRANSPORT,
            required=(n, k) in REQUIRED,
        )
        print(f"R10ET_R6C_{target}={'PASS' if judgment['passed'] else 'FAIL'}", flush=True)
        cases.append(judgment)
    success = all(case["passed"] for case in cases)
    pi108 = next(item for item in cases if item["case"] == "pi_10^8")
    if (pi108["reference_locators"] != [
        "DB prior: sphere.csv (n=4, k=2) [参考: Proposition 5.3]", "(4.5)",
    ] or pi108["root_support"][0]["citation_numbers"] != [1]
       or pi108["root_support"][1]["citation_numbers"] != [2]):
        success = False
        pi108["problems"].append("pi_10^8 exact root source/iso provenance changed")
    report = {"phase":"169 R10ET-R6C", "cases":cases,
              "pi108_root_reference_correct":not pi108["problems"], "success":success}
    (output / "audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "audit.md").write_text(
        "# R10ET-R6C — completed root citation audit\n\n"
        + "\n".join(f"- {c['case']}: {'PASS' if c['passed'] else 'FAIL'}"
                    for c in cases) + "\n\n"
        + f"pi_10^8 references: {pi108['reference_locators']}\n"
        + f"all_pass: {success}\n", encoding="utf-8",
    )
    return report
