"""Phase 169 R3J: read-only audit of the completed pi_5^3 model narrative.

All evidence is collected from the standard public Web entry. This module never
adds source claims, patches production files, or rewrites mathematical output.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
from unittest.mock import patch

from phase165_r52_partial_proof import ProofSearchStatus
from proof import ProofRule
from web_group_proof import build_standard_web_group_proof_view
import phase168_r3_5_model_renderer as model_renderer
from phase168_r3_27_typed_statement_projection import typed_sentence
from web_group_proof_common import _group_proof_statement_latex

ROOT = Path(__file__).resolve().parent
ENGLISH_TOKENS = (
    "is surjective", "is injective", "is the zero map", "is an isomorphism",
    "is exact", "is zero",
)


def capture_actual_narrative():
    """Capture the exact canonical Web route and its searched proof/model."""
    captures = []
    genuine = model_renderer.render_model_backed_narrative_markdown

    def capture(result, model):
        markdown = genuine(result, model)
        captures.append((result, model, markdown))
        return markdown

    with patch.object(
        model_renderer, "render_model_backed_narrative_markdown", side_effect=capture,
    ):
        view = build_standard_web_group_proof_view(
            n=3, k=2, mode="narrative", citation_source="model",
        )
    if len(captures) != 1:
        raise AssertionError(
            "standard Web route must use one common Model renderer: "
            + str(len(captures))
        )
    result, model, markdown = captures[0]
    if (result.status is not ProofSearchStatus.COMPLETE
            or view.partial_result
            or view.key != "generic-complete-proof"
            or model.root_index is None):
        raise AssertionError("pi5_3 must have a searched, model-backed complete root")
    if model.steps != result.proven_steps:
        raise AssertionError("narrative model does not match the actual ProofSteps")
    return result, model, markdown, view


def split_narrative(markdown):
    """Split the actual rendered text, preserving source citations and formulas."""
    start = markdown.find("使用する結果")
    proof = markdown.find("証明", start + len("使用する結果")) if start >= 0 else -1
    if start < 0 or proof < 0:
        raise ValueError("standard narrative is missing Reference or Proof sections")
    return (
        markdown[start + len("使用する結果"):proof].strip(),
        markdown[proof + len("証明"):].strip(),
    )


def _inline_math_counts(proof):
    expressions = re.findall(r"(?<!\\)\$([^\n$]+)\$", proof)
    canonical = [re.sub(r"\s+", "", value) for value in expressions]
    counts = Counter(canonical)
    repeated = sorted(
        ({"formula": value, "count": number} for value, number in counts.items()
         if number > 1),
        key=lambda item: (-item["count"], item["formula"]),
    )
    return repeated


def _step_report(model):
    rows = []
    for i, step in enumerate(model.steps):
        latex, fallback = _group_proof_statement_latex(step.conclusion)
        try:
            candidate = typed_sentence(step.conclusion, step)
        except (TypeError, ValueError, AttributeError) as exc:
            candidate = None
            typed_error = type(exc).__name__ + ": " + str(exc)
        else:
            typed_error = None
        rows.append({
            "step_index": i,
            "rule": step.rule.value,
            "statement_type": type(step.conclusion).__name__,
            "premise_count": len(step.premises),
            "citation_numbers": list(model.step_citation_numbers[i]),
            "latex": latex,
            "fallback": fallback,
            "typed_japanese_candidate": candidate,
            "typed_candidate_error": typed_error,
            "is_root": i == model.root_index,
        })
    return rows


def build_audit(result, model, markdown, view):
    """Describe anomalies without turning display preferences into proof facts."""
    reference, proof = split_narrative(markdown)
    numbers = sorted({int(n) for n in re.findall(r"\[R(\d+)\]", proof)})
    citations = [
        {
            "number": citation.number,
            "locator": citation.reference.locator or citation.reference.label,
            "assertion_ids": list(citation.assertion_ids),
            "reference_ids": list(citation.reference_ids),
            "body_count": len(citation.statement_bodies),
            "statement_bodies": list(citation.statement_bodies),
            "step_indices": list(citation.step_indices),
            "mentioned_in_proof": citation.number in numbers,
        }
        for citation in model.citations
    ]
    lines = proof.splitlines()
    english = [
        {"line": i + 1, "text": line, "tokens": [t for t in ENGLISH_TOKENS if t in line]}
        for i, line in enumerate(lines, start=0)
        if any(t in line for t in ENGLISH_TOKENS)
    ]
    unsupported = [
        {"line": i + 1, "text": line}
        for i, line in enumerate(lines) if "数式表示未対応" in line
    ]
    steps = _step_report(model)
    summaries = {
        "pi4_2_presentation_mentions": len(re.findall(
            r"\\pi_\{4\}\^\{2\}\s*=\s*\\mathbb\{Z\}/2", proof
        )),
        "reference_eta_family_heading": any(
            "Chapter V, i)" in c["locator"] for c in citations
        ),
        "visible_eta_suspension_lines": [
            line for line in lines if "E(\\eta_{2})" in line
            or "E(\\eta_{3})" in line
        ],
        "explicit_eta_squared_transport": "E(\\eta_{2}^{2})" in proof,
        "terminal_hopf_surjectivity_proven": any(
            row["statement_type"] == "TodaHopfInvariantSurjectiveStatement"
            and row["rule"] == ProofRule.INFERENCE.value for row in steps
        ),
        "terminal_delta_injectivity_proven": any(
            row["statement_type"] == "TodaDeltaInjectiveStatement"
            and row["rule"] == ProofRule.INFERENCE.value for row in steps
        ),
    }
    return {
        "phase": "169-R3J",
        "mode": "AUDIT_ONLY",
        "target": "pi_5^3",
        "status": result.status.value,
        "proven_steps": len(result.proven_steps),
        "model_steps": len(model.steps),
        "root_index": model.root_index,
        "web_key": view.key,
        "web_partial": view.partial_result,
        "citation_count": len(citations),
        "citations": citations,
        "proof_citation_numbers": numbers,
        "all_citations_mentioned": all(c["mentioned_in_proof"] for c in citations),
        "reference_section_line_count": len(reference.splitlines()),
        "proof_section_line_count": len(lines),
        "english_map_property_lines": english,
        "unrenderable_lines": unsupported,
        "duplicated_math_expressions": _inline_math_counts(proof),
        "presentation_diagnostics": summaries,
        "step_diagnostics": steps,
        "limitations": [
            "Display anomalies do not invalidate or certify mathematical inferences.",
            "This audit never modifies ProofStep, Narrative Model, citation positions, or renderer.",
            "A source heading must not be removed without separate citation-coverage verification.",
            "Eta-squared transport must not be inserted without a typed proof ancestor.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description="Read-only pi_5^3 narrative audit")
    parser.add_argument("--output", type=Path, default=ROOT / "output")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    result, model, markdown, view = capture_actual_narrative()
    report = build_audit(result, model, markdown, view)
    (args.output / "pi5_3_current.md").write_text(markdown, encoding="utf-8")
    (args.output / "pi5_3_narrative_audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("PHASE=169-R3J AUDIT_ONLY=True")
    print("STATUS=" + report["status"])
    print("MODEL_STEPS=" + str(report["model_steps"]))
    print("REFERENCE_COUNT=" + str(report["citation_count"]))
    print("ENGLISH_LINES=" + str(len(report["english_map_property_lines"])))
    print("REPEATED_MATH=" + str(len(report["duplicated_math_expressions"])))
    print("PI4_2_REPEATS=" + str(report["presentation_diagnostics"]["pi4_2_presentation_mentions"]))
    print("ETA_REFERENCE_HEADING=" + str(report["presentation_diagnostics"]["reference_eta_family_heading"]))
    print("ETA_SQUARED_TRANSPORT_VISIBLE=" + str(report["presentation_diagnostics"]["explicit_eta_squared_transport"]))
    print("CITATION_COVERAGE=" + str(report["all_citations_mentioned"]))
    print("REPORT=" + str(args.output / "pi5_3_narrative_audit.json"))
    print("MARKDOWN=" + str(args.output / "pi5_3_current.md"))
    print("R3J_AUDIT_COMPLETE: no repository files modified")


if __name__ == "__main__":
    main()
