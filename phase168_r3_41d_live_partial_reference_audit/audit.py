"""Read-only audit of real, live Web search results and their explicit citations.

A search yielding no relevant proof evidence is reported as unobserved coverage,
not fabricated or counted as a successful cited partial proof.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from unittest.mock import patch
from zipfile import ZIP_DEFLATED, ZipFile

from phase168_r3_41d_live_partial_reference_audit.audit_core import (
    audit_citation_projection,
    markdown_reference_text,
    section_bullets,
    web_text,
)

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / "output"
# All are real standard-Web searches; the final known complete case is a
# control for comparison with citation-bearing complete proofs.
CASES = (
    ("pi6_4", 4, 2),
    ("pi6_3", 3, 3),
    ("pi7_5", 5, 2),
    ("pi7_4", 4, 3),
    ("pi8_5", 5, 3),
    ("pi4_3_control", 3, 1),
)
SOURCES = (
    "phase165_r55_nk_only_goal.py",
    "phase168_r3_4_link_bridge.py",
    "phase168_r3_3_proof_narrative_model.py",
    "phase168_r3_5_model_renderer.py",
    "phase165_r52_r3_web_adapter.py",
    "web_group_proof.py",
)


def capture_live_case(n: int, k: int):
    """Capture the genuine screened bridge and renderer in one public search."""
    import phase168_r3_4_link_bridge as linked
    import phase168_r3_5_model_renderer as renderer
    from web_group_proof import build_standard_web_group_proof_view

    original_link = linked.build_linked_proof_narrative_model
    original_render = renderer.render_model_backed_narrative_markdown
    linked_samples = []
    rendered_samples = []

    def record_link(result, bridge):
        model = original_link(result, bridge)
        linked_samples.append((result, bridge, model))
        return model

    def record_render(result, model):
        text = original_render(result, model)
        rendered_samples.append((result, model, text))
        return text

    with patch.object(linked, "build_linked_proof_narrative_model", side_effect=record_link), \
         patch.object(renderer, "render_model_backed_narrative_markdown", side_effect=record_render):
        view = build_standard_web_group_proof_view(n=n, k=k, mode="narrative")

    if len(linked_samples) != 1 or len(rendered_samples) != 1:
        raise RuntimeError(
            "Expected exactly one common model and renderer invocation, got "
            + f"{len(linked_samples)}/{len(rendered_samples)}")
    result, bridge, model = linked_samples[0]
    rendered_result, rendered_model, markdown = rendered_samples[0]
    if result is not rendered_result or model is not rendered_model:
        raise AssertionError("The public Web route did not render the captured result/model")
    return result, bridge, model, markdown, view


def one_case(name: str, n: int, k: int) -> dict:
    from phase165_r52_partial_proof import ProofSearchStatus

    try:
        result, bridge, model, markdown, view = capture_live_case(n, k)
        (OUTPUT / f"{name}_reference.md").write_text(
            markdown_reference_text(markdown), encoding="utf-8")
        (OUTPUT / f"{name}_narrative.md").write_text(markdown, encoding="utf-8")
        (OUTPUT / f"{name}_web.txt").write_text(web_text(view), encoding="utf-8")
        citations = audit_citation_projection(model, bridge, markdown, view)
        goal_section, goals = section_bullets(markdown, "未解決 Goal")
        diagnostic_section, diagnostics = section_bullets(markdown, "探索診断")
        incomplete = result.status is not ProofSearchStatus.COMPLETE
        source_and_state_issues = []
        if model.steps != result.proven_steps:
            source_and_state_issues.append("MODEL_PROOF_STEPS_DO_NOT_MATCH_RESULT")
        if model.status is not result.status or model.target != result.target:
            source_and_state_issues.append("MODEL_STATUS_OR_TARGET_MISMATCH")
        if model.open_goals != result.open_goals:
            source_and_state_issues.append("MODEL_OPEN_GOALS_MISMATCH")
        if model.diagnostics != result.diagnostics:
            source_and_state_issues.append("MODEL_DIAGNOSTICS_MISMATCH")
        if view.partial_result != incomplete:
            source_and_state_issues.append("WEB_PARTIAL_FLAG_MISMATCH")
        if incomplete:
            if "□" in markdown:
                source_and_state_issues.append("INCOMPLETE_PROOF_HAS_QED")
            if "探索状態：" not in web_text(view):
                source_and_state_issues.append("SEARCH_STATUS_NOT_IN_WEB")
            if result.open_goals and (not goal_section or len(goals) != len(result.open_goals)):
                source_and_state_issues.append("OPEN_GOALS_NOT_FULLY_RENDERED")
            if result.diagnostics and (
                not diagnostic_section or len(diagnostics) != len(result.diagnostics)
            ):
                source_and_state_issues.append("DIAGNOSTICS_NOT_FULLY_RENDERED")
            headings = [line.prefix for line in view.rendered_lines
                        if line.kind == "heading"]
            if result.open_goals and "未解決 Goal" not in headings:
                source_and_state_issues.append("OPEN_GOAL_HEADING_MISSING_FROM_WEB")
            if result.diagnostics and "探索診断" not in headings:
                source_and_state_issues.append("DIAGNOSTIC_HEADING_MISSING_FROM_WEB")
        elif not markdown.rstrip().endswith("□"):
            source_and_state_issues.append("COMPLETE_PROOF_LACKS_QED")

        steps = []
        for index, step in enumerate(model.steps):
            steps.append({
                "index": index,
                "rule": step.rule.value,
                "conclusion_type": type(step.conclusion).__name__,
                "conclusion_excerpt": str(step.conclusion)[:240],
                "inference_name": (step.inference_rule.name if step.inference_rule else None),
                "citation_numbers": list(model.step_citation_numbers[index]),
                "premise_count": len(step.premises),
            })
        status = result.status.value
        row = {
            "name": name, "n": n, "k": k, "status": status,
            "status_is_incomplete": incomplete,
            "search_step_count": len(result.proven_steps),
            "given_step_count": sum(step.rule.value == "given" for step in result.proven_steps),
            "open_goal_count": len(result.open_goals),
            "diagnostic_count": len(result.diagnostics),
            "citation_count": len(model.citations),
            "registered_citation_count": sum(bool(c.assertion_ids) for c in model.citations),
            "reference_with_body_count": sum(bool(c.statement_bodies) for c in model.citations),
            "web_partial_result": view.partial_result,
            "model_premise_steps": steps,
            "citation_projection": citations,
            "state_issues": sorted(set(source_and_state_issues)),
            "capture_error": None,
        }
        print(name, "status", status, "steps", len(result.proven_steps),
              "refs", len(model.citations), "bodies", row["reference_with_body_count"],
              "open_goals", len(result.open_goals), "state_issues", len(source_and_state_issues),
              "citation_issues", len(citations["issues"]))
        return row
    except Exception as exc:
        error = type(exc).__name__ + ": " + str(exc)
        print(name, "CAPTURE_ERROR", error)
        return {"name": name, "n": n, "k": k, "capture_error": error}


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    cases = [one_case(name, n, k) for name, n, k in CASES]
    successful = [case for case in cases if case["capture_error"] is None]
    if not successful:
        raise RuntimeError("All real public searches failed; no audit evidence obtained")
    live_partial = [case for case in successful
                    if case["status_is_incomplete"] and case["name"] != "pi4_3_control"]
    cited_partial = [case for case in live_partial if case["citation_count"]]
    stepped_partial = [case for case in live_partial if case["search_step_count"]]
    registered_partial = [case for case in live_partial if case["registered_citation_count"]]
    body_partial = [case for case in live_partial if case["reference_with_body_count"]]
    unresolved_issues = sorted({issue for case in successful
                                for issue in case["state_issues"]
                                + case["citation_projection"]["issues"]})
    source_hashes = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in SOURCES
    }
    report = {
        "phase": "168 R3-41D",
        "mode": "READ_ONLY_REAL_SEARCH_REFERENCE_AUDIT",
        "source_sha256": source_hashes,
        "cases": cases,
        "coverage": {
            "real_search_attempts": len(CASES) - 1,
            "real_search_successful": len([case for case in successful
                                           if case["name"] != "pi4_3_control"]),
            "actual_incomplete_cases": len(live_partial),
            "actual_incomplete_with_steps": len(stepped_partial),
            "actual_incomplete_with_any_citation": len(cited_partial),
            "actual_incomplete_with_registered_citation": len(registered_partial),
            "actual_incomplete_with_reference_body": len(body_partial),
            "live_cited_partial_proven": bool(cited_partial),
        },
        "observed_issues": unresolved_issues,
        "scope_limits": [
            "No mathematical conclusion or reference is inferred from a goal.",
            "Samples are real Web searches, not a complete census of 112 targets.",
            "A zero-citation incomplete result does not validate partial citation rendering.",
            "A reference heading with no body is counted as a content gap.",
            "A standalone rule reference and a registered assertion are distinguished.",
            "This audit neither changes implementation nor runs full pytest.",
        ],
    }
    (OUTPUT / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    table = [
        "# Phase 168 R3-41D — 実探索の Reference・Narrative 監査", "",
        "読み取り専用。使用された ProofStep と screened bridge、Model、Web 表示を同時に確認する。", "",
        "| 対象 | 状態 | 証明 Step | Reference | 本文あり | Goal | 表示・引用の問題 |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for case in cases:
        if case["capture_error"] is not None:
            table.append(f'| {case["name"]} | 実行エラー | - | - | - | - | {case["capture_error"]} |')
            continue
        issues = len(case["state_issues"] + case["citation_projection"]["issues"])
        table.append(f'| {case["name"]} | {case["status"]} | '
                     f'{case["search_step_count"]} | {case["citation_count"]} | '
                     f'{case["reference_with_body_count"]} | {case["open_goal_count"]} | {issues}件 |')
    c = report["coverage"]
    table.extend(("", "## 実探索の観測範囲", "",
                  f'- 未完成の検索結果: {c["actual_incomplete_cases"]}件',
                  f'- うち ProofStep あり: {c["actual_incomplete_with_steps"]}件',
                  f'- うち Reference あり: {c["actual_incomplete_with_any_citation"]}件',
                  f'- うち登録出典あり: {c["actual_incomplete_with_registered_citation"]}件',
                  f'- うち Reference 本文あり: {c["actual_incomplete_with_reference_body"]}件',
                  "", "## 判定上の注意", "",
                  "- Reference 番号や見出しがあっても、本文がなければ本文完成とは判定しない。",
                  "- 非完成の探索結果に引用が存在しなければ、実際の部分証明の引用表示は未検証と記録する。",
                  "- GIVEN で出典がない場合は未接続として報告し、引用は補わない。",
                  "- 各群の `*_reference.md` と `*_narrative.md` に実表示の内容を保存する。",
                  "- 実行エラーや表示不足があっても調査結果として報告し、実装ファイルは変更しない。",
                  "- 全体 pytest は実行しない。", "",
                  "## 見つかった問題", ""))
    if unresolved_issues:
        table.extend("- " + issue for issue in unresolved_issues)
    else:
        table.append("- 観測できた範囲では整合性違反なし（未観測範囲は未検証）。")
    table.append("")
    (OUTPUT / "audit.md").write_text("\n".join(table), encoding="utf-8")
    bundle = OUTPUT / "review_bundle.zip"
    with ZipFile(bundle, "w", compression=ZIP_DEFLATED) as archive:
        for file in sorted(OUTPUT.glob("*.md")) + sorted(OUTPUT.glob("*.json")) + sorted(OUTPUT.glob("*.txt")):
            archive.write(file, file.name)
    print("R3-41D READ_ONLY audit captured", len(successful), "real cases")
    print("ACTUAL_INCOMPLETE", len(live_partial),
          "CITED_PARTIAL", len(cited_partial), "REGISTERED_PARTIAL", len(registered_partial))
    print("ISSUES", unresolved_issues)
    print("REPORT", OUTPUT / "audit.md")
    print("UPLOAD_BUNDLE", bundle)
    print("Implementation unchanged. Full pytest NOT run.")


if __name__ == "__main__":
    main()
