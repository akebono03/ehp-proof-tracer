"""Focused tests for the R3R4 read-only frontier audit."""
from __future__ import annotations

import json

import pytest

from phase176_r3r4_zero_image_and_hopf_lift_frontier import audit


def test_source_contract_accepts_literal_fixture(tmp_path) -> None:
    for name in audit.SOURCES:
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        anchors = audit.SOURCE_CONTRACT.get(name, ())
        target.write_text('\n'.join(anchors), encoding='utf-8')
    assert len(audit.verify_sources(tmp_path)) == len(audit.SOURCES)


def test_missing_source_anchor_blocks_audit(tmp_path) -> None:
    for name in audit.SOURCES:
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('unrelated', encoding='utf-8')
    with pytest.raises(RuntimeError, match='SOURCE_ANCHORS_MISSING'):
        audit.verify_sources(tmp_path)


def test_nu_prime_source_anchor_preserves_apostrophe() -> None:
    anchors = audit.SOURCE_CONTRACT['sources/toda/Toda_05_2.tex']
    assert r"E(\eta_2\circ\nu')=0" in anchors
    assert all(r"\nu\'" not in value for value in anchors)


def test_proposal_is_not_a_proof() -> None:
    class Rule:
        name = 'hypothetical'

    class Option:
        rule = Rule()
        subgoals = ('unresolved premise',)

    result = audit.proposal_summary((Option(),))
    assert result['count'] == 1
    assert result['status'] == 'UNVERIFIED_PROPOSALS'
    assert result['options'][0]['rule'] == 'hypothetical'


def test_provider_error_is_not_reported_as_empty_success() -> None:
    def broken(goal):
        raise ValueError('example')

    found = audit.safe_provider(broken, 'goal')
    assert found['status'] == 'PROVIDER_ERROR'
    assert 'ValueError' in found['error']


def test_dry_run_does_not_call_worker(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(audit, 'preflight', lambda: {'head': 'test-only'})
    monkeypatch.setattr(audit, 'worker', lambda timeout: pytest.fail('worker must not run'))
    monkeypatch.setenv('LOCALAPPDATA', str(tmp_path))
    assert audit.run(True, 120) == 0
    target = tmp_path / 'EHPProofTracerAudit' / audit.PACKAGE / 'report.json'
    report = json.loads(target.read_text(encoding='utf-8'))
    assert report['proof_complete'] is False
    assert report['new_given'] == 0
    assert report['full_pytest'] == 'NOT_RUN'
