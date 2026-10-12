"""Phase 164 R7-R2: conservative static audit of live statement acquisition paths."""
from __future__ import annotations

import ast
import json
from collections import deque
from pathlib import Path

TARGETS = {
    "group": ("web_group_proof.py", "toda_group_proof_presentation.py", "toda_group_result_proof_replay.py"),
    "generator": ("web_generator_proof.py", "repository_generator_known_group_proof_replay.py", "repository_generator_known_group_identity_lookup.py"),
    "operation": ("web_operation_query_proof.py", "repository_operation_query_facade.py", "repository_operation_query_lookup.py", "repository_operation_query_proof_replay.py"),
}
ENTRY_POINTS = tuple(sorted({p for paths in TARGETS.values() for p in paths}))
DIRECT_MODULES = {"proof_repository", "standard_repository", "standard_production_repository", "theorem_facts", "unified_statement_registry", "phase163_r4_registry_bridge", "phase164_r7_statement_resolution", "phase163_source_archive_registry"}
DIRECT_CALLS = {"get", "entries", "find_by_conclusion", "find_by_statement_type", "find_by_phase", "find_by_theorem", "assertion", "reference", "assertions_for", "build_registry_bridge", "build_registry_with_source_archive", "resolve_registered_statement", "build_standard_proof_repository", "build_standard_production_proof_repository"}
PRIORITY = {
    "phase164_r7_statement_resolution": "already-common-api",
    "proof_repository": "repository-provider",
    "standard_repository": "repository-provider",
    "standard_production_repository": "repository-provider",
    "unified_statement_registry": "registry-provider",
    "phase163_r4_registry_bridge": "bridge-provider",
}


def inspect_source(source: str, filename: str) -> dict:
    tree = ast.parse(source, filename=filename)
    imports = set()
    aliases = {}
    definitions = []
    calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.name.split(".")[0]
                imports.add(name)
                aliases[alias.asname or name] = name
        elif isinstance(node, ast.ImportFrom) and node.module:
            module = node.module.split(".")[0]
            imports.add(module)
            for alias in node.names:
                aliases[alias.asname or alias.name] = module
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            definitions.append({"name": node.name, "line": node.lineno, "kind": type(node).__name__})
        elif isinstance(node, ast.Call):
            f = node.func
            call_name = f.attr if isinstance(f, ast.Attribute) else f.id if isinstance(f, ast.Name) else None
            if call_name in DIRECT_CALLS:
                base = f.value.id if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name) else None
                imported_from = aliases.get(base or call_name)
                calls.append({"line": node.lineno, "name": call_name, "receiver": base, "import_origin": imported_from, "certainty": "import_bound" if imported_from in DIRECT_MODULES else "candidate_unresolved_receiver"})
    return {"imports": sorted(imports), "definitions": sorted(definitions, key=lambda x: x["line"]), "calls": sorted(calls, key=lambda x: x["line"])}


def inspect_repo(root: Path) -> dict:
    root = root.resolve()
    modules = {}
    parse_errors = []
    for path in sorted(root.glob("*.py")):
        if path.name.startswith("audit_") or ".backup" in path.name or "_backup" in path.name:
            continue
        try:
            modules[path.stem] = inspect_source(path.read_text(encoding="utf-8-sig"), path.name)
        except (SyntaxError, UnicodeError) as exc:
            parse_errors.append({"path": path.name, "error": str(exc)})
    adjacency = {m: sorted(name for name in value["imports"] if name in modules) for m, value in modules.items()}
    branches = {}
    for branch, entries in TARGETS.items():
        queue = deque((Path(e).stem, 0) for e in entries if Path(e).stem in modules)
        distances = {}
        while queue:
            current, d = queue.popleft()
            if current in distances:
                continue
            distances[current] = d
            if d < 8:
                queue.extend((name, d + 1) for name in adjacency[current] if name not in distances)
        hits = []
        for name, depth in sorted(distances.items(), key=lambda item: (item[1], item[0])):
            item = modules[name]
            direct_imports = sorted(set(item["imports"]) & DIRECT_MODULES)
            if direct_imports or item["calls"] or name in PRIORITY:
                hits.append({"module": name + ".py", "import_depth": depth, "direct_provider_imports": direct_imports, "candidate_calls": item["calls"], "classification": PRIORITY.get(name, "candidate-needs-manual-review")})
        branches[branch] = {"entry_files": list(entries), "reachable_module_count": len(distances), "candidates": hits}
    test_dir = root / "tests"
    tests = {}
    for branch, entries in TARGETS.items():
        matching = []
        if test_dir.is_dir():
            tokens = {Path(e).stem for e in entries}
            for test in sorted(test_dir.glob("test_*.py")):
                try:
                    contents = test.read_text(encoding="utf-8-sig")
                except UnicodeError:
                    continue
                if any(t in contents for t in tokens):
                    matching.append(str(test.relative_to(root)).replace("\\", "/"))
        tests[branch] = matching
    local_r7 = [n for n in ("phase164_r7_statement_resolution", "tests/test_phase164_r7_statement_resolution") if (root / (n + ("" if n.endswith(".py") else ".py"))).exists()]
    return {"phase": "164 R7-R2", "mode": "READ_ONLY_STATIC_CALL_PATH_INVENTORY", "root": str(root), "module_count": len(modules), "parse_errors": parse_errors, "branches": branches, "related_tests": tests, "local_r7_files": local_r7, "full_pytest_run": False, "production_modified": False, "deletion_authorized": False}


def write_report(data: dict, path: Path) -> None:
    lines = ["# Phase 164 R7-R2 命題取得経路の静的監査", "", "これは import 到達性と AST 呼出候補の調査です。実行時の到達性・証明の正当性・削除安全性は未確認です。", "", f"- 対象ルート直下の Python ファイル: {data['module_count']}", f"- 構文エラー: {len(data['parse_errors'])}", "- 既存本番コード変更: なし", "- 全体 pytest: 未実行", ""]
    for branch, info in data["branches"].items():
        lines += [f"## {branch.title()}", "", f"- 静的到達モジュール: {info['reachable_module_count']}", f"- 要確認候補: {len(info['candidates'])}", "", "| 深さ | モジュール | 直接 import | 呼出候補 | 判定 |", "|---:|---|---|---:|---|"]
        for hit in info["candidates"]:
            lines.append(f"| {hit['import_depth']} | `{hit['module']}` | {', '.join(hit['direct_provider_imports']) or '-'} | {len(hit['candidate_calls'])} | {hit['classification']} |")
        lines += ["", "### 関連 tests/ の候補", ""]
        lines += [f"- `{p}`" for p in data["related_tests"][branch][:35]] or ["- 見つかりませんでした（網羅性を意味しません）"]
        lines.append("")
    lines += ["## R7-R3 に向けた分類", "", "1. Group／Generator／Operation の Web 入口から深さ順に import 依存を確認する。", "2. 命題取得と ProofStep 取得を分離し、文献固定命題は既存の引用適格性判定を必ず維持する。", "3. `ProofRepository` は証明木の保存・検索として残し、文献の真偽を Repository の存在から推論しない。", "4. `source_archive` と `metadata_only` は proof eligible に昇格させない。", "5. 共通 API 経由への切替は利用箇所と対応するテストが確認できてから一箇所ずつ実施する。", "", "## 結論", "", "R7-R2 静的経路棚卸し終了。旧経路削除・本番 API 切替は未許可。", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    for required in ("proof.py", "proof_repository.py", "unified_statement_registry.py", "web_group_proof.py", "web_generator_proof.py", "web_operation_query_proof.py"):
        if not (root / required).is_file():
            raise SystemExit(f"Missing repository baseline file: {required}")
    out = root / "phase164_r7_r2_output"
    out.mkdir(exist_ok=True)
    data = inspect_repo(root)
    (out / "audit.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(data, out / "report.md")
    print((out / "report.md").read_text(encoding="utf-8"))
    if data["parse_errors"]:
        raise SystemExit("Parse errors: investigate audit.json")
    print("Phase 164 R7-R2 read-only scan complete; production unchanged; full pytest NOT run.")


if __name__ == "__main__":
    main()
