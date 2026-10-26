"""Follow-up narrative audit, compared with R3J's prior diagnostics."""
from __future__ import annotations

import json
from pathlib import Path
from phase169_r3j_narrative_boundary_audit.audit import capture_actual_narrative, build_audit


def main() -> None:
    result, model, markdown, view = capture_actual_narrative()
    report = build_audit(result, model, markdown, view)
    out = Path(__file__).resolve().parent / "output"
    out.mkdir(exist_ok=True)
    (out / "pi5_3_after.md").write_text(markdown,encoding="utf-8")
    (out / "pi5_3_after_audit.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    for key, value in (
        ("STATUS", report["status"]),
        ("MODEL_STEPS", report["model_steps"]),
        ("REFERENCE_COUNT", report["citation_count"]),
        ("ENGLISH_LINES", len(report["english_map_property_lines"])),
        ("REPEATED_MATH", len(report["duplicated_math_expressions"])),
        ("PI4_2_REPEATS", report["presentation_diagnostics"]["pi4_2_presentation_mentions"]),
        ("CITATION_COVERAGE", report["all_citations_mentioned"]),
        ("HOPF_TERMINAL", report["presentation_diagnostics"]["terminal_hopf_surjectivity_proven"]),
        ("DELTA_TERMINAL", report["presentation_diagnostics"]["terminal_delta_injectivity_proven"]),
    ):
        print(f"R3K_{key}={value}",flush=True)
    if (report["status"] != "complete" or not report["all_citations_mentioned"]
        or report["english_map_property_lines"]
        or report["presentation_diagnostics"]["pi4_2_presentation_mentions"] != 1
        or not report["presentation_diagnostics"]["terminal_hopf_surjectivity_proven"]
        or not report["presentation_diagnostics"]["terminal_delta_injectivity_proven"]):
        raise AssertionError("R3K narrative acceptance condition unmet")
    print("R3K_AUDIT_PASS=True",flush=True)
    print("REPORT="+str(out/"pi5_3_after_audit.json"),flush=True)


if __name__ == "__main__":
    main()
