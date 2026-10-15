"""Read-only R57-R6 check of the common search and stable transport boundary.

Do not replay historical proofs, manufacture GIVEN facts, or edit production.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path


REQUIRED = (
    "phase165_r52_r9_shared_math.py",
    "toda_stable_group_transport.py",
    "toda_stable_transport.py",
    "toda_group_proof_narrative_renderer.py",
    "phase165_r55_nk_only_goal.py",
)


def _call_names(function: ast.AST) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(function):
        if isinstance(node, ast.Call):
            candidate = node.func
            if isinstance(candidate, ast.Name):
                names.add(candidate.id)
            elif isinstance(candidate, ast.Attribute):
                names.add(candidate.attr)
    return names


def audit_stable_transport_boundary(root: Path) -> dict:
    """Report recorded wiring only; do not assert proof completion."""
    if not isinstance(root, Path):
        raise TypeError("root must be pathlib.Path")
    missing = [name for name in REQUIRED if not (root / name).is_file()]
    if missing:
        raise FileNotFoundError("Missing installed R55 or production sources: " + ", ".join(missing))
    shared = ast.parse((root / REQUIRED[0]).read_text(encoding="utf-8-sig"))
    transport = ast.parse((root / REQUIRED[1]).read_text(encoding="utf-8-sig"))
    goal_source = ast.parse((root / REQUIRED[4]).read_text(encoding="utf-8-sig"))
    narrative = ast.parse((root / REQUIRED[3]).read_text(encoding="utf-8-sig"))
    shared_provider = next(n for n in shared.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == "shared_expansion_provider")
    goal_selector = next(n for n in goal_source.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == "search_group_from_registered_goal")
    transport_rules = sorted(n.name for n in transport.body if isinstance(n, ast.FunctionDef) and "transport_inference_rule" in n.name)
    presentation_branches = sorted(n.name for n in narrative.body if isinstance(n, ast.FunctionDef) and "stable" in n.name and "narrative" in n.name)
    source_calls = _call_names(shared_provider)
    source_names = {n.id for n in ast.walk(shared_provider) if isinstance(n, ast.Name)}
    wired = any(name in source_calls or name in source_names for name in transport_rules)
    # R55 finds only concrete group equality goals available in its fixed-source catalog.
    selector_calls = sorted(_call_names(goal_selector))
    report = {
        "phase": "165 R57-R6",
        "mode": "READ_ONLY_STABLE_TRANSPORT_CONNECTION_AUDIT",
        "production_modified": False,
        "case": {"n": 4, "k": 1, "target": "pi_5^4", "stable_base": "pi_4^3"},
        "old_toda45_transport_rules": transport_rules,
        "shared_search_provider_calls_transport_rule": wired,
        "shared_search_provider_calls": sorted(source_calls),
        "registry_goal_selector_calls": selector_calls,
        "public_renderer_stable_branches": presentation_branches,
        "proof_for_pi5_4_established": False,
        "source_given_promoted": False,
        "delete_live_transport_renderer_allowed": False,
        "next_gate": "Register and type Toda (4.5) isomorphism, base group, and generator correspondence; connect backward expansion; prove pi_5^4 before removing live stable display branch",
        "full_pytest_run": False,
    }
    return report


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    report = audit_stable_transport_boundary(root)
    location = root / "phase165_r57_r6_stable_transport_audit.json"
    location.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("Audit saved:", location)
    if report["shared_search_provider_calls_transport_rule"]:
        print("Transport factory appears in shared provider; review dynamic bindings before any deletion")
    else:
        print("Existing typed Toda (4.5) transport rule is not wired directly into shared_expansion_provider")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
