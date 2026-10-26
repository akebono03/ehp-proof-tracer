"""R3K2: read-only audit of the public model-backed pi5_3 Markdown."""
from __future__ import annotations

import json
from pathlib import Path
import re

from phase169_r3j1_narrative_import_isolation.audit import capture_actual_narrative, split_narrative
from phase168_r3_27_typed_statement_projection import element_tex
from phase165_r14_r6_generic_iso import GeneratorImage
from proof import ProofRule

OUTPUT = Path(__file__).resolve().parent / "output"


def audit() -> dict:
    result, model, markdown, view = capture_actual_narrative()
    reference, proof = split_narrative(markdown)
    images = [
        (index, step) for index, step in enumerate(model.steps)
        if isinstance(step.conclusion, GeneratorImage)
        and element_tex(step.conclusion.source_generator) == r"\eta_{2}^{2}"
        and element_tex(step.conclusion.target_generator) == r"\eta_{3}^{2}"
    ]
    refs = {citation.number for citation in model.citations}
    used = {int(item) for item in re.findall(r"\[R(\d+)\]", proof)}
    image_inferred = len(images) == 1 and images[0][1].rule is ProofRule.INFERENCE
    image_premises = len(images[0][1].premises) if images else 0
    heading = "η 系列の定義（Chapter V, i）" in reference
    transport = r"E(\eta_{2}^{2})=\eta_{3}^{2}" in proof
    duplicate_eta = any(
        snippet in proof for snippet in (
            r"[R6]より, $E(\eta_{2})=\eta_{3}$.",
            r"[R6]より, $E(\eta_{3})=\eta_{4}$.",
        )
    )
    status = (
        result.status.value == "complete"
        and view.key == "generic-complete-proof"
        and not view.partial_result
        and model.steps == result.proven_steps
        and len(model.steps) == 26
        and image_inferred and image_premises == 2
        and heading and transport and not duplicate_eta and refs == used
    )
    return {
        "phase": "169-R3K2",
        "mode": "RENDERER_ONLY",
        "status": result.status.value,
        "proof_steps": len(model.steps),
        "reference_count": len(model.citations),
        "proven_eta_squared_image": image_inferred,
        "eta_squared_image_premises": image_premises,
        "eta_squared_transport_visible": transport,
        "duplicate_eta_components_visible": duplicate_eta,
        "source_locator_preserved_in_view": heading,
        "citation_coverage": refs == used,
        "audit_pass": status,
        "markdown": markdown,
    }


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    report = audit()
    (OUTPUT / "pi5_3_r3k2.md").write_text(report.pop("markdown"), encoding="utf-8")
    (OUTPUT / "pi5_3_r3k2_audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    for key, value in report.items():
        print("R3K2_" + key.upper() + "=" + str(value))
    print("R3K2_AUDIT_REPORT=" + str(OUTPUT / "pi5_3_r3k2_audit.json"))
    if not report["audit_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
