from pathlib import Path
from phase163_r1i_remaining_registry.audit import discover_singletons


def test_discover_singletons_restricts_to_root_and_named_assignments(tmp_path: Path):
    (tmp_path / 'sample.py').write_text('FACT_REPOSITORY = object()\nOTHER = 1\nRULE_CATALOG = None\n', encoding='utf-8')
    nested = tmp_path / 'archive'
    nested.mkdir()
    (nested / 'ignored.py').write_text('SHOULD_NOT_REPOSITORY = 1\n', encoding='utf-8')
    rows = discover_singletons(tmp_path)
    assert [row['name'] for row in rows] == ['FACT_REPOSITORY', 'RULE_CATALOG']


def test_discover_singletons_handles_parse_error(tmp_path: Path):
    (tmp_path / 'bad.py').write_text('def broken(:\n', encoding='utf-8')
    rows = discover_singletons(tmp_path)
    assert len(rows) == 1
    assert rows[0]['name'] == '(parse error)'
