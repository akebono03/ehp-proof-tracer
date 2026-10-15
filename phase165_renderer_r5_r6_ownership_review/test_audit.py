"""Narrow tests for the read-only ownership audit."""
import pytest
from audit import category, extract_references, HISTORICAL, OWNED_PARTIAL, HELPER_COMPONENTS, SEPARATE_PRESENTATION_SURFACES, LEGACY_CHAINS


def test_category_sets_are_disjoint():
    groups=[HISTORICAL,OWNED_PARTIAL,HELPER_COMPONENTS,SEPARATE_PRESENTATION_SURFACES,LEGACY_CHAINS]
    assert sum(map(len,groups))==len(set().union(*groups))==26


def test_historical_never_classified_as_active():
    assert all(category(x)=='HISTORICAL_BACKUP' for x in HISTORICAL)


def test_partial_is_not_declared_independent_or_certified():
    assert category('phase165_r57_r2_partial_narrative.py')=='CANONICAL_OWNED_SUBROUTINE_REVIEW'


def test_phase162_chain_requires_review():
    assert category('phase162_r3_narrative_connection.py')=='LEGACY_OR_SPECIALIZED_CHAIN_REVIEW'


def test_unknown_candidate_causes_failure():
    with pytest.raises(ValueError,match='Unclassified'):
        category('new_unexpected_narrative_renderer.py')


def test_import_evidence_tracks_from_and_import():
    source='from phase162_r3_narrative_connection import render_phase162_r3_narrative\nimport toda_group_proof_narrative_renderer\n'
    result=extract_references(source,{'phase162_r3_narrative_connection','toda_group_proof_narrative_renderer'})
    assert [(x['kind'],x['line']) for x in result]==[('from',1),('import',2)]
