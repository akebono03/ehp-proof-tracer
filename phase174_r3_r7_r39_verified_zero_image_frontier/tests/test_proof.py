"""Actual R39 source-bound generator-zero proof and signed DB boundary."""
from __future__ import annotations

import pytest

from phase174_r3_r7_r39_verified_zero_image_frontier.audit import (
    derive_from_expansion, inspect_proof_frontier,
)
from phase174_r3_r7_r39_verified_zero_image_frontier.source_guard import verify_checkout


def test_real_screened_toda_source_derives_generator_zero_only():
    result = inspect_proof_frontier()
    assert result["cited_annihilator_source"] == "(5.9)"
    assert result["n6_annihilator_inferred"] is True
    assert result["stable_factor_images_inferred"] == 2
    assert result["composite_image_inferred"] is True
    assert result["associativity_inferred"] is True
    assert result["generator_zero_inferred"] is True
    assert result["zero_suspension_image_proved"] is False


def test_db_prior_stays_given_not_a_fake_inference():
    result = inspect_proof_frontier()
    assert result["adopted_earlier_db_prior_accepted"] is True
    assert result["db_prior_is_independent_literature"] is False
    assert result["db_presentation_step_rule"] == "GIVEN"
    assert result["r6_accepts_db_prior_as_inferred_presentation"] is False
    assert result["cyclic_presentation_inference_available_in_this_audit"] is False
    assert result["new_givens"] == 0
    assert result["new_public_rules"] == 0
    assert result["root_complete"] is False


def test_inference_step_factory_rejects_nonexpansion_arguments():
    with pytest.raises(TypeError, match="GoalExpansion"):
        derive_from_expansion(object(), ())
