"""Read-only provenance audit for canonical complete group proofs."""
from __future__ import annotations

import pytest

from phase168_r3_41p16_origin_boundary_audit.audit import (
    CASES,
    audit_case,
    observe_search_origin,
    source_hashes,
    trust_scope_probes,
)


@pytest.fixture(scope="module")
def observed_cases():
    return {
        name: audit_case(name, n, k, expected)
        for name, n, k, expected in CASES
    }


@pytest.mark.parametrize("name,n,k,expected", CASES)
def test_observed_inference_factory_and_screened_bridge_are_used(
    observed_cases, name, n, k, expected,
):
    row = observed_cases[name]
    assert row["observed_invariants_pass"]
    assert row["factory_output_identity_count"] == expected[0]
    assert row["screened_given_link_count"] == expected[1]
    assert row["prior_given_count"] == expected[1]
    assert row["search_received_the_same_screened_bridge"]
    assert row["verification_counts"] == list(expected)


@pytest.mark.parametrize("name,n,k,expected", CASES)
def test_public_proof_narrative_and_citations_do_not_change(
    observed_cases, name, n, k, expected,
):
    row = observed_cases[name]
    assert row["steps"] == sum(expected)
    assert row["model_step_identity_preserved"]
    assert row["web_fulltext_equal"]
    assert row["citation_numbers_equal"]
    assert row["reference_section_present"]
    assert row["proof_section_present"]
    assert not row["web_partial"]


def test_rule_and_bridge_inputs_are_not_independent_certificates():
    scope = trust_scope_probes()
    assert scope["generic_matcher_accepts_self_supplied_rule"]
    assert scope["generic_checker_accepts_self_supplied_bridge"]
    assert scope["artificial_target_statement_does_not_match_result"]
    assert scope["bare_model_accepts_unregistered_given"]
    assert scope["rule_registry_is_not_an_independent_mathematical_certificate"]


def test_renderer_mathematical_guards_remain_installed():
    scope = trust_scope_probes()
    assert scope["projection_guards_unchanged"]


def test_read_only_provenance_audit_does_not_change_application_sources():
    before = source_hashes()
    result, screened, original, row = observe_search_origin(2, 1)
    assert row["search_received_the_same_screened_bridge"]
    assert row["factory_output_identity_count"] == 13
    assert source_hashes() == before
