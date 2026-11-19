"""Focused tests for R13R8 read-only source diagnostic."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from audit import collect, inspect_module


def test_inspect_module_tracks_crlf_and_lf(tmp_path: Path) -> None:
    target = tmp_path / 'sample.py'
    target.write_bytes(b'def example():\r\n    return 1\n')
    record = inspect_module(target)
    assert record['crlf'] == 1
    assert record['bare_lf'] == 1
    assert record['functions'] == ['example']


def test_collect_reports_missing_sources(tmp_path: Path) -> None:
    record = collect(tmp_path)
    assert 'phase168_r3_3_proof_narrative_model.py' in record['missing']
    assert record['gate'] == 'SOURCE_OR_PIPELINE_GAP'


def test_diagnostic_never_writes_to_repo(tmp_path: Path) -> None:
    before = tuple(tmp_path.iterdir())
    collect(tmp_path)
    assert tuple(tmp_path.iterdir()) == before
