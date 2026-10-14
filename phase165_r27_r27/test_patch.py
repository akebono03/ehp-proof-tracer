from pathlib import Path

import pytest

from apply import TARGETS, active_imports, apply


def test_r27_r27_targets_are_only_orphaned_upper_chain():
    assert TARGETS == (
        "toda_prop515_sigma_chain_bootstrap.py",
        "toda_prop515_low_bootstrap.py",
    )


def test_r27_r27_blocks_imports_without_deleting(tmp_path: Path):
    for name in TARGETS:
        (tmp_path / name).write_text("VALUE = 1\n", encoding="utf-8")
    (tmp_path / "consumer.py").write_text(
        "from toda_prop515_low_bootstrap import VALUE\n", encoding="utf-8"
    )
    assert active_imports(tmp_path)
    with pytest.raises(RuntimeError, match="Active imports"):
        apply(tmp_path)
    assert all((tmp_path / name).exists() for name in TARGETS)
    assert (tmp_path / "phase165_r27_r27_audit.json").exists()


def test_r27_r27_deletes_only_targets_and_creates_backup(tmp_path: Path):
    for name in TARGETS:
        (tmp_path / name).write_text("VALUE = 1\n", encoding="utf-8")
    (tmp_path / "unrelated.py").write_text("VALUE = 7\n", encoding="utf-8")
    result = apply(tmp_path)
    assert result["status"] == "REMOVED"
    assert set(result["deleted"]) == set(TARGETS)
    assert all(not (tmp_path / name).exists() for name in TARGETS)
    assert all((tmp_path / "phase165_r27_r27_removed_backup" / name).exists() for name in TARGETS)
    assert (tmp_path / "unrelated.py").read_text(encoding="utf-8") == "VALUE = 7\n"


def test_r27_r27_reinstall_is_idempotent(tmp_path: Path):
    (tmp_path / TARGETS[0]).write_text("VALUE = 2\n", encoding="utf-8")
    apply(tmp_path)
    result = apply(tmp_path)
    assert result["status"] == "ALREADY_REMOVED"
    assert result["deleted"] == []


def test_r27_r27_supports_plain_import_syntax(tmp_path: Path):
    (tmp_path / "consumer.py").write_text(
        "import toda_prop515_sigma_chain_bootstrap as legacy\n", encoding="utf-8"
    )
    found = active_imports(tmp_path)
    assert len(found) == 1
    assert found[0]["module"] == "toda_prop515_sigma_chain_bootstrap"


def test_r27_r27_production_modules_do_not_depend_on_removed_chain():
    root = Path(__file__).resolve().parent.parent
    assert active_imports(root) == []
