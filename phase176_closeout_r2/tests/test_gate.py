"""Focused R2 contracts; never launch a full pytest process."""
import json

import pytest

from phase176_closeout_r2 import gate
from phase176_closeout_r2.documents import sections
from phase176_closeout.documents import DOCUMENT_BLOBS, MARKER, HISTORICAL_HEADINGS, render_full
from phase176_closeout_r1_test_scope_repair import repair


def test_count_and_command():
    assert gate.ACTIVE_COMMAND == gate.original.ACTIVE_COMMAND
    assert gate.parse_summary('3546 passed in 40.00s', 0)[0] == 3546
    for count in (3545, 3547):
        with pytest.raises(RuntimeError):
            gate.parse_summary(f'{count} passed in 40.00s', 0)
    with pytest.raises(RuntimeError):
        gate.parse_summary('3546 passed, 1 skipped in 40.00s', 0)


def test_dryrun_and_no_second_attempt(monkeypatch, tmp_path):
    monkeypatch.setattr(gate, 'evidence_dir', lambda: tmp_path)
    monkeypatch.setattr(gate, 'preflight', lambda: {'head': gate.HEAD})
    def refuse(*args, **kwargs):
        raise AssertionError('NO_FULL_PYTEST')
    monkeypatch.setattr(gate.subprocess, 'run', refuse)
    assert gate.run(True) == 0
    assert not list(tmp_path.iterdir())
    attempt = tmp_path / 'attempt.json'
    attempt.write_text('{}', encoding='utf-8')
    assert gate.run(False) == 1
    assert attempt.read_text(encoding='utf-8') == '{}'


@pytest.fixture
def evidence(monkeypatch, tmp_path):
    first = {'attempt.json': 'old-attempt-hash', 'report.json': 'old-report-hash'}
    monkeypatch.setattr(repair, 'evidence_root', lambda: tmp_path)
    monkeypatch.setattr(repair, 'failed_evidence', lambda: first)
    folder = tmp_path / repair.PACKAGE
    folder.mkdir()
    out = b'3546 tests collected in 7.73s\n'
    pre = {'head': repair.HEAD, 'first_failure_evidence': first}
    report = {'gate': 'PASS_PHASE176_CLOSEOUT_R1_ACTIVE_COLLECTION_RESTORED',
              'collection_exit': 0, 'collection_count': 3546, 'first_failure_preserved': True,
              'baseline_inventory_restored': True, 'full_pytest': 'NOT_RUN',
              'phase176_formally_closed': False, 'preflight': pre, 'summary': out.decode().strip(),
              'stdout_sha256': repair.sha(out), 'stderr_sha256': repair.sha(b''),
              'archives': {n: {} for n in repair.PINS}}
    (folder / 'attempt.json').write_text(json.dumps({'preflight': pre}), encoding='utf-8')
    (folder / 'report.json').write_text(json.dumps(report), encoding='utf-8')
    (folder / 'collect_stdout.txt').write_bytes(out)
    (folder / 'collect_stderr.txt').write_bytes(b'')
    return folder, report


def test_verified_r1_evidence(evidence):
    folder, _ = evidence
    info = gate.verify_r1_evidence()
    assert info['collection_count'] == 3546
    assert info['r1_evidence']['report.json'] == repair.sha((folder / 'report.json').read_bytes())


def test_tampered_collection_rejected(evidence):
    folder, _ = evidence
    (folder / 'collect_stdout.txt').write_bytes(b'changed')
    with pytest.raises(RuntimeError, match='R1_EVIDENCE_MISMATCH'):
        gate.verify_r1_evidence()


def test_failed_r1_rejected(evidence):
    folder, report = evidence
    report['collection_exit'] = 2
    (folder / 'report.json').write_text(json.dumps(report), encoding='utf-8')
    with pytest.raises(RuntimeError, match='R1_REPORT_NOT_VERIFIED'):
        gate.verify_r1_evidence()


def test_full_documents_record_both_attempts():
    report = {'full_pytest_exit': 0, 'passed': 3546, 'summary': '3546 passed in 40.00s',
              'head': gate.HEAD, 'stdout_sha256': '0'*64, 'stderr_sha256': '1'*64,
              'preflight': {'r1': {'collection_count': 3546}}}
    result = sections(report)
    assert set(result) == set(DOCUMENT_BLOBS)
    for name, text in result.items():
        assert repair.FAIL_STDOUT in text and repair.FAIL_STDERR in text
        assert repair.HEAD in text and gate.HEAD in text
        assert 'R1' in text and 'R2' in text
        assert text.count(MARKER) == 1
        heading = HISTORICAL_HEADINGS.get(name, ('historical', 'historical'))[0]
        raw = ('# Title\n\n'+heading+'\nOld record\n').encode('utf-8')
        full = render_full(name, raw, text)
        assert b'Old record\n' in full
        if name not in HISTORICAL_HEADINGS:
            assert full.startswith(raw)
    report['full_pytest_exit'] = 2
    with pytest.raises(ValueError):
        sections(report)
