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
