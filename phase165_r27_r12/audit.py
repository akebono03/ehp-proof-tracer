"""Phase 165 R27-R12: conservative AST legacy-deletion boundary audit."""
from __future__ import annotations

import ast
import json
from pathlib import Path

PHASE = "165 R27-R12"
SCANNED = (
    "standard_production_repository.py", "standard_repository.py",
    "proof_repository.py", "toda_prop515_upper_bootstrap.py",
    "toda_prop515_sigma_chain_bootstrap.py", "toda_upstream_bootstrap.py",
    "toda_calculation_facade.py", "web_group_proof.py",
    "web_group_proof_common.py", "phase165_r52_r3_web_adapter.py",
    "phase165_r52_r5_auto_search.py", "phase165_r9_production_wiring.py",
    "phase165_r4_production_connection.py", "phase163_r4_registry_bridge.py",
    "unified_statement_registry.py", "main.py", "web_app.py",
)
SYMBOLS = (
    "build_standard_production_proof_repository",
    "build_standard_proof_repository",
    "build_toda_prop515_upper_bootstrap",
    "build_toda_prop515_sigma_chain_bootstrap",
    "build_toda_upstream_bootstrap",
    "build_standard_toda_report",
    "build_toda_group_result_proof_replay",
    "ProofRepository", "ProofRepositoryEntry",
    "build_standard_web_group_proof_view",
)
PROTECTED = (
    "unified_statement_registry.py", "phase163_r4_registry_bridge.py",
    "phase165_r52_r2_search_adapter.py", "toda_rules.py",
    "proof.py", "theorem_facts.py",
)


def scan_file(path: Path) -> dict:
    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    events = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name in SYMBOLS:
            events.append({"symbol": node.name, "kind": "definition", "line": node.lineno})
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name in SYMBOLS:
                    events.append({"symbol": alias.name, "kind": "import", "line": node.lineno})
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id in SYMBOLS:
            events.append({"symbol": node.id, "kind": "use", "line": node.lineno})
        elif isinstance(node, ast.Attribute) and node.attr in SYMBOLS:
            events.append({"symbol": node.attr, "kind": "attribute", "line": node.lineno})
    events.sort(key=lambda x: (x["line"], x["kind"], x["symbol"]))
    return {"path": path.as_posix(), "references": events}


def classify(path: str) -> str:
    if path.startswith("tests/") or Path(path).name.startswith("test_"):
        return "TEST_REFERENCE"
    if path.startswith("archive/") or "backup" in path or path.startswith("phase") and "/" in path:
        return "HISTORICAL_OR_PACKAGE_REVIEW"
    if path in PROTECTED:
        return "PROTECTED"
    return "ACTIVE_OR_UNCLASSIFIED_REVIEW"


def collect(root: Path) -> dict:
    missing = [p for p in SCANNED if not (root / p).is_file()]
    if missing:
        raise FileNotFoundError("Required source files missing: " + ", ".join(missing))
    results = []
    for path in sorted(root.rglob("*.py")):
        rel = path.relative_to(root)
        if any(p in {".git", ".venv", "venv", "__pycache__", "site-packages"} for p in rel.parts):
            continue
        # Old phase packages and snapshots are reported separately, never deletion-authorized.
        try:
            item = scan_file(path)
        except (SyntaxError, UnicodeError):
            continue
        if item["references"]:
            item["path"] = rel.as_posix()
            item["scope"] = classify(item["path"])
            results.append(item)
    return {
        "phase": PHASE,
        "mode": "READ_ONLY_SYMBOL_LEVEL_DELETION_BOUNDARY_AUDIT",
        "production_files_modified": False,
        "full_pytest_run": False,
        "scanned_required_files": len(SCANNED),
        "missing_required_files": missing,
        "protected_files": list(PROTECTED),
        "deletion_authorized": False,
        "references": results,
        "next_action": "Classify live dependency edges and replace necessary consumers before any legacy Bootstrap/Repository deletion",
    }


def main() -> int:
    root = Path.cwd()
    report = collect(root)
    out = Path(__file__).with_name("audit_report.json")
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k != "references"}, ensure_ascii=False, indent=2))
    print("Files with references:", len(report["references"]))
    print("Report:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
