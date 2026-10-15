# Phase 165 R5-R14 新規コード全文

追加位置：リポジトリ直下 `phase165_renderer_r5_r14_retirement_batch_gate/` 内。

## audit.py

```python
"""R5-R14: read-only, function-level old Narrative retirement gate."""
from __future__ import annotations
import ast
import json
import re
from pathlib import Path

TARGETS = {
    "phase162_web_narrative_integration": (
        "_format_phase162_proof_sentences",
        "_compose_phase162_group_conclusion",
        "_build_phase162_legacy_validated_isomorphism_markdown",
        "_build_phase162_existing_group_connection",
        "build_phase162_web_validated_isomorphism_markdown",
        "_phase162_ehp_leaves",
    ),
    "phase162_r3_narrative_connection": (
        "_element_latex", "_group_latex", "_structure_latex",
        "_ordered_ancestry", "_reference_section",
        "_phase162_legacy_ehp_body", "_phase162_web_display_math_delimiters",
        "render_phase162_r3_narrative",
        "render_phase162_r3_with_public_references",
    ),
    "toda_group_proof_narrative_proof_chain_renderer": (
        "render_toda_group_proof_narrative_from_proof_chains_markdown",
    ),
    "toda_group_proof_narrative_concrete_transport": (
        "render_concrete_transport_proof_from_steps",
    ),
}
ROOTS = ("web_group_proof.py", "main.py", "cli.py")
EXEMPT_ARCHIVE = re.compile(r"\.phase\d+_.*\.py$", re.I)

def read_source(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")

def is_audit(path: Path) -> bool:
    return path.name.startswith(("audit_", "probe_", "check_")) or path.name.endswith("_audit.py")

def candidates(root: Path):
    for p in sorted(root.glob("*.py")):
        if EXEMPT_ARCHIVE.search(p.name):
            continue
        yield p, "audit" if is_audit(p) else "application"
    tests = root / "tests"
    if tests.exists():
        for p in sorted(tests.rglob("*.py")):
            yield p, "test"

def calls_in(node: ast.AST) -> set[str]:
    return {
        x.func.id if isinstance(x.func, ast.Name) else x.func.attr
        for x in ast.walk(node) if isinstance(x, ast.Call)
        if isinstance(x.func, (ast.Name, ast.Attribute))
    }

def inspect(root: Path) -> dict:
    root = root.resolve()
    trees = {}
    errors = []
    for path, kind in candidates(root):
        try:
            trees[path.relative_to(root).as_posix()] = (ast.parse(read_source(path), filename=str(path)), kind)
        except (SyntaxError, UnicodeError) as exc:
            errors.append({"path":str(path.relative_to(root)), "error":str(exc)})
    dependencies = {}
    for module, funcs in TARGETS.items():
        src_key = module + ".py"
        tree = trees.get(src_key, (None, None))[0]
        definitions = {node.name:node for node in tree.body if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef))} if tree else {}
        reexports = {
            alias.asname or alias.name for node in tree.body
            if isinstance(node,ast.ImportFrom) and node.module == "phase162_ehp_leaf_inputs"
            for alias in node.names
        } if tree else set()
        for fn in funcs:
            key=module+":"+fn
            records=[]
            for rel,(other,kind) in trees.items():
                aliases=set()
                modules=set()
                if rel == src_key:
                    aliases.add(fn)
                for node in ast.walk(other):
                    if isinstance(node,ast.ImportFrom) and node.module == module:
                        for alias in node.names:
                            if alias.name == fn:
                                aliases.add(alias.asname or alias.name)
                    if isinstance(node,ast.Import):
                        for alias in node.names:
                            if alias.name == module:
                                modules.add(alias.asname or alias.name)
                for node in ast.walk(other):
                    if not isinstance(node,ast.Call):
                        continue
                    called = node.func
                    direct = isinstance(called,ast.Name) and called.id in aliases
                    dotted = isinstance(called,ast.Attribute) and called.attr == fn and isinstance(called.value,ast.Name) and called.value.id in modules
                    if direct or dotted:
                        records.append({"file":rel,"line":node.lineno,"kind":kind,"internal":rel==src_key})
            external_prod=[r for r in records if r["kind"]=="application" and not r["internal"]]
            external_audit=[r for r in records if r["kind"]=="audit"]
            external_test=[r for r in records if r["kind"]=="test"]
            internal=[r for r in records if r["internal"]]
            if fn in definitions:
                state="DEFINED"
            elif fn in reexports:
                state="REEXPORTED"
            else:
                state="MISSING"
            if external_prod:
                decision="KEEP_APPLICATION_CALLER"
            elif external_test:
                decision="KEEP_TEST_API_PENDING_MIGRATION"
            elif internal:
                decision="KEEP_INTERNAL_PENDING_REMOVAL"
            elif external_audit:
                decision="RETIRED_FROM_APPLICATION_AUDIT_ONLY"
            else:
                decision="NO_STATIC_CALLERS_REVIEW_EXTERNAL_API"
            dependencies[key]={"state":state,"decision":decision,"application":external_prod,"tests":external_test,
                               "audit":external_audit,"internal":internal}
    leaf=root/"phase162_ehp_leaf_inputs.py"
    replay=root/"phase162_pi5_3_web_replay.py"
    old=root/"phase162_web_narrative_integration.py"
    guards={
        "shared_leaf_module":leaf.is_file(),
        "replay_uses_shared_module": replay.is_file() and "from phase162_ehp_leaf_inputs import _phase162_ehp_leaves" in read_source(replay),
        "web_reexports_leaf":old.is_file() and "from phase162_ehp_leaf_inputs import _phase162_ehp_leaves" in read_source(old),
        "public_web_entry_present":(root/"web_group_proof.py").is_file(),
        "no_parse_errors":not errors,
    }
    high_risk=[k for k,v in dependencies.items() if v["decision"]=="KEEP_APPLICATION_CALLER"]
    missing=[k for k,v in dependencies.items() if v["state"]=="MISSING"]
    return {"phase":"165 R5-R14","status":"REVIEW_REQUIRED" if all(guards.values()) and not missing else "PRECONDITION_FAILED",
            "guards":guards,"counts":{"scanned":len(trees),"functions":len(dependencies),
             "app_bound":len(high_risk),"missing":len(missing),
             "test_contracts":sum(v["decision"]=="KEEP_TEST_API_PENDING_MIGRATION" for v in dependencies.values())},
            "application_bound":high_risk,"missing_symbols":missing,
            "decisions":dependencies,"parse_errors":errors,
            "notes":["R5-R14 is read only; it never deletes or rewrites application code.",
                     "Static imports and direct calls do not prove absence of dynamic/external dependencies.",
                     "Historical Phase162 fixture regressions are not resolved here.",
                     "Phase165 global pytest is not run."]}

def save_report(result:dict, out:Path)->None:
    out.mkdir(parents=True,exist_ok=True)
    (out/"audit.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    lines=["# Phase 165 R5-R14 一括撤去準備監査", "",f"判定: **{result['status']}**","",
           "## 前提条件",""]
    lines += [f"- {k}: {'PASS' if v else 'FAIL'}" for k,v in result["guards"].items()]
    lines += ["","## 関数別の撤去ゲート",""]
    for k,v in result["decisions"].items():
        lines += [f"### `{k}`",f"- 定義: `{v['state']}`",f"- 判定: `{v['decision']}`"]
        for label,field in (("本番","application"),("内部","internal"),("テスト","tests"),("監査","audit")):
            a=v[field]
            lines.append(f"- {label}直接呼出: {len(a)}")
            for x in a[:12]: lines.append(f"  - `{x['file']}:{x['line']}`")
        lines.append("")
    lines += ["## R5-R15 に向けた条件","",
              "- アプリケーションの呼出元を先に共通モジュールへ移すか、保存する互換 API を明示する。",
              "- 旧 Narrative の出力関数は、テスト・外部 API 契約を確認するまで無条件には削除しない。",
              "- 旧 Phase 162 fixture の6件の失敗は別途記録し、成功扱いにしない。",
              "- Group Proof の完成・未完成 Narrative の一致を R5-R15 の限定回帰テストで保持する。"]
    (out/"review.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

if __name__=="__main__":
    project=Path(__file__).resolve().parent.parent
    result=inspect(project)
    save_report(result,Path(__file__).resolve().parent/"audit_output")
    print(json.dumps({k:result[k] for k in ("status","guards","counts","application_bound","missing_symbols")},ensure_ascii=False,indent=2))
    raise SystemExit(0 if result["status"]=="REVIEW_REQUIRED" else 2)

```

## test_audit.py

```python
from pathlib import Path
from audit import inspect, save_report, calls_in, is_audit, read_source, TARGETS
import ast
import json

def make_project(tmp_path:Path):
    (tmp_path/"tests").mkdir()
    (tmp_path/"phase162_ehp_leaf_inputs.py").write_text("def _phase162_ehp_leaves(): return ()\n",encoding="utf-8")
    (tmp_path/"phase162_pi5_3_web_replay.py").write_text(
        "from phase162_ehp_leaf_inputs import _phase162_ehp_leaves\n"
        "def replay(): return _phase162_ehp_leaves()\n",encoding="utf-8")
    (tmp_path/"phase162_web_narrative_integration.py").write_text(
        "from phase162_ehp_leaf_inputs import _phase162_ehp_leaves\n"
        "def build_phase162_web_validated_isomorphism_markdown(): return _phase162_ehp_leaves()\n",encoding="utf-8")
    (tmp_path/"phase162_r3_narrative_connection.py").write_text(
        "def render_phase162_r3_narrative(): return 1\n"
        "def render_phase162_r3_with_public_references(): return render_phase162_r3_narrative()\n",encoding="utf-8")
    (tmp_path/"toda_group_proof_narrative_proof_chain_renderer.py").write_text(
        "def render_toda_group_proof_narrative_from_proof_chains_markdown(): return ''\n",encoding="utf-8")
    (tmp_path/"toda_group_proof_narrative_concrete_transport.py").write_text(
        "def render_concrete_transport_proof_from_steps(): return ''\n",encoding="utf-8")
    (tmp_path/"web_group_proof.py").write_text("def build_standard_web_group_proof_view(): return None\n",encoding="utf-8")
    for module, names in TARGETS.items():
        path=tmp_path/(module+".py")
        present=path.read_text(encoding="utf-8")
        for name in names:
            if "def "+name+"(" not in present and not (name=="_phase162_ehp_leaves" and module=="phase162_web_narrative_integration"):
                present += "def "+name+"(): return None\n"
        path.write_text(present,encoding="utf-8")

def test_r14_reexport_is_not_missing(tmp_path):
    make_project(tmp_path)
    r=inspect(tmp_path)
    assert r["status"]=="REVIEW_REQUIRED"
    assert r["decisions"]["phase162_web_narrative_integration:_phase162_ehp_leaves"]["state"]=="REEXPORTED"

def test_r14_application_calls_block_removal(tmp_path):
    make_project(tmp_path)
    (tmp_path/"client.py").write_text(
        "from phase162_r3_narrative_connection import render_phase162_r3_narrative\n"
        "def client(): return render_phase162_r3_narrative()\n",encoding="utf-8")
    r=inspect(tmp_path)
    assert r["decisions"]["phase162_r3_narrative_connection:render_phase162_r3_narrative"]["decision"]=="KEEP_APPLICATION_CALLER"

def test_r14_test_contract_detected(tmp_path):
    make_project(tmp_path)
    (tmp_path/"tests"/"test_old.py").write_text(
        "from phase162_r3_narrative_connection import render_phase162_r3_narrative\n"
        "def test_old(): assert render_phase162_r3_narrative() == 1\n",encoding="utf-8")
    r=inspect(tmp_path)
    assert r["decisions"]["phase162_r3_narrative_connection:render_phase162_r3_narrative"]["decision"]=="KEEP_TEST_API_PENDING_MIGRATION"

def test_r14_missing_reexport_is_failure(tmp_path):
    make_project(tmp_path)
    (tmp_path/"phase162_web_narrative_integration.py").write_text(
        "def build_phase162_web_validated_isomorphism_markdown(): return 1\n",encoding="utf-8")
    r=inspect(tmp_path)
    assert r["status"]=="PRECONDITION_FAILED"

def test_r14_bom_and_archives(tmp_path):
    make_project(tmp_path)
    (tmp_path/"client.py").write_bytes(b"\xef\xbb\xbf"+b"def client(): return 1\n")
    (tmp_path/"phase162_r3_narrative_connection.phase165_r43_backup.py").write_text("def broken(:\n",encoding="utf-8")
    assert inspect(tmp_path)["guards"]["no_parse_errors"]

def test_r14_report_outputs(tmp_path):
    make_project(tmp_path)
    r=inspect(tmp_path)
    save_report(r,tmp_path/"reports")
    assert json.loads((tmp_path/"reports"/"audit.json").read_text(encoding="utf-8"))["phase"]=="165 R5-R14"
    assert "一括撤去" in (tmp_path/"reports"/"review.md").read_text(encoding="utf-8")

def test_r14_audit_classification():
    assert is_audit(Path("audit_phase144.py"))
    assert not is_audit(Path("phase162_web_narrative_integration.py"))

def test_r14_call_parser():
    assert calls_in(ast.parse("run(); object.render()"))=={"run","render"}

```

## run.ps1

```powershell
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = "$here;$(Split-Path -Parent $here);$env:PYTHONPATH"
python -m pytest -q "$here\test_audit.py"
if ($LASTEXITCODE -ne 0) { throw "R5-R14 audit self-tests failed" }
python "$here\audit.py"
if ($LASTEXITCODE -ne 0) { throw "R5-R14 precondition failed; inspect audit_output\review.md" }
Write-Host "R5-R14 retirement gate recorded. No application code modified; full pytest NOT run."

```
