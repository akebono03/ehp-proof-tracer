from pathlib import Path

from phase165_reference_stop_r1.audit import inspect_boundary
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r57_r12_ordered_proofs import validate_prior_internal_proofs


def test_existing_eligibility_and_prior_proof_interfaces_exist():
    assert callable(screen_shared_proof_context)
    assert callable(validate_prior_internal_proofs)


def test_boundary_report_has_no_premature_certification():
    report = inspect_boundary()
    assert report["source_files_modified"] is False
    assert report["search_stopping_behavior_verified"] is False
    assert report["actual_pi43_proof_tree_checked"] is False
    assert isinstance(report["matching_registry_assertions"], list)


def test_no_automatic_internal_proof_without_order():
    assert validate_prior_internal_proofs((), None, ()) == ()
