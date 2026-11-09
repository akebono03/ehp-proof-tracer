"""R40 actual source-bound citation and adopted-prior proof frontier checks."""
from __future__ import annotations

from phase174_r3_r7_r40_adopted_db_zero_image_isolated.audit import inspect_isolated_zero_image


def test_real_toda_annihilator_and_prior_db_derive_zero_image():
    report = inspect_isolated_zero_image()
    assert report["source_locator"] == "(5.9)"
    assert report["inferred_stable_factor_images"] == 2
    assert report["inferred_generator_zero"] is True
    assert report["isolated_zero_image_proved"] is True
    assert report["db_given_preserved_inside_proof_tree"] is True


def test_no_independent_literature_or_public_root_claim():
    report = inspect_isolated_zero_image()
    assert report["earlier_adopted_db_prior_verified"] is True
    assert report["db_prior_rule"] == "GIVEN"
    assert report["db_prior_is_independent_literature"] is False
    assert report["isolated_not_public_provider"] is True
    assert report["upper_delta_surjectivity_proved"] is False
    assert report["root_complete"] is False
    assert report["new_givens"] == 0
    assert report["new_direct_root_givens"] == 0
    assert report["public_production_files_changed"] == 0
