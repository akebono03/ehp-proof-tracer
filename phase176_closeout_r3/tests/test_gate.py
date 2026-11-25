"""Focused recovery contracts; no full suite execution or real checkout mutation."""
import json
from pathlib import Path
import zipfile

import pytest

from phase176_closeout_r3 import gate
from phase176_closeout_r3.documents import sections


def test_choose_original_requires_exact_hash_and_blob():
    raw = b'# Original\r\n'
    assert gate.choose_original([b'wrong', raw], gate.original.digest(raw), len(raw),
                                gate.repair.blob(raw)) == raw
    with pytest.raises(RuntimeError, match='ORIGINAL_BYTES_NOT_RECOVERABLE'):
        gate.choose_original([raw], gate.original.digest(raw), len(raw), gate.repair.blob(b'other'))


def test_known_states_and_unknown_edit():
    values = (b'original', b'r2', b'r3')
    assert [gate.classify(raw, *values) for raw in values] == ['ORIGINAL', 'R2_FINAL', 'R3_FINAL']
    with pytest.raises(RuntimeError, match='UNREVIEWED_DOCUMENT_CONTENT'):
        gate.classify(b'edited', *values)


def test_locked_document_remains_intact_and_can_resume(monkeypatch, tmp_path):
    target = tmp_path / 'README.md'
    target.write_bytes(b'old')
    real_replace = gate.os.replace
    calls = []
    def refuse(src, dest):
        calls.append(dest)
        raise PermissionError(13, 'locked')
    monkeypatch.setattr(gate.os, 'replace', refuse)
    monkeypatch.setattr(gate.time, 'sleep', lambda seconds: None)
    with pytest.raises(PermissionError, match='DOCUMENT_LOCKED'):
        gate.replace_document(target, b'old', b'new')
    assert calls == [target] * 3
    assert target.read_bytes() == b'old'
    assert list(tmp_path.iterdir()) == [target]
    monkeypatch.setattr(gate.os, 'replace', real_replace)
    gate.replace_document(target, b'old', b'new')
    gate.replace_document(target, b'new', b'new')
    assert target.read_bytes() == b'new'


def test_concurrent_edit_not_overwritten(tmp_path):
    target = tmp_path / 'README.md'
    target.write_bytes(b'edited')
    with pytest.raises(RuntimeError, match='CONCURRENT_DOCUMENT_CHANGE'):
        gate.replace_document(target, b'old', b'new')
    assert target.read_bytes() == b'edited'


def test_full_bundle_and_original_preserved(tmp_path):
    plan = {n: {'original': b'old', 'final': b'new'} for n in gate.DOCUMENT_BLOBS}
    archive = gate.write_bundle(tmp_path, plan)
    with zipfile.ZipFile(archive) as zf:
        assert set(zf.namelist()) == set(gate.DOCUMENT_BLOBS)
        assert zf.testzip() is None
        assert all(zf.read(n) == b'new' for n in plan)
    assert all((tmp_path / 'original_full' / n).read_bytes() == b'old' for n in plan)
    assert all((tmp_path / 'final_full' / n).read_bytes() == b'new' for n in plan)


@pytest.fixture
def evidence(monkeypatch):
    out = (gate.SUMMARY + '\n').encode()
    err = b''
    monkeypatch.setattr(gate, 'STDOUT', gate.original.digest(out))
    monkeypatch.setattr(gate, 'STDERR', gate.original.digest(err))
    info = {'first_failure_evidence': {'report.json': 'first'}, 'r1_evidence': {'report.json': 'r1'}}
    preflight = {'head': gate.HEAD, 'r1': info, 'historical_tests': list(gate.original.HISTORICAL),
                 'documents': {n: {'git_blob': pin} for n, pin in gate.DOCUMENT_BLOBS.items()}}
    public = {'gate': 'PASS_R3R60R2_PUBLIC_CITATION_PREMISE_ELISION_CONNECTED',
              'status': 'complete', 'web_key': 'generic-complete-proof', 'proof_steps': 62,
              'inference_steps': 51, 'given_steps': 11, 'citation_count': 10, 'open_goals': [],
              'body_rows_after': 18, 'display_reference_count_after': 9, 'root_display_count': 1,
              'references_without_explicit_body_use': [], 'model_unchanged': True,
              'partial_render_unchanged': True, 'public_adapter_verified': True,
              'retained_reference_blocks_unchanged_except_display_numbers': True,
              'public_connection': 'APPLIED', 'new_math_rules': 0, 'new_given_registrations': 0}
    report = {'gate': 'FAIL_PHASE176_CLOSEOUT_R2', 'head': gate.HEAD, 'full_pytest_exit': 0,
              'passed': 3546, 'summary': gate.SUMMARY, 'stdout_sha256': gate.STDOUT,
              'stderr_sha256': gate.STDERR, 'phase176_formally_closed': False,
              'first_failure_preserved': True, 'r1_evidence_preserved': True,
              'active_scope': 'tests/', 'historical_source_guard': 'FOUR_KNOWN_FAILURES_NOT_RERUN_NOT_PASSING',
              'error': "PermissionError(13, 'locked')", 'traceback': 'write_full_documents\nPermissionError',
              'preflight': preflight, 'public_audit': public}
    attempt = {'head': gate.HEAD, 'command': ['python', *gate.r2.ACTIVE_COMMAND], **info}
    raw = {n: json.dumps(obj).encode() for n, obj in (
        ('report.json', report), ('attempt.json', attempt), ('preflight.json', preflight),
        ('public_audit.json', public))}
    raw.update({'full_pytest_stdout.txt': out, 'full_pytest_stderr.txt': err})
    return raw, info, report


def test_saved_r2_evidence(evidence):
    raw, info, report = evidence
    assert gate.validate_r2_evidence(raw, info) == report


def test_tampered_stdout_refused(evidence):
    raw, info, _ = evidence
    raw['full_pytest_stdout.txt'] += b'changed'
    with pytest.raises(RuntimeError, match='R2_FULL_PYTEST_HASH_MISMATCH'):
        gate.validate_r2_evidence(raw, info)


def test_non_document_failure_refused(evidence):
    raw, info, report = evidence
    report['error'] = 'RuntimeError("different failure")'
    raw['report.json'] = json.dumps(report).encode()
    with pytest.raises(RuntimeError, match='R2_FAILURE_NOT_DOCUMENT_PERMISSION_ERROR'):
        gate.validate_r2_evidence(raw, info)


def test_recovery_documents_keep_r2_and_r1_history():
    report = {'full_pytest_exit': 0, 'passed': 3546, 'summary': gate.SUMMARY, 'head': gate.HEAD,
              'stdout_sha256': gate.STDOUT, 'stderr_sha256': gate.STDERR,
              'preflight': {'r1': {'collection_count': 3546}}}
    result = sections(report, 'f'*64)
    assert set(result) == set(gate.DOCUMENT_BLOBS)
    assert all(gate.SUMMARY in text and 'PermissionError' in text and 'f'*64 in text
               and text.count(gate.original.MARKER) == 1 for text in result.values())


def test_dry_run_no_output_or_full_test(monkeypatch, tmp_path):
    monkeypatch.setattr(gate, 'evidence_dir', lambda: tmp_path)
    monkeypatch.setattr(gate, 'preflight', lambda: ({'traceback': 'locked'}, {}, {}))
    def refuse(*args, **kwargs):
        raise AssertionError('NO_FULL_SUITE_OR_DOCUMENT_WRITES')
    monkeypatch.setattr(gate, 'write_bundle', refuse)
    monkeypatch.setattr(gate, 'apply_documents', refuse)
    monkeypatch.setattr(gate.original.subprocess, 'run', refuse)
    assert gate.run(True) == 0
    assert not list(tmp_path.iterdir())
