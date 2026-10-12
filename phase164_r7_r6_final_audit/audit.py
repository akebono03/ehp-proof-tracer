"""Phase 164 R7-R6: read-only inspection of registry resolution and entry paths."""
from __future__ import annotations

import ast
import json
from pathlib import Path

ENTRYPOINTS = {
    "generator": ("repository_generator_known_group_identity_lookup.py", "find_standard_repository_generator_known_group_identity_nodes"),
    "operation": ("repository_operation_query_facade.py", "query_standard_repository_operation_input"),
    "group": ("toda_calculation_facade.py", "build_standard_toda_report"),
}
SHARED = "phase164_r7_repository_root_resolution.py"
RESOLVER = "phase164_r7_statement_resolution.py"
REQUIRED = (SHARED, RESOLVER, "phase164_r7_r3_generator_registry.py", "phase164_r2_citation_eligibility.py", "phase163_r4_registry_bridge.py")
SCOPED_FILES = (
    "phase164_r3_registry_search_connection.py", "phase164_r4_r8_registry_reconstruction.py",
    "phase164_r5_web_registry_connection.py", "repository_proof_scope.py", "repository_element_lookup.py",
    "repository_operation_query_lookup.py", "toda_group_lookup.py", "toda_calculation.py",
    "toda_literature_statement_boundary.py", "phase163_source_archive_registry.py",
    "phase164_r7_r3_generator_registry.py", SHARED, RESOLVER,
)
REFERENCE_CALLS = {"assertion", "reference", "assertions_for", "assess_phase164_r2_citation", "resolve_registered_statement"}
REPOSITORY_CALLS = {"entries", "get", "find_by_conclusion", "find_by_statement_type", "build_repository_proof_scope"}


def parse_file(root: Path, relative: str) -> ast.Module:
    return ast.parse((root / relative).read_text(encoding="utf-8-sig"), filename=relative)


def find_function(tree: ast.Module, name: str) -> ast.FunctionDef | None:
    return next((node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name), None)


def imported_names(tree: ast.Module) -> set[str]:
    names = set()
    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            names.update(alias.asname or alias.name for alias in node.names)
        elif isinstance(node, ast.Import):
            names.update(alias.asname or alias.name.split('.')[0] for alias in node.names)
    return names


def calls(node: ast.AST) -> list[dict]:
    items = []
    for call in ast.walk(node):
        if not isinstance(call, ast.Call):
            continue
        func = call.func
        name = func.id if isinstance(func, ast.Name) else (func.attr if isinstance(func, ast.Attribute) else None)
        if not name:
            continue
        owner = func.value.id if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name) else None
        items.append({"line": call.lineno, "name": name, "receiver": owner})
    return sorted(items, key=lambda item: (item["line"], item["name"]))


def audit(root: Path) -> dict:
    missing = sorted(p for p in (*REQUIRED, *(file for file, _ in ENTRYPOINTS.values())) if not (root / p).is_file())
    result = {"phase": "164 R7-R6", "mode": "READ_ONLY_POST_CONNECTION_AUDIT", "missing_files": missing,
              "entrypoints": {}, "residual_candidates": [], "citation_boundaries": {}, "findings": [],
              "production_modified": False, "full_pytest_run": False}
    parsed = {}
    for filename in set((*SCOPED_FILES, *(file for file, _ in ENTRYPOINTS.values()), "phase164_r2_citation_eligibility.py")):
        if (root / filename).is_file():
            try:
                parsed[filename] = parse_file(root, filename)
            except (SyntaxError, UnicodeError) as exc:
                result["findings"].append({"kind": "PARSE_ERROR", "file": filename, "detail": str(exc)})
    for kind, (filename, function_name) in ENTRYPOINTS.items():
        tree = parsed.get(filename)
        if tree is None:
            result["entrypoints"][kind] = {"status": "MISSING"}
            continue
        fn = find_function(tree, function_name)
        if fn is None:
            result["entrypoints"][kind] = {"status": "FUNCTION_MISSING"}
            continue
        all_calls = calls(fn)
        guard = [c for c in all_calls if c["name"] in {"validate_repository_internal_proof_roots", "validate_generator_repository_registry_links"}]
        repo = [c for c in all_calls if c["name"] == "build_standard_production_proof_repository"]
        result["entrypoints"][kind] = {"status": "GUARD_CALL_PRESENT" if guard and repo else "GUARD_NOT_CONFIRMED",
            "function": function_name, "guard_calls": guard, "repository_builder_calls": repo,
            "imports": sorted(imported_names(tree))}
        if not guard or not repo:
            result["findings"].append({"kind": "ENTRY_GUARD_NOT_CONFIRMED", "file": filename, "detail": function_name})
    for filename in SCOPED_FILES:
        tree = parsed.get(filename)
        if tree is None:
            result["findings"].append({"kind": "SCOPED_FILE_UNAVAILABLE", "file": filename})
            continue
        for c in calls(tree):
            if c["name"] in REFERENCE_CALLS | REPOSITORY_CALLS:
                result["residual_candidates"].append({"file": filename, **c,
                    "classification": ("citation_or_registry_review" if c["name"] in REFERENCE_CALLS
                                       else "repository_proof_graph_not_automatically_a_defect")})
    citation_tree = parsed.get("phase164_r2_citation_eligibility.py")
    citation_function = find_function(citation_tree, "assess_phase164_r2_citation") if citation_tree else None
    citation_source = ast.get_source_segment((root / "phase164_r2_citation_eligibility.py").read_text(encoding="utf-8-sig"), citation_function) if citation_function else ""
    for token in ("SOURCE_ARCHIVE", "PROOF_INTERNAL", "METADATA_ONLY", "verified_assertion_ids", "assess_citation"):
        result["citation_boundaries"][token] = token in citation_source
        if token not in citation_source:
            result["findings"].append({"kind": "CITATION_GUARD_TOKEN_MISSING", "file": "phase164_r2_citation_eligibility.py", "detail": token})
    special = parsed.get("phase164_r4_r8_registry_reconstruction.py")
    result["fixed_literature_special_route"] = {
        "exists": special is not None,
        "separate_source_confirmation": ("user_confirmed_original" in (root / "phase164_r4_r8_registry_reconstruction.py").read_text(encoding="utf-8-sig")) if special else False,
        "not_equivalent_to_r2_document_order": True,
    }
    result["summary"] = {"guarded_entrypoints": sum(v["status"] == "GUARD_CALL_PRESENT" for v in result["entrypoints"].values()),
        "entrypoints_total": len(ENTRYPOINTS), "residual_candidates": len(result["residual_candidates"]),
        "reference_candidates": sum(c["classification"] == "citation_or_registry_review" for c in result["residual_candidates"]),
        "finding_count": len(result["findings"])}
    result["r7_closure_status"] = "NOT_CERTIFIED_BY_STATIC_AUDIT"
    return result


def write_report(output: Path, result: dict) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Phase 164 R7-R6 最終監査（静的・読み取り専用）", "",
             "- R7 完了判定: **静的監査だけでは認定しない**", "- 既存本番コード変更: なし", "- 全体 pytest: 未実施", "",
             "## 標準入口", ""]
    for branch, item in result["entrypoints"].items():
        lines.append(f"- {branch}: {item['status']} ({item.get('function', 'N/A')})")
    lines.extend(["", "## 候補数", "", f"- 残存呼出候補: {result['summary']['residual_candidates']}",
                  f"- Registry・引用候補: {result['summary']['reference_candidates']}",
                  "- `entries()` / `get()` / `build_repository_proof_scope()` は証明木用のため、それだけで違反ではない。",
                  "", "## 引用境界", ""])
    for token, present in result["citation_boundaries"].items():
        lines.append(f"- {token}: {'検出' if present else '未検出'}")
    lines.extend(["", "## 残件", "",
                  "- 静的に検出した Registry 直接参照は、数学的命題取得なのか検証・監査なのか個別に確認する。",
                  "- π₅³ の固定文献接続（原本確認経路）は R2 掲載順判定と同一ではない。",
                  "- ProofRepository の存在だけで出典・文献命題の真偽・引用適格性を認定しない。",
                  "- Source Archive、metadata_only は証明根拠への自動昇格を認めない。",
                  "- R7 終了には残件の用途分類・対象限定テスト・明示的完了判定が必要。", "",
                  "## 注意事項", "", "これは AST による呼出候補検出であり、動的経路の全探索や数学的証明ではない。", ""])
    if result["findings"]:
        lines.extend(["## 構造上の要確認項目", ""])
        lines.extend(f"- {f['kind']}: {f['file']}" for f in result["findings"])
    (output / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    root = Path.cwd()
    result = audit(root)
    out = root / "phase164_r7_r6_output"
    write_report(out, result)
    print((out / "report.md").read_text(encoding="utf-8"))
    if result["missing_files"] or any(f["kind"] in ("PARSE_ERROR", "ENTRY_GUARD_NOT_CONFIRMED", "CITATION_GUARD_TOKEN_MISSING") for f in result["findings"]):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
