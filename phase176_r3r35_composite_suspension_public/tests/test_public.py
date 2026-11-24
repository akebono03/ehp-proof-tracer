"""Public-source-screened proposal tests; proof completion is not asserted."""
from __future__ import annotations

import pytest

from phase176_r3r35_composite_suspension_public.audit import probe
from phase176_r3r35_composite_suspension_public.installer import TARGET, PATCH


@pytest.fixture(scope="module")
def observed() -> dict:
    return probe()


def test_public_composite_suspension_candidate(observed: dict) -> None:
    assert observed["public_candidate_count"] == 1
    assert observed["public_subgoal_count"] == 1
    assert observed["source_screened_context_used"] is True


def test_public_connection_is_not_group_proof(observed: dict) -> None:
    assert observed["root_group_proved"] is False
    assert observed["hopf_image_proved"] is False
    assert observed["new_given"] == 0
    assert PATCH in TARGET.read_text(encoding="utf-8-sig")
