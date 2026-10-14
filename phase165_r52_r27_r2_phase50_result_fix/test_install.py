"""R27-R2 focused tests for the replacement and shape validation."""
import ast
from pathlib import Path

from install import OLD, NEW, function_node, install


def fixture_source() -> str:
    return (
        "def build_toda_52_composition_isomorphism_step():\n"
        "  phase50 = _build_phase50_result()\n"
        "  eta2_definition_steps = tuple(\n"
        '    step for step in phase50["premise_steps"]\n'
        "    if isinstance(step.conclusion, TodaPi32Eta2DefinitionStatement)\n"
        "  )\n"
        "  return eta2_definition_steps\n"
    )


def test_replacement_compiles():
    before = fixture_source()
    after = before.replace(OLD, NEW)
    ast.parse(after)
    assert NEW in after
    assert OLD not in after


def test_installer_is_idempotent(tmp_path: Path):
    target = tmp_path / "toda_upstream_bootstrap.py"
    target.write_text(fixture_source(), encoding="utf-8")
    assert install(tmp_path)["status"] == "INSTALLED"
    assert install(tmp_path)["status"] == "ALREADY_INSTALLED"
    assert NEW in target.read_text(encoding="utf-8")


def test_unexpected_shape_rejected(tmp_path: Path):
    target = tmp_path / "toda_upstream_bootstrap.py"
    target.write_text(fixture_source().replace(OLD, 'for step in phase50["other"]'), encoding="utf-8")
    try:
        install(tmp_path)
    except RuntimeError:
        pass
    else:
        raise AssertionError("Guard did not reject unexpected shape")
    assert "other" in target.read_text(encoding="utf-8")


def test_return_shape_is_accessible_from_phase50():
    text = Path(__file__).with_name("install.py").read_text(encoding="utf-8")
    assert 'phase50["result"].steps' in text
    assert "create_legacy_given_proof_step" not in text
