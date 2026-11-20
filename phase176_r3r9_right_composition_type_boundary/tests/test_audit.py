"""Focused read-only contract tests for the R3R9 typing boundary."""
from __future__ import annotations

import json

import pytest

from phase176_r3r9_right_composition_type_boundary import audit


def test_source_contract_accepts_literal_fixture(tmp_path) -> None:
    for name, anchors in audit.SOURCES.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('\n'.join(anchors), encoding='utf-8')
    assert set(audit.check_sources(tmp_path)) == set(audit.SOURCES)


def test_source_contract_rejects_changed_source(tmp_path) -> None:
    for name in audit.SOURCES:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('unrelated', encoding='utf-8')
    with pytest.raises(RuntimeError, match='SOURCE_ANCHOR_MISSING'):
        audit.check_sources(tmp_path)


def test_summary_does_not_report_proof() -> None:
    class Rule:
        name = 'fixture only'

    class Candidate:
        rule = Rule()
        subgoals = ('one',)

    info = audit.summarize((Candidate(),))
    assert info == {'count': 1, 'status': 'UNVERIFIED_PROPOSALS',
                    'rules': ['fixture only'], 'subgoal_counts': [1]}


def test_summary_preserves_empty_candidate_count() -> None:
    assert audit.summarize(())['count'] == 0


def test_dryrun_does_not_execute_worker(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(audit, 'preflight', lambda: {'head': 'test'})
    monkeypatch.setattr(audit, 'worker', lambda timeout: pytest.fail('worker was started'))
    monkeypatch.setenv('LOCALAPPDATA', str(tmp_path))
    assert audit.execute(True, 120) == 0
    report = json.loads((tmp_path / 'EHPProofTracerAudit' / audit.PACKAGE / 'report.json').read_text(encoding='utf-8'))
    assert report['root_proof_complete'] is False
    assert report['full_pytest'] == 'NOT_RUN'


def test_worker_rejects_false_proof_claim(monkeypatch) -> None:
    class Result:
        returncode = 0
        stdout = audit.MARKER + json.dumps({'root_proof_complete': True,
                                            'new_given': 0, 'base_step_inferred': True})
        stderr = ''

    monkeypatch.setattr(audit.subprocess, 'run', lambda *args, **kwargs: Result())
    with pytest.raises(RuntimeError, match='FALSE_PROOF_CLAIM'):
        audit.worker(5)
