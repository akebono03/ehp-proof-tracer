"""R48 only adds an auditable scoped proof-search procedure."""
from __future__ import annotations

import ast
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]


def test_new_python_source_parses_without_placeholders() -> None:
    for path in (PKG / "audit.py", PKG / "source_guard.py", PKG / "tests/test_static.py", PKG / "tests/test_frontier.py", PKG / "tests/test_guard.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        assert not any(isinstance(node, ast.Constant) and node.value is Ellipsis for node in ast.walk(tree))


def test_runner_is_read_only_and_runs_only_focused_pytest() -> None:
    script = (PKG / "run.ps1").read_text(encoding="utf-8")
    assert "--dry-run" in script
    assert "--import-mode=$ImportMode" in script
    assert "R36_CITED_KERNEL_REGRESSION" in script
    assert "R47_FRONTIER_REGRESSION" in script
    assert "FULL_PYTEST=False" in script
    assert "git reset" not in script
    assert "git clean" not in script
    assert "install.py" not in script


def test_no_direct_proof_or_new_source_is_installed() -> None:
    source = (PKG / "audit.py").read_text(encoding="utf-8")
    assert "ProofStep(" not in source
    assert "checked_prior_statements()" in source
    assert "search_registered_partial_proof(" in source
    assert "isolated_proof_steps_injected" in source
    assert "R35/R36" in source

def test_kernel_diagonal_matcher_is_imported_in_the_audit_function() -> None:
    """Catch missing symbols before a real kernel search hits this branch."""
    tree = ast.parse((PKG / "audit.py").read_text(encoding="utf-8"))
    audit_functions = tuple(
        node for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "inspect_integrated_lower_kernel_frontier"
    )
    assert len(audit_functions) == 1
    audit_function = audit_functions[0]
    proof_imports = tuple(
        node for node in audit_function.body
        if isinstance(node, ast.ImportFrom) and node.module == "proof"
    )
    assert len(proof_imports) == 1
    assert {alias.name for alias in proof_imports[0].names} == {
        "ProofRule", "ProofStep", "Relation", "RelationType",
        "find_inference_matches_for_rule",
    }
    matcher_calls = tuple(
        node for node in ast.walk(audit_function)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "find_inference_matches_for_rule"
    )
    assert len(matcher_calls) == 1


def test_r35_kernel_domain_is_explicitly_bound_to_a_cited_inference() -> None:
    """A direct fixed GIVEN must not satisfy R35's INFERENCE domain premise."""
    tree = ast.parse((PKG / "audit.py").read_text(encoding="utf-8"))
    functions = tuple(
        node for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "inspect_integrated_lower_kernel_frontier"
    )
    assert len(functions) == 1
    imports = {
        alias.name
        for node in functions[0].body
        if isinstance(node, ast.ImportFrom)
        and node.module == "phase165_r3_recursive_search"
        for alias in node.names
    }
    assert {"GoalExpansion", "SourceBoundGoal"}.issubset(imports)
    source_bound_calls = tuple(
        node for node in ast.walk(functions[0])
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "SourceBoundGoal"
    )
    assert len(source_bound_calls) == 1
    assert {arg.arg for arg in source_bound_calls[0].keywords} == {"conclusion", "source"}
    content = (PKG / "audit.py").read_text(encoding="utf-8")
    assert "rule=expansions[0].rule" in content
    assert "for option in diagonal_options" in content
    assert '"canonical_kernel_domain_bound_inference_proved": bool(domain_steps)' in content
    assert "ProofStep(" not in content
