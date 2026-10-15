# R5-R12-R1 コード全文

追加・変更対象は監査 ZIP 内の `audit.py`、`test_audit.py`、`README.md`、`AUDIT.md` である。既存アプリケーションコードは変更しない。関数全体と import の全文は以下のファイル内容に含まれる。

## audit.py

```python
"""Read-only Phase 165 R5-R12 function-level retirement gate."""
from __future__ import annotations

import ast
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

TARGETS = {
    "phase162_web_narrative_integration": (
        "build_phase162_web_validated_isomorphism_markdown",
        "_build_phase162_legacy_validated_isomorphism_markdown",
        "_build_phase162_existing_group_connection",
        "_format_phase162_proof_sentences",
        "_compose_phase162_group_conclusion",
        "_phase162_ehp_leaves",
    ),
    "phase162_r3_narrative_connection": (
        "render_phase162_r3_narrative",
        "render_phase162_r3_with_public_references",
        "_phase162_legacy_ehp_body",
    ),
}
BACKUP_PATTERN = re.compile(r"\.phase\d+_[^/\\]*\.py$", re.IGNORECASE)


def production_files(root: Path):
    """Scan active root modules and tests; ignore historical backup snapshots."""
    for path in sorted(root.glob("*.py")):
        if not BACKUP_PATTERN.search(path.name):
            yield path, "application"
    tests = root / "tests"
    if tests.is_dir():
        for path in sorted(tests.rglob("*.py")):
            yield path, "test"


def references_in(tree: ast.AST, module: str, symbol: str) -> list[dict]:
    """Resolve direct from-import, module import aliases, and simple attribute uses."""
    from_aliases = set()
    module_aliases = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == module:
            for alias in node.names:
                if alias.name == symbol:
                    from_aliases.add(alias.asname or alias.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == module:
                    module_aliases.add(alias.asname or module.split(".")[0])
    seen = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Name) and f.id in from_aliases:
                seen.append({"line": node.lineno, "kind": "call"})
            elif isinstance(f, ast.Attribute) and f.attr == symbol and isinstance(f.value, ast.Name) and f.value.id in module_aliases:
                seen.append({"line": node.lineno, "kind": "call"})
        elif isinstance(node, ast.ImportFrom) and node.module == module:
            if any(a.name == symbol for a in node.names):
                seen.append({"line": node.lineno, "kind": "import"})
        elif isinstance(node, ast.Import):
            if any(a.name == module for a in node.names):
                seen.append({"line": node.lineno, "kind": "module_import"})
    return sorted(seen, key=lambda item: (item["line"], item["kind"]))


def local_calls(tree: ast.Module, symbol: str) -> list[dict]:
    out = []
    for fn in tree.body:
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for node in ast.walk(fn):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == symbol:
                out.append({"function": fn.name, "line": node.lineno})
    return out


def audit(root: Path) -> dict:
    root = root.resolve()
    trees = {}
    errors = []
    by_type = defaultdict(int)
    for path, kind in production_files(root):
        try:
            source = path.read_text(encoding="utf-8-sig")
            trees[path] = (ast.parse(source, filename=str(path)), kind)
            by_type[kind] += 1
        except (SyntaxError, UnicodeError) as exc:
            errors.append({"file": str(path.relative_to(root)), "error": str(exc)})
    results = {}
    for module, symbols in TARGETS.items():
        target = root / (module + ".py")
        target_tree = trees.get(target, (None, None))[0]
        for symbol in symbols:
            refs = []
            for path, (tree, kind) in trees.items():
                if path == target:
                    continue
                sites = references_in(tree, module, symbol)
                if sites:
                    refs.append({"file": path.relative_to(root).as_posix(), "kind": kind, "sites": sites})
            defs = [] if target_tree is None else [n.lineno for n in target_tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == symbol]
            internal = [] if target_tree is None else local_calls(target_tree, symbol)
            app = [x for x in refs if x["kind"] == "application"]
            tests = [x for x in refs if x["kind"] == "test"]
            reexports = [] if target_tree is None else [
                {"module": node.module, "line": node.lineno}
                for node in ast.walk(target_tree)
                if isinstance(node, ast.ImportFrom)
                for alias in node.names
                if (alias.asname or alias.name) == symbol
            ]
            shared_reexport = (
                module == "phase162_web_narrative_integration"
                and symbol == "_phase162_ehp_leaves"
                and len(defs) == 0
                and any(entry["module"] == "phase162_ehp_leaf_inputs" for entry in reexports)
            )
            if len(defs) != 1 and not shared_reexport:
                status = "DEFINITION_MISMATCH"
            elif shared_reexport:
                status = "RETAIN_SHARED_REEXPORT"
            elif app:
                status = "RETAIN_APPLICATION_DEPENDENCY"
            elif tests:
                status = "RETAIN_TEST_CONTRACT_REVIEW"
            elif internal:
                status = "RETAIN_INTERNAL_DEPENDENCY_REVIEW"
            else:
                status = "RETIREMENT_CANDIDATE_REVIEW_DYNAMIC"
            results[module + ":" + symbol] = {"definitions": defs, "reexports": reexports, "application_references": app, "test_references": tests, "internal_calls": internal, "decision": status}
    # Verify R5-R11 migration without importing modules or running heavy mathematical fixtures.
    shared = root / "phase162_ehp_leaf_inputs.py"
    replay = root / "phase162_pi5_3_web_replay.py"
    old = root / "phase162_web_narrative_integration.py"
    def has_from(path, mod, name):
        tree = trees.get(path, (None,))[0]
        return tree is not None and any(isinstance(n, ast.ImportFrom) and n.module == mod and any(a.name == name for a in n.names) for n in ast.walk(tree))
    guards = {
        "r5_r11_shared_file_exists": shared.is_file(),
        "replay_imports_shared_leaves": has_from(replay, "phase162_ehp_leaf_inputs", "_phase162_ehp_leaves"),
        "legacy_web_reexports_shared_leaves": has_from(old, "phase162_ehp_leaf_inputs", "_phase162_ehp_leaves"),
        "all_old_entry_symbols_defined_or_shared_reexported": all(
            len(v["definitions"]) == 1 or (
                name == "phase162_web_narrative_integration:_phase162_ehp_leaves"
                and v["decision"] == "RETAIN_SHARED_REEXPORT"
            )
            for name, v in results.items()
        ),
        "parse_errors_empty": not errors,
    }
    return {
        "phase": "165 R5-R12", "status": "REVIEW_REQUIRED" if all(guards.values()) else "PRECONDITION_FAILED",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "scan_counts": dict(by_type), "guards": guards, "parse_errors": errors,
        "functions": results,
        "limitations": [
            "External Python consumers, reflection, dynamic imports and monkeypatching are not fully enumerable.",
            "A retirement candidate is not permission to delete a documented or externally used API.",
            "GitHub may lag behind local R5-R11 patches; verify local source first.",
            "Historical Phase162 fixture failures are not changed or marked successful.",
            "No full pytest or mathematical certification is performed.",
        ],
    }


def review(result: dict) -> str:
    lines = ["# Phase 165 R5-R12 旧 Narrative 関数単位の撤去判定", "", f"判定: **{result['status']}**", "", "## R5-R11 前提条件"]
    lines += [f"- {'PASS' if ok else 'FAIL'}: `{k}`" for k, ok in result["guards"].items()]
    lines += ["", "## 関数別の依存と暫定判定", ""]
    for name, item in result["functions"].items():
        lines += [f"### `{name}`", f"- 判定: `{item['decision']}`", f"- 定義行: {item['definitions']}", f"- 共通再公開: {item['reexports'] or 'なし'}", f"- 同一ファイル内の呼出: {item['internal_calls'] or '検出なし'}"]
        for label, key in (("アプリケーション", "application_references"), ("テスト", "test_references")):
            lines.append(f"- {label}側の参照:")
            values = item[key]
            lines += [f"  - `{v['file']}`: {v['sites']}" for v in values] if values else ["  - 検出なし"]
        lines.append("")
    lines += ["## 判断の境界", "", "本監査は関数単位の静的な依存関係を分類するもので、旧関数の削除は実施しません。", "", "旧 Phase 162 の fixture 不整合6件は引き続き未解決です。", "", "全体 pytest は実施していません。"]
    return "\n".join(lines) + "\n"


def main():
    root = Path(__file__).resolve().parent.parent
    out = Path(__file__).resolve().parent / "audit_output"
    out.mkdir(exist_ok=True)
    result = audit(root)
    (out / "audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "review.md").write_text(review(result), encoding="utf-8")
    print(json.dumps({"status": result["status"], "guards": result["guards"], "decisions": {k:v["decision"] for k,v in result["functions"].items()}, "report": str(out / "review.md"), "full_pytest_run": False}, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["status"] == "REVIEW_REQUIRED" else 1)


if __name__ == "__main__":
    main()

```

## test_audit.py

```python
"""Focused unit tests; no project-wide pytest."""
import ast
from pathlib import Path
from tempfile import TemporaryDirectory

from audit import audit, local_calls, production_files, references_in, review


def test_from_import_call():
    tree = ast.parse("from old import target as t\nt()\n")
    assert {x["kind"] for x in references_in(tree, "old", "target")} == {"import", "call"}


def test_module_import_call():
    tree = ast.parse("import old as obj\nobj.target()\n")
    assert {x["kind"] for x in references_in(tree, "old", "target")} == {"module_import", "call"}


def test_unrelated_symbol_excluded():
    tree = ast.parse("from old import different\ndifferent()\n")
    assert references_in(tree, "old", "target") == []


def test_local_calls():
    tree = ast.parse("def first():\n    target()\n\ndef second():\n    other()\n")
    assert local_calls(tree, "target") == [{"function": "first", "line": 2}]


def test_backup_files_excluded():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "active.py").write_text("pass\n", encoding="utf-8")
        (root / "active.phase165_r48_backup.py").write_text("pass\n", encoding="utf-8")
        selected = [p.name for p, _ in production_files(root)]
        assert selected == ["active.py"]


def test_audit_fail_closed_when_r5_r11_missing():
    with TemporaryDirectory() as tmp:
        result = audit(Path(tmp))
        assert result["status"] == "PRECONDITION_FAILED"
        assert not result["guards"]["r5_r11_shared_file_exists"]


def test_review_contains_decisions():
    with TemporaryDirectory() as tmp:
        result = audit(Path(tmp))
        text = review(result)
        assert "関数別の依存" in text
        assert "PRECONDITION_FAILED" in text


def test_shared_reexport_is_valid_r5_r11_state():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "phase162_ehp_leaf_inputs.py").write_text(
            "def _phase162_ehp_leaves():\n    return ()\n", encoding="utf-8"
        )
        old = "phase162_web_narrative_integration.py"
        (root / old).write_text(
            "from phase162_ehp_leaf_inputs import _phase162_ehp_leaves\n" +
            "\n".join("def " + n + "():\n    pass" for n in (
                "build_phase162_web_validated_isomorphism_markdown",
                "_build_phase162_legacy_validated_isomorphism_markdown",
                "_build_phase162_existing_group_connection",
                "_format_phase162_proof_sentences",
                "_compose_phase162_group_conclusion",
            )) + "\n", encoding="utf-8"
        )
        (root / "phase162_pi5_3_web_replay.py").write_text(
            "from phase162_ehp_leaf_inputs import _phase162_ehp_leaves\n", encoding="utf-8"
        )
        (root / "phase162_r3_narrative_connection.py").write_text(
            "\n".join("def " + n + "():\n    pass" for n in (
                "render_phase162_r3_narrative",
                "render_phase162_r3_with_public_references",
                "_phase162_legacy_ehp_body",
            )) + "\n", encoding="utf-8"
        )
        result = audit(root)
        assert result["status"] == "REVIEW_REQUIRED"
        assert result["guards"]["all_old_entry_symbols_defined_or_shared_reexported"]
        key = "phase162_web_narrative_integration:_phase162_ehp_leaves"
        assert result["functions"][key]["decision"] == "RETAIN_SHARED_REEXPORT"


def test_missing_shared_reexport_still_fails_closed():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "phase162_ehp_leaf_inputs.py").write_text(
            "def _phase162_ehp_leaves():\n    return ()\n", encoding="utf-8"
        )
        (root / "phase162_web_narrative_integration.py").write_text(
            "pass\n", encoding="utf-8"
        )
        (root / "phase162_pi5_3_web_replay.py").write_text(
            "from phase162_ehp_leaf_inputs import _phase162_ehp_leaves\n", encoding="utf-8"
        )
        result = audit(root)
        assert result["status"] == "PRECONDITION_FAILED"
        assert not result["guards"]["legacy_web_reexports_shared_leaves"]

```
