"""Focused, source-agnostic checks for the read-only binding audit."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pytest

from phase175_r4r12r13r8r5_reference_binding_audit.audit import (
    DEFAULT_TARGETS, REQUIRED, TRACKED_ALLOWED, parse_targets,
)


def test_targets_are_validated_without_silent_reordering() -> None:
    assert parse_targets("5:4,6:5,7:5") == DEFAULT_TARGETS
    assert parse_targets(" 7:5 , 5:4 ") == ((7, 5), (5, 4))
    for value in ("", "five:four", "5", "5:4,5:4", "1:4", "5:-1"):
        with pytest.raises(ValueError):
            parse_targets(value)


def test_audit_guard_only_accepts_preexisting_display_edits() -> None:
    assert TRACKED_ALLOWED == frozenset({
        "phase168_r3_37c_reference_projection.py",
        "phase168_r3_5_model_renderer.py",
    })
    assert "phase168_r3_3_proof_narrative_model.py" in REQUIRED
    assert "phase168_r3_12_body_binding.py" in REQUIRED


def test_registered_citation_missing_body_is_reported_without_fabrication() -> None:
    from phase175_r4r12r13r8r5_reference_binding_audit.audit import citation_rows
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin

    @dataclass
    class FakeAssertion:
        content: object
        origin: object = AssertionOrigin.FIXED_STATEMENT

    @dataclass
    class FakeReference:
        locator: str
        label: str = ""

    @dataclass
    class FakeCitation:
        number: int
        reference: object
        step_indices: tuple[int, ...]
        assertion_ids: tuple[str, ...]
        reference_ids: tuple[str, ...]
        statement_bodies: tuple[str, ...]

    @dataclass
    class FakeStep:
        rule: object
        conclusion: object
        premises: tuple[object, ...] = ()

    @dataclass
    class FakeModel:
        citations: tuple[object, ...]
        steps: tuple[object, ...]
        step_citation_numbers: tuple[tuple[int, ...], ...]

    class FakeRegistry:
        def assertion(self, key: str) -> FakeAssertion:
            assert key == "source:one"
            return FakeAssertion(content="typed source")

    @dataclass
    class FakeBridge:
        registry: object

    model = FakeModel(
        citations=(FakeCitation(1, FakeReference("(sample)"), (0,),
                                ("source:one",), ("ref:one",), ()),),
        steps=(FakeStep(ProofRule.GIVEN, "typed source"),),
        step_citation_numbers=((1,),),
    )
    rows = citation_rows(model, FakeBridge(FakeRegistry()))
    assert rows[0]["registered_fixed_body_missing"] is True
    assert rows[0]["statement_bodies"] == []
    assert rows[0]["given_indices"] == [0]


def test_unregistered_reference_is_not_misclassified_as_fixed_source() -> None:
    from phase175_r4r12r13r8r5_reference_binding_audit.audit import citation_rows
    from types import SimpleNamespace
    ref = SimpleNamespace(number=1, reference=SimpleNamespace(locator="DB prior", label=""),
                          step_indices=(), assertion_ids=(), reference_ids=(), statement_bodies=())
    model = SimpleNamespace(citations=(ref,), steps=(), step_citation_numbers=())
    bridge = SimpleNamespace(registry=SimpleNamespace())
    row = citation_rows(model, bridge)[0]
    assert row["registered_fixed_statement"] is False
    assert row["registered_fixed_body_missing"] is False


def test_run_script_uses_package_module_execution() -> None:
    script = (Path(__file__).resolve().parents[1] / "run.ps1").read_text(encoding="utf-8-sig")
    module = "-m phase175_r4r12r13r8r5_reference_binding_audit.audit"
    assert script.count(module) == 2
    assert "python -B $audit" not in script
    assert "-p no:cacheprovider" in script


def test_web_display_guard_checks_display_not_typed_equality() -> None:
    from pathlib import Path
    source = (Path(__file__).resolve().parents[1] / "audit.py").read_text(encoding="utf-8")
    # The bridge may prove equivalent written forms that are not object-equal.
    assert 'not value["reference_body_present"]' in source
    assert 'not value["proof_body_yori"]' in source
    assert 'all(value.values())' not in source
    assert '"direct_typed_consumer": any(' in source


def test_audit_reports_actual_web_failure_after_collecting_targets() -> None:
    import ast
    from pathlib import Path
    source = (Path(__file__).resolve().parents[1] / "audit.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "run")
    assert any(isinstance(node, ast.Assign) and any(
        isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name)
        and target.value.id == "report" for target in node.targets
    ) for node in ast.walk(function))
    assert "FAIL_R13R8R5_ACTUAL_WEB_DISPLAY_REGRESSION" in source
    assert '"display_regressions"' in source
