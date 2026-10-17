"""Phase 165 R11: active rule registry to backward search audit (read-only)."""
from __future__ import annotations

import ast
import json
from pathlib import Path

from phase165_r10_rule_registry import build_rule_registry
from phase165_r8_rule_provider import DEFAULT_RULE_MODULES, discover_inference_rules
from phase165_r57_r26_generic_search_connection import build_generic_backward_expansion_provider

ROOT = Path(__file__).resolve().parent.parent
REMOVED_FACTORIES = (
    "toda_pi4_3_delta_image_free_cyclic_inference_rule",
    "toda_pi4_3_finite_cyclic_inference_rule",
    "toda_pi4_3_zero_right_implies_suspension_surjective_inference_rule",
    "toda_pi4_3_exactness_delta_image_to_suspension_kernel_inference_rule",
    "toda_pi4_3_eta3_generator_inference_rule",
    "toda_45_pi4_3_finite_cyclic_transport_inference_rule",
)


def function_calls(path: Path, function_name: str) -> tuple[str, ...]:
    """Return source calls in a single function without executing legacy code."""
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    functions = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == function_name]
    if len(functions) != 1:
        raise AssertionError(f"expected one {function_name} in {path.name}")
    return tuple(
        node.func.id if isinstance(node.func, ast.Name) else node.func.attr
        for node in ast.walk(functions[0]) if isinstance(node, ast.Call)
        if isinstance(node.func, (ast.Name, ast.Attribute))
    )


def main() -> dict:
    discovery_file = ROOT / "phase165_r8_rule_provider.py"
    search_file = ROOT / "phase165_r57_r26_generic_search_connection.py"
    shared_file = ROOT / "phase165_r52_r9_shared_math.py"
    assert "build_rule_registry" in function_calls(discovery_file, "discover_inference_rules"), "R10 registry not connected to discovery"
    assert "discover_inference_rules" in function_calls(search_file, "build_generic_backward_expansion_provider"), "generic search not connected to discovery"
    shared_calls = function_calls(shared_file, "shared_expansion_provider")
    assert "build_generic_backward_expansion_provider" in shared_calls, "shared search not connected to generic provider"
    assert "discover_inference_rules" in shared_calls, "shared witness search not connected to discovery"
    assert not (ROOT / "phase165_r52_r23_existing_rule_adapter.py").exists(), "removed adapter returned"
    factory_tree = ast.parse((ROOT / "toda_rules.py").read_text(encoding="utf-8-sig"))
    defined = {n.name for n in factory_tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    resurrected = sorted(defined.intersection(REMOVED_FACTORIES))
    assert not resurrected, f"removed dedicated rules returned: {resurrected}"
    registry = build_rule_registry(DEFAULT_RULE_MODULES)
    rules, report = discover_inference_rules()
    ids = tuple(entry.rule_id for entry in registry.entries)
    assert len(ids) == len(set(ids)), "duplicate Rule IDs"
    assert tuple(entry.rule.name for entry in registry.entries) == tuple(rule.name for rule in rules), "Rule Registry order mismatch"
    assert registry.skipped_factories == report.skipped_factories, "skipped factories diverged"
    assert registry.skipped_rules == report.skipped_rules, "skipped rules diverged"
    assert len(rules) == len(registry.entries), "registered and discovered counts differ"
    # This check uses only an existing rule instance and does not add facts or create ProofSteps.
    generic_provider = build_generic_backward_expansion_provider(tuple(rules))
    from proof import Relation, RelationType
    from expression import eta
    concrete_goal = Relation(lhs=eta(2), rhs=eta(2), relation_type=RelationType.EQUALITY)
    proposals = generic_provider(concrete_goal)
    proposal_names = tuple(p.rule.name for p in proposals)
    assert all(name in {r.name for r in rules} for name in proposal_names)
    report_data = {
        "phase": "165 R11 rule registry connection",
        "status": "CONNECTED" if not resurrected else "FAILED",
        "mode": "READ_ONLY_TARGETED",
        "registry_entries": len(ids),
        "discovered_rules": len(rules),
        "rule_ids_unique": len(ids) == len(set(ids)),
        "ordering_matches": True,
        "skipped_factory_count": len(registry.skipped_factories),
        "reverse_pattern_candidates": sum(e.backward_pattern_candidate for e in registry.entries),
        "generic_provider_executed": True,
        "probe_goal": repr(concrete_goal),
        "probe_proposal_count": len(proposals),
        "probe_rules": list(proposal_names),
        "removed_pi43_rule_definitions": resurrected,
        "removed_adapter_absent": True,
        "retired_production_catalog_invoked": False,
        "scope_limit": "R8 active zero-argument factories only; reverse-candidate count is not certified proof availability or full rule universe coverage",
        "full_pytest_run": False,
    }
    output = Path(__file__).resolve().parent / "audit_result.json"
    output.write_text(json.dumps(report_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k:report_data[k] for k in ("phase","status","registry_entries","discovered_rules","rule_ids_unique","skipped_factory_count","reverse_pattern_candidates","generic_provider_executed","probe_proposal_count","removed_adapter_absent","full_pytest_run")}, ensure_ascii=False, indent=2))
    print("Audit saved:", output)
    return report_data


if __name__ == "__main__":
    main()
