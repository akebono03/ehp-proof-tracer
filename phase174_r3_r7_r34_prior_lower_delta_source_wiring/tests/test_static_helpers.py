"""Repository-independent source-static smoke tests for R34 packaging."""
from __future__ import annotations

import ast
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (BASE / path).read_text(encoding="utf-8")


def test_full_changed_function_is_present_and_parseable():
    tree = ast.parse(read("CHANGED_FUNCTION_FULL.py"))
    functions = [x for x in tree.body if isinstance(x, ast.FunctionDef)]
    assert [x.name for x in functions] == ["build_shared_typed_bridge"]
    assert "build_cited_lower_delta_sources" in ast.unparse(functions[0])


def test_only_two_prior_literature_references_are_registered():
    tree = ast.parse(read("source.py"))
    items = [x for x in tree.body if isinstance(x, ast.Assign)
             and any(isinstance(v, ast.Name) and v.id == "MANIFEST_ROWS"
                     for v in x.targets)]
    assert len(items) == 1
    assert len(items[0].value.elts) == 2


def test_checked_prior_sources_exclude_derived_statement():
    source = read("source.py")
    assert "KernelMultipleStatement(" not in source
    assert "TodaPrimaryGroupZeroStatement(" not in source
    assert "TodaDeltaImageUpToSignStatement(" in source
    assert "FiniteCyclicGroup" in source


def test_runner_is_focused_only():
    runner = read("run.ps1")
    assert "-m pytest -q" in runner
    assert "-DryRun" in runner or "$DryRun" in runner
    assert "pytest --maxfail" not in runner
    assert "FULL_PYTEST=False" in runner


def test_complete_replacement_and_installer_use_same_source_call():
    text = read("CHANGED_FUNCTION_FULL.py")
    installer = read("install.py")
    for token in (
        "from phase174_r3_r7_r34_prior_lower_delta_source_wiring.source import",
        "build_cited_lower_delta_sources(Path(__file__).resolve().parent)",
    ):
        assert token in text
        if "from phase" in token:
            assert "phase174_r3_r7_r34_prior_lower_delta_source_wiring.source" in installer
        else:
            assert token in installer
