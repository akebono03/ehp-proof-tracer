from pathlib import Path
import ast
import pytest
from install import install

BASE = """from dataclasses import dataclass
from expression import MapSymbol
from proof import InferenceRule, PremisePattern
@dataclass(frozen=True)
class InjectiveMapStatement:
    map: MapSymbol
@dataclass(frozen=True)
class IsomorphismStatement:
    map: MapSymbol
def isomorphism_implies_injective_inference_rule():
    return None
"""


def test_install_and_idempotence(tmp_path):
    (tmp_path / "map_property_rules.py").write_text(BASE, encoding="utf-8")
    assert install(tmp_path) == "INSTALLED"
    assert install(tmp_path) == "ALREADY_INSTALLED"


def test_syntax_after_install(tmp_path):
    path = tmp_path / "map_property_rules.py"
    path.write_text(BASE, encoding="utf-8")
    install(tmp_path)
    ast.parse(path.read_text(encoding="utf-8"))


def test_backup_created(tmp_path):
    (tmp_path / "map_property_rules.py").write_text(BASE, encoding="utf-8")
    install(tmp_path)
    assert (tmp_path / "map_property_rules.py.r4_r4_stage2_before.bak").read_text(encoding="utf-8") == BASE


def test_refuses_partial_install(tmp_path):
    path = tmp_path / "map_property_rules.py"
    path.write_text(BASE + "\ndef kernel_zero_implies_injective_inference_rule():\n    pass\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="partial"):
        install(tmp_path)


def test_refuses_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        install(tmp_path)
