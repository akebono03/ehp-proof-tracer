# Phase 165 R5-R10 追加コード全文

新規ファイルの追加位置：リポジトリ直下の `phase165_renderer_r5_r10_dependency_triage/`。既存の import・クラス・関数には変更なし。

## audit.py

```python
"""Phase 165 R5-R10: read-only runtime/audit/test ownership triage."""
from __future__ import annotations

import ast
from collections import defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "audit_output"
TARGETS = {
    "phase162_web_narrative_integration": (
        "build_phase162_web_validated_isomorphism_markdown", "_phase162_ehp_leaves"
    ),
    "phase162_r3_narrative_connection": (
        "render_phase162_r3_narrative", "render_phase162_r3_with_public_references"
    ),
    "toda_group_proof_narrative_proof_chain_renderer": (
        "render_toda_group_proof_narrative_from_proof_chains_markdown",
    ),
    "toda_group_proof_narrative_concrete_transport": (
        "render_concrete_transport_proof_from_steps",
    ),
}
ROOTS = ("web_group_proof", "main", "cli")


def files_in_scope(root: Path) -> list[Path]:
    paths = [p for p in root.glob("*.py") if ".phase" not in p.name]
    tests = root / "tests"
    if tests.is_dir():
        paths.extend(tests.rglob("*.py"))
    return sorted(paths)


def owner(path: Path, root: Path) -> str:
    relative = path.relative_to(root).as_posix()
    if relative.startswith("tests/") or path.name.startswith("test_"):
        return "test"
    if path.name.startswith(("audit_", "probe_", "check_")) or relative.startswith("probes/"):
        return "audit"
    return "application"


def imported_usage(tree: ast.AST, targets: dict[str, tuple[str, ...]]) -> list[dict]:
    """Record imports and direct calls, preserving the imported symbol's owner."""
    symbols: dict[str, tuple[str, str]] = {}
    modules: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            module = node.module.split(".")[0]
            if module in targets:
                for alias in node.names:
                    symbols[alias.asname or alias.name] = (module, alias.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                module = alias.name.split(".")[0]
                if module in targets:
                    modules[alias.asname or module] = module
    usage = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        imported = None
        if isinstance(node.func, ast.Name):
            imported = symbols.get(node.func.id)
        elif (isinstance(node.func, ast.Attribute)
              and isinstance(node.func.value, ast.Name)):
            module = modules.get(node.func.value.id)
            if module:
                imported = (module, node.func.attr)
        if imported:
            usage.append({"module":imported[0], "symbol":imported[1],
                          "line":node.lineno, "kind":"call"})
    for alias, (module, symbol) in symbols.items():
        usage.append({"module":module,"symbol":symbol,"line":None,
                      "kind":"import", "alias":alias})
    for alias, module in modules.items():
        usage.append({"module":module,"symbol":"*","line":None,
                      "kind":"module_import", "alias":alias})
    return usage


def analyze(root: Path) -> dict:
    files = files_in_scope(root)
    found = {module:{"symbols":[],"application":[],"audit":[],"test":[],
                     "module_present":(root / (module+".py")).is_file()}
             for module in TARGETS}
    errors = []
    for path in files:
        relative = path.relative_to(root).as_posix()
        try:
            source = path.read_text(encoding="utf-8-sig")
            tree = ast.parse(source, filename=relative)
        except (UnicodeError, SyntaxError) as e:
            errors.append({"file":relative,"message":str(e)})
            continue
        module = path.stem
        if path.parent == root and module in TARGETS:
            found[module]["symbols"] = sorted({node.name for node in tree.body
                                                if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef))})
        bucket = owner(path,root)
        for hit in imported_usage(tree,TARGETS):
            if path.parent == root and module == hit["module"]:
                continue
            found[hit["module"]][bucket].append({"file":relative,**hit})

    decisions = {}
    for module, data in found.items():
        application_calls = [x for x in data["application"] if x["kind"] == "call"]
        app_any = len(data["application"])
        non_test_callers = sorted({x["file"] for x in data["application"]})
        by_symbol = defaultdict(lambda:{"application":[],"audit":[],"test":[]})
        for bucket in ("application","audit","test"):
            for item in data[bucket]:
                by_symbol[item["symbol"]][bucket].append(item)
        if app_any:
            disposition = "RETAIN_UNTIL_APPLICATION_DEPENDENCIES_MIGRATED"
        elif data["test"]:
            disposition = "NO_APPLICATION_IMPORT_FOUND_TEST_OR_EXTERNAL_API_REVIEW"
        else:
            disposition = "NO_SCANNED_IMPORT_FOUND_DYNAMIC_API_REVIEW"
        decisions[module] = {
            "defined_functions":data["symbols"],
            "focus_functions":list(TARGETS[module]),
            "module_present":data["module_present"],
            "application_refs":data["application"],
            "audit_refs":data["audit"],
            "test_refs":data["test"],
            "application_call_count":len(application_calls),
            "application_caller_files":non_test_callers,
            "symbol_owners":dict(by_symbol),
            "disposition":disposition,
        }
    checks = {
        "all_target_modules_present": all(v["module_present"] for v in decisions.values()),
        "no_ast_errors":not errors,
        "shared_leaf_dependency_retained": any(
            x["symbol"] == "_phase162_ehp_leaves" and x["file"] == "phase162_pi5_3_web_replay.py"
            for x in decisions["phase162_web_narrative_integration"]["application_refs"]),
        "all_four_targets_classified":len(decisions)==4,
    }
    return {"phase":"165 R5-R10","status":"REVIEW_REQUIRED" if all(checks.values()) else "PRECHECK_FAIL",
            "timestamp_utc":datetime.now(timezone.utc).isoformat(),"scanned_python":len(files),
            "checks":checks,"parse_errors":errors,"targets":decisions,
            "limitations":[
                "Ownership classifies scripts by filename, not by Git tracking or runtime invocation.",
                "A static import or call is not evidence of live runtime execution.",
                "Dynamic imports, external consumers, monkeypatching and reflection may be missed.",
                "This stage does not remove any existing module or change proof rendering.",
                "Historical Phase 162 fixture failures remain unresolved.",
                "Full pytest is deferred until the end of Phase 165.",
            ]}


def markdown(data:dict)->str:
    lines=["# Phase 165 R5-R10 旧 Narrative 依存の用途別監査", "",f"状態: **{data['status']}**", "", "## 事前条件", ""]
    for check,ok in data["checks"].items():
        lines.append(f"- {'PASS' if ok else 'FAIL'}: `{check}`")
    lines.extend(["", "## ファイル別依存と撤去判定", ""])
    for module,result in data["targets"].items():
        lines.extend([f"### `{module}.py`", "",f"- 判定: `{result['disposition']}`",
                      f"- 実行側の直接呼出件数: {result['application_call_count']}",
                      f"- 実行側参照ファイル: {', '.join(result['application_caller_files']) or '検出なし'}"])
        for bucket,japanese in (("application_refs","アプリケーション"),("audit_refs","監査"),("test_refs","テスト")):
            for ref in result[bucket]:
                at=f":{ref['line']}" if ref['line'] else ""
                lines.append(f"- {japanese}: `{ref['file']}{at}` — `{ref['kind']}` / `{ref['symbol']}`")
        lines.append("")
    lines.extend(["## 結論の境界", ""])
    lines.extend("- "+x for x in data["limitations"])
    return "\n".join(lines)+"\n"


def main()->int:
    data=analyze(ROOT)
    OUT.mkdir(exist_ok=True)
    (OUT/"audit.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (OUT/"review.md").write_text(markdown(data),encoding="utf-8")
    counts={name:{"application":len(v["application_refs"]),"audit":len(v["audit_refs"]),
                  "tests":len(v["test_refs"]),"application_calls":v["application_call_count"],
                  "decision":v["disposition"]} for name,v in data["targets"].items()}
    print(json.dumps({"status":data["status"],"checks":data["checks"],
                      "counts":counts,"report":str(OUT/"review.md"),"full_pytest_run":False},
                     ensure_ascii=False,indent=2))
    return 0 if all(data["checks"].values()) else 1

if __name__=="__main__":
    raise SystemExit(main())

```

## test_audit.py

```python
"""Focused tests for R5-R10 ownership attribution; no application code changed."""
from pathlib import Path
import ast
from audit import TARGETS, imported_usage, owner, analyze


def test_r10_owner_separates_app_audit_tests(tmp_path):
    (tmp_path / "tests").mkdir()
    assert owner(tmp_path / "phase162_pi5_3_web_replay.py", tmp_path) == "application"
    assert owner(tmp_path / "audit_phase144.py", tmp_path) == "audit"
    assert owner(tmp_path / "tests" / "test_case.py", tmp_path) == "test"


def test_r10_imported_symbol_alias_records_real_target():
    tree = ast.parse("from phase162_web_narrative_integration import _phase162_ehp_leaves as leaves\nleaves()\n")
    refs = imported_usage(tree,TARGETS)
    assert any(r["symbol"] == "_phase162_ehp_leaves" and r["kind"] == "call" for r in refs)


def test_r10_module_alias_is_recognized():
    tree = ast.parse("import phase162_r3_narrative_connection as old\nold.render_phase162_r3_narrative(None)\n")
    refs = imported_usage(tree,TARGETS)
    assert any(r["symbol"] == "render_phase162_r3_narrative" and r["kind"] == "call" for r in refs)


def test_r10_unrelated_functions_not_misattributed():
    tree = ast.parse("from math import sqrt\nsqrt(4)\n")
    assert imported_usage(tree,TARGETS) == []


def test_r10_fixture_declares_application_dependency(tmp_path):
    root=tmp_path
    for module in TARGETS:
        (root/(module+".py")).write_text("def example():\n    return 1\n",encoding="utf-8")
    (root / "phase162_pi5_3_web_replay.py").write_text(
        "from phase162_web_narrative_integration import _phase162_ehp_leaves\n"
        "_phase162_ehp_leaves()\n",encoding="utf-8")
    result=analyze(root)
    assert result["checks"]["shared_leaf_dependency_retained"]
    assert result["status"] == "REVIEW_REQUIRED"


def test_r10_bom_is_accepted(tmp_path):
    for module in TARGETS:
        (tmp_path/(module+".py")).write_bytes(b"\xef\xbb\xbfdef example():\n    return 1\n")
    (tmp_path / "phase162_pi5_3_web_replay.py").write_text(
        "from phase162_web_narrative_integration import _phase162_ehp_leaves\n",encoding="utf-8")
    result=analyze(tmp_path)
    assert result["checks"]["no_ast_errors"]


def test_r10_removal_requires_no_application_ref(tmp_path):
    for module in TARGETS:
        (tmp_path/(module+".py")).write_text("pass\n",encoding="utf-8")
    (tmp_path / "phase162_pi5_3_web_replay.py").write_text(
        "from phase162_web_narrative_integration import _phase162_ehp_leaves\n",encoding="utf-8")
    result=analyze(tmp_path)
    assert result["targets"]["phase162_web_narrative_integration"]["disposition"] == "RETAIN_UNTIL_APPLICATION_DEPENDENCIES_MIGRATED"

```

## run.ps1

```powershell
$ErrorActionPreference = 'Stop'
$project = Split-Path -Parent $PSScriptRoot
$env:PYTHONPATH = "$PSScriptRoot;$project"
python -m pytest -q "$PSScriptRoot\test_audit.py"
if ($LASTEXITCODE -ne 0) { throw 'R5-R10 scoped audit tests failed' }
python "$PSScriptRoot\audit.py"
if ($LASTEXITCODE -ne 0) { throw 'R5-R10 dependency triage precheck failed; see audit_output\review.md' }
Write-Host 'R5-R10 dependency ownership triage recorded. No application code changed; full pytest NOT run.'

```

