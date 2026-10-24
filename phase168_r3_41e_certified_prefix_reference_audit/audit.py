"""R3-41E: read-only citation trace audit on a certified proof prefix.

IMPORTANT: The partial state is reconstructed from a genuinely completed proof.
It is NOT a naturally produced PARTIAL search, and is never described as one.
Every included ProofStep is copied by identity from the observed public search.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / "output"

SOURCES = (
    "phase168_r3_3_proof_narrative_model.py",
    "phase168_r3_4_link_bridge.py",
    "phase168_r3_5_model_renderer.py",
    "phase165_r52_r3_web_adapter.py",
    "web_group_proof.py",
)


def select_closed_proof_prefix(complete_result, limit: int = 13) -> tuple:
    """Select a strict, premise-closed prefix of observed non-concluding steps.

    No step is constructed or inferred. Skip candidates whose premises have
    not already been selected; only the real ProofStep objects are returned.
    """
    if type(limit) is not int or limit < 1:
        raise ValueError("limit must be a positive int")
    selected = []
    for step in complete_result.proven_steps:
        if step.conclusion == complete_result.conclusion:
            continue
        if all(any(parent is earlier or parent == earlier for earlier in selected)
               for parent in step.premises):
            selected.append(step)
        if len(selected) == limit:
            break
    if not selected or len(selected) >= len(complete_result.proven_steps):
        raise ValueError("no strict premise-closed proof prefix available")
    return tuple(selected)


def audit_inline_step_sources(model, markdown: str) -> dict:
    """Require each rendered certified step to show its existing citation IDs.

    Reference headings are excluded. A citation appearing somewhere in the
    document is not sufficient; it must be on the associated step line.
    """
    from phase168_r3_41d1_boundary_audit_fix.audit_core import split_narrative_sections

    _, proof = split_narrative_sections(markdown)
    rendered_steps = [line for line in proof.splitlines()
                      if line.startswith("- 与件:") or line.startswith("- 推論:")]
    issues = []
    if len(rendered_steps) != len(model.steps):
        issues.append("RENDERED_STEP_COUNT_MISMATCH")
    gaps = []
    for index, expected in enumerate(model.step_citation_numbers):
        if not expected:
            continue
        line = rendered_steps[index] if index < len(rendered_steps) else ""
        missing = [number for number in expected if f"[R{number}]" not in line]
        if missing:
            gaps.append({
                "step_index": index,
                "step_rule": model.steps[index].rule.value,
                "expected_numbers": list(expected),
                "missing_numbers": missing,
                "displayed_line": line,
            })
    return {
        "steps": len(model.steps),
        "rendered_steps": len(rendered_steps),
        "cited_steps": sum(bool(numbers) for numbers in model.step_citation_numbers),
        "missing_inline_citation_steps": gaps,
        "issues": issues,
    }


def run_certified_prefix_case() -> tuple[dict, str, object]:
    """Construct a marked audit-only incomplete projection of real π4³ steps."""
    from phase165_r52_partial_proof import (
        ProofSearchStatus, make_partial_proof_result,
    )
    from phase168_r3_41d1_boundary_audit_fix.audit import capture_live_case
    from phase168_r3_41d1_boundary_audit_fix.audit_core import (
        audit_citation_projection, split_narrative_sections, web_text,
    )
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view

    completed, screened_bridge, _, _, _ = capture_live_case(3, 1)
    if completed.status is not ProofSearchStatus.COMPLETE:
        raise AssertionError("control search must be genuinely complete")
    observed_prefix = select_closed_proof_prefix(completed)
    if not any(step.rule.value == "given" for step in observed_prefix):
        raise AssertionError("control prefix has no observed GIVEN")
    if not any(step.rule.value == "inference" for step in observed_prefix):
        raise AssertionError("control prefix has no observed inference")
    if not all(any(step is original for original in completed.proven_steps)
               for step in observed_prefix):
        raise AssertionError("a newly constructed ProofStep entered the audit")
    partial = make_partial_proof_result(
        n=3, k=1, status=ProofSearchStatus.PARTIAL,
        proven_steps=observed_prefix,
        open_goals=(completed.conclusion,),
        diagnostics=("監査用再構成: 完成証明の既存 ProofStep の一部のみを使用。実探索の PARTIAL ではない。",),
    )
    model = build_linked_proof_narrative_model(partial, screened_bridge)
    if model.steps != observed_prefix:
        raise AssertionError("model did not retain the real prefix")
    markdown = render_model_backed_narrative_markdown(partial, model)
    view = build_partial_web_group_proof_view(partial, narrative_model=model)
    ref_audit = audit_citation_projection(model, screened_bridge, markdown, view)
    inline = audit_inline_step_sources(model, markdown)
    reference_section, proof_section = split_narrative_sections(markdown)
    if not (model.citations and any(citation.assertion_ids for citation in model.citations)
            and any(citation.statement_bodies for citation in model.citations)):
        raise AssertionError("prefix did not retain certified registered Reference bodies")
    if "□" in markdown or not view.partial_result:
        raise AssertionError("audit-only prefix incorrectly claims completion")
    if "## 未解決 Goal" not in markdown or "## 探索診断" not in markdown:
        raise AssertionError("audit-only incomplete result lost its status")
    if len(ref_audit["citations"]) != len(model.citations):
        raise AssertionError("reference audit lost citations")
    if not all(body["raw_reference_present"] and body["web_reference_present"]
               for citation in ref_audit["citations"] for body in citation["bodies"]):
        raise AssertionError("certified Reference body missing in Web")

    report = {
        "case": "pi4_3_certified_strict_prefix",
        "classification": "AUDIT_ONLY_RECONSTRUCTED_PARTIAL_FROM_REAL_COMPLETE_PROOF",
        "not_a_genuine_partial_search": True,
        "original_status": completed.status.value,
        "displayed_status": partial.status.value,
        "full_control_step_count": len(completed.proven_steps),
        "selected_observed_proof_steps": len(observed_prefix),
        "selected_indices_in_complete": [next(i for i, original in enumerate(completed.proven_steps)
                                      if original is step) for step in observed_prefix],
        "model_citation_count": len(model.citations),
        "registered_assertion_citation_count": sum(bool(c.assertion_ids) for c in model.citations),
        "citation_body_count": sum(len(c.statement_bodies) for c in model.citations),
        "original_proof_steps_not_recreated": True,
        "reference_projection": ref_audit,
        "step_inline_citation_audit": inline,
        "unresolved_goal_kept": "## 未解決 Goal" in proof_section,
        "diagnostics_kept": "## 探索診断" in proof_section,
        "web_is_partial": view.partial_result,
        "qed_absent": "□" not in markdown,
    }
    return report, markdown, view


def main() -> None:
    from phase168_r3_41d1_boundary_audit_fix.audit_core import (
        markdown_reference_text, web_text,
    )
    OUTPUT.mkdir(parents=True, exist_ok=True)
    case, markdown, view = run_certified_prefix_case()
    source_sha256 = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in SOURCES
    }
    report = {
        "phase": "168 R3-41E",
        "mode": "READ_ONLY_CERTIFIED_PREFIX_REFERENCE_LINK_AUDIT",
        "case": case,
        "source_sha256": source_sha256,
        "scope_limits": [
            "The incomplete result is reconstructed from a truly complete search.",
            "No true PARTIAL with retained steps was observed in R3-41D1's five real targets.",
            "All copied steps are original certified ProofStep objects; no inference is added.",
            "The open goal and diagnostics are audit markers, not a real search trace.",
            "This checks shared partial rendering of real cited premises, not real partial search coverage.",
            "No implementation files or mathematical rules were changed.",
            "Full pytest is deferred to the end of Phase 168.",
        ],
    }
    (OUTPUT / "audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUTPUT / "pi4_3_certified_prefix_narrative.md").write_text(markdown, encoding="utf-8")
    (OUTPUT / "pi4_3_certified_prefix_reference.md").write_text(markdown_reference_text(markdown), encoding="utf-8")
    (OUTPUT / "pi4_3_certified_prefix_web.txt").write_text(web_text(view), encoding="utf-8")
    lines = [
        "# Phase 168 R3-41E — 実証済み ProofStep の切り出しによる部分表示監査", "",
        "この部分状態は完成証明から再構成した**監査用の例**であり、実際に失敗した探索結果ではない。", "",
        f"- 元の完全証明: {case['full_control_step_count']} steps",
        f"- 選択した実 ProofStep: {case['selected_observed_proof_steps']} steps",
        f"- Reference: {case['model_citation_count']}件 (登録主張を伴うもの {case['registered_assertion_citation_count']}件)",
        f"- Reference 本文: {case['citation_body_count']}件",
        f"- 引用を持つステップ: {case['step_inline_citation_audit']['cited_steps']}件",
        f"- ステップ本文に引用番号が欠けたもの: {len(case['step_inline_citation_audit']['missing_inline_citation_steps'])}件",
        f"- Reference 投影の問題: {len(case['reference_projection']['issues'])}件", "",
        "## ステップと出典の接続漏れ", "",
    ]
    missing = case['step_inline_citation_audit']['missing_inline_citation_steps']
    if missing:
        for gap in missing:
            lines.append(f"- step {gap['step_index']} ({gap['step_rule']}): 欠落 {gap['missing_numbers']}")
    else:
        lines.append("- この監査例で欠落は観測されなかった。")
    lines.extend(("", "## 監査範囲", "",
                  "- 実検索5例が0ステップだった問題を解消したわけではない。",
                  "- 使用した出典は既存の screened bridge の実リンクだけであり、新しい引用を生成しない。",
                  "- 全体 pytest は実行しない。", ""))
    (OUTPUT / "audit.md").write_text("\n".join(lines), encoding="utf-8")
    bundle = OUTPUT / "review_bundle.zip"
    with ZipFile(bundle, "w", ZIP_DEFLATED) as archive:
        for file in sorted(OUTPUT.iterdir()):
            if file.suffix in (".json", ".md", ".txt"):
                archive.write(file, file.name)
    print("R3-41E READ_ONLY audit complete")
    print("CONTROL_PREFIX_STEPS", case["selected_observed_proof_steps"], "REGISTERED_REFERENCES", case["registered_assertion_citation_count"])
    print("REFERENCE_BODIES", case["citation_body_count"], "MISSING_STEP_INLINE_CITATIONS", len(missing))
    print("REFERENCE_ISSUES", case["reference_projection"]["issues"])
    print("REPORT", OUTPUT / "audit.md")
    print("UPLOAD_BUNDLE", bundle)
    print("Implementation unchanged; full pytest NOT run")


if __name__ == "__main__":
    main()
