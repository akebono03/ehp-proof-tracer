"""Phase 168 R3-41I: read-only renderer closure and frozen-baseline audit.

This audit deliberately reports remaining gaps; a clean execution does not
mean the proof narratives have matched their fixed mathematical benchmarks.
"""
from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path

from phase168_r3_38_frozen_fulltext_audit import audit as frozen
from phase168_r3_39f_frozen_comparison.audit import assess

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "output"
CASES = (("pi3_2", 2, 1), ("pi4_3", 3, 1), ("pi5_4", 4, 1))
WATCHED_SOURCES = (
    "web_group_proof.py",
    "phase165_r52_r4_flask_bridge.py",
    "phase165_r52_r3_web_adapter.py",
    "phase168_r3_3_proof_narrative_model.py",
    "phase168_r3_5_model_renderer.py",
    "phase168_r3_29_order_projection.py",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inspect_route_contract(root: Path) -> dict[str, bool]:
    """Observe public routing, without claiming the absence of every legacy API."""
    standard = (root / "web_group_proof.py").read_text(encoding="utf-8-sig")
    flask = (root / "phase165_r52_r4_flask_bridge.py").read_text(encoding="utf-8-sig")
    adapter = (root / "phase165_r52_r3_web_adapter.py").read_text(encoding="utf-8-sig")
    renderer = (root / "phase168_r3_5_model_renderer.py").read_text(encoding="utf-8-sig")
    return {
        "standard_model_is_default": bool(re.search(r'citation_source\s*:\s*str\s*=\s*[\'\"]model[\'\"]', standard)),
        "standard_explicit_legacy_retained": 'citation_source == "legacy"' in standard,
        "standard_builds_linked_model": "build_linked_proof_narrative_model(result, model_bridge)" in standard,
        "explicit_partial_builds_model": "narrative_model = build_proof_narrative_model(result)" in standard,
        "flask_standard_routes_to_model": 'citation_source="model"' in flask,
        "flask_partial_uses_model": "build_linked_proof_narrative_model(result, bridge)" in flask,
        "adapter_explicit_model_uses_common_renderer": "render_model_backed_narrative_markdown(result, narrative_model)" in adapter,
        "adapter_legacy_fallback_retained": "render_partial_proof_markdown(result)" in adapter,
        "partial_step_uses_model_citation_numbers": "model.step_citation_numbers[index]" in renderer,
    }


def summarize_comparison(comparison: dict, markdown: str) -> dict:
    """Make quality gaps explicit; do not use numerical line equality as proof."""
    name = comparison["name"]
    _, proof = frozen.sections(markdown)
    explanations = assess(name, proof)
    refs = comparison["reference_entries"]
    ref_section, proof_section = frozen.sections(markdown)
    headings = set(int(x) for x in re.findall(r"\[R(\d+)\]", ref_section))
    used_in_body = set(int(x) for x in re.findall(r"\[R(\d+)\]", proof_section))
    model_numbers = {x["number"] for x in refs}
    differences = comparison["comparison"]
    missing_explanations = [x["key"] for x in explanations if not x["present"]]
    missing_body_locators = [x["locator"] for x in refs if not x["body_count"]]
    issues = []
    if comparison["web_partial"]:
        issues.append("CONTROL_NOT_COMPLETE")
    if not refs:
        issues.append("REFERENCE_EMPTY")
    if missing_body_locators:
        issues.append("REFERENCE_BODIES_MISSING")
    if headings != model_numbers:
        issues.append("REFERENCE_HEADING_MODEL_MISMATCH")
    if not used_in_body.issubset(model_numbers):
        issues.append("PROOF_HAS_DANGLING_REFERENCE_NUMBERS")
    if missing_explanations:
        issues.append("BENCHMARK_EXPLANATION_GAPS")
    if "□" not in proof_section:
        issues.append("COMPLETE_MARKER_MISSING")
    reference_different = not differences["reference"]["exact_after_line_cleanup"]
    proof_different = not differences["proof"]["exact_after_line_cleanup"]
    if reference_different or proof_different:
        issues.append("MANUAL_FROZEN_TEXT_REVIEW_REQUIRED")
    return {
        "name": name,
        "baseline_path": comparison["baseline_path"],
        "baseline_sha256": comparison["baseline_sha256"],
        "search_step_count": comparison["rendered_step_count"],
        "web_partial": comparison["web_partial"],
        "references": len(refs),
        "references_with_bodies": sum(x["body_count"] > 0 for x in refs),
        "model_reference_numbers": sorted(model_numbers),
        "reference_heading_numbers": sorted(headings),
        "used_reference_numbers_in_proof": sorted(used_in_body),
        "references_not_explicitly_tagged_in_proof": sorted(model_numbers - used_in_body),
        "reference_difference_lines": differences["reference"]["difference_line_count"],
        "proof_difference_lines": differences["proof"]["difference_line_count"],
        "reference_text_matches_frozen_after_cleanup": not reference_different,
        "proof_text_matches_frozen_after_cleanup": not proof_different,
        "benchmark_explanations": explanations,
        "missing_benchmark_explanations": missing_explanations,
        "missing_body_locators": missing_body_locators,
        "issues": issues,
    }


def render_report(rows: list[dict], route: dict, errors: list[dict]) -> str:
    lines = [
        "# Phase 168 R3-41I — 共通 Renderer 終了条件・固定基準監査",
        "",
        "読み取り専用。固定原文・実装・証明探索を変更しない。",
        "",
        "| 群 | ProofStep | Reference 本文あり | Reference 差分行 | 証明差分行 | 基準説明の不足 |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for r in rows:
        missing = ", ".join(r["missing_benchmark_explanations"]) or "なし（限定項目）"
        lines.append(f'| {r["name"]} | {r["search_step_count"]} | {r["references_with_bodies"]}/{r["references"]} | {r["reference_difference_lines"]} | {r["proof_difference_lines"]} | {missing} |')
    for e in errors:
        lines.append(f'| {e["name"]} | ERROR | - | - | - | {e["error"]} |')
    lines.extend(["", "## 公開経路の確認", ""])
    for key, value in route.items():
        lines.append(f"- {key}: `{value}`")
    for r in rows:
        lines.extend(["", f'## {r["name"]}', ""])
        lines.append(f'- 判定: {", ".join(r["issues"]) if r["issues"] else "限定項目に違反なし"}')
        lines.append(f'- 証明本文に番号が現れない Reference: {r["references_not_explicitly_tagged_in_proof"]}')
        for check in r["benchmark_explanations"]:
            lines.append(f'- {"有" if check["present"] else "不足・要確認"}: {check["why"]} (`{check["key"]}`)')
        lines.append(f'- 比較ファイル: `{r["name"]}_frozen.txt`, `{r["name"]}_current.md`, `{r["name"]}_reference.diff`, `{r["name"]}_proof.diff`')
    lines.extend([
        "", "## 判定上の境界", "",
        "- 固定原文の論証内容・順序・詳しさを評価する。Reference 番号・順序は固定対象ではない。",
        "- 差分行数は数学的誤りの件数ではない。説明項目の通過は全文一致を意味しない。",
        "- Reference の未使用番号は注意情報であり、必要な数学的根拠が欠けるとの断定ではない。",
        "- 以前の4群のバイト同一性は回帰試験であり、固定原文との同一性ではない。",
        "- R3-41H で確認した有限巡回群構造の未解決問題は探索側の課題であり、この監査では修正しない。",
        "- 残存する明示的 legacy API は互換境界として報告し、今回撤去しない。",
        "- 全体 pytest は Phase 168 の終了時まで実行しない。",
        "",
    ])
    return "\n".join(lines)


def run_audit(root: Path = ROOT, output: Path = OUTPUT) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    watched = {name: digest(root / name) for name in WATCHED_SOURCES}
    baseline_paths = {name: frozen.baseline_path(name) for name, _, _ in CASES}
    baseline_before = {name: digest(path) for name, path in baseline_paths.items()}
    old_output = frozen.OUT
    rows = []
    errors = []
    try:
        frozen.OUT = output
        for name, n, k in CASES:
            try:
                cmp = frozen.compare(name, n, k)
                content = (output / f"{name}_current.md").read_text(encoding="utf-8")
                rows.append(summarize_comparison(cmp, content))
                (output / f"{name}_frozen.txt").write_bytes(baseline_paths[name].read_bytes())
            except Exception as exc:
                errors.append({"name": name, "error": type(exc).__name__ + ": " + str(exc)})
    finally:
        frozen.OUT = old_output
    route = inspect_route_contract(root)
    watched_after = {name: digest(root / name) for name in WATCHED_SOURCES}
    baseline_after = {name: digest(path) for name, path in baseline_paths.items()}
    if watched != watched_after or baseline_before != baseline_after:
        raise AssertionError("audit detected unexpected modification to watched source/baseline")
    state = (
        "EXECUTION_ERRORS" if errors else
        "ROUTE_CONTRACT_GAPS" if not all(route.values()) else
        "BASELINE_REVIEW_REQUIRED" if any(r["issues"] for r in rows) else
        "LIMITED_AUDIT_PASSED"
    )
    report = {
        "phase": "168 R3-41I",
        "mode": "AUDIT_ONLY_FROZEN_CLOSURE",
        "status": state,
        "cases": rows,
        "errors": errors,
        "route_contract": route,
        "source_sha256": watched_after,
        "baseline_sha256": baseline_after,
        "implementation_modified": False,
        "frozen_baseline_modified": False,
        "full_pytest_run": False,
    }
    (output / "audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "audit.md").write_text(render_report(rows, route, errors), encoding="utf-8")
    bundle = output / "review_bundle.zip"
    with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(output.iterdir()):
            if path.is_file() and path != bundle:
                zf.write(path, path.name)
    return report


def main() -> int:
    report = run_audit()
    for row in report["cases"]:
        print(row["name"], "steps", row["search_step_count"],
              "reference_bodies", f'{row["references_with_bodies"]}/{row["references"]}',
              "reference_diff", row["reference_difference_lines"],
              "proof_diff", row["proof_difference_lines"],
              "benchmark_gaps", row["missing_benchmark_explanations"])
    for err in report["errors"]:
        print("CAPTURE_ERROR", err["name"], err["error"])
    print("R3-41I", report["status"])
    print("REPORT", OUTPUT / "audit.md")
    print("UPLOAD_BUNDLE", OUTPUT / "review_bundle.zip")
    print("READ_ONLY; implementation and baselines unchanged. Full pytest NOT run.")
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
