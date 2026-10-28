"""Focused, read-only shared-contract tests; no proof is fabricated."""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from phase169_r10ek_shared_transport_projection_design_audit.contract import (
    CASES,
    AuditCase,
    inspect_shared_contract,
    structure_components,
)


def test_r10ek_coverage_includes_distinct_cyclic_and_direct_sum_shapes():
    assert {(case.k, case.category) for case in CASES} == {
        (6, "finite_cyclic"),
        (10, "finite_cyclic"),
        (8, "direct_sum"),
        (9, "direct_sum"),
    }
    assert {case.expected_components for case in CASES} == {1, 2, 3}
    assert {case.expected_exponent for case in CASES} == {5, 10, 13, 14}


def test_r10ek_case_names_are_homotopy_indexed_without_search():
    assert AuditCase(22, 6, "finite_cyclic", 1, 14).group == "pi_28^22"
    assert AuditCase(24, 9, "direct_sum", 3, 13).group == "pi_33^24"


def test_r10ek_unknown_group_shape_is_not_assumed_cyclic():
    assert structure_components(None) is None
    assert structure_components("Z/2") is None
    assert structure_components(object()) is None


def test_r10ek_empty_model_is_not_a_verified_proof():
    model = SimpleNamespace(steps=(), step_citation_numbers=(), root_index=None)
    with pytest.raises(ValueError, match="presentation index"):
        inspect_shared_contract(model, (), SimpleNamespace(), CASES[0])


def test_r10ek_index_validation_fails_closed():
    model = SimpleNamespace(steps=(object(),), step_citation_numbers=((),), root_index=0)
    with pytest.raises(ValueError, match="presentation index"):
        inspect_shared_contract(model, (0, 0), SimpleNamespace(), CASES[0])
    with pytest.raises(ValueError, match="presentation index"):
        inspect_shared_contract(model, (1,), SimpleNamespace(), CASES[0])


def test_r10ek_no_fake_root_is_accepted():
    model = SimpleNamespace(
        steps=(SimpleNamespace(rule=None, conclusion=None, premises=()),),
        step_citation_numbers=((),),
        root_index=0,
    )
    with pytest.raises(ValueError, match="typed inferred group root"):
        inspect_shared_contract(model, (0,), SimpleNamespace(), CASES[0])
