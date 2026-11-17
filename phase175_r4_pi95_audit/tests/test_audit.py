"""Focused R4 read-only audit contracts (synthetic fixtures only in tests)."""
from __future__ import annotations

import json

import pytest

from phase175_r4_pi95_audit import audit


def example_toda_text() -> str:
    return (
        r"\begin{proposition}\label{prop:5.8}" + "\n"
        + r"\pi^{4}_{8}=\mathbb Z_2\gen{\nu_{4}\circ\eta_7}\oplus \mathbb Z_2\gen{E\nu'\circ\eta_7}"
        + "\n" + r"\pi^{5}_{9}=\mathbb Z_2\gen{\nu_{5}\circ\eta_8}"
        + "\n" + r"\end{proposition}" + "\n"
        + r"\pi^{9}_{10} \pi^{9}_{8}"
        + "\n" + r"\Delta:\pi_9^9\to\pi_7^4"
        + "\n" + r"\Delta(\eta_9)"
        + "\n" + r"(2\nu_4-E\nu')" + " by Prop2.5"
        + "\n" + r"\pi_9^5=E\pi_8^4" + "\n"
        + r"\begin{equation}\label{eq:5.9}" + "\n"
    )


def example_target() -> dict[str, object]:
    return {
        "n": 5, "k": 4, "audit_result": "INCOMPLETE_AND_WEB_CONFIRMED",
        "search_status": "search_failed", "db_goal_typed": True,
        "search_conclusion_is_none": True, "web_key": "generic-partial-proof",
        "web_partial": True, "search_proven_count": 0,
        "search_open_goals": [
            "CyclicStructureStatement(group=sample, order=2)",
            "Relation(lhs=group, rhs=summands)",
            "Relation(lhs=summands, rhs=group)",
        ],
    }


def example_prior() -> dict[str, object]:
    return {
        "n": 4, "k": 4, "audit_result": "COMPLETE_AND_WEB_VERIFIED",
        "db_goal_typed": True, "trust_verified": True,
        "search_open_count": 0,
    }


def test_observed_source_proof_fragments_are_recorded_not_promoted() -> None:
    report = audit.evidence_from_text(example_toda_text())
    assert report["source_ehp_dimension_typo"] is True
    assert report["target_pi95_printed"] is True
    assert report["prior_pi84_printed"] is True
    assert report["no_direct_goal_given"] is True


def test_source_rejects_missing_actual_proof_clauses() -> None:
    with pytest.raises(RuntimeError, match="SOURCE_PROOF_CLAUSE_MISSING"):
        audit.evidence_from_text(example_toda_text().replace("by Prop2.5", "NO SOURCE"))
    with pytest.raises(RuntimeError, match="PROP58_SOURCE_AMBIGUOUS"):
        audit.evidence_from_text(example_toda_text() * 2)
    with pytest.raises(RuntimeError, match="PROOF_BOUNDARY_MISSING"):
        audit.evidence_from_text(example_toda_text().replace(r"\begin{equation}\label{eq:5.9}", "NO END"))


def test_not_a_typo_only_source_still_parses() -> None:
    report = audit.evidence_from_text(example_toda_text().replace(r"\pi^{9}_{8}", r"\pi^{4}_{8}"))
    assert report["source_ehp_dimension_typo"] is False


def test_current_known_target_and_prior_frontier_is_incomplete() -> None:
    observations = audit.validate_observations(example_target(), example_prior())
    assert observations["open_goals_count"] == 3
    assert observations["proof_complete"] is False
    assert observations["target_status"] == "INCOMPLETE_AND_WEB_CONFIRMED"


@pytest.mark.parametrize("field,value", [
    ("audit_result", "COMPLETE_AND_WEB_VERIFIED"),
    ("search_status", "complete"),
    ("search_conclusion_is_none", False),
    ("web_key", "generic-complete-proof"),
    ("web_partial", False),
    ("search_proven_count", 1),
    ("db_goal_typed", False),
])
def test_unexpected_status_must_not_be_silently_promoted(field: str, value: object) -> None:
    target = example_target()
    target[field] = value
    with pytest.raises(RuntimeError, match="TARGET_STATUS_CHANGED"):
        audit.validate_observations(target, example_prior())


def test_open_goal_shape_must_remain_derived_not_given() -> None:
    target = example_target()
    target["search_open_goals"] = ["Relation(lhs=target, rhs=direct GIVEN)"]
    with pytest.raises(RuntimeError, match="TARGET_OPEN_GOALS_CHANGED"):
        audit.validate_observations(target, example_prior())


def test_prior_must_have_completed_trust() -> None:
    prior = example_prior()
    prior["trust_verified"] = False
    with pytest.raises(RuntimeError, match="PI84_PRIOR_NOT_VERIFIED"):
        audit.validate_observations(example_target(), prior)


def test_r3_display_dirty_paths_allowed_but_other_dirty_paths_fail() -> None:
    paths = audit.validate_dirty_paths(["phase175_r3r12_hopf_conclusion/audit.py"])
    assert paths == ["phase175_r3r12_hopf_conclusion/audit.py"]
    with pytest.raises(RuntimeError, match="UNREVIEWED_TRACKED_CHANGES"):
        audit.validate_dirty_paths(["phase165_r55_nk_only_goal.py"])


def test_preexisting_tracked_pytest_nodeids_is_explicitly_allowed() -> None:
    paths = audit.validate_dirty_paths([
        ".pytest_cache/v/cache/nodeids",
        "phase175_r3r12_hopf_conclusion/audit.py",
        ".pytest_cache/v/cache/nodeids",
    ])
    assert paths == [
        ".pytest_cache/v/cache/nodeids",
        "phase175_r3r12_hopf_conclusion/audit.py",
    ]
    assert audit.TRACKED_PYTEST_CACHE_FILE == ".pytest_cache/v/cache/nodeids"


@pytest.mark.parametrize("unexpected", [
    "phase165_r55_nk_only_goal.py",
    ".pytest_cache/v/cache/lastfailed",
    ".pytest_cache/v/cache/nodeids.backup",
    ".pytest_cache/pytest.ini",
    "tests/test_broken.py",
])
def test_unreviewed_paths_remain_blocked_with_pytest_cache(
    unexpected: str,
) -> None:
    with pytest.raises(RuntimeError, match="UNREVIEWED_TRACKED_CHANGES"):
        audit.validate_dirty_paths([
            ".pytest_cache/v/cache/nodeids",
            unexpected,
        ])


def test_worker_parser_rejects_spoofed_malformed_and_duplicate_rows() -> None:
    payload = json.dumps(example_target())
    assert audit.decode_worker(audit.WORKER_MARKER + payload, 0, 5, 4)["n"] == 5
    with pytest.raises(RuntimeError, match="WORKER_COORDINATES_INVALID"):
        audit.decode_worker(audit.WORKER_MARKER + payload, 0, 4, 4)
    with pytest.raises(RuntimeError, match="WORKER_FAILURE_OR_MARKERS"):
        audit.decode_worker(audit.WORKER_MARKER + payload, 1, 5, 4)
    with pytest.raises(RuntimeError, match="WORKER_FAILURE_OR_MARKERS"):
        audit.decode_worker("", 0, 5, 4)
    with pytest.raises(RuntimeError, match="WORKER_JSON_INVALID"):
        audit.decode_worker(audit.WORKER_MARKER + "invalid", 0, 5, 4)


def test_r4_audit_does_not_offer_new_axioms_or_rules() -> None:
    assert audit.TARGET == (5, 4)
    assert audit.PRIOR == (4, 4)
    assert audit.REVIEWED_R3_HEAD.startswith("a1ce1558")


def test_reviewed_r3_source_pin_transition_is_exact_and_nonmutating(
    monkeypatch: pytest.MonkeyPatch, tmp_path,
) -> None:
    old = audit.REVIEWED_R1_SOURCE_BLOB
    new = audit.REVIEWED_R3_SOURCE_BLOB
    path = audit.REVIEWED_R3_SOURCE_PATH
    calls: list[tuple[str, str]] = []

    def fake_git(root, *args: str, allow_failure: bool = False):
        assert root == tmp_path
        calls.append(args)
        if args == ("rev-parse", audit.REVIEWED_R3_HEAD + ":" + path):
            return 0, new
        raise AssertionError("Unexpected git call: " + repr(args))

    monkeypatch.setattr(audit, "git", fake_git)
    old_pins = {path: old, "stable.py": "stable-sha"}
    more_pins = {"other.py": "other-sha"}
    observed = audit.reviewed_source_pins(tmp_path, old_pins, more_pins)
    assert observed == {path: new, "stable.py": "stable-sha", "other.py": "other-sha"}
    assert old_pins[path] == old
    assert more_pins == {"other.py": "other-sha"}
    assert calls == [("rev-parse", audit.REVIEWED_R3_HEAD + ":" + path)]


def test_reviewed_r3_pin_rejects_drift_without_loosening_other_guards(
    monkeypatch: pytest.MonkeyPatch, tmp_path,
) -> None:
    path = audit.REVIEWED_R3_SOURCE_PATH
    pins = {path: audit.REVIEWED_R1_SOURCE_BLOB, "stable.py": "stable-sha"}

    def good_git(root, *args: str, allow_failure: bool = False):
        return 0, audit.REVIEWED_R3_SOURCE_BLOB

    monkeypatch.setattr(audit, "git", good_git)
    with pytest.raises(RuntimeError, match="SOURCE_PIN_CONFLICT"):
        audit.reviewed_source_pins(tmp_path, pins, {"stable.py": "different"})
    with pytest.raises(RuntimeError, match="REVIEWED_R1_SOURCE_PIN_CHANGED"):
        audit.reviewed_source_pins(
            tmp_path, {path: "unexpected-r1-hash"}, {},
        )
    with pytest.raises(RuntimeError, match="REVIEWED_R1_SOURCE_PIN_CHANGED"):
        audit.reviewed_source_pins(tmp_path, {}, {})

    def bad_git(root, *args: str, allow_failure: bool = False):
        return 0, "arbitrary-new-head-sha"

    monkeypatch.setattr(audit, "git", bad_git)
    with pytest.raises(RuntimeError, match="REVIEWED_R3_SOURCE_PIN_MISMATCH"):
        audit.reviewed_source_pins(tmp_path, pins, {})
