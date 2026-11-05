"""Targeted regression tests for two-hop source-first frontier diagnostics."""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from phase174_r3_r1_frontier_audit.audit import (
    describe_first_two_hops,
    signature,
    validate_r2_record,
    verify_against_r2,
)


def _example_r2_record():
    return {
        "phase": "174-R2",
        "head": "3558d713fd7939ded656f2458aacc62d71c7e0b3",
        "mode": "READ_ONLY_SOURCE_FIRST",
        "new_given": 0,
        "new_inference_rules": 0,
        "new_proof_steps": 0,
        "new_completed_named_proofs": 0,
        "full_pytest_performed": False,
        "pi85_root_frontier": {
            "typed_goal": {"type": "str", "repr": "'target'"},
            "screened_given_count": 27,
            "target_direct_given_count": 0,
            "proposal_count": 3,
            "source_screening": "publication_screened",
            "citing_assertion_id": "source-id",
            "proposals": [
                {"rule_name": "root", "subgoal_count": 1,
                 "subgoals": [{"type": "str", "repr": "'middle'", "exact_screened_given": False}]}
                for _ in range(3)
            ],
        },
    }


def test_r2_contract_requires_unchanged_three_candidates():
    payload = _example_r2_record()
    assert validate_r2_record(payload)["screened_given_count"] == 27
    payload["pi85_root_frontier"]["proposal_count"] = 4
    with pytest.raises(ValueError, match="three observed candidates"):
        validate_r2_record(payload)


def test_r2_contract_rejects_new_proofs():
    payload = _example_r2_record()
    payload["new_proof_steps"] = 1
    with pytest.raises(ValueError, match="new proof evidence"):
        validate_r2_record(payload)


def test_two_hop_frontier_detects_existing_source_and_cycle():
    def proposal(name, *children):
        return SimpleNamespace(rule=SimpleNamespace(name=name), subgoals=children)

    def provider(goal):
        if goal == "target":
            return (proposal("root", "middle"),)
        if goal == "middle":
            return (proposal("circular", "target"), proposal("leaf", "source"))
        return ()

    output = describe_first_two_hops("target", provider, ("source",))
    assert output["root_proposal_count"] == 1
    branch = output["root_proposals"][0]["children"][0]
    assert branch["second_hop_proposal_count"] == 2
    assert branch["second_hop_proposals"][0]["subgoals"][0]["returns_to_root"] is True
    assert branch["second_hop_proposals"][1]["subgoals"][0]["exact_screened_given"] is True
    assert output["proofs_verified_by_this_audit"] == 0


def test_r2_root_replay_requires_matching_children():
    old = validate_r2_record(_example_r2_record())
    fresh = {
        "goal": signature("target"),
        "screened_given_count": 27,
        "root_proposal_count": 3,
        "screening_mode": "publication_screened",
        "citing_assertion_id": "source-id",
        "root_proposals": [
            {"rule": "root", "child_count": 1, "children": [
                {"goal": signature("middle"), "exact_screened_given": False},
            ]} for _ in range(3)
        ],
    }
    verify_against_r2(fresh, old)
    fresh["root_proposals"][1]["children"][0]["goal"] = signature("different")
    with pytest.raises(ValueError, match="child differs"):
        verify_against_r2(fresh, old)


def test_source_bound_diagnostic_is_not_accepted_as_proof():
    def proposal(name, *children):
        return SimpleNamespace(rule=SimpleNamespace(name=name), subgoals=children)

    class Scoped:
        def __init__(self, conclusion):
            self.conclusion = conclusion

    def provider(goal):
        if goal == "root":
            return (proposal("scoped", Scoped("child")),)
        return ()

    output = describe_first_two_hops(
        "root", provider, ("child",),
        unwrap=lambda obj: obj.conclusion if isinstance(obj, Scoped) else obj,
    )
    child = output["root_proposals"][0]["children"][0]
    assert child["is_source_bound_wrapper"] is True
    assert child["exact_screened_given"] is True
    assert output["proofs_verified_by_this_audit"] == 0
