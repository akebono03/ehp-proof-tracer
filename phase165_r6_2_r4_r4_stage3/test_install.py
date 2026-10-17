from pathlib import Path
import pytest
from install import install, NAMES


def test_install_requires_stage2(tmp_path):
    (tmp_path / "map_property_rules.py").write_text("class Dummy: pass\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="prerequisite"):
        install(tmp_path)


def test_install_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        install(tmp_path)


def test_install_refuses_partial(tmp_path):
    src = "\n".join("class " + name + ": pass" for name in (
        "KernelZeroStatement", "ImageWholeStatement", "SurjectiveMapStatement"))
    src += "\ndef kernel_zero_implies_injective_inference_rule(): pass\n"
    src += "def whole_image_implies_surjective_inference_rule(): pass\n"
    src += "class ImageZeroStatement: pass\n"
    path = tmp_path / "map_property_rules.py"
    path.write_text(src, encoding="utf-8")
    with pytest.raises(RuntimeError, match="partial"):
        install(tmp_path)
    assert path.read_text(encoding="utf-8") == src


def test_install_is_idempotent(tmp_path):
    src = "\n".join("class " + name + ": pass" for name in (
        "KernelZeroStatement", "ImageWholeStatement", "SurjectiveMapStatement"))
    src += "\ndef kernel_zero_implies_injective_inference_rule(): pass\n"
    src += "def whole_image_implies_surjective_inference_rule(): pass\n"
    path = tmp_path / "map_property_rules.py"
    path.write_text(src, encoding="utf-8")
    assert install(tmp_path) == "INSTALLED"
    assert install(tmp_path) == "ALREADY_INSTALLED"
    updated = path.read_text(encoding="utf-8")
    assert all(name in updated for name in NAMES)
    assert path.with_name("map_property_rules.py.r4_r4_stage3_before.bak").exists()
