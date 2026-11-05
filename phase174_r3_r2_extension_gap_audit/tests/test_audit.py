"""Focused regression tests for the source-first cyclic gap assessment."""
from copy import deepcopy

import pytest

from phase174_r3_r2_extension_gap_audit.audit import (
    R3R1_ORIGINAL_HEAD,
    derive_structural_obligations,
    validate_prior_frontier,
)


def _prior():
    def cyclic():
        return {
            "rule": "finite cyclic structure gives group relation",
            "child_count": 1,
            "children": [{
                "unwrapped_goal": {"type": "CyclicStructureStatement", "repr": "cyclic"},
                "exact_screened_given": False,
                "second_hop_proposal_count": 0,
            }],
        }

    return {
        "phase": "174-R3-R1",
        "mode": "READ_ONLY_TWO_HOP_FRONTIER",
        "local_head": R3R1_ORIGINAL_HEAD,
        "new_proof_steps": 0,
        "full_pytest_performed": False,
        "pi85_frontier": {
            "root_proposal_count": 3,
            "screened_given_count": 27,
            "root_proposals": [
                cyclic(),
                {
                    "rule": "equality symmetry",
                    "child_count": 1,
                    "children": [{
                        "unwrapped_goal": {"type": "Relation", "repr": "reverse"},
                        "second_hop_proposal_count": 1,
                    }],
                },
                cyclic(),
            ],
            "new_given": 0,
            "proofs_verified_by_this_audit": 0,
        },
    }


def test_prior_provenance_preserves_two_unexpanded_cyclic_children():
    value = validate_prior_frontier(_prior())
    assert value["root_proposal_count"] == 3
    assert value["root_proposals"][2]["children"][0]["second_hop_proposal_count"] == 0


def test_prior_rejects_promoted_direct_given():
    prior = _prior()
    prior["pi85_frontier"]["root_proposals"][0]["children"][0]["exact_screened_given"] = True
    with pytest.raises(ValueError, match="GIVEN"):
        validate_prior_frontier(prior)


def test_prior_rejects_modified_root_number():
    prior = _prior()
    prior["pi85_frontier"]["root_proposal_count"] = 4
    with pytest.raises(ValueError, match="root proposal count"):
        validate_prior_frontier(prior)


def test_prior_rejects_changed_original_head():
    prior = _prior()
    prior["local_head"] = "other"
    with pytest.raises(ValueError, match="HEAD provenance"):
        validate_prior_frontier(prior)


def test_extension_arithmetic_does_not_certify_mathematical_premises():
    result = derive_structural_obligations(
        source_order=4, subgroup_index=2, doubled_lift=True,
        mono_proved=False, index_proved=False, double_proved=False,
    )
    assert result["conditional_cardinality"] == 8
    assert result["not_a_ProofStep"] is True
    assert result["all_obligations_proved_by_this_audit"] is False
    assert all(not x["verified_by_this_audit"] for x in result["requirements"])


def test_extension_inputs_reject_nonintegral_order():
    with pytest.raises(ValueError, match="source_order"):
        derive_structural_obligations(
            source_order=True, subgroup_index=2, doubled_lift=True,
            mono_proved=False, index_proved=False, double_proved=False,
        )
