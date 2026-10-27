"""Small focused tests for read-only prose diagnostics."""
from __future__ import annotations

import pytest

from phase169_r10ea_direct_sum_narrative_audit.prose_metrics import (
    count_rendered_image_equations, render_report,
)


def test_r10ea_distinguishes_duplicate_equations_from_distinct_steps():
    observed = (
        "[R5]より, $E(\\eta_{11})=\\eta_{12}$.\n"
        "$E(\\eta_{11})=\\eta_{12}$.\n"
        "$E(\\eta_{12})=\\eta_{13}$.\n"
    )
    report = count_rendered_image_equations(observed)
    assert report["total_occurrences"] == 3
    assert report["distinct_equations"] == 2
    assert report["extra_duplicate_occurrences"] == 1
    assert report["repeated_equations"] == [
        {"from": r"\eta_{11}", "to": r"\eta_{12}", "copies": 2},
    ]


def test_r10ea_does_not_conflate_different_endpoints():
    observed = (
        "$E(\\nu_{11})=\\nu_{12}$.\n"
        "$E(\\mu_{11})=\\mu_{12}$.\n"
        "$E(\\nu_{12})=\\nu_{13}$.\n"
    )
    assert count_rendered_image_equations(observed)["extra_duplicate_occurrences"] == 0


def test_r10ea_does_not_count_general_definitions_as_one_step_images():
    observed = (
        r"$\varepsilon_n=E^{n-3}\varepsilon_3$" + "\n" +
        r"$E(\varepsilon_{11})=\varepsilon_{12}$." + "\n"
    )
    assert count_rendered_image_equations(observed)["total_occurrences"] == 1


def test_r10ea_rejects_non_text_input():
    with pytest.raises(TypeError, match="markdown"):
        count_rendered_image_equations(None)


def test_r10ea_scope_remains_selected_focused_groups():
    from pathlib import Path
    source = (Path(__file__).resolve().parents[1] / "audit.py").read_text(encoding="utf-8")
    assert "CASES = ((13, 9), (15, 8), (15, 9), (30, 9))" in source


def test_r10ea_report_does_not_claim_proof_if_rejected():
    report = {"cases": [{
        "goal": "pi_22^13", "search_status": "partial",
        "trust_boundary": "not_checked", "inferred_generator_image_steps": 4,
        "open_goal_types": ["GeneratorImage"],
    }]}
    markdown = render_report(report)
    assert "partial" in markdown
    assert "not_checked" in markdown
    assert "未解決型: GeneratorImage" in markdown
    assert "□" not in markdown
