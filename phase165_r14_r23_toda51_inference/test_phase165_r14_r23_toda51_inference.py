from pathlib import Path
import pytest
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap, TodaSuspensionIsomorphismStatement
from phase165_r14_r23_toda51_inference import (
    AdoptedTextReview, promote_diagonal_from_existing_reference,
    derive_reviewed_diagonal_iso, audit_r23,
)
from phase165_r14_r22_same_reference import integrate_toda51_into_existing_reference
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from phase165_r14_r21_toda51_completion import complete_toda51_source
from proof import ProofRule
from unified_statement_registry import AssertionOrigin

TEX_PATH = Path(__file__).with_name("toda_51_complete.tex")

def setup_source():
    base, _ = build_phase165_r5_manifest_bridge()
    tex = TEX_PATH.read_text(encoding="utf-8")
    result = integrate_toda51_into_existing_reference(base, tex)
    return base, result, complete_toda51_source(tex)

def accepted_review(source):
    return AdoptedTextReview(source.source_sha256, True, "(5.1) adopted TeX reviewed")

def test_explicit_source_review_required():
    _, result, source = setup_source()
    with pytest.raises(ValueError, match="review required"):
        promote_diagonal_from_existing_reference(result.bridge, None)
    with pytest.raises(ValueError, match="review required"):
        promote_diagonal_from_existing_reference(result.bridge, AdoptedTextReview(source.source_sha256, False, "unchecked"))

def test_checksum_mismatch_rejected():
    _, result, source = setup_source()
    with pytest.raises(ValueError, match="checksum"):
        promote_diagonal_from_existing_reference(result.bridge, AdoptedTextReview("bad", True, "reviewed"))

def test_two_typed_leaves_under_existing_reference():
    base, result, source = setup_source()
    updated, ids = promote_diagonal_from_existing_reference(result.bridge, accepted_review(source))
    assert len(ids) == 2
    assert all(updated.registry.assertion(aid).reference_id == result.reference_id for aid in ids)
    assert all(updated.registry.assertion(aid).origin is AssertionOrigin.FIXED_STATEMENT for aid in ids)
    assert len(base.registry._assertions) + 8 == len(updated.registry._assertions)
    assert all(updated.registry.assertion(aid).available_after_position is None for aid in ids)

def test_e_isomorphism_derived_by_existing_inference_rule():
    _, result, source = setup_source()
    updated, ids = promote_diagonal_from_existing_reference(result.bridge, accepted_review(source))
    proof = derive_reviewed_diagonal_iso(updated, ids)
    expected_map = TodaSuspensionMap(TodaPrimaryGroup(1,1), TodaPrimaryGroup(2,2))
    assert proof.conclusion == TodaSuspensionIsomorphismStatement(expected_map)
    assert proof.rule is ProofRule.INFERENCE
    assert len(proof.premises) == 3

def test_archived_source_not_promoted():
    _, result, source = setup_source()
    updated, ids = promote_diagonal_from_existing_reference(result.bridge, accepted_review(source))
    assert all(updated.registry.assertion(aid).origin is AssertionOrigin.SOURCE_ARCHIVE for aid in result.component_ids)
    assert result.bridge.registry._assertions.keys() != updated.registry._assertions.keys()

def test_incorrect_proof_link_pair_rejected():
    _, result, source = setup_source()
    updated, ids = promote_diagonal_from_existing_reference(result.bridge, accepted_review(source))
    with pytest.raises(ValueError):
        derive_reviewed_diagonal_iso(updated, (ids[0], ids[0]))

def test_source_audit_derives_concrete_iso():
    report = audit_r23(TEX_PATH)
    assert report["typed_fixed_diagonal_claims"] == 2
    assert report["reviewed_toda_leaf_proofsteps"] == 2
    assert report["derived_suspension_iso_steps"] == 1
    assert report["production_pi32_proved"] is False
