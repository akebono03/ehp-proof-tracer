"""Pure, offline-safe classification tests for R20R1."""
from __future__ import annotations

from phase171_r2j_r4_r9_r20r1_post_patch_route_audit.classification import classify_routes


def test_proved_right_is_not_reclassified_as_ambiguous():
    assert classify_routes("proved", ("proved", "proved")) == "RIGHT_ALREADY_PROVED"


def test_two_independent_proofs_are_distinct():
    assert classify_routes("unresolved", ("proved", "unresolved", "proved")) == "MULTIPLE_INDEPENDENT_PROVED_ROUTES"


def test_one_path_is_not_called_completed_when_full_goal_fails():
    assert classify_routes("unresolved", ("unresolved", "proved")) == "SINGLE_ROUTE_PROVED_BUT_UNSCOPED_GOAL_UNRESOLVED"


def test_every_route_can_be_unresolved():
    assert classify_routes("unresolved", ("unresolved",)) == "NO_INDIVIDUAL_ROUTE_PROVED"


def test_empty_provider_is_separate_from_unresolved_proposals():
    assert classify_routes("unresolved", ()) == "NO_PROVIDER_ROUTES"


def test_unknown_status_is_not_promoted_to_proved():
    assert classify_routes("unresolved", ("inconclusive",)) == "SOME_ROUTE_PROBES_INCONCLUSIVE"
    assert classify_routes("search_failed", ("proved",)) == "UNEXPECTED_DIRECT_STATUS"
