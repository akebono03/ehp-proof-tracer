from pathlib import Path
from audit import active_python_sources, audit


def test_active_python_sources_excludes_historical_packages(tmp_path: Path):
    (tmp_path / 'active.py').write_text('x = 1\n', encoding='utf-8')
    (tmp_path / 'historical').mkdir()
    (tmp_path / 'historical' / 'broken.py').write_text('def (\n', encoding='utf-8')
    (tmp_path / 'probes').mkdir()
    (tmp_path / 'probes' / 'sample.py').write_text('x = 1\n', encoding='utf-8')
    assert {p.relative_to(tmp_path).as_posix() for p in active_python_sources(tmp_path)} == {'active.py', 'probes/sample.py'}


def test_audit_detects_legacy_import_without_mutation(tmp_path: Path):
    (tmp_path / 'tests').mkdir()
    path = tmp_path / 'tests' / 'test_consumer.py'
    source = 'from probes.probe_phase49_capabilities import print_separator\n'
    path.write_text(source, encoding='utf-8')
    report = audit(tmp_path)
    assert report['status'] == 'AUDITED_NO_CHANGES'
    assert report['references'][0]['names'] == ['print_separator']
    assert path.read_text(encoding='utf-8') == source
