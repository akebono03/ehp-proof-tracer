"""R3R2: one canonical Reference heading for each renderer status.

These tests deliberately inspect the *existing* complete and partial heading
formats. They do not change proof states, renderer output, or cited steps.
"""
from __future__ import annotations

import pytest

from phase173_r4_r15r17r3_goal_contract_audit.audit import (
    count_canonical_reference_headings,
)


def test_incomplete_reference_heading_is_counted_once() -> None:
    markdown = "## 証明対象\n\n## 使用する結果\n\n**[R1] Lemma.**\n"
    assert count_canonical_reference_headings(markdown, complete=False) == 1


def test_completed_reference_heading_is_counted_once() -> None:
    markdown = "使用する結果\n\n**[R1] Lemma.**\n\n証明\n"
    assert count_canonical_reference_headings(markdown, complete=True) == 1


def test_two_reference_headings_are_detected_as_duplicates() -> None:
    markdown = "## 使用する結果\n\n## 使用する結果\n"
    assert count_canonical_reference_headings(markdown, complete=False) == 2


def test_missing_reference_heading_is_distinguished_from_duplicates() -> None:
    assert count_canonical_reference_headings("## 証明\n", complete=False) == 0


def test_unexpected_heading_for_proof_status_is_rejected() -> None:
    with pytest.raises(ValueError, match="unexpected Reference heading"):
        count_canonical_reference_headings("使用する結果", complete=False)
    with pytest.raises(ValueError, match="unexpected Reference heading"):
        count_canonical_reference_headings("## 使用する結果", complete=True)


def test_reference_heading_contract_rejects_invalid_arguments() -> None:
    with pytest.raises(TypeError, match="Markdown"):
        count_canonical_reference_headings(None, complete=True)
    with pytest.raises(TypeError, match="complete"):
        count_canonical_reference_headings("使用する結果", complete=1)
