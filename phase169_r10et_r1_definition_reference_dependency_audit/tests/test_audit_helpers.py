"""Offline smoke tests for read-only graph/citation audit helpers."""
from __future__ import annotations

import importlib.util
from pathlib import Path
from types import SimpleNamespace


def module():
    filepath = Path(__file__).resolve().parents[1] / "audit.py"
    spec = importlib.util.spec_from_file_location("r10et_read_only_audit", filepath)
    result = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(result)
    return result


def test_ancestor_indices_follow_actual_dependencies():
    audit = module()
    graph = ((), (0,), (0,), (1, 2))
    assert audit.ancestor_indices(3, graph) == (0, 1, 2, 3)
    assert audit.ancestor_indices(2, graph) == (0, 2)


def test_step_linked_citations_preserves_source_identity():
    audit = module()
    model = SimpleNamespace(citations=(SimpleNamespace(
        number=3,
        reference=SimpleNamespace(locator="Chapter V, i)", label="Toda"),
        step_indices=(0, 4),
        assertion_ids=("assertion",),
        reference_ids=("reference",),
        statement_bodies=("definition",),
    ),))
    assert audit.step_linked_citations(model) == [{
        "number": 3,
        "locator": "Chapter V, i)",
        "step_indices": [0, 4],
        "assertion_ids": ["assertion"],
        "reference_ids": ["reference"],
        "statement_bodies": ["definition"],
    }]


def test_body_excludes_reference_section():
    audit = module()
    content = "使用する結果\n**[R3] Chapter V.**\n証明\n[R3]より, 式.\n"
    assert audit.body_text(content) == "\n[R3]より, 式.\n"
    assert audit.body_text("使用する結果だけ") == ""


def test_case_scope_contains_requested_regressions():
    audit = module()
    assert len(audit.CORE_CASES) == 6
    assert len(audit.ALL_CASES) == 12
    assert (43, 26) in audit.ALL_CASES
    assert (30, 11) in audit.ALL_CASES
    assert (30, 14) in audit.ALL_CASES
    assert (30, 16) in audit.ALL_CASES
    assert (30, 26) in audit.ALL_CASES
    assert (30, 9) in audit.ALL_CASES
    assert (4, 2) in audit.ALL_CASES
