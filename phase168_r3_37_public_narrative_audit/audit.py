"""R3-37: capture ordinary Web output without modifying production functions."""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import phase168_r3_5_model_renderer as renderer
from web_group_proof import build_standard_web_group_proof_view


CASES = ((2, 1), (3, 1), (4, 1))


def capture_case(n: int, k: int) -> dict:
    captured = []
    original = renderer.render_model_backed_narrative_markdown

    def record(result, model):
        markdown = original(result, model)
        captured.append((markdown, model))
        return markdown

    with patch.object(renderer, "render_model_backed_narrative_markdown", side_effect=record):
        view = build_standard_web_group_proof_view(n=n, k=k)
    if len(captured) != 1:
        raise AssertionError(f"Expected one common model renderer call, got {len(captured)} for {(n,k)}")
    markdown, model = captured[0]
    references = []
    for citation in model.citations:
        references.append({
            "number": citation.number,
            "locator": citation.reference.locator or citation.reference.label,
            "assertion_ids": list(citation.assertion_ids),
            "reference_ids": list(citation.reference_ids),
            "step_indices": list(citation.step_indices),
        })
    sections = markdown.split("証明", 1)
    return {
        "target": f"pi_{n+k}^{n}",
        "public_mode": view.mode,
        "model_render_calls": len(captured),
        "reference_section": sections[0],
        "proof_section": sections[1] if len(sections) > 1 else "",
        "references": references,
        "markdown": markdown,
        "missing_registered_ids": [
            f'R{ref["number"]}' for ref in references if not ref["assertion_ids"]
        ],
    }


def main():
    output = Path(__file__).resolve().parent / "output"
    output.mkdir(exist_ok=True)
    entries = []
    for n, k in CASES:
        report = capture_case(n, k)
        entries.append(report)
        (output / f'pi_{n+k}_{n}_narrative.md').write_text(report["markdown"], encoding="utf-8")
        print(report["target"], "references=", len(report["references"]),
              "missing_ids=", report["missing_registered_ids"],
              "reference_lines=", len(report["reference_section"].splitlines()),
              "proof_lines=", len(report["proof_section"].splitlines()))
    (output / "audit.json").write_text(
        json.dumps({"mode": "AUDIT_ONLY", "cases": entries}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print("AUDIT_ONLY: existing repository files unchanged.")
    print("FULL_MARKDOWN:", output)
    print("NOTE: Baseline wording is not automatically certified; compare saved markdown against fixed criteria.")


if __name__ == "__main__":
    main()
