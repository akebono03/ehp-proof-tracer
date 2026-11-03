"""Repository-backed focused mathematical trust-boundary regression tests."""
from __future__ import annotations

from expression import Composition
from phase169_r10d2_general_family_definition.family_citation import CitedStableFamilyDefinition
from phase173_r4_r15r4_cited_composition_image.audit import (
    atom_evidence,
    expression_atoms,
    inspect_k,
)
from phase173_r4_r15r4_cited_composition_image.replay import (
    cited_source_steps,
    replay_named_image,
)
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r4_typed_generator_audit.audit import _group_components


def test_real_chapter_definitions_are_only_given_leaves() -> None:
    sources = cited_source_steps()
    ids = {
        step.conclusion.family_id for step in sources
        if isinstance(step.conclusion, CitedStableFamilyDefinition)
    }
    assert {4, 9, 10, 11, 12}.issubset(ids)
    assert 56 not in ids
    assert 88 not in ids
    assert all(not step.premises for step in sources)


def test_k31_composition_images_require_independent_family_sources() -> None:
    row = inspect_k(31)
    assert row["left_source_count"] == 4
    assert row["right_named_image_shape_matches"] == 4
    assert row["residual_target_count"] == 4
    assert row["public_completion"] is False
    assert row["new_source_given"] is False
    assert row["proved_named_images"] <= 4
    blockers = {
        fid for candidate in row["candidate_pairs"]
        for fid in candidate["missing_family_ids"]
    }
    assert 56 in blockers or 88 in blockers


def test_cited_phi_prime_nu_square_image_is_replayable_when_registered() -> None:
    # The proof engine must establish every atomic image; textual matching is
    # insufficient. This is a source-backed, nonpublic regression target.
    row = inspect_k(31)
    matches = [x for x in row["candidate_pairs"] if x["proof_engine_replayed"]]
    assert any(x["source_index"] == 3 for x in matches)
    assert all(x["proof_step_count"] > 0 for x in matches)
    assert all(x["cited_references"] for x in matches)


def test_no_citation_means_no_nu_named_composite_proof() -> None:
    left = _group_components(exact_prior_database_result(3, 31))
    target = _group_components(exact_prior_database_result(4, 31))
    assert left is not None and target is not None
    # No cited ν-family GIVEN: E(phi' nu_28^2) cannot be identified with ν_29^2.
    assert replay_named_image(left[3].generator, target[7].generator, ()) is None


def test_generic_flattening_preserves_all_composition_atoms() -> None:
    left = _group_components(exact_prior_database_result(3, 31))
    assert left is not None
    for component in left:
        atoms = expression_atoms(component.generator)
        assert len(atoms) >= 2
        assert not any(isinstance(x, Composition) for x in atoms)
