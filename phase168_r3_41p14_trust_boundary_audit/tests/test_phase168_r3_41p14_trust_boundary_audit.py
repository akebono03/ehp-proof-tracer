"""R3-41P14: focused read-only probes of known P13 trust-boundary gaps."""
from __future__ import annotations

import pytest

from phase168_r3_41p14_trust_boundary_audit.audit import (
    probe_projection_guards,
    probe_raw_model,
    probe_supplied_bridge,
    probe_supplied_rule,
    probe_web_route,
)


@pytest.mark.parametrize("options,expected_verify,expected_model,expected_rejected", (
    ({"context": False, "positioned": True}, 0, 0, True),
    ({"context": True, "positioned": False}, 0, 0, True),
    # The probe deliberately replaces the checker with a mock that accepts
    # every call. This case measures invocation, not real-rule acceptance.
    ({"context": True, "positioned": True, "unsupported_rule": True}, 1, 1, False),
))
def test_complete_web_boundary_is_always_required(
    options, expected_verify, expected_model, expected_rejected,
):
    row = probe_web_route(**options)
    assert row["status"] == "complete"
    assert row["verify"] == expected_verify
    assert row["model"] == expected_model
    assert row["render"] == expected_model
    assert row["rejected"] is expected_rejected


def test_positioned_complete_route_invokes_boundary_before_model():
    row = probe_web_route(context=True, positioned=True)
    assert row["verify"] == 1
    assert row["model"] == 1
    assert row["render"] == 1
    assert row["rejected"] is False
    assert row["used_screened_bridge"] is True


def test_boundary_rejection_prevents_model_construction():
    row = probe_web_route(context=True, positioned=True, reject=True)
    assert row["verify"] == 1
    assert row["model"] == 0
    assert row["render"] == 0
    assert row["rejected"] is True


def test_partial_keeps_display_route_but_does_not_inherit_verified_status():
    row = probe_web_route(context=True, positioned=True, partial=True)
    assert row["status"] == "partial"
    assert row["verify"] == 0
    assert row["model"] == 1
    assert row["render"] == 1


def test_arbitrary_direct_model_is_not_a_certificate():
    row = probe_raw_model()
    assert row["bare_model_accepts_unregistered_given"] is True
    assert row["model_has_trust_certificate"] is False


def test_matcher_replay_is_not_an_independent_rule_registry():
    row = probe_supplied_rule()
    assert row["self_supplied_rule_accepted_by_generic_matcher"] is True
    assert row["counts"] == [1, 0]


def test_caller_supplied_bridge_is_not_a_search_provenance_certificate():
    row = probe_supplied_bridge()
    assert row["caller_supplied_bridge_can_authorize_its_own_given"] is True
    assert row["counts"] == [0, 1]
    assert row["target_assertion_matches_conclusion"] is False


def test_two_mathematical_projection_guards_are_still_present():
    assert probe_projection_guards() == {
        "stable_eta_shape_guard_present": True,
        "prop42_exactness_guard_present": True,
    }
