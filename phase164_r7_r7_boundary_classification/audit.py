"""R7-R7: fail-closed classification of the eight R7-R6 registry/citation sites."""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path

SITES = (
    ("phase164_r3_registry_search_connection.py", "resolve_registered_statement", "shared_resolver_caller"),
    ("phase164_r4_r8_registry_reconstruction.py", "assertion", "fixed_literature_special_path_exception"),
    ("phase164_r4_r8_registry_reconstruction.py", "reference", "fixed_literature_special_path_exception"),
    ("phase163_source_archive_registry.py", "reference", "source_archive_registration_only"),
    ("phase164_r7_repository_root_resolution.py", "resolve_registered_statement", "shared_internal_root_caller"),
    ("phase164_r7_statement_resolution.py", "assertion", "shared_resolver_implementation"),
    ("phase164_r7_statement_resolution.py", "reference", "shared_resolver_implementation"),
    ("phase164_r7_statement_resolution.py", "assess_phase164_r2_citation", "citation_policy_delegate"),
)

ENTRYPOINTS = (
    ("repository_generator_known_group_identity_lookup.py", "find_standard_repository_generator_known_group_identity_nodes", "validate_generator_repository_registry_links"),
    ("repository_operation_query_facade.py", "query_standard_repository_operation_input", "validate_repository_internal_proof_roots"),
    ("toda_calculation_facade.py", "build_standard_toda_report", "validate_repository_internal_proof_roots"),
)

def _tree(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))

def _calls(tree: ast.AST, target: str) -> list[dict]:
    result = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        callee = node.func
        name = callee.id if isinstance(callee, ast.Name) else callee.attr if isinstance(callee, ast.Attribute) else None
        if name == target:
            receiver = callee.value.id if isinstance(callee, ast.Attribute) and isinstance(callee.value, ast.Name) else None
            result.append({"line": node.lineno, "receiver": receiver})
    return sorted(result, key=lambda row: row["line"])

def audit(root: Path) -> dict:
    rows = []
    for filename, call, category in SITES:
        path = root / filename
        if not path.is_file():
            rows.append({"file": filename, "call": call, "category": category, "status": "MISSING_FILE", "lines": []})
            continue
        lines = _calls(_tree(path), call)
        rows.append({"file": filename, "call": call, "category": category, "status": "PRESENT" if lines else "MISSING_CALL", "lines": lines})
    entries = []
    for filename, function, guard in ENTRYPOINTS:
        path = root / filename
        if not path.is_file():
            entries.append({"file": filename, "function": function, "status": "MISSING_FILE"})
            continue
        tree = _tree(path)
        matches = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == function]
        good = len(matches) == 1 and bool(_calls(matches[0], guard))
        entries.append({"file": filename, "function": function, "status": "GUARDED" if good else "NOT_GUARDED"})
    special = root / "phase164_r4_r8_registry_reconstruction.py"
    special_text = special.read_text(encoding="utf-8-sig") if special.is_file() else ""
    boundaries = {
        "special_citation_mode": 'confirmed_fixed_literature' in special_text,
        "special_user_confirmation": 'user_confirmed_original' in special_text,
        "special_requires_root_validation": 'validate_phase161_r7_provenance' in special_text,
        "special_does_not_claim_r2": 'r2_same_document_order_approval_claimed' in special_text,
    }
    exceptions = [x for x in rows if x["category"] == "fixed_literature_special_path_exception" and x["status"] == "PRESENT"]
    blockers = []
    if any(x["status"] != "PRESENT" for x in rows):
        blockers.append("site_inventory_drift")
    if any(x["status"] != "GUARDED" for x in entries):
        blockers.append("unguarded_standard_entrypoint")
    if not all(boundaries.values()):
        blockers.append("special_citation_boundary_drift")
    if exceptions:
        blockers.append("special_fixed_literature_path_not_migrated_to_shared_resolver")
    return {
        "phase": "164 R7-R7", "mode": "READ_ONLY_EIGHT_SITE_BOUNDARY_CLASSIFICATION",
        "site_count": len(rows), "sites": rows, "entrypoints": entries,
        "special_boundary_evidence": boundaries,
        "known_exception_count": len(exceptions),
        "blockers": blockers,
        "r7_status": "NOT_CLOSED" if blockers else "CANDIDATE_FOR_CLOSURE_REQUIRES_TARGETED_TESTS",
        "production_modified": False, "full_pytest_run": False,
    }

def report(result: dict) -> str:
    lines = ["# Phase 164 R7-R7 — 残存8箇所の用途分類", "", "- 状態: **" + result["r7_status"] + "**", "- 本番ファイル変更: なし", "- 全体 pytest: 未実行", "", "## 監査対象8箇所", "", "| ファイル | 呼出 | 分類 | 検出行 | 状態 |", "|---|---|---|---|---|"]
    for item in result["sites"]:
        lines.append("| `" + item["file"] + "` | `" + item["call"] + "` | " + item["category"] + " | " + ", ".join(str(r["line"]) for r in item["lines"]) + " | " + item["status"] + " |")
    lines += ["", "## 3つの標準入口", ""]
    for entry in result["entrypoints"]:
        lines.append("- `" + entry["function"] + "`: " + entry["status"])
    lines += ["", "## 完了を妨げる残件", ""]
    for b in result["blockers"]:
        lines.append("- " + b)
    lines += ["", "**判定:** π₅³ の固定文献接続には特殊な原本確認・ProofStep 同一性契約がある。共通 resolver の通常引用ポリシーとは同一視できない。R7-R8 で契約を明示して統合するまでは R7 全体を閉じない。", "", "この監査は AST による存在確認であり、すべての動的経路の完全性を証明しない。", ""]
    return "\n".join(lines)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, default=Path("phase164_r7_r7_output"))
    args = parser.parse_args()
    result = audit(args.root.resolve())
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.output / "report.md").write_text(report(result), encoding="utf-8")
    print(report(result))
    if any(x["status"] != "PRESENT" for x in result["sites"]) or any(x["status"] != "GUARDED" for x in result["entrypoints"]):
        raise SystemExit("R7-R7 expected sites/guards missing: inspect audit.json")

if __name__ == "__main__":
    main()
