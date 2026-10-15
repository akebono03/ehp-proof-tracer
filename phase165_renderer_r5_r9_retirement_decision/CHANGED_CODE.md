# Phase 165 R5-R9 変更コード全文

新規ファイルのみ。既存コードは変更しない。追加位置はリポジトリ直下の `phase165_renderer_r5_r9_retirement_decision/`。

## `audit.py`

```python
"""Read-only Phase 165 R5-R9 historical Narrative retirement dependency audit."""
from __future__ import annotations

import ast
from collections import deque
from datetime import datetime, timezone
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "audit_output"
TARGETS = {
    "phase162_web_narrative_integration.py": (
        "build_phase162_web_validated_isomorphism_markdown",
        "_phase162_ehp_leaves",
    ),
    "phase162_r3_narrative_connection.py": (
        "render_phase162_r3_narrative",
        "render_phase162_r3_with_public_references",
    ),
    "toda_group_proof_narrative_proof_chain_renderer.py": (
        "render_toda_group_proof_narrative_from_proof_chains_markdown",
    ),
    "toda_group_proof_narrative_concrete_transport.py": (
        "render_concrete_transport_proof_from_steps",
    ),
}
PUBLIC = ("web_group_proof.py", "main.py", "cli.py")
SECONDARY = (
    "web_generator_proof.py", "web_generator_exploration.py",
    "web_generator_execution.py", "web_operation_query_proof.py",
)


def source_files(root: Path) -> list[Path]:
    """Live root and tracked-style tests only; exclude root historical copies."""
    files = [p for p in root.glob("*.py") if ".phase" not in p.name]
    tests = root / "tests"
    if tests.is_dir():
        files.extend(tests.rglob("*.py"))
    return sorted(files)


def shortest(graph: dict[str, set[str]], start: str, target: str):
    if start not in graph or target not in graph:
        return None
    queue = deque([(start,)])
    seen = {start}
    while queue:
        route = queue.popleft()
        if route[-1] == target:
            return list(route)
        for nxt in sorted(graph.get(route[-1], ())):
            if nxt not in seen:
                seen.add(nxt)
                queue.append(route + (nxt,))
    return None


def analyze(root: Path) -> dict:
    files = source_files(root)
    root_modules = {p.stem: p.name for p in files if p.parent == root}
    graph = {p.name: set() for p in files if p.parent == root}
    dependencies = []
    string_references = []
    errors = []
    target_modules = {Path(name).stem for name in TARGETS}
    for path in files:
        relative = path.relative_to(root).as_posix()
        try:
            data = path.read_text(encoding="utf-8-sig")
            tree = ast.parse(data, filename=relative)
        except (SyntaxError, UnicodeError) as exc:
            errors.append({"file": relative, "error": str(exc)})
            continue
        local_modules = {}
        symbols = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                module = node.module.split(".")[0]
                if module in root_modules and path.parent == root:
                    graph[path.name].add(root_modules[module])
                if module in target_modules:
                    for a in node.names:
                        symbols[a.asname or a.name] = (module, a.name)
                        dependencies.append({"caller":relative,"line":node.lineno,
                                             "module":module,"kind":"from_import","symbol":a.name})
            elif isinstance(node, ast.Import):
                for a in node.names:
                    module = a.name.split(".")[0]
                    if module in root_modules and path.parent == root:
                        graph[path.name].add(root_modules[module])
                    if module in target_modules:
                        local_modules[a.asname or module] = module
                        dependencies.append({"caller":relative,"line":node.lineno,
                                             "module":module,"kind":"module_import","symbol":a.name})
            elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                if any(module in node.value for module in target_modules):
                    string_references.append({"caller":relative,"line":getattr(node,"lineno",0),
                                              "value":node.value[:160]})
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            module = symbol = None
            if isinstance(node.func, ast.Name) and node.func.id in symbols:
                module, symbol = symbols[node.func.id]
            elif (isinstance(node.func,ast.Attribute) and isinstance(node.func.value,ast.Name)
                  and node.func.value.id in local_modules):
                module = local_modules[node.func.value.id]
                symbol = node.func.attr
            if module is not None:
                dependencies.append({"caller":relative,"line":node.lineno,
                                     "module":module,"kind":"call","symbol":symbol})
    results = {}
    for path, symbols in TARGETS.items():
        module = Path(path).stem
        module_deps = [x for x in dependencies if x["module"] == module]
        production = [x for x in module_deps if not x["caller"].startswith("tests/")]
        test = [x for x in module_deps if x["caller"].startswith("tests/")]
        public_paths = {p:shortest(graph,p,path) for p in PUBLIC+SECONDARY}
        results[path] = {
            "defined_focus_symbols":list(symbols),
            "production_dependencies":production,
            "test_dependencies":test,
            "production_dependency_count":len(production),
            "test_dependency_count":len(test),
            "public_import_paths":public_paths,
            "decision": "RETAIN_DEPENDENT_MODULE" if production else (
                "RETAIN_TEST_CONTRACT_REVIEW" if test else "NO_STATIC_DEPENDENCY_REVIEW_DYNAMIC"),
        }
    checks = {
        "target_files_exist":all((root / p).is_file() for p in TARGETS),
        "no_parse_errors":not errors,
        "normal_web_not_reaching_legacy":all(
            results[t]["public_import_paths"].get("web_group_proof.py") is None
            for t in ("phase162_web_narrative_integration.py","phase162_r3_narrative_connection.py")),
    }
    return {
        "phase":"165 R5-R9","status":"REVIEW_REQUIRED",
        "timestamp_utc":datetime.now(timezone.utc).isoformat(),
        "scanned_python":len(files),"checks":checks,"parse_errors":errors,
        "targets":results,"string_references":string_references,
        "limitations":[
            "No source files were removed or modified.",
            "Root-module static imports and direct calls do not establish all runtime reachability.",
            "Reflection, dynamic imports, external consumers, and indirect callable aliases require separate review.",
            "Absence of import does not by itself authorize deletion of a public API.",
            "Historical Phase162 fixture failures (6) remain unresolved and are not marked passing.",
            "Full pytest must only run at the end of Phase 165.",
        ],
    }


def markdown(data: dict) -> str:
    lines = ["# Phase 165 R5-R9 旧 Narrative 経路の撤去可否監査", "", f"判定: **{data['status']}**", "", "## 事前チェック", ""]
    for name, valid in data["checks"].items():
        lines.append(f"- {'PASS' if valid else 'FAIL'}: `{name}`")
    lines += ["", "## 関数・モジュール別の判定", ""]
    for name, result in data["targets"].items():
        lines += [f"### `{name}`", "",f"- 判定: `{result['decision']}`",
                  f"- 本番側参照: {result['production_dependency_count']} 件",
                  f"- テスト側参照: {result['test_dependency_count']} 件"]
        for label, key in (("本番側", "production_dependencies"),("テスト側","test_dependencies")):
            for item in result[key]:
                lines.append(f"- {label}: `{item['caller']}:{item['line']}` — `{item['kind']}` / `{item['symbol']}`")
        for entry, chain in result["public_import_paths"].items():
            if chain:
                lines.append(f"- 既知入口 `{entry}`: " + " → ".join(f"`{p}`" for p in chain))
        lines.append("")
    lines += ["## 動的参照の可能性がある文字列", ""]
    for item in data["string_references"]:
        lines.append(f"- `{item['caller']}:{item['line']}`: `{item['value']}`")
    if not data["string_references"]:
        lines.append("- 検出なし（動的参照が存在しないことの証明ではない）")
    lines += ["", "## 制約と次の境界", ""] + [f"- {v}" for v in data["limitations"]]
    return "\n".join(lines) + "\n"


def main() -> int:
    data = analyze(ROOT)
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/"audit.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (OUT/"review.md").write_text(markdown(data),encoding="utf-8")
    counts = {k:{"production":v["production_dependency_count"],"tests":v["test_dependency_count"],"decision":v["decision"]} for k,v in data["targets"].items()}
    print(json.dumps({"status":data["status"],"checks":data["checks"],"scanned_python":data["scanned_python"],"target_decisions":counts,"report":str(OUT/"review.md"),"full_pytest_run":False},ensure_ascii=False,indent=2))
    return 0 if all(data["checks"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())

```

## `test_audit.py`

```python
"""Focused isolated tests for the R5-R9 audit utility."""
from pathlib import Path

from audit import analyze, markdown, shortest, source_files


def _fixture(tmp_path: Path):
    (tmp_path/"phase162_web_narrative_integration.py").write_text("def _phase162_ehp_leaves():\n    return ()\n",encoding="utf-8")
    (tmp_path/"phase162_r3_narrative_connection.py").write_text("def render_phase162_r3_narrative():\n    return ''\n",encoding="utf-8")
    (tmp_path/"toda_group_proof_narrative_proof_chain_renderer.py").write_text("def render_toda_group_proof_narrative_from_proof_chains_markdown():\n    return ''\n",encoding="utf-8")
    (tmp_path/"toda_group_proof_narrative_concrete_transport.py").write_text("def render_concrete_transport_proof_from_steps():\n    return ''\n",encoding="utf-8")
    (tmp_path/"web_group_proof.py").write_text("from phase165_r52_partial_proof import render_partial_proof_markdown\n",encoding="utf-8")
    (tmp_path/"phase162_pi5_3_web_replay.py").write_text("from phase162_web_narrative_integration import _phase162_ehp_leaves\ndef use():\n    return _phase162_ehp_leaves()\n",encoding="utf-8")
    tests=tmp_path/"tests"
    tests.mkdir()
    (tests/"test_old.py").write_text("from phase162_r3_narrative_connection import render_phase162_r3_narrative\n",encoding="utf-8")


def test_r9_dependency_blocks_wholesale_deletion(tmp_path):
    _fixture(tmp_path)
    result=analyze(tmp_path)
    old=result["targets"]["phase162_web_narrative_integration.py"]
    assert old["decision"]=="RETAIN_DEPENDENT_MODULE"
    assert any(x["symbol"]=="_phase162_ehp_leaves" for x in old["production_dependencies"])


def test_r9_test_only_dependency_is_not_auto_deleted(tmp_path):
    _fixture(tmp_path)
    old=analyze(tmp_path)["targets"]["phase162_r3_narrative_connection.py"]
    assert old["decision"]=="RETAIN_TEST_CONTRACT_REVIEW"
    assert old["production_dependency_count"]==0
    assert old["test_dependency_count"]==1


def test_r9_absence_does_not_imply_safe_deletion(tmp_path):
    _fixture(tmp_path)
    old=analyze(tmp_path)["targets"]["toda_group_proof_narrative_concrete_transport.py"]
    assert old["decision"]=="NO_STATIC_DEPENDENCY_REVIEW_DYNAMIC"


def test_r9_public_path_detected(tmp_path):
    _fixture(tmp_path)
    (tmp_path/"web_group_proof.py").write_text("from phase162_r3_narrative_connection import render_phase162_r3_narrative\n",encoding="utf-8")
    result=analyze(tmp_path)
    assert not result["checks"]["normal_web_not_reaching_legacy"]


def test_r9_bom_and_archive_exclusion(tmp_path):
    _fixture(tmp_path)
    (tmp_path/"extra.phase165_r5_backup.py").write_text("invalid!",encoding="utf-8")
    (tmp_path/"bom.py").write_bytes(b"\xef\xbb\xbffrom phase162_r3_narrative_connection import render_phase162_r3_narrative\n")
    result=analyze(tmp_path)
    assert not result["parse_errors"]
    assert all("backup" not in p.name for p in source_files(tmp_path))


def test_r9_report_contains_decisions(tmp_path):
    _fixture(tmp_path)
    report=markdown(analyze(tmp_path))
    assert "RETAIN_DEPENDENT_MODULE" in report
    assert "RETAIN_TEST_CONTRACT_REVIEW" in report
    assert "## 制約と次の境界" in report


def test_r9_shortest_path():
    graph={"a.py":{"b.py"},"b.py":{"c.py"},"c.py":set()}
    assert shortest(graph,"a.py","c.py")==["a.py","b.py","c.py"]
    assert shortest(graph,"c.py","a.py") is None

```

## `run.ps1`

```powershell
$ErrorActionPreference = 'Stop'
$project = Split-Path -Parent $PSScriptRoot
$env:PYTHONPATH = "$PSScriptRoot;$project"
python -m pytest -q "$PSScriptRoot\test_audit.py"
if ($LASTEXITCODE -ne 0) { throw 'R5-R9 audit tests failed' }
python "$PSScriptRoot\audit.py"
if ($LASTEXITCODE -ne 0) { throw 'R5-R9 audit preflight failed: inspect audit_output\review.md' }
Write-Host 'R5-R9 dependency decisions recorded. REVIEW REQUIRED. No application source changed; full pytest NOT run.'

```

