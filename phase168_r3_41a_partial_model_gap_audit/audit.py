"""R3-41A: read-only partial Narrative routing and coverage audit.

No inference rules, proof steps, sources, renderer, or Web entry are changed.
"""
from __future__ import annotations

import ast
import hashlib
import json
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / "output"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SOURCES = (
    "phase165_r52_partial_proof.py",
    "phase165_r52_r3_web_adapter.py",
    "phase165_r52_r4_flask_bridge.py",
    "web_group_proof.py",
    "phase168_r3_3_proof_narrative_model.py",
    "phase168_r3_5_model_renderer.py",
)


def _function(tree: ast.Module, name: str) -> ast.FunctionDef:
    matches = [node for node in tree.body
               if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(matches) != 1:
        raise AssertionError(f"expected exactly one function: {name}")
    return matches[0]


def _named_calls(node: ast.AST, name: str) -> list[int]:
    return sorted(c.lineno for c in ast.walk(node)
                  if isinstance(c, ast.Call)
                  and ((isinstance(c.func, ast.Name) and c.func.id == name)
                       or (isinstance(c.func, ast.Attribute)
                           and c.func.attr == name)))


def analyze_route_contract(root: Path) -> dict:
    """Inspect only current production root modules (not historical backups)."""
    trees = {
        name: ast.parse((root / name).read_text(encoding="utf-8-sig"), filename=name)
        for name in SOURCES
    }
    web_standard = _function(trees["web_group_proof.py"], "build_standard_web_group_proof_view")
    web_partial = _function(trees["web_group_proof.py"], "build_web_partial_group_proof_view")
    flask = _function(trees["phase165_r52_r4_flask_bridge.py"], "build_group_proof_progress_view")
    adapter = _function(trees["phase165_r52_r3_web_adapter.py"], "build_partial_web_group_proof_view")
    common = _function(trees["phase168_r3_5_model_renderer.py"], "render_model_backed_narrative_markdown")
    defaults = {}
    for arg, val in zip(web_standard.args.kwonlyargs, web_standard.args.kw_defaults):
        if val is not None and isinstance(val, ast.Constant):
            defaults[arg.arg] = val.value
    direct_calls = []
    for name in ("web_group_proof.py", "phase165_r52_r4_flask_bridge.py"):
        tree = trees[name]
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if (isinstance(node.func, ast.Name)
                    and node.func.id == "build_partial_web_group_proof_view"):
                direct_calls.append({
                    "file": name, "line": node.lineno,
                    "narrative_model_provided": any(k.arg == "narrative_model" for k in node.keywords),
                })
    return {
        "source_sha256": {name: hashlib.sha256((root / name).read_bytes()).hexdigest()
                          for name in SOURCES},
        "web_default_citation_source": defaults.get("citation_source"),
        "web_standard_uses_common_model": bool(_named_calls(web_standard, "build_linked_proof_narrative_model")),
        "web_standard_uses_adapter": bool(_named_calls(web_standard, "build_partial_web_group_proof_view")),
        "web_explicit_partial_uses_adapter": bool(_named_calls(web_partial, "build_partial_web_group_proof_view")),
        "flask_uses_standard_web": bool(_named_calls(flask, "build_standard_web_group_proof_view")),
        "flask_explicit_case_uses_adapter": bool(_named_calls(flask, "build_partial_web_group_proof_view")),
        "adapter_fallback_calls": _named_calls(adapter, "render_partial_proof_markdown"),
        "adapter_common_calls": _named_calls(adapter, "render_model_backed_narrative_markdown"),
        "direct_calls": direct_calls,
        "common_renderer_reads_open_goals": bool(any(
            isinstance(node, ast.Attribute) and node.attr == "open_goals"
            for node in ast.walk(common))),
        "common_renderer_reads_diagnostics": bool(any(
            isinstance(node, ast.Attribute) and node.attr == "diagnostics"
            for node in ast.walk(common))),
        "common_renderer_reads_status": bool(any(
            isinstance(node, ast.Attribute) and node.attr == "status"
            for node in ast.walk(common))),
    }


def synthetic_cases():
    """Construct only legal status fixtures; do not run new proof search."""
    from phase165_r52_partial_proof import (
        ProofSearchStatus, make_partial_proof_result,
    )
    from proof import ProofRule, ProofStep
    return (
        ("not_searched", make_partial_proof_result(
            n=100, k=20, status=ProofSearchStatus.NOT_SEARCHED,
            open_goals=("target",),
        )),
        ("partial", make_partial_proof_result(
            n=3, k=2, status=ProofSearchStatus.PARTIAL,
            proven_steps=(ProofStep("observed", (), ProofRule.GIVEN),),
            open_goals=("unknown",), references=("General theorem",),
        )),
        ("search_failed", make_partial_proof_result(
            n=17, k=4, status=ProofSearchStatus.SEARCH_FAILED,
            open_goals=("no-rule",), diagnostics=("No applicable typed rule",),
        )),
    )


def audit_incomplete_statuses() -> list[dict]:
    """Compare existing no-model Web contract with direct common-model output.

    The comparison is diagnostic, not an assertion that the common model is
    already a drop-in replacement for incomplete results.
    """
    from phase165_r52_partial_proof import render_partial_proof_markdown
    from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
    from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown

    rows = []
    for label, result in synthetic_cases():
        legacy = render_partial_proof_markdown(result)
        adapter_view = build_partial_web_group_proof_view(result)
        model = build_proof_narrative_model(result)
        common = render_model_backed_narrative_markdown(result, model)
        rows.append({
            "case": label,
            "status": result.status.value,
            "proof_steps": len(result.proven_steps),
            "open_goal_count": len(result.open_goals),
            "diagnostic_count": len(result.diagnostics),
            "legacy_sha256": hashlib.sha256(legacy.encode("utf-8")).hexdigest(),
            "common_sha256": hashlib.sha256(common.encode("utf-8")).hexdigest(),
            "legacy_has_status": "探索状態" in legacy,
            "common_has_status": "探索状態" in common,
            "legacy_has_open_goal_section": "未解決 Goal" in legacy,
            "common_has_open_goal_section": "未解決 Goal" in common,
            "legacy_has_diagnostic_section": "探索診断" in legacy,
            "common_has_diagnostic_section": "探索診断" in common,
            "legacy_contains_observed_step": "observed" in legacy,
            "common_contains_observed_step": "observed" in common,
            "adapter_has_lines": bool(adapter_view.rendered_lines),
            "adapter_partial_result": adapter_view.partial_result,
            "legacy_qed": "□" in legacy,
            "common_qed": "□" in common,
            "legacy_text": legacy,
            "common_text": common,
        })
    return rows


def markdown_report(report: dict) -> str:
    route = report["routes"]
    rows = report["cases"]
    lines = [
        "# Phase 168 R3-41A — 未完成証明の共通 Narrative 移行ギャップ監査", "",
        "読み取り専用。数学的推論・Web 経路・Renderer・Reference 台帳は変更しない。", "",
        "## 現行の経路", "",
        f'- 標準 Web の既定 citation_source: `{route["web_default_citation_source"]}`',
        f'- 標準 Web が共通 Model を構築する: `{route["web_standard_uses_common_model"]}`',
        f'- Flask の通常問い合わせが標準 Web を使う: `{route["flask_uses_standard_web"]}`',
        f'- Flask の独自探索入力が Model 未指定 Adapter を使う: `{route["flask_explicit_case_uses_adapter"]}`',
        f'- Adapter の旧 fallback 呼出: `{route["adapter_fallback_calls"]}`',
        f'- Adapter の共通 Renderer 呼出: `{route["adapter_common_calls"]}`',
        f'- 共通 Renderer が open_goals を直接参照する: `{route["common_renderer_reads_open_goals"]}`',
        f'- 共通 Renderer が diagnostics を直接参照する: `{route["common_renderer_reads_diagnostics"]}`',
        "", "## 既存表示と共通 Model の状態別比較", "",
        "| 状態 | 旧状態表示 | 共通状態表示 | 旧未解決 Goal | 共通未解決 Goal | 旧診断 | 共通診断 |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        label = row["case"]
        truth = lambda key: "あり" if row[key] else "なし"
        lines.append(
            f'| {label} | {truth("legacy_has_status")} | {truth("common_has_status")} | '
            f'{truth("legacy_has_open_goal_section")} | {truth("common_has_open_goal_section")} | '
            f'{truth("legacy_has_diagnostic_section")} | {truth("common_has_diagnostic_section")} |'
        )
    lines.extend([
        "", "## 判定", "",
        "- 既定の完成証明 Narrative は既に共通 Model 経由である。", 
        "- 未完成の結果では、旧 fallback が探索状態・未解決 Goal・探索診断を担っている。",
        "- 共通 Renderer へ単純に差し替えると、それらの情報を失う可能性がある。",
        "- 証明探索や出典を補完するのではなく、実際の PartialProofResult を共通の表示モデルへ拡張することが次の実装課題。",
        "- 既存の明示 legacy API と NarrativeOrderEntry.after_indices は今回変更しない。",
        "- 以上は人工の不完全状態3ケースの比較であり、全群の正常性を保証するものではない。",
        "- 全体 pytest は Phase 168 の最後に実行する。", "",
    ])
    return "\n".join(lines)


def run_audit(root: Path = ROOT, output: Path = OUTPUT) -> dict:
    """Create output before any write, including direct invocation from pytest."""
    output.mkdir(parents=True, exist_ok=True)
    routes = analyze_route_contract(root)
    rows = audit_incomplete_statuses()
    if routes["web_default_citation_source"] != "model":
        raise AssertionError("default public Web no longer uses model path")
    if not routes["adapter_fallback_calls"] or not routes["adapter_common_calls"]:
        raise AssertionError("expected to identify both adapter routing paths")
    if not routes["flask_explicit_case_uses_adapter"]:
        raise AssertionError("custom-search Flask path was not located")
    for row in rows:
        if not row["adapter_partial_result"] or not row["adapter_has_lines"]:
            raise AssertionError(f"existing partial adapter failed: {row['case']}")
        if row["legacy_qed"] or row["common_qed"]:
            raise AssertionError(f"incomplete state incorrectly claims proof: {row['case']}")
        if row["open_goal_count"] and not row["legacy_has_open_goal_section"]:
            raise AssertionError(f"current fallback dropped a goal: {row['case']}")
        if row["diagnostic_count"] and not row["legacy_has_diagnostic_section"]:
            raise AssertionError(f"current fallback dropped diagnostics: {row['case']}")
    report = {
        "mode": "AUDIT_ONLY",
        "status": "PASS",
        "routes": routes,
        "cases": rows,
        "caveats": [
            "Source hashes represent the user's local working tree, not necessarily GitHub develop.",
            "The synthetic cases do not measure all proof-status conditions.",
            "The compared common output has no externally screened bridge; no citation claims are inferred.",
            "This audit does not modify or replace the old fallback.",
        ],
    }
    (output / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "audit.md").write_text(markdown_report(report), encoding="utf-8")
    for row in rows:
        (output / f"{row['case']}_fallback.md").write_text(row["legacy_text"], encoding="utf-8")
        (output / f"{row['case']}_common.md").write_text(row["common_text"], encoding="utf-8")
    with ZipFile(output / "review_bundle.zip", "w", ZIP_DEFLATED) as archive:
        for filename in sorted(output.glob("*.json")) + sorted(output.glob("*.md")):
            archive.write(filename, filename.name)
    return report


def main() -> None:
    report = run_audit()
    print("R3-41A READ_ONLY audit PASS")
    for row in report["cases"]:
        print(row["case"], "legacy_goals", row["legacy_has_open_goal_section"],
              "common_goals", row["common_has_open_goal_section"],
              "legacy_diagnostics", row["legacy_has_diagnostic_section"],
              "common_diagnostics", row["common_has_diagnostic_section"])
    print("REPORT", OUTPUT / "audit.md")
    print("UPLOAD_BUNDLE", OUTPUT / "review_bundle.zip")
    print("Implementation files untouched. Full pytest NOT run.")


if __name__ == "__main__":
    main()
