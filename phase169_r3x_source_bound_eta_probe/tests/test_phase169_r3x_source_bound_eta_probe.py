"""Focused read-only tests for direct source-bound specialization."""
from __future__ import annotations

import pytest

from phase169_r3x_source_bound_eta_probe.audit import examine


@pytest.fixture(scope='module')
def report():
    return examine()


def test_pi53_baseline_and_read_only_boundary(report):
    assert report['pi53_status'] == 'complete'
    assert report['mode'] == 'AUDIT_ONLY'
    assert report['production_modified'] is False
    assert report['existing_tests_modified'] is False
    assert report['full_pytest_run'] is False


def test_source_bound_higher_eta_proof_is_unique_and_cited(report):
    assert report['source_bound_proposal_count'] == 1
    assert report['bound_proof_rule'] == 'inference'
    assert report['bound_proof_premise_rule'] == 'given'
    assert report['source_locator'] == 'Proposition 5.1'
    assert report['source_assertion_id'] == report['bound_proof_citation_id']
    assert report['source_prior_to_goal'] is True


def test_missing_source_fails_closed_without_suppressing_other_routes(report):
    assert report['missing_source_failed_closed'] is True
    assert report['public_provider_unchanged'] is True
    routes = report['public_provider_route_names']
    assert 'Toda Proposition 5.1 generic higher-eta specialization' in routes
    assert 'cited stable eta-family notation for iterated transport' in routes
