"""Read-only full-text comparison with the frozen Phase 168 narrative originals."""
from __future__ import annotations

import difflib
import hashlib
import json
import re
from pathlib import Path
from unittest.mock import patch

import phase168_r3_5_model_renderer as renderer
from web_group_proof import build_standard_web_group_proof_view

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "output"
CASES = (
    ("pi3_2", 2, 1),
    ("pi4_3", 3, 1),
    ("pi5_4", 4, 1),
)
BASELINE_DIRS = (
    ROOT / "phase168_narrative_baseline_frozen",
    ROOT / "phase168_frozen_v1",
    ROOT / "phase168_r3_34_fulltext_reaudit" / "baselines",
)


def sections(text):
    text = re.sub(r"(?m)^\d{3} ", "", text)
    a = text.find("使用する結果")
    b = text.find("証明", a + len("使用する結果")) if a >= 0 else -1
    if a < 0 or b < 0:
        raise ValueError("Missing Reference or proof section")
    return (
        text[a+len("使用する結果"):b].strip(),
        text[b+len("証明"):].strip(),
    )


def normalized_for_diff(text):
    # Strip only historical line indexes and ordinary empty-line differences.
    text = re.sub(r"(?m)^\d{3} ", "", text)
    return "\n".join(line.rstrip() for line in text.splitlines() if line.strip())


def baseline_path(name):
    for base in BASELINE_DIRS:
        candidate = base / (name + "_original.txt")
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(
        "Frozen original is missing: " + name +
        ". Expected phase168_narrative_baseline_frozen or phase168_frozen_v1."
    )


def capture(n, k):
    samples = []
    original = renderer.render_model_backed_narrative_markdown

    def capture_renderer(result, model):
        value = original(result, model)
        samples.append((value, model))
        return value

    with patch.object(renderer, "render_model_backed_narrative_markdown", side_effect=capture_renderer):
        view = build_standard_web_group_proof_view(n=n, k=k)
    if len(samples) != 1:
        raise AssertionError("Expected one common Model Renderer call")
    return samples[0][0], samples[0][1], view


def compare(name,n,k):
    path = baseline_path(name)
    raw = path.read_bytes()
    original = raw.decode("utf-8-sig")
    current, model, view = capture(n,k)
    baseline_ref, baseline_proof = sections(original)
    current_ref, current_proof = sections(current)
    (OUT/(name+"_current.md")).write_text(current,encoding="utf-8")
    comparisons={}
    for section, before, after in (
        ("reference",baseline_ref,current_ref),
        ("proof",baseline_proof,current_proof),
    ):
        diff = "".join(difflib.unified_diff(
            normalized_for_diff(before).splitlines(keepends=True),
            normalized_for_diff(after).splitlines(keepends=True),
            fromfile=name+"_frozen_"+section,
            tofile=name+"_current_"+section,
        ))
        (OUT/(name+"_"+section+".diff")).write_text(diff,encoding="utf-8")
        comparisons[section]={
            "exact_after_line_cleanup": not bool(diff),
            "difference_line_count":len(diff.splitlines()),
            "diff_file":name+"_"+section+".diff",
        }
    refs=[
        {
            "locator":citation.reference.locator or citation.reference.label,
            "number":citation.number,
            "assertion_ids":list(citation.assertion_ids),
            "body_count":len(citation.statement_bodies),
            "bodies":list(citation.statement_bodies),
        } for citation in model.citations
    ]
    return {
        "name":name,
        "baseline_path":str(path),
        "baseline_sha256":hashlib.sha256(raw).hexdigest(),
        "rendered_step_count":len(model.steps),
        "web_partial":view.partial_result,
        "reference_entries":refs,
        "comparison":comparisons,
        "observations":{
            "all_reference_entries_have_body":all(x["body_count"]>0 for x in refs),
            "toda45_specialization_literal":("(n,m,k)=(3,4,1)" in current_proof),
            "pi54_specific_iso_literal":(r"E: \pi_{4}^{3}\to \pi_{5}^{4}" in current_proof),
            "complete_sequence_count":current_proof.count("次の完全列を考える"),
        },
        "caveats":[
            "Differences are textual; a diff alone cannot certify mathematical equivalence.",
            "Reference numbering and its order are not frozen by BASELINE_POLICY.",
            "The mathematical generality and indexing of Proposition 4.2 require separate source verification.",
        ],
    }


def main():
    OUT.mkdir(exist_ok=True)
    cases=[compare(name,n,k) for name,n,k in CASES]
    report={"mode":"AUDIT_ONLY","status":"DIFFERENCES_REPORTED","cases":cases}
    (OUT/"audit.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    for c in cases:
        print(c["name"],
              "REFERENCE_DIFF_LINES",c["comparison"]["reference"]["difference_line_count"],
              "PROOF_DIFF_LINES",c["comparison"]["proof"]["difference_line_count"],
              "REF_BODIES_COMPLETE",c["observations"]["all_reference_entries_have_body"])
    print("AUDIT_ONLY: no repository code or frozen originals modified")
    print("REPORT:",OUT/"audit.json")


if __name__=="__main__":
    main()
