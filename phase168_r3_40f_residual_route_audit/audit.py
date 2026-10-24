"""Phase 168 R3-40F: read-only audit of remaining Narrative compatibility routes.

No implementation, mathematical source, or frozen baseline is changed.
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

SOURCE_FILES = (
    "phase168_r3_29_order_projection.py",
    "phase168_r3_5_model_renderer.py",
    "phase168_r3_27_typed_statement_projection.py",
    "phase168_r3_3_proof_narrative_model.py",
    "web_group_proof.py",
    "phase165_r52_r3_web_adapter.py",
)
CASES = (("pi3_2", 2, 1), ("pi4_3", 3, 1),
         ("pi5_4", 4, 1), ("pi6_5", 5, 1))


def module_ast(root: Path, name: str) -> ast.Module:
    return ast.parse((root / name).read_text(encoding="utf-8-sig"), filename=name)


def named_function(module: ast.Module, name: str) -> ast.FunctionDef:
    matches = [node for node in module.body
               if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(matches) != 1:
        raise AssertionError(f"Expected one function {name}; found {len(matches)}")
    return matches[0]


def has_call(node: ast.AST, name: str) -> bool:
    return any(isinstance(child, ast.Call)
               and ((isinstance(child.func, ast.Name) and child.func.id == name)
                    or (isinstance(child.func, ast.Attribute) and child.func.attr == name))
               for child in ast.walk(node))


def analyze_structure(root: Path) -> dict:
    order_ast = module_ast(root, SOURCE_FILES[0])
    renderer_ast = module_ast(root, SOURCE_FILES[1])
    web_ast = module_ast(root, "web_group_proof.py")
    adapter_ast = module_ast(root, "phase165_r52_r3_web_adapter.py")
    order_func = named_function(order_ast, "project_narrative_order")
    renderer_func = named_function(renderer_ast, "render_model_backed_narrative_markdown")
    web_func = named_function(web_ast, "build_standard_web_group_proof_view")
    adapter_func = named_function(adapter_ast, "build_partial_web_group_proof_view")
    dataclasses = [node for node in order_ast.body
                   if isinstance(node, ast.ClassDef) and node.name == "NarrativeOrderEntry"]
    if len(dataclasses) != 1:
        raise AssertionError("NarrativeOrderEntry must be kept as an API")
    after_field = [node for node in dataclasses[0].body
                   if isinstance(node, ast.AnnAssign)
                   and isinstance(node.target, ast.Name)
                   and node.target.id == "after_indices"]
    retains_after_field = (len(after_field) == 1 and
                           isinstance(after_field[0].value, ast.Tuple) and
                           not after_field[0].value.elts)
    renderer_deferred_reads = [node.lineno for node in ast.walk(renderer_func)
                               if isinstance(node, ast.Attribute)
                               and node.attr == "after_indices"]
    projection_deferred_reads = [node.lineno for node in ast.walk(order_func)
                                 if isinstance(node, ast.Attribute)
                                 and node.attr == "after_indices"]
    web_defaults = {
        argument.arg: ast.literal_eval(value)
        for argument, value in zip(
            web_func.args.args[-len(web_func.args.defaults):],
            web_func.args.defaults,
        )
        if isinstance(value, ast.Constant)
    }
    web_defaults.update({
        argument.arg: ast.literal_eval(value)
        for argument, value in zip(web_func.args.kwonlyargs, web_func.args.kw_defaults)
        if value is not None and isinstance(value, ast.Constant)
    })
    root_readers = []
    for path in sorted(root.glob("*.py")):
        module = module_ast(root, path.name)
        matches = [node.lineno for node in ast.walk(module)
                   if isinstance(node, ast.Attribute) and node.attr == "after_indices"]
        if matches:
            root_readers.append({"file": path.name, "lines": matches})
    old_test = root / "phase168_r3_29_order_projection" / "tests" / "test_phase168_r3_29_order_projection.py"
    historic_test_uses_field = (old_test.is_file() and
                                "after_indices" in old_test.read_text(encoding="utf-8"))

    return {
        "source_sha256": {
            name: hashlib.sha256((root / name).read_bytes()).hexdigest()
            for name in SOURCE_FILES
        },
        "order_has_dependency_graph": (
            has_call(order_func, "heappush") and
            has_call(order_func, "heappop") and
            any(isinstance(node, ast.Attribute) and node.attr == "premises"
                for node in ast.walk(order_func))
        ),
        "order_emits_narrative_order_entries": has_call(order_func, "NarrativeOrderEntry"),
        "retains_compatibility_field": retains_after_field,
        "renderer_after_indices_reads": renderer_deferred_reads,
        "projection_after_indices_reads": projection_deferred_reads,
        "root_after_indices_reads": root_readers,
        "historical_focused_test_reads_after_indices": historic_test_uses_field,
        "renderer_uses_shared_order": has_call(renderer_func, "project_narrative_order"),
        "renderer_uses_shared_citation_model": (
            any(isinstance(node, ast.Attribute) and node.attr == "citations"
                for node in ast.walk(renderer_func))
        ),
        "web_defaults": web_defaults,
        "standard_web_has_explicit_legacy_branch": (
            "legacy" in ast.unparse(web_func) and "trace" in ast.unparse(web_func)
        ),
        "adapter_has_model_renderer": has_call(adapter_func, "render_model_backed_narrative_markdown"),
        "adapter_has_no_model_fallback": has_call(adapter_func, "render_partial_proof_markdown"),
    }


def audit_four_cases(root: Path) -> list[dict]:
    from phase168_r3_38_frozen_fulltext_audit.audit import capture
    from phase168_r3_29_order_projection import project_narrative_order
    from phase168_r3_26_exactness_projection import project_exactness_chains

    # This function is also invoked directly by pytest, before main().
    OUTPUT.mkdir(parents=True, exist_ok=True)
    results = []
    for label, n, k in CASES:
        narrative, model, view = capture(n, k)
        suppressed = {i for chain in project_exactness_chains(model)
                      for i in chain.step_indices}
        entries = project_narrative_order(model)
        indices = [entry.step_index for entry in entries]
        positions = {index: position for position, index in enumerate(indices)}
        inversions = []
        for child_index, step in enumerate(model.steps):
            for premise in step.premises:
                matches = [i for i, candidate in enumerate(model.steps) if candidate is premise]
                if not matches:
                    matches = [i for i, candidate in enumerate(model.steps) if candidate == premise]
                if not matches or positions[matches[0]] >= positions[child_index]:
                    inversions.append([matches[0] if matches else None, child_index])
        current_path = OUTPUT / (label + "_current.md")
        current_path.write_text(narrative, encoding="utf-8")
        previous_path = (root / "phase168_r3_40e_remove_deferred_render" / "output"
                         / (label + "_after.md"))
        previous_identical = (
            current_path.read_bytes() == previous_path.read_bytes()
            if previous_path.is_file() else None
        )
        result = {
            "case": label,
            "step_count": len(model.steps),
            "citation_count": len(model.citations),
            "narrative_sha256": hashlib.sha256(narrative.encode("utf-8")).hexdigest(),
            "complete_coverage": sorted(indices) == list(range(len(model.steps))),
            "all_after_indices_empty": all(entry.after_indices == () for entry in entries),
            "no_dependency_inversions": len(inversions) == 0,
            "dependency_inversions": inversions,
            "all_suppressed_still_in_dependency_order": suppressed.issubset(set(indices)),
            "matches_r3_40e_snapshot": previous_identical,
            "web_narrative_route": view.key,
        }
        results.append(result)
    return results


def markdown_report(report: dict) -> str:
    structure, cases = report["structure"], report["cases"]
    lines = [
        "# Phase 168 R3-40F — 共通 Renderer の残存互換経路監査", "",
        "監査専用。実装・固定基準・命題台帳は変更していない。", "",
        "## 静的監査", "",
        f'- `NarrativeOrderEntry.after_indices` は互換フィールドとして残る: **{structure["retains_compatibility_field"]}**',
        f'- 現在の共通 Renderer による `after_indices` 参照: **{len(structure["renderer_after_indices_reads"])} 件**',
        f'- 現在の Projection による `after_indices` 参照: **{len(structure["projection_after_indices_reads"])} 件**',
        f'- 共通 Projection の Proof Tree 依存関係整列: **{structure["order_has_dependency_graph"]}**',
        f'- 共通 Renderer の Citation Model 参照: **{structure["renderer_uses_shared_citation_model"]}**',
        f'- 旧テストの互換フィールド参照: **{structure["historical_focused_test_reads_after_indices"]}**',
        f'- 標準 Web の既定: `{structure["web_defaults"]}`',
        f'- 標準 Web に互換 `legacy` 分岐が残る: **{structure["standard_web_has_explicit_legacy_branch"]}**',
        f'- Web Adapter にモデル未指定時の旧 Narrative fallback が残る: **{structure["adapter_has_no_model_fallback"]}**',
        "", "## 対象4群の実行時監査", "",
        "| 群 | Steps | Reference | Deferred | 依存逆転 | R3-40E からの変更 |",
        "|---|---:|---:|---|---|---|",
    ]
    for case in cases:
        unchanged = case["matches_r3_40e_snapshot"]
        comparison = "一致" if unchanged else ("不一致" if unchanged is False else "記録なし")
        lines.append(f'| {case["case"]} | {case["step_count"]} | {case["citation_count"]} | '
                     f'{"なし" if case["all_after_indices_empty"] else "あり"} | '
                     f'{"0" if case["no_dependency_inversions"] else case["dependency_inversions"]} | '
                     f'{comparison} |')
    lines.extend([
        "", "## 分類・次工程との境界", "",
        "- `after_indices` は通常描画で未使用でも既存のテストが参照するため、この監査では削除しない。",
        "- `legacy` とモデル未指定時の fallback は、標準 Narrative の既定経路とは別。利用者・テストの実際の使用状況は未確認であり、即時撤去しない。",
        "- 次の変更では、個別の public entry を触る前に呼出元と互換テストを確認する。",
        "- 今回は新しい数学規則・出典登録・Web 分岐変更を行わない。",
        "- 全体 pytest は Phase 168 の最後にだけ実行する。", "",
    ])
    return "\n".join(lines)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    structure = analyze_structure(ROOT)
    cases = audit_four_cases(ROOT)
    if (not structure["retains_compatibility_field"] or
            structure["renderer_after_indices_reads"] or
            structure["projection_after_indices_reads"] or
            not structure["renderer_uses_shared_order"] or
            not structure["renderer_uses_shared_citation_model"] or
            any(not item["complete_coverage"] or
                not item["all_after_indices_empty"] or
                not item["no_dependency_inversions"] or
                item["matches_r3_40e_snapshot"] is False
                for item in cases)):
        raise AssertionError("R3-40F audit detected a violation; see output")
    report = {"mode": "READ_ONLY", "status": "PASS", "structure": structure,
              "cases": cases,
              "notes": [
                  "GitHub develop and the locally patched working tree may differ; local source hashes are authoritative for this audit.",
                  "A remaining fallback is not automatically reachable in the default Web Narrative.",
                  "This is a four-group audit, not a project-wide regression suite.",
              ]}
    (OUTPUT / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUTPUT / "audit.md").write_text(markdown_report(report), encoding="utf-8")
    bundle = OUTPUT / "review_bundle.zip"
    with ZipFile(bundle, "w", ZIP_DEFLATED) as archive:
        for path in sorted(OUTPUT.glob("*.md")) + sorted(OUTPUT.glob("*.json")):
            archive.write(path, path.name)
    print("R3-40F READ_ONLY audit PASS")
    for item in cases:
        print(item["case"], "steps", item["step_count"], "refs", item["citation_count"],
              "inversions", len(item["dependency_inversions"]),
              "deferred", not item["all_after_indices_empty"])
    print("COMPAT_AFTER_INDICES", structure["retains_compatibility_field"])
    print("ACTIVE_RENDER_DEFERRED_READS", structure["renderer_after_indices_reads"])
    print("LEGACY_COMPAT_ROUTE", structure["standard_web_has_explicit_legacy_branch"])
    print("NO_MODEL_FALLBACK", structure["adapter_has_no_model_fallback"])
    print("REPORT", OUTPUT / "audit.md")
    print("UPLOAD_BUNDLE", bundle)
    print("No implementation changes. Full pytest NOT run.")


if __name__ == "__main__":
    main()
