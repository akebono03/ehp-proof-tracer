"""Phase 173 five-complete-document closeout, isolated from the real repository."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from phase173_final_closeout_docs.docs_closeout import (
    CHECKPOINT,
    EXPECTED_SUMMARY,
    FINAL_BLOCKS,
    MARKER,
    README_FINAL,
    REVIEWED_BLOBS,
    REVIEWED_HEAD,
    transform_document,
    verify_report,
)


def test_exactly_five_docs_selected() -> None:
    assert set(REVIEWED_BLOBS) == {
        'README.md', 'docs/design.md', 'docs/development_log.md',
        'docs/roadmap.md', 'docs/proof_records.md',
    }


def test_readme_complete_text_prepends_closeout_and_preserves_history() -> None:
    raw = (
        '# EHP Proof Tracer\n\n' + CHECKPOINT + '\n'
        '## Current status — Phase 173 R15R17 checkpoint (2026-11-04)\n'
        'Older checkpoint content.\n'
    ).encode('utf-8')
    result = transform_document('README.md', raw).decode('utf-8')
    assert result.count(MARKER) == 1
    assert 'Older checkpoint content.' in result
    assert '## Historical checkpoint — Phase 173 R15R17' in result
    assert '## Current status — Phase 173 formally closed' in result
    assert result.index(MARKER) < result.index(CHECKPOINT)
    assert result.endswith('Older checkpoint content.\n')


@pytest.mark.parametrize('path', tuple(FINAL_BLOCKS))
def test_four_japanese_docs_append_complete_copy(path: str) -> None:
    raw = ('# EHP Proof Tracer 記録\n\n先行記録。\n' + CHECKPOINT + '\n').encode('utf-8')
    result = transform_document(path, raw)
    assert result.startswith(raw)
    assert result.count(MARKER.encode('utf-8')) == 1
    assert b'\r\n' not in result
    assert '$\\pi' in result.decode('utf-8') or path == 'docs/development_log.md'


def test_windows_newlines_preserved() -> None:
    path = 'docs/design.md'
    raw = ('# EHP Proof Tracer 設計\r\n' + CHECKPOINT + '\r\n').encode('utf-8')
    result = transform_document(path, raw)
    assert result.startswith(raw)
    assert b'\r\n' in result[len(raw):]
    assert b'\n' not in result[len(raw):].replace(b'\r\n', b'')


def test_duplicate_closeout_rejected() -> None:
    raw = ('# EHP Proof Tracer\n' + CHECKPOINT + '\n' + MARKER).encode('utf-8')
    with pytest.raises(ValueError, match='already applied'):
        transform_document('docs/proof_records.md', raw)


def test_missing_checkpoint_rejected() -> None:
    with pytest.raises(ValueError, match='checkpoint'):
        transform_document('docs/design.md', b'# EHP Proof Tracer\n')


def test_unreviewed_target_rejected() -> None:
    with pytest.raises(ValueError, match='unsupported'):
        transform_document('docs/unreviewed.md', b'')


def make_report(tmp_path: Path) -> Path:
    stdout = tmp_path / 'active_suite_stdout_r2.txt'
    stdout.write_text('..................................... [100%]\n'
                      + EXPECTED_SUMMARY + '\n', encoding='utf-8')
    report = {
        'phase': 173,
        'checkpoint': 'phase_end_corrective_r2',
        'status': 'PASS',
        'head': REVIEWED_HEAD,
        'pytest_exit_code': 0,
        'pytest_passed_count': 3546,
        'pytest_summary': EXPECTED_SUMMARY,
        'prior_failure_evidence_status': 'UNAVAILABLE_ORIGINAL_FILES',
        'prior_failure_sha256': {},
        'browser_content_checked': [[4, 8], [4, 9], [5, 3], [4, 4]],
        'phase_formally_closed': False,
        'pytest_stdout': str(stdout),
    }
    report_path = tmp_path / 'phase173_full_test_report_r2.json'
    report_path.write_text(json.dumps(report), encoding='utf-8')
    return report_path


def test_valid_success_report_accepted(tmp_path: Path) -> None:
    output = verify_report(make_report(tmp_path))
    assert output['head'] == REVIEWED_HEAD
    assert output['summary'] == EXPECTED_SUMMARY
    assert output['prior_evidence_status'] == 'UNAVAILABLE_ORIGINAL_FILES'
    assert len(output['report_sha256']) == 64


def test_forged_full_suite_count_rejected(tmp_path: Path) -> None:
    path = make_report(tmp_path)
    content = json.loads(path.read_text(encoding='utf-8'))
    content['pytest_passed_count'] = 3545
    path.write_text(json.dumps(content), encoding='utf-8')
    with pytest.raises(RuntimeError, match='differs'):
        verify_report(path)


def test_missing_report_rejected(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match='not found'):
        verify_report(tmp_path / 'absent.json')


def test_missing_stdout_rejected(tmp_path: Path) -> None:
    path = make_report(tmp_path)
    stdout = tmp_path / 'active_suite_stdout_r2.txt'
    stdout.unlink()
    with pytest.raises(RuntimeError, match='stdout'):
        verify_report(path)


def test_original_failure_not_claimed_verified() -> None:
    assert 'not verifiable' in README_FINAL
    assert '未検証' in FINAL_BLOCKS['docs/design.md']
    assert 'NOT_VERIFIABLE' in FINAL_BLOCKS['docs/development_log.md']


def test_full_document_dry_run_and_apply_preserve_backups(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    from types import SimpleNamespace
    from phase173_final_closeout_docs import docs_closeout as module

    repo = tmp_path / 'repo'
    package = repo / 'phase173_final_closeout_docs'
    package.mkdir(parents=True)
    originals = {}
    for path in REVIEWED_BLOBS:
        if path == 'README.md':
            content = (
                '# EHP Proof Tracer\n' + CHECKPOINT + '\n'
                '## Current status — Phase 173 R15R17 checkpoint (2026-11-04)\n'
                'Historical README prose.\n'
            ).encode('utf-8')
        else:
            content = ('# EHP Proof Tracer 記録\n' + CHECKPOINT + '\n'
                       '過去の記録を保持。\n').encode('utf-8')
        target = repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        originals[path] = content

    monkeypatch.setattr(module, 'verify_repo', lambda directory: REVIEWED_HEAD)
    monkeypatch.setattr(module, 'git', lambda *args, **kwargs: SimpleNamespace(stdout='stable-index\n'))
    evidence = {'head': REVIEWED_HEAD, 'report_sha256': 'a' * 64}

    module.produce_full_documents(repo, package, evidence, apply=False)
    for path, original in originals.items():
        assert (repo / path).read_bytes() == original
        preview = (package / 'full_documents' / path).read_bytes()
        assert MARKER.encode('utf-8') in preview

    module.produce_full_documents(repo, package, evidence, apply=True)
    for path, original in originals.items():
        assert (package / 'original_backups' / path).read_bytes() == original
        assert (repo / path).read_bytes() == (package / 'full_documents' / path).read_bytes()
        assert MARKER.encode('utf-8') in (repo / path).read_bytes()
    state = json.loads((package / 'installed_state.json').read_text('utf-8'))
    assert state['phase'] == 173
    assert set(state['files']) == set(REVIEWED_BLOBS)
