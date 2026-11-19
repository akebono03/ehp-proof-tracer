from __future__ import annotations

import json

import pytest

from phase176_r3_n3_rule_sufficiency_audit import audit


def test_source_anchor_contract_on_fixture(tmp_path) -> None:
    for label, (name, *anchors) in audit.SOURCE_ANCHORS.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('a', encoding='utf-8') as stream:
            stream.write('\n' + '\n'.join(anchors))
    checked = audit.check_source_anchors(tmp_path)
    assert set(checked) == set(audit.SOURCE_ANCHORS)
    assert all(row['present'] for row in checked.values())


def test_missing_anchor_is_not_accepted(tmp_path) -> None:
    for name, *_ in audit.SOURCE_ANCHORS.values():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('unrelated text', encoding='utf-8')
    assert all(not row['present'] for row in audit.check_source_anchors(tmp_path).values())


def test_proposal_is_never_reported_as_proved() -> None:
    class FakeExpansion:
        def __init__(self) -> None:
            self.premises = ('open premise',)

    row = audit.summarize_proposals('goal', lambda goal: (FakeExpansion(),))
    assert row['status'] == 'inspected'
    assert row['proposal_count'] == 1
    assert 'verified' not in row
    assert row['proposals'][0]['premises'] == "('open premise',)"


def test_provider_failure_is_visible() -> None:
    def invalid(goal):
        raise ValueError('not applicable')

    row = audit.summarize_proposals('goal', invalid)
    assert row['status'] == 'provider_error'
    assert 'ValueError' in row['error']


def test_dry_run_does_not_launch_worker(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.setattr(audit, 'preflight', lambda: {'head': 'test'})
    monkeypatch.setattr(audit, 'worker', lambda timeout: pytest.fail('worker launched'))
    monkeypatch.setenv('LOCALAPPDATA', str(tmp_path))
    assert audit.execute(True, 120) == 0
    report = json.loads((tmp_path / 'EHPProofTracerAudit' / audit.PACKAGE / 'report.json').read_text(encoding='utf-8'))
    assert report['full_pytest'] == 'NOT_RUN'
    assert report['mathematical_proof_complete'] is False


def test_nu_prime_source_anchors_do_not_escape_apostrophe() -> None:
    lemma = audit.SOURCE_ANCHORS['Lemma 5.7'][2]
    hopf = audit.SOURCE_ANCHORS['(5.3)'][2]
    assert lemma == r"E(\eta_2\circ\nu')=0"
    assert hopf == r"H(\nu')=\eta_5"
    assert r"\nu\'" not in lemma
    assert r"\nu\'" not in hopf


def test_nu_prime_anchors_match_literal_toda_excerpt(tmp_path) -> None:
    ch5 = tmp_path / 'sources' / 'toda' / 'Toda_05_2.tex'
    ch2 = tmp_path / 'sources' / 'toda' / 'Toda_02_2.tex'
    ch5.parent.mkdir(parents=True)
    ch5.write_text(
        r"\label{lemma:5.7} E(\eta_2\circ\nu')=0 "
        r"\textbf{(5.3).} H(\nu')=\eta_5",
        encoding='utf-8',
    )
    ch2.write_text('', encoding='utf-8')
    checked = audit.check_source_anchors(tmp_path)
    assert checked['Lemma 5.7']['present'] is True
    assert checked['(5.3)']['present'] is True
