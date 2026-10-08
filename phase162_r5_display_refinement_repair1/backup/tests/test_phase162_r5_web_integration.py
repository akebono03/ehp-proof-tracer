"""Focused Phase 162 R5 web integration contracts."""

from unittest.mock import patch

from web_group_proof import build_standard_web_group_proof_view
from phase162_web_narrative_integration import (
    build_phase162_web_validated_isomorphism_markdown,
)


def test_phase162_r5_verified_web_payload_contains_map_goal():
    narrative = build_phase162_web_validated_isomorphism_markdown()
    assert "## 使用する結果" in narrative
    assert "## 証明" in narrative
    assert r"E: \pi_{4}^{2} \to \pi_{5}^{3}" in narrative
    assert narrative.rstrip().endswith("□")


def test_phase162_r5_web_narrative_adds_subproof_without_changing_group_conclusion():
    with patch(
        "phase162_web_narrative_integration.build_phase162_web_validated_isomorphism_markdown",
        return_value="# Backward proof narrative\n\n## 証明\n\nVALIDATED_MARKER\n\n□\n",
    ) as builder:
        view = build_standard_web_group_proof_view(3, 2, max_depth=2, mode="narrative")
    builder.assert_called_once_with()
    rendered = " ".join(
        line.prefix + " " + line.suffix + " " + " ".join(s.value for s in line.segments)
        for line in view.rendered_lines
    )
    assert "VALIDATED_MARKER" in rendered
    assert "懸垂同型の検証済み証明" in rendered
    assert view.n == 3 and view.k == 2
    assert view.conclusion_latex


def test_phase162_r5_outline_does_not_run_reconstruction():
    with patch(
        "phase162_web_narrative_integration.build_phase162_web_validated_isomorphism_markdown",
        side_effect=AssertionError("must not run"),
    ):
        view = build_standard_web_group_proof_view(3, 2, max_depth=1, mode="outline")
    assert view.mode == "outline"
