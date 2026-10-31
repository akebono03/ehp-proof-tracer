"""Canonical R20R13R2 audit: exactly three named eta equalities in one line."""
from __future__ import annotations

import json
from pathlib import Path

from phase171_r20r13_eta_sentence_layout.audit import run as run_r20r13

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "output"


def run() -> dict[str, object]:
    prior = run_r20r13()
    old_output = HERE.parent / "phase171_r20r13_eta_sentence_layout" / "output" / "web_narrative.md"
    markdown = old_output.read_text(encoding="utf-8")
    if "\n証明\n" not in markdown:
        raise RuntimeError("narrative proof heading missing")
    reference, body = markdown.split("\n証明\n", 1)
    grouped = [line for line in body.splitlines() if line.startswith("[R3]より, $E(")
               and r",\quad E(" in line]
    three = [line for line in grouped if all(term in line for term in (
        r"E(\eta_{2})=\eta_{3}",
        r"E(\eta_{3}^{2})=\eta_{4}^{2}",
        r"E(\eta_{2}^{3})=\eta_{3}^{3}",
    ))]
    if (prior["public_status"] != "complete"
            or prior["reference_count"] != 8
            or len(three) != 1
            or "短完全列となる. 両端" in body
            or r"\operatorname{ord}" not in body
            or r"\neq0" not in body
            or "[R3] Chapter V, i)." not in reference):
        raise RuntimeError("all three certified eta equalities must appear on one cited line")
    report = dict(prior)
    report.update({
        "phase": "171-R20R13R2",
        "correction": "IGNORE_ORPHAN_BLANK_LINES_BETWEEN_CERTIFIED_ETA_EQUATIONS",
        "exact_three_eta_grouped": True,
        "corrected_grouped_line": three[0],
        "renderer_modified_by_correction": False,
        "math_inference_modified": False,
        "full_pytest": False,
        "web_browser_verified": False,
    })
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUTPUT / "web_narrative.md").write_text(markdown, encoding="utf-8")
    print("PHASE171_R20R13R2_PUBLIC_STATUS=" + prior["public_status"], flush=True)
    print("PHASE171_R20R13R2_ETA_GROUPED_THREE=True", flush=True)
    print("PHASE171_R20R13R2_PERIOD_BREAKS=True", flush=True)
    print("PHASE171_R20R13R2_REFERENCES=8", flush=True)
    print("PHASE171_R20R13R2_REPORT=" + str(OUTPUT / "audit.json"), flush=True)
    print("PHASE171_R20R13R2_MARKDOWN=" + str(OUTPUT / "web_narrative.md"), flush=True)
    print("PHASE171_R20R13R2_RESULT=PASS_THREE_ETA_LAYOUT", flush=True)
    return report


if __name__ == "__main__":
    run()
