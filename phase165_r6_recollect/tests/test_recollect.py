from pathlib import Path

from phase165_r6_recollect.recollect import parse_errors, select_paths


def test_selection_only_active_tests(tmp_path: Path) -> None:
    (tmp_path / 'tests').mkdir()
    (tmp_path / 'archive').mkdir()
    (tmp_path / 'test_active.py').write_text('def test_ok(): pass\n')
    (tmp_path / 'archive' / 'test_old.py').write_text('def test_old(): pass\n')
    assert select_paths(tmp_path) == ['tests', 'test_active.py']


def test_parse_collection_errors() -> None:
    log = '___ ERROR collecting tests/test_a.py ___\nERROR collecting tests/test_b.py\nERROR collecting tests/test_a.py\n'
    assert parse_errors(log) == ['tests/test_a.py', 'tests/test_b.py']
