"""Phase 166 R3: read-only internal proof reuse qualification audit."""
from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent


def function_tree(path: Path, name: str) -> ast.FunctionDef:
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    found = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(found) != 1:
        raise ValueError(f"expected one {name} in {path}")
    return found[0]


def called_names(node: ast.AST) -> set[str]:
    names = set()
    for part in ast.walk(node):
        if isinstance(part, ast.Call):
            if isinstance(part.func, ast.Name):
                names.add(part.func.id)
            elif isinstance(part.func, ast.Attribute):
                names.add(part.func.attr)
    return names


def inspect() -> dict:
    legacy = ROOT / "phase165_r52_r17_internal_dependency.py"
    catalog = ROOT / "phase165_r57_r13_proof_order_catalog.py"
    search = ROOT / "phase165_r3_recursive_search.py"
    missing = [str(p.name) for p in (legacy, catalog, search) if not p.is_file()]
    if missing:
        raise FileNotFoundError("required production modules absent: " + ", ".join(missing))

    validation = function_tree(legacy, "validate_ancestry")
    reuse = function_tree(legacy, "find_reusable_internal_proof")
    search_fn = function_tree(search, "reconstruct_registered_goal")
    catalog_cls = next(n for n in ast.parse(catalog.read_text(encoding="utf-8-sig")).body if isinstance(n, ast.ClassDef) and n.name == "ProofOrderCatalog")
    prior = next(n for n in catalog_cls.body if isinstance(n, ast.FunctionDef) and n.name == "select_prior")
    search_text = ast.get_source_segment(search.read_text(encoding="utf-8-sig"), search_fn) or ""
    result = {
        "phase": "166 R3 internal proof reuse audit",
        "read_only": True,
        "ancestry_checks": sorted(called_names(validation)),
        "reuse_checks": sorted(called_names(reuse)),
        "catalog_prior_checks": sorted(called_names(prior)),
        "search_accepts_completed_internal_proofs": "completed_internal_proofs" in [arg.arg for arg in search_fn.args.kwonlyargs],
        "search_calls_internal_reuse": "find_reusable_internal_proof" in called_names(search_fn),
        "search_calls_proof_order_catalog": "select_prior" in called_names(search_fn),
        "search_explicitly_restricts_completed_proofs": "validate_prior_internal_proofs" in called_names(search_fn),
        "completed_proof_is_not_mathematical_certification": True,
        "proof_permission_granted": 0,
        "production_code_modified": False,
        "full_pytest_run": False,
    }
    result["status"] = ("PRIOR_ORDER_GATE_CONNECTED" if result["search_calls_proof_order_catalog"] or result["search_explicitly_restricts_completed_proofs"] else "PRIOR_ORDER_GATE_NOT_OBSERVED_IN_DIRECT_SEARCH")
    return result


def main() -> None:
    result = inspect()
    (HERE / "results").mkdir(exist_ok=True)
    (HERE / "results" / "summary.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
