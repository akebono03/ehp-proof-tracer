#!/usr/bin/env python3
"""Phase 168 R3-41P: audit-only renderer and citation/proof responsibility boundaries.

This script never modifies project source files or the proof tree.
It writes only within its own package/output directory.
"""
from __future__ import annotations

import ast
import difflib
import hashlib
import json
import re
import subprocess
import sys
import traceback
from collections import Counter
from dataclasses import asdict, is_dataclass
from pathlib import Path
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parent
PROJECT = PACKAGE.parent
OUT = PACKAGE / "output"
OUT.mkdir(parents=True, exist_ok=True)

SOURCE_FILES = (
    "phase168_r3_5_model_renderer.py",
    "phase168_r3_27_typed_statement_projection.py",
    "phase168_r3_3_proof_narrative_model.py",
    "phase168_r3_4_link_bridge.py",
    "phase168_r3_12_body_binding.py",
    "phase168_r3_29_order_projection.py",
)
RELATED_FILES = (
    "phase165_r57_r20_general_specialization.py",
    "phase166_r3ac_stable_notation.py",
    "phase165_r12_r11_prop42_unified.py",
)
TEST_FILES = (
    "phase168_r3_41o_renderer_closure/tests/test_phase168_r3_41o_renderer_closure.py",
    "phase168_r3_41n1_import_scope_fix/tests/test_phase168_r3_41n_composed_proof_display.py",
    "phase168_r3_29_order_projection/tests/test_phase168_r3_29_order_projection.py",
    "phase168_r3_39a_reference_accuracy/tests/test_phase168_r3_39a_reference_accuracy.py",
    "phase168_r3_8_citation_origin/tests/test_phase168_r3_8_citation_origin.py",
)
KNOWN_CALLS = {
    "specialize_typed_statement": "MATHEMATICAL_REVALIDATION",
    "_stable_eta_renaming_shape": "MATHEMATICAL_SHAPE_RECHECK",
    "prop42_exactness_indices": "EXACTNESS_SHAPE_RECHECK",
    "match_guard": "RULE_REPLAY",
    "generator_transport_normalization_rule": "RULE_FACTORY_IN_RENDERER",
}
EXPECTED = {
    "pi3_2": (2, 1, 18, 4),
    "pi4_3": (3, 1, 25, 4),
    "pi5_4": (4, 1, 10, 3),
}


def file_digest(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
        "lines": len(data.decode("utf-8-sig").splitlines()),
    }


def git(command: list[str]) -> str | None:
    try:
        result = subprocess.run(
            ["git", *command], cwd=PROJECT, check=False,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding="utf-8", errors="replace",
        )
    except (FileNotFoundError, OSError):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def code_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return ""


def scan_file(path: Path) -> dict[str, object]:
    source = path.read_text(encoding="utf-8-sig")
    tree = ast.parse(source, filename=str(path))
    lines = source.splitlines()
    findings: list[dict[str, object]] = []

    class Scanner(ast.NodeVisitor):
        def __init__(self) -> None:
            self.stack: list[str] = []

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            self.stack.append(node.name)
            self.generic_visit(node)
            self.stack.pop()

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            self.stack.append(node.name)
            self.generic_visit(node)
            self.stack.pop()

        def visit_Call(self, node: ast.Call) -> None:
            name = code_name(node.func)
            if name in KNOWN_CALLS:
                findings.append({
                    "line": node.lineno,
                    "function": ".".join(self.stack),
                    "identifier": name,
                    "classification": KNOWN_CALLS[name],
                    "excerpt": lines[node.lineno - 1].strip(),
                })
            if (
                name == "getattr"
                and len(node.args) >= 2
                and isinstance(node.args[1], ast.Constant)
                and node.args[1].value == "name"
                and any(
                    isinstance(child, ast.Attribute)
                    and child.attr == "inference_rule"
                    for child in ast.walk(node.args[0])
                )
            ):
                findings.append({
                    "line": node.lineno,
                    "function": ".".join(self.stack),
                    "identifier": "getattr(inference_rule, 'name')",
                    "classification": "STRING_COUPLED_PRESENTATION",
                    "excerpt": lines[node.lineno - 1].strip(),
                })
            self.generic_visit(node)

        def visit_Compare(self, node: ast.Compare) -> None:
            if any(
                isinstance(sub, ast.Attribute) and sub.attr == "name"
                and isinstance(sub.value, ast.Attribute)
                and sub.value.attr == "inference_rule"
                for sub in ast.walk(node)
            ):
                findings.append({
                    "line": node.lineno,
                    "function": ".".join(self.stack),
                    "identifier": "inference_rule.name",
                    "classification": "STRING_COUPLED_PRESENTATION",
                    "excerpt": lines[node.lineno - 1].strip(),
                })
            self.generic_visit(node)

    Scanner().visit(tree)
    return {
        "file": str(path.relative_to(PROJECT)),
        "digest": file_digest(path),
        "findings": findings,
    }


def snapshot_model(model: object) -> str:
    # Stable within one process: checks that calling the renderer does not
    # directly mutate the existing ProofStep tuple or citation objects.
    return hashlib.sha256(repr((model.steps, model.citations,
                                model.step_citation_numbers)).encode("utf-8")).hexdigest()


def source_trace() -> dict[str, object]:
    metadata = {
        "branch": git(["branch", "--show-current"]),
        "head": git(["rev-parse", "HEAD"]),
        "status": git(["status", "--short"]),
    }
    digests = {}
    static = []
    missing = []
    for name in (*SOURCE_FILES, *RELATED_FILES, *TEST_FILES):
        path = PROJECT / name
        if not path.is_file():
            missing.append(name)
            continue
        digests[name] = file_digest(path)
        if name in SOURCE_FILES:
            static.append(scan_file(path))
    return {"git": metadata, "digests": digests, "missing": missing, "static": static}


def runtime_audit() -> dict[str, object]:
    import phase165_r57_r20_general_specialization as specialization
    import phase166_r3ac_stable_notation as notation
    import phase168_r3_27_typed_statement_projection as typed_projection
    import phase168_r3_5_model_renderer as model_renderer
    from web_group_proof import build_standard_web_group_proof_view
    from phase168_r3_38_frozen_fulltext_audit import audit as frozen
    from phase168_r3_39f_frozen_comparison.audit import assess

    outputs = {}
    for name, (n, k, expected_steps, expected_refs) in EXPECTED.items():
        events: list[dict[str, object]] = []
        try:

            def track(module, function, tag):
                original = getattr(module, function)

                def wrapper(*args, **kwargs):
                    frame = sys._getframe(1)
                    result = original(*args, **kwargs)
                    events.append({
                        "validator": tag,
                        "caller_file": Path(frame.f_code.co_filename).name,
                        "caller_function": frame.f_code.co_name,
                        "called_from_renderer_projection": frame.f_code.co_filename.endswith((
                            "phase168_r3_5_model_renderer.py",
                            "phase168_r3_27_typed_statement_projection.py",
                        )),
                        "accepted": result is not None if tag == "specialize_typed_statement" else bool(result),
                    })
                    return result

                return wrapper

            captures = []

            def capture_renderer(result, model):
                before = snapshot_model(model)
                result_before = repr(result.proven_steps)
                rendered_text = original_renderer(result, model)
                after = snapshot_model(model)
                result_after = repr(result.proven_steps)
                captures.append((
                    rendered_text, model,
                    before == after and result_before == result_after,
                ))
                return rendered_text

            original_renderer = model_renderer.render_model_backed_narrative_markdown
            with patch.object(
                specialization, "specialize_typed_statement",
                track(specialization, "specialize_typed_statement", "specialize_typed_statement"),
            ), patch.object(
                notation, "_stable_eta_renaming_shape",
                track(notation, "_stable_eta_renaming_shape", "_stable_eta_renaming_shape"),
            ), patch.object(
                typed_projection, "prop42_exactness_indices",
                track(typed_projection, "prop42_exactness_indices", "prop42_exactness_indices"),
            ), patch.object(
                model_renderer, "render_model_backed_narrative_markdown",
                side_effect=capture_renderer,
            ):
                view = build_standard_web_group_proof_view(n=n, k=k)
            if len(captures) != 1:
                raise AssertionError(
                    f"Expected one shared renderer call for {name}, got {len(captures)}"
                )
            rendered, model, model_unchanged = captures[0]

            reference, proof = frozen.sections(rendered)
            baseline = None
            baseline_error = None
            ref_diff = None
            proof_diff = None
            try:
                baseline_path = frozen.baseline_path(name)
                baseline = baseline_path.read_text(encoding="utf-8-sig")
                original_ref, original_proof = frozen.sections(baseline)
                ref_diff = "".join(difflib.unified_diff(
                    frozen.normalized_for_diff(original_ref).splitlines(keepends=True),
                    frozen.normalized_for_diff(reference).splitlines(keepends=True),
                    fromfile=name + "_baseline_reference",
                    tofile=name + "_current_reference",
                ))
                proof_diff = "".join(difflib.unified_diff(
                    frozen.normalized_for_diff(original_proof).splitlines(keepends=True),
                    frozen.normalized_for_diff(proof).splitlines(keepends=True),
                    fromfile=name + "_baseline_proof",
                    tofile=name + "_current_proof",
                ))
            except (OSError, ValueError) as exc:
                baseline_error = str(exc)

            (OUT / (name + "_current.md")).write_text(rendered, encoding="utf-8")
            if ref_diff is not None:
                (OUT / (name + "_reference.diff")).write_text(ref_diff, encoding="utf-8")
                (OUT / (name + "_proof.diff")).write_text(proof_diff, encoding="utf-8")

            used_numbers = sorted({int(x) for x in re.findall(r"\[R(\d+)\]", proof)})
            available_numbers = sorted(c.number for c in model.citations)
            source_rows = []
            for citation in model.citations:
                source_rows.append({
                    "number": citation.number,
                    "locator": citation.reference.locator or citation.reference.label,
                    "step_indices": list(citation.step_indices),
                    "assertion_ids": list(citation.assertion_ids),
                    "reference_ids": list(citation.reference_ids),
                    "statement_bodies": list(citation.statement_bodies),
                    "body_count": len(citation.statement_bodies),
                })
            consistency = all(
                citation.number in model.step_citation_numbers[i]
                for citation in model.citations
                for i in citation.step_indices
            ) and all(
                i in next(c.step_indices for c in model.citations if c.number == num)
                for i, numbers in enumerate(model.step_citation_numbers)
                for num in numbers
            )
            available_premises = all(
                any(candidate is premise or candidate == premise for candidate in model.steps)
                for step in model.steps for premise in step.premises
            )
            criteria = assess(name, proof)
            outputs[name] = {
                "status": str(model.status),
                "target": str(model.target),
                "proof_steps": len(model.steps),
                "expected_proof_steps": expected_steps,
                "references": len(model.citations),
                "expected_references": expected_refs,
                "reference_bodies_complete": all(c.statement_bodies for c in model.citations),
                "used_citations": used_numbers,
                "available_citations": available_numbers,
                "no_unused_reference": used_numbers == available_numbers,
                "bidirectional_provenance_consistent": consistency,
                "proof_premises_present_in_model": available_premises,
                "model_unchanged_by_capture": model_unchanged,
                "benchmark_checks": criteria,
                "benchmark_all_present": all(x["present"] for x in criteria),
                "baseline_available": baseline is not None,
                "baseline_error": baseline_error,
                "reference_diff_lines": None if ref_diff is None else len(ref_diff.splitlines()),
                "proof_diff_lines": None if proof_diff is None else len(proof_diff.splitlines()),
                "runtime_validator_calls": events,
                "runtime_renderer_projection_rechecks": sum(e["called_from_renderer_projection"] for e in events),
                "source_rows": source_rows,
                "web_partial": str(view.partial_result),
            }
        except Exception:
            detail = traceback.format_exc()
            (OUT / (name + "_audit_error.txt")).write_text(detail, encoding="utf-8")
            outputs[name] = {
                "audit_error": detail,
                "proof_steps": None,
                "references": None,
                "runtime_validator_calls": events,
                "runtime_renderer_projection_rechecks": sum(
                    event["called_from_renderer_projection"] for event in events
                ),
            }
            print("AUDIT_GROUP_ERROR", name, "see", OUT / (name + "_audit_error.txt"))
    return outputs


def render_report(result: dict[str, object]) -> str:
    rows = [
        "# Phase 168 R3-41P — Renderer と証明検証の責務境界監査",
        "",
        "## 実行条件",
        "",
        "- 監査専用。プロジェクトの Python 実装は変更していない。",
        "- 数学的再判定と構造・表示の整合性確認を区別して記録する。",
        "- 動的監査は公開 Web 経路を使用し、全体 pytest は実行しない。",
        "- 比較は文字列の差分と既存固定基準の論証チェックであり、数学的正しさを新たに証明しない。",
        "",
        "## Git 状態",
        "",
        f"- branch: `{result['sources']['git']['branch']}`",
        f"- HEAD: `{result['sources']['git']['head']}`",
        f"- working status (audit start): `{result['sources']['git']['status']}`",
        "",
        "## 静的監査",
        "",
        "| ファイル | 行 | 関数 | 呼び出し・条件 | 分類 |",
        "|---|---:|---|---|---|",
    ]
    for file_row in result["sources"]["static"]:
        for finding in file_row["findings"]:
            rows.append("| `{}` | {} | `{}` | `{}` | {} |".format(
                file_row["file"], finding["line"], finding["function"],
                finding["identifier"], finding["classification"],
            ))
    rows.extend([
        "",
        "## Model の現状",
        "",
        "`ProofNarrativeModel` は `steps`, `citations`, `step_citation_numbers` を保持する。",
        "`NarrativeCitation` は `step_indices`, `assertion_ids`, `reference_ids`, `statement_bodies` を保持する。",
        "しかしパラメータ特殊化・引用祖先の確定済み導出記録を持つ専用フィールドは現行定義では確認できない。",
        "不足が本当に問題になる実例は、動的ログとテスト結果に基づいて判断する。",
        "",
        "## 3群の Web 経路比較",
        "",
        "| 群 | ProofStep | Reference | 引用対応 | 固定論証 | 本文差分行 | Reference差分行 |",
        "|---|---:|---:|---|---|---:|---:|",
    ])
    runtime = result.get("runtime", {})
    if not runtime:
        rows.append("| 未実施 | — | — | — | — | — | — |")
    for name, entry in runtime.items():
        if "audit_error" in entry:
            rows.append(f"| {name} | — | — | ERROR | ERROR | — | — |")
            continue
        rows.append("| {} | {} | {} | {} | {} | {} |".format(
            name, entry["proof_steps"], entry["references"],
            "PASS" if entry["no_unused_reference"] and entry["bidirectional_provenance_consistent"] else "REVIEW",
            "PASS" if entry["benchmark_all_present"] else "REVIEW",
            entry["proof_diff_lines"], entry["reference_diff_lines"],
        ))
    rows.extend([
        "",
        "## 要注意点",
        "",
        "1. Renderer 内の `validated_specialization_citation_numbers` は特殊化を再判定する。",
        "2. Typed Projection の `toda45_specialization_evidence` は一般 Toda (4.5) を再特殊化する。",
        "3. 安定 η 表記では `_stable_eta_renaming_shape`、完全性の文章では `prop42_exactness_indices` を呼ぶ。",
        "4. 中間ステップ表示省略が `inference_rule.name` の固定文字列に依存する。",
        "5. Citation の全番号が本文に現れることだけでは、各引用の数学的適用条件が保証されたとは言えない。",
        "",
        "## 変更方針（監査の結論ではなく検討案）",
        "",
        "既存の Narrative Model / Projection の拡張可能性を優先し、Renderer では数学的な Rule を再実行しない。",
        "ただし構造検査・循環依存検出・Citation 番号の双方向一致チェックは維持する。",
        "本 R3-41P 監査パッケージにはコード変更を含めない。",
        "",
        "## 次の境界",
        "",
        "監査結果を確認した後で、必要性を実証できた箇所だけ最小修正する。",
        "全体 pytest は Phase 168 終了時に実行する。",
        "",
    ])
    failures = {name: entry["audit_error"] for name, entry in runtime.items()
                if "audit_error" in entry}
    if failures:
        rows.extend(["## 群別の動的監査エラー", ""])
        for name, detail in failures.items():
            rows.extend([f"### {name}", "", "```text", detail, "```", ""])
    if result.get("error"):
        rows.extend(["## 動的監査エラー", "", "```text", result["error"], "```", ""])
    return "\n".join(rows)


def main() -> int:
    if not PROJECT.joinpath(SOURCE_FILES[0]).is_file():
        print("ERROR: Run the package from the project root after extraction.", file=sys.stderr)
        return 2
    for name in EXPECTED:
        for suffix in ("_current.md", "_reference.diff", "_proof.diff", "_audit_error.txt"):
            (OUT / (name + suffix)).unlink(missing_ok=True)
    report: dict[str, object] = {"sources": source_trace()}
    if report["sources"]["missing"]:
        report["error"] = "Missing required source/test files: " + ", ".join(report["sources"]["missing"])
        status = 2
    else:
        status = 0
        try:
            report["runtime"] = runtime_audit()
        except Exception:
            report["error"] = traceback.format_exc()
            status = 1
    print("STATIC_FINDINGS", sum(
        len(x["findings"]) for x in report["sources"]["static"]))
    if "runtime" in report:
        failed_groups = [name for name, item in report["runtime"].items()
                         if "audit_error" in item]
        if failed_groups:
            status = 1
            report["error"] = "Group audit failures: " + ", ".join(failed_groups)
        for name, item in report["runtime"].items():
            if "audit_error" in item:
                print(name, "ERROR", "see", OUT / (name + "_audit_error.txt"))
                continue
            print(name, "steps", item["proof_steps"],
                  "references", item["references"],
                  "citations_match", item["no_unused_reference"],
                  "benchmark", item["benchmark_all_present"],
                  "math_recheck_calls", item["runtime_renderer_projection_rechecks"])
    (OUT / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, default=str) + "\n",
        encoding="utf-8",
    )
    (OUT / "audit.md").write_text(render_report(report), encoding="utf-8")
    if "error" in report:
        print("AUDIT_ERROR:", report["error"])
    print("AUDIT_REPORT", OUT / "audit.md")
    print("AUDIT_JSON", OUT / "audit.json")
    print("FULL_PYTEST_NOT_RUN")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
