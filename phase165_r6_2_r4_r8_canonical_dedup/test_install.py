from pathlib import Path
import ast

PACKAGE = Path(__file__).resolve().parent


def test_helper_syntax():
    ast.parse((PACKAGE / "phase165_r6_2_r4_r8_dedup.py").read_text(encoding="utf-8"))


def test_installer_syntax():
    ast.parse((PACKAGE / "install.py").read_text(encoding="utf-8"))


def test_anchor_guard_present():
    source = (PACKAGE / "install.py").read_text(encoding="utf-8")
    assert "source.count(OLD) != 1" in source
    assert "backup.write_bytes(data)" in source


def test_no_group_target_or_adapter():
    src = (PACKAGE / "phase165_r6_2_r4_r8_dedup.py").read_text(encoding="utf-8")
    assert "pi43" not in src
    assert "existing_pi43" not in src
