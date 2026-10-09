from pathlib import Path

from phase163_r4_r2_coverage_audit import inspect_source, scan_root, summarize


def test_detects_typed_statement_and_definition_classes(tmp_path: Path) -> None:
    source = tmp_path / 'math_model.py'
    source.write_text('class ExampleStatement:\n    pass\nclass ExampleDefinition:\n    pass\n', encoding='utf-8')
    rows = inspect_source(source, tmp_path)
    assert {r['symbol'] for r in rows} == {'ExampleStatement', 'ExampleDefinition'}
    assert all(r['kind'] == 'statement_or_definition_class' for r in rows)


def test_constructor_site_preserves_explicit_key(tmp_path: Path) -> None:
    source = tmp_path / 'facts.py'
    source.write_text("entry = ProofRepositoryEntry(key='known', step=step)\n", encoding='utf-8')
    rows = inspect_source(source, tmp_path)
    assert len(rows) == 1
    assert rows[0]['explicit_key'] == 'known'
    assert rows[0]['mapping_status'] == 'not_verified'


def test_excludes_phase_and_test_files_from_active_root(tmp_path: Path) -> None:
    for filename in ('active.py', 'phase163_sample.py', 'test_sample.py'):
        (tmp_path / filename).write_text('class AStatement:\n    pass\n', encoding='utf-8')
    rows, errors = scan_root(tmp_path)
    assert errors == []
    assert [row['file'] for row in rows] == ['active.py']


def test_invalid_python_is_reported_not_silently_ignored(tmp_path: Path) -> None:
    (tmp_path / 'broken.py').write_text('def broken(:\n', encoding='utf-8')
    rows, errors = scan_root(tmp_path)
    assert rows == []
    assert len(errors) == 1
    assert 'broken.py' in errors[0]


def test_counts_are_candidate_sites_not_mathematical_identities(tmp_path: Path) -> None:
    (tmp_path / 'active.py').write_text(
        'class AStatement:\n    pass\n\n'
        'first = ProofRepositoryEntry(key="a", step=s)\n'
        'second = ProofRepositoryEntry(key="a", step=s)\n', encoding='utf-8')
    rows, errors = scan_root(tmp_path)
    assert not errors
    counts = summarize(rows)
    assert counts['entry_constructor_site'] == 2
    assert counts['statement_or_definition_class'] == 1
