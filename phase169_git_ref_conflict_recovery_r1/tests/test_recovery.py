"""Focused offline tests for file discovery and safe relocation."""
from __future__ import annotations

from pathlib import Path
import subprocess

import pytest

from phase169_git_ref_conflict_recovery_r1.recovery import (
    classify_loose_ref,
    rescue,
    scan_git_metadata,
)


def repo_fixture(tmp_path: Path) -> Path:
    root = tmp_path / 'ehp_proof'
    root.mkdir()
    subprocess.run(['git', 'init', '-q', str(root)], check=True)
    subprocess.run(['git', '-C', str(root), 'config', 'user.name', 'tester'], check=True)
    subprocess.run(['git', '-C', str(root), 'config', 'user.email', 'tester@example.invalid'], check=True)
    (root / 'test.txt').write_text('initial\n', encoding='utf-8')
    subprocess.run(['git', '-C', str(root), 'add', 'test.txt'], check=True)
    subprocess.run(['git', '-C', str(root), 'commit', '-qm', 'initial'], check=True)
    subprocess.run(['git', '-C', str(root), 'branch', '-M', 'develop'], check=True)
    sha = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD']).decode().strip()
    subprocess.run(['git', '-C', str(root), 'update-ref', 'refs/remotes/origin/develop', sha], check=True)
    return root


def test_classification_only_expected_invalid_names():
    assert classify_loose_ref(Path('refs/heads/develop (x の競合コピー 2026-10-28)')) == 'CONFLICT_CANDIDATE'
    assert classify_loose_ref(Path('refs/remotes/origin/develop (x の競合コピー 2026-10-28)')) == 'CONFLICT_CANDIDATE'
    assert classify_loose_ref(Path('refs/heads/develop')) == 'DEVELOP_NEIGHBOR'
    assert classify_loose_ref(Path('refs/heads/feature (x の競合コピー)')) == 'OUT_OF_SCOPE'
    assert classify_loose_ref(Path('logs/refs/heads/develop (x の競合コピー)')) == 'OUT_OF_SCOPE'


def test_recursive_scan_unicode_conflicted_loose_ref(tmp_path: Path):
    dotgit = tmp_path / '.git'
    parent = dotgit / 'refs' / 'heads'
    parent.mkdir(parents=True)
    conflict = parent / 'develop (oomae-pc11 の競合コピー 2026-10-28)'
    conflict.write_text('0' * 40 + '\n', encoding='utf-8')
    report = scan_git_metadata(dotgit)
    assert len(report['candidates']) == 1
    assert '競合コピー' in report['candidates'][0]['path']


def test_dry_run_does_not_touch_invalid_loose_ref(tmp_path: Path):
    root = repo_fixture(tmp_path)
    invalid = root / '.git' / 'refs' / 'heads' / 'develop (oomae-pc11 の競合コピー 2026-10-28)'
    invalid.write_text('7' * 40 + '\n', encoding='utf-8')
    result = rescue(root, repair=False)
    assert result['status'] == 'CANDIDATES_FOUND_DRY_RUN'
    assert invalid.is_file()


def test_repair_moves_only_invalid_ref_and_keeps_valid_shas(tmp_path: Path):
    root = repo_fixture(tmp_path)
    invalid = root / '.git' / 'refs' / 'heads' / 'develop (oomae-pc11 の競合コピー 2026-10-28)'
    invalid.write_text('7' * 40 + '\n', encoding='utf-8')
    before = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD']).decode().strip()
    result = rescue(root, repair=True, backup_parent=tmp_path)
    assert result['status'] == 'PASS'
    assert not invalid.exists()
    assert Path(result['backup']).is_dir()
    assert subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD']).decode().strip() == before
    assert (Path(result['backup']) / 'manifest.json').is_file()


def test_no_file_does_not_claim_repair_success(tmp_path: Path):
    root = repo_fixture(tmp_path)
    result = rescue(root, repair=True, backup_parent=tmp_path)
    assert result['status'] == 'NO_CONFLICT_CANDIDATE_FOUND'
    assert result['backup'] is None


def test_reject_more_than_two_candidates(tmp_path: Path):
    root = repo_fixture(tmp_path)
    parent = root / '.git' / 'refs' / 'heads'
    for count in range(3):
        (parent / f'develop (host{count} の競合コピー 2026-10-28)').write_text('9' * 40 + '\n', encoding='utf-8')
    with pytest.raises(RuntimeError, match='More than two'):
        rescue(root, repair=True, backup_parent=tmp_path)
