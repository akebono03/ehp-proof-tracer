"""Focused R3J read-only diagnostics of the actual pi5_3 Web route."""
from __future__ import annotations

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase169_r3j_narrative_boundary_audit.audit import (
    build_audit,
    capture_actual_narrative,
    split_narrative,
)


@pytest.fixture(scope="module")
def actual():
    return capture_actual_narrative()


def test_r3j_public_model_route_has_completed_typed_root(actual):
    result, model, markdown, view = actual
    assert result.status is ProofSearchStatus.COMPLETE
    assert view.key == "generic-complete-proof"
    assert not view.partial_result
    assert model.root_index is not None
    assert model.steps[model.root_index].conclusion == result.conclusion
    assert model.steps == result.proven_steps
    assert markdown.rstrip().endswith("□")


def test_r3j_reference_items_trace_to_actual_model(actual):
    result, model, markdown, view = actual
    report = build_audit(result, model, markdown, view)
    assert report["citation_count"] == len(model.citations)
    assert report["all_citations_mentioned"]
    assert all(item["body_count"] > 0 for item in report["citations"])
    assert all(
        0 <= index < len(model.steps)
        for citation in report["citations"]
        for index in citation["step_indices"]
    )


def test_r3j_display_anomalies_are_diagnostics_only(actual):
    result, model, markdown, view = actual
    reference, proof = split_narrative(markdown)
    report = build_audit(result, model, markdown, view)
    assert report["mode"] == "AUDIT_ONLY"
    assert len(report["step_diagnostics"]) == len(result.proven_steps)
    assert report["presentation_diagnostics"]["pi4_2_presentation_mentions"] >= 1
    assert isinstance(report["english_map_property_lines"], list)
    assert isinstance(report["duplicated_math_expressions"], list)
    assert "使用する結果" in markdown and "証明" in markdown
    assert reference and proof


def test_r3j_inference_terminal_steps_are_preserved(actual):
    result, model, markdown, view = actual
    report = build_audit(result, model, markdown, view)
    assert report["presentation_diagnostics"]["terminal_hopf_surjectivity_proven"]
    assert report["presentation_diagnostics"]["terminal_delta_injectivity_proven"]
    assert not report["web_partial"]
