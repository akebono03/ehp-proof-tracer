"""Focused assertions about certified sources and the common Web narrative."""
from __future__ import annotations

import pytest

from phase173_r4_r13_narrative_audit.audit import (
    inspect_dimension,
    inspect_unproven_epsilon,
)


@pytest.mark.parametrize("dimension", (7, 8, 9, 10, 11))
def test_five_proven_toda_narratives_preserve_sources_and_web(
    dimension: int,
) -> None:
    row = inspect_dimension(dimension, with_web=True)
    assert row["source_verified"] is True
    assert row["web_verified"] is True
    assert row["open_goals"] == 0
    assert row["source_reference_count"] == 4
    assert "使用する結果" in row["narrative_markdown"]
    assert row["narrative_markdown"].endswith("□\n")


def test_zero_group_has_no_fake_generator_image() -> None:
    row = inspect_dimension(11, with_web=False)
    assert row["source_verified"] is True
    assert row["source_reference_count"] == 4
    assert r"\Phi_{11}(" not in row["narrative_markdown"]


def test_unproved_epsilon_does_not_enter_common_root() -> None:
    assert inspect_unproven_epsilon() is True


def test_audit_rejects_unreviewed_group_dimensions() -> None:
    with pytest.raises(ValueError):
        inspect_dimension(12, with_web=False)
