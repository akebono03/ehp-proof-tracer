"""R49 audit must be read-only, source-cited, and bounded."""
from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]


def test_r49_sources_parse_without_placeholders() -> None:
    targets = (
        "__init__.py", "audit.py", "source_guard.py",
        "tests/test_static.py", "tests/test_frontier.py", "tests/test_guard.py",
    )
    for relative in targets:
        tree = ast.parse((PACKAGE / relative).read_text(encoding="utf-8"))
        assert not any(
            isinstance(node, ast.Constant) and node.value is Ellipsis
            for node in ast.walk(tree)
        )


def test_r49_does_not_install_a_proof_or_edit_production() -> None:
    content = (PACKAGE / "audit.py").read_text(encoding="utf-8")
    runner = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    assert "ProofStep(" not in content
    assert "search_registered_partial_proof(" in content
    assert "SourceBoundGoal(" in content
    assert "has_certified_prop27_leaf(bridge)" in content
    assert "root_exactness_outside_scope" in content
    assert "R48_FRONTIER_REGRESSION" in runner
    assert "R30_PROP27_REGRESSION" in runner
    assert "not test_source_guard_accepts_reviewed_change" in runner
    assert "-DryRun" not in runner or "[switch]$DryRun" in runner
    assert "FULL_PYTEST=False" in runner
    assert "git reset" not in runner
    assert "git clean" not in runner


def test_r49_requires_cited_general_prop27_before_typed_specialization() -> None:
    content = (PACKAGE / "audit.py").read_text(encoding="utf-8")
    assert "select(prop27_witness, PROP27_RULE, (general_prop27,))" in content
    assert '"Toda Proposition 2.7 typed literature universal premise"' in content
    assert '"canonical_prop27_cited_three_level_ancestry"' in content
    assert '"canonical_upper_delta_four_independent_inference_parents"' in content
    assert "Prop27UniversalLiteratureStatement()" in content
    assert "Prop27GeneralTheoremPremise()" in content
