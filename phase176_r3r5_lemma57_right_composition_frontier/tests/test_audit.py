"""Focused R3R5 audit contracts, no mathematical proof certification."""
from __future__ import annotations

import json
import pytest

from phase176_r3r5_lemma57_right_composition_frontier import audit


def test_source_contract_fixture(tmp_path):
    for name in audit.SOURCE_PATHS:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('\n'.join(audit.ANCHORS.get(name, ())), encoding='utf-8')
    assert len(audit.verify_source_contract(tmp_path)) == len(audit.SOURCE_PATHS)


def test_missing_source_anchor_refused(tmp_path):
    for name in audit.SOURCE_PATHS:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('unrelated text', encoding='utf-8')
    with pytest.raises(RuntimeError, match='SOURCE_ANCHOR_MISSING'):
        audit.verify_source_contract(tmp_path)


def test_nu_prime_apostrophe_not_escaped():
    values = audit.ANCHORS['sources/toda/Toda_05_2.tex']
    assert r"E(\eta_2\circ\nu')=0" in values
    assert all(r"\nu\'" not in s for s in values)


def test_factor_analysis_does_not_claim_proof():
    row = audit.analyze_generator_factors(('eta2', 'nu_prime', 'eta6'))
    assert row['factor_count'] == 3
    assert row['right_factor_count'] == 1
    assert row['can_form_two_factor_lemma57_prefix'] is True
    assert 'proved' not in row


def test_options_not_proof():
    class Rule:
        name = 'hypothetical'
    class Option:
        rule = Rule()
        subgoals = ('unproved',)
    value = audit.summarize_options((Option(),))
    assert value['status'] == 'UNVERIFIED_PROPOSALS'
    assert value['count'] == 1


def test_dryrun_no_worker(monkeypatch, tmp_path):
    monkeypatch.setattr(audit, 'preflight', lambda: {'head': 'fixture'})
    monkeypatch.setattr(audit, 'worker', lambda timeout: pytest.fail('Worker invoked'))
    monkeypatch.setenv('LOCALAPPDATA', str(tmp_path))
    assert audit.execute(True, 120) == 0
    report = json.loads((tmp_path / 'EHPProofTracerAudit' / audit.PACKAGE / 'report.json').read_text(encoding='utf-8'))
    assert report['proof_complete'] is False
    assert report['new_given'] == 0
    assert report['full_pytest'] == 'NOT_RUN'
