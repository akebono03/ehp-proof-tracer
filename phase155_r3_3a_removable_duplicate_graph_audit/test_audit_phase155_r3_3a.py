from __future__ import annotations

import pytest

import audit_phase155_r3_3a as audit


def _row(
    candidate_id: str,
    older: str,
    newer: str,
    decision: str,
    authorized: bool = False,
):
    return {
        "candidate_id": candidate_id,
        "older_test_id": older,
        "newer_test_id": newer,
        "decision": decision,
        "deletion_authorized": str(
            authorized
        ),
    }


def test_linear_chain_keeps_newest_sink_and_deletes_older_nodes():
    rows = [
        _row(
            "R1",
            "tests/test_phase140_a.py::test_a",
            "tests/test_phase150_b.py::test_b",
            audit.DECISION_REMOVABLE,
            True,
        ),
        _row(
            "R2",
            "tests/test_phase150_b.py::test_b",
            "tests/test_phase154_c.py::test_c",
            audit.DECISION_REMOVABLE,
            True,
        ),
    ]

    components, nodes = (
        audit.build_graph_audit(
            rows
        )
    )

    assert len(
        components
    ) == 1
    assert (
        components[
            0
        ].canonical_survivor
        == "tests/test_phase154_c.py::test_c"
    )
    deletion = {
        row.test_id
        for row in nodes
        if row.deletion_candidate
    }
    assert deletion == {
        "tests/test_phase140_a.py::test_a",
        "tests/test_phase150_b.py::test_b",
    }


def test_historical_keep_protects_node_from_deletion():
    old = (
        "tests/test_phase140_a.py::test_a"
    )
    new = (
        "tests/test_phase154_c.py::test_c"
    )

    rows = [
        _row(
            "R1",
            old,
            new,
            audit.DECISION_REMOVABLE,
            True,
        ),
        _row(
            "R2",
            old,
            "tests/test_phase120_legacy.py::test_legacy",
            audit.DECISION_HISTORICAL,
            False,
        ),
    ]

    components, nodes = (
        audit.build_graph_audit(
            rows
        )
    )

    old_node = next(
        row
        for row in nodes
        if row.test_id
        == old
    )

    assert (
        old_node.historical_protected
        is True
    )
    assert (
        old_node.deletion_candidate
        is False
    )
    assert (
        components[
            0
        ].needs_manual_review
        is False
    )


def test_two_old_tests_can_share_one_new_survivor():
    survivor = (
        "tests/test_phase154_c.py::test_c"
    )
    rows = [
        _row(
            "R1",
            "tests/test_phase140_a.py::test_a",
            survivor,
            audit.DECISION_REMOVABLE,
            True,
        ),
        _row(
            "R2",
            "tests/test_phase141_b.py::test_b",
            survivor,
            audit.DECISION_REMOVABLE,
            True,
        ),
    ]

    _components, nodes = (
        audit.build_graph_audit(
            rows
        )
    )

    deletion = {
        row.test_id
        for row in nodes
        if row.deletion_candidate
    }

    assert deletion == {
        "tests/test_phase140_a.py::test_a",
        "tests/test_phase141_b.py::test_b",
    }


def test_cycle_without_sink_requires_manual_review():
    a = (
        "tests/test_phase150_a.py::test_a"
    )
    b = (
        "tests/test_phase151_b.py::test_b"
    )
    rows = [
        _row(
            "R1",
            a,
            b,
            audit.DECISION_REMOVABLE,
            True,
        ),
        _row(
            "R2",
            b,
            a,
            audit.DECISION_REMOVABLE,
            True,
        ),
    ]

    components, _nodes = (
        audit.build_graph_audit(
            rows
        )
    )

    assert (
        components[
            0
        ].cycle_present
        is True
    )
    assert (
        components[
            0
        ].needs_manual_review
        is False
    )
    assert (
        components[
            0
        ].deletion_candidate_count
        == 1
    )


def test_needs_review_input_is_rejected():
    rows = [
        _row(
            "R1",
            "tests/test_a.py::test_a",
            "tests/test_b.py::test_b",
            audit.DECISION_REVIEW,
            False,
        )
    ]

    with pytest.raises(
        ValueError,
        match="needs_review",
    ):
        audit.build_graph_audit(
            rows
        )


def test_unauthorized_removable_edge_is_not_used():
    rows = [
        _row(
            "R1",
            "tests/test_phase140_a.py::test_a",
            "tests/test_phase154_b.py::test_b",
            audit.DECISION_REMOVABLE,
            False,
        )
    ]

    components, nodes = (
        audit.build_graph_audit(
            rows
        )
    )

    assert components == []
    assert nodes == []


def test_phase_number_prefers_later_phase():
    assert (
        audit._canonical_key(
            "tests/test_phase154_a.py::test_a"
        )
        > audit._canonical_key(
            "tests/test_phase143_z.py::test_z"
        )
    )
