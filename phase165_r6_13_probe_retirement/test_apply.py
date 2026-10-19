import ast
from pathlib import Path

from apply import prepare_consumer, dependencies


def test_prepare_consumer_preserves_builder_and_creates_local_helper():
    old = 'from probes.probe_phase49_capabilities import (\n  print_separator,\n)\n\ndef build_phase58_representative_result():\n  return 42\n'
    new = prepare_consumer(old)
    tree = ast.parse(new)
    assert 'probes.probe_phase49_capabilities' not in new
    assert any(isinstance(node, ast.FunctionDef) and node.name == 'print_separator' for node in tree.body)
    assert 'def build_phase58_representative_result():\n  return 42' in new


def test_dependencies_finds_external_import(tmp_path: Path):
    (tmp_path / 'tests').mkdir()
    (tmp_path / 'probes').mkdir()
    (tmp_path / 'tests' / 'test_x.py').write_text('from probes.probe_phase56_capabilities import main\n')
    hits = dependencies(tmp_path)
    assert len(hits) == 1
    assert hits[0]['path'] == 'tests/test_x.py'
