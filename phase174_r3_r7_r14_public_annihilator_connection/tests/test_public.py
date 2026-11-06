"""Post-patch public source-first integration; run ONLY after guarded apply."""
from __future__ import annotations

from phase174_r3_r7_r14_public_annihilator_connection.audit import (
    inspect_public_source_and_proof,
)


def test_public_cited_general_source_and_n6_specialization_have_verified_ancestry() -> None:
    status = inspect_public_source_and_proof()
    assert status["public_general_source_givens"] == 1
    assert status["public_n6_specialization_proposals"] == 1
    assert status["public_n6_cited_parent"] is True
    assert status["new_group_given"] == 0
    assert status["goal_complete_claimed"] is False
