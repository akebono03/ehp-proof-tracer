"""Migration acceptance gate. Expected to FAIL before dedicated paths are removed.

DO NOT run during the read-only audit. Enable only after implementing the
unified renderer and replacing legacy prose-exact tests with semantic tests.
"""
from __future__ import annotations

from pathlib import Path

from phase173_r4_r12r3_architecture_audit.audit import (
    CORE_GATE_FILES,
    scan_source,
)


ROOT = Path(__file__).resolve().parents[2]
PROHIBITED = {
    "DEDICATED_NARRATIVE_FUNCTION",
    "DEDICATED_NARRATIVE_IMPORT",
    "DEDICATED_NARRATIVE_CALL",
    "LITERAL_DIMENSION_DISPATCH",
    "LEGACY_RULE_DISPATCH",
    "POST_RENDER_NARRATIVE_OVERRIDE",
    "FIXED_SPHERE_CONSTRUCTOR",
    "HARDCODED_PRESENTATION_CANDIDATE",
}


def test_unified_renderer_contains_no_structural_special_cases() -> None:
    violations = []
    for path in CORE_GATE_FILES:
        source = (ROOT / path).read_text(encoding="utf-8-sig")
        violations.extend(
            finding for finding in scan_source(source, path)
            if finding.code in PROHIBITED
        )
    assert violations == [], "Specialized Narrative architecture is still active"


def test_complete_five_groups_keep_certified_sources_and_web() -> None:
    from phase173_r4_r13_narrative_audit.audit import inspect_dimension

    for dimension in (7, 8, 9, 10, 11):
        row = inspect_dimension(dimension, with_web=True)
        assert row["source_verified"] is True
        assert row["web_verified"] is True
        assert row["open_goals"] == 0
        assert row["source_reference_count"] >= 4


def test_unproved_pi12_is_still_refused() -> None:
    from phase173_r4_r13_narrative_audit.audit import inspect_unproven_epsilon

    assert inspect_unproven_epsilon() is True
