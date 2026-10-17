from pathlib import Path

import pytest

from install import FUNCTION, install


BASE = """from dataclasses import dataclass
@dataclass(frozen=True)
class InjectiveMapStatement:
    map: object
@dataclass(frozen=True)
class SurjectiveMapStatement:
    map: object
@dataclass(frozen=True)
class IsomorphismStatement:
    map: object
"""


def test_install_adds_one_complete_function(tmp_path: Path):
    target = tmp_path / "map_property_rules.py"
    target.write_text(BASE, encoding="utf-8")
    assert install(target) == "INSTALLED"
    assert target.read_text(encoding="utf-8").count("def " + FUNCTION) == 1


def test_install_idempotent(tmp_path: Path):
    target = tmp_path / "map_property_rules.py"
    target.write_text(BASE, encoding="utf-8")
    assert install(target) == "INSTALLED"
    once = target.read_text(encoding="utf-8")
    assert install(target) == "ALREADY_INSTALLED"
    assert target.read_text(encoding="utf-8") == once


def test_missing_previous_stage_fails_closed(tmp_path: Path):
    target = tmp_path / "map_property_rules.py"
    target.write_text("class InjectiveMapStatement: pass\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="SurjectiveMapStatement"):
        install(target)
    assert target.read_text(encoding="utf-8") == "class InjectiveMapStatement: pass\n"


def test_backup_keeps_preinstall_content(tmp_path: Path):
    target = tmp_path / "map_property_rules.py"
    target.write_text(BASE, encoding="utf-8")
    install(target)
    assert (tmp_path / "map_property_rules.py.phase165_r4_r4_stage5_before.bak").read_text(encoding="utf-8") == BASE
