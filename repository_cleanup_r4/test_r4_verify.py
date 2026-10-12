"""Focused checks for the repository cleanup R4 verifier."""
import json
from pathlib import Path

from repository_cleanup_r4.r4_verify import validate_r3


def make_summary():
    return {'phase': 'Repository Cleanup R3', 'mode': 'APPLY_CACHE_ONLY',
            'deleted_files': 3276, 'deleted_bytes': 3276,
            'deletion_failures': 0, 'tracked_status_unchanged': True,
            'tracked_files_modified_by_cleanup': False, 'backups_deleted': 0}


def test_r3_count_mismatch_is_rejected(tmp_path):
    result = validate_r3(make_summary(), [{'Path': '__pycache__/a.pyc', 'Bytes': '1'}], tmp_path)
    assert result['r3_log_consistent'] is False


def test_reappeared_cache_is_detected(tmp_path):
    directory = tmp_path / '__pycache__'
    directory.mkdir()
    (directory / 'a.pyc').write_bytes(b'x')
    result = validate_r3(make_summary(), [{'Path': '__pycache__/a.pyc', 'Bytes': '1'}], tmp_path)
    assert result['cache_reappeared_count'] == 1


def test_path_traversal_is_rejected(tmp_path):
    result = validate_r3(make_summary(), [{'Path': '../outside.pyc', 'Bytes': '1'}], tmp_path)
    assert result['r3_log_consistent'] is False
    assert result['invalid_log_entries'] == ['../outside.pyc']
