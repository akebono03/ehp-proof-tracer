"""Capture completion/compatibility baselines and a certified partial prefix."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

from phase168_r3_38_frozen_fulltext_audit.audit import capture
from phase168_r3_41e_certified_prefix_reference_audit.audit import run_certified_prefix_case
from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
from web_group_proof import build_standard_web_group_proof_view

PACKAGE = Path(__file__).resolve().parent
OUT = PACKAGE / "output"
CASES = (("pi3_2", 2, 1), ("pi4_3", 3, 1),
         ("pi5_4", 4, 1), ("pi6_5", 5, 1))


def view_text(view):
    return "\n".join("".join(part.value for part in line.segments)
                     if line.segments else line.prefix + (line.statement_latex or "") + line.suffix
                     for line in view.rendered_lines)


def capture_stage(stage: str) -> dict:
    if stage not in ("before", "after"):
        raise ValueError("capture stage must be before or after")
    OUT.mkdir(parents=True, exist_ok=True)
    summary = {"stage": stage, "completed": [], "partial_prefix": {}}
    for name, n, k in CASES:
        narrative, model, view = capture(n, k)
        if view.partial_result:
            raise AssertionError("expected completed proof: " + name)
        data = narrative.encode("utf-8")
        (OUT / f"{name}_{stage}.md").write_bytes(data)
        row = {"case": name, "sha256": hashlib.sha256(data).hexdigest(),
               "steps": len(model.steps), "references": len(model.citations)}
        summary["completed"].append(row)
        print(stage, name, "steps", row["steps"], "refs", row["references"])
    legacy = build_standard_web_group_proof_view(2, 1, citation_source="legacy")
    (OUT / f"legacy_explicit_{stage}.md").write_text(view_text(legacy), encoding="utf-8")
    direct_result = make_partial_proof_result(n=3, k=2, status=ProofSearchStatus.PARTIAL,
                                               open_goals=("unknown",))
    fallback = build_partial_web_group_proof_view(direct_result)
    (OUT / f"direct_fallback_{stage}.md").write_text(view_text(fallback), encoding="utf-8")
    prefix, markdown, view = run_certified_prefix_case()
    missing = prefix["step_inline_citation_audit"]["missing_inline_citation_steps"]
    summary["partial_prefix"] = {
        "steps": prefix["selected_observed_proof_steps"],
        "references": prefix["model_citation_count"],
        "reference_bodies": prefix["citation_body_count"],
        "cited_steps": prefix["step_inline_citation_audit"]["cited_steps"],
        "missing_step_citations": len(missing),
        "reference_issues": prefix["reference_projection"]["issues"],
        "qed_absent": prefix["qed_absent"],
        "goals_kept": prefix["unresolved_goal_kept"],
        "diagnostics_kept": prefix["diagnostics_kept"],
        "audit_reconstruction_only": prefix["not_a_genuine_partial_search"],
    }
    (OUT / f"certified_prefix_{stage}.md").write_text(markdown, encoding="utf-8")
    (OUT / f"certified_prefix_web_{stage}.txt").write_text(view_text(view), encoding="utf-8")
    (OUT / f"capture_{stage}.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(stage, "cited prefix steps", summary["partial_prefix"]["cited_steps"],
          "missing inline citations", len(missing))
    if prefix["reference_projection"]["issues"]:
        raise AssertionError("certified partial prefix has Reference inconsistencies")
    return summary


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: capture before|after")
    capture_stage(sys.argv[1])
