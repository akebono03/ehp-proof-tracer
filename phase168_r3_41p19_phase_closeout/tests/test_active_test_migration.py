"""R3-41P19 closeout migration: retain archived tests and restore exact bytes."""
from __future__ import annotations

import pytest

from phase168_r3_41p19_phase_closeout import active_tests


def _fixture(tmp_path, monkeypatch, *, eol):
    root = tmp_path / "repo"
    (root / "tests").mkdir(parents=True)
    historical = (
        root / "phase165_r6_audit_results" / "retired_phase144_tests"
        / "20261019T070710Z"
    )
    historical.mkdir(parents=True)
    output = root / "phase168_r3_41p19_phase_closeout" / "output"
    output.mkdir(parents=True)
    baseline = {}
    for name in active_tests.REPLACEMENTS:
        text = (active_tests.FILES / (name + ".BEFORE.py")).read_text(encoding="utf-8")
        data = text.replace("\n", eol).encode("utf-8")
        (root / "tests" / name).write_bytes(data)
        baseline[name] = data
    for name in active_tests.RETIRED:
        data = ("# archived duplicate: " + name + "\n").replace("\n", eol).encode("utf-8")
        (root / "tests" / name).write_bytes(data)
        (historical / name).write_bytes(data)
        baseline[name] = data
    monkeypatch.setattr(active_tests, "ROOT", root)
    monkeypatch.setattr(active_tests, "OUTPUT", output)
    monkeypatch.setattr(active_tests, "MANIFEST", output / "active_tests_manifest.json")
    monkeypatch.setattr(active_tests, "ARCHIVE", historical)
    return root, baseline


@pytest.mark.parametrize("eol", ["\n", "\r\n"])
def test_migrate_restore_and_retry_without_losing_historical_tests(tmp_path, monkeypatch, eol):
    root, baseline = _fixture(tmp_path, monkeypatch, eol=eol)
    for _ in range(2):
        active_tests.install()
        for name in active_tests.REPLACEMENTS:
            result = (root / "tests" / name).read_bytes()
            assert result != baseline[name]
            assert (b"\r\n" in result) is (eol == "\r\n")
        for name in active_tests.RETIRED:
            assert not (root / "tests" / name).exists()
            assert (active_tests.ARCHIVE / name).read_bytes() == baseline[name]
        active_tests.restore()
        for name, original in baseline.items():
            assert (root / "tests" / name).read_bytes() == original
        assert not active_tests.MANIFEST.exists()


def test_refuse_to_retire_when_historical_copy_differs(tmp_path, monkeypatch):
    root, baseline = _fixture(tmp_path, monkeypatch, eol="\n")
    name = active_tests.RETIRED[0]
    (active_tests.ARCHIVE / name).write_bytes(b"changed archive\n")
    with pytest.raises(RuntimeError, match="differs from archived byte-exact copy"):
        active_tests.install()
    assert not active_tests.MANIFEST.exists()
    for item, original in baseline.items():
        assert (root / "tests" / item).read_bytes() == original


def test_refuse_to_replace_modified_active_reference_test(tmp_path, monkeypatch):
    root, baseline = _fixture(tmp_path, monkeypatch, eol="\n")
    name = active_tests.REPLACEMENTS[0]
    changed = baseline[name] + b"\nnew_reference_semantics = True\n"
    (root / "tests" / name).write_bytes(changed)
    with pytest.raises(RuntimeError, match="differs from reviewed baseline"):
        active_tests.install()
    assert (root / "tests" / name).read_bytes() == changed
    assert not active_tests.MANIFEST.exists()


def test_refuse_to_restore_user_modified_test(tmp_path, monkeypatch):
    root, baseline = _fixture(tmp_path, monkeypatch, eol="\n")
    active_tests.install()
    name = active_tests.REPLACEMENTS[0]
    path = root / "tests" / name
    path.write_bytes(path.read_bytes() + b"\n# edit while installed\n")
    with pytest.raises(RuntimeError, match="changed after migration"):
        active_tests.restore()
    assert active_tests.MANIFEST.exists()
    assert not (root / "tests" / active_tests.RETIRED[0]).exists()
