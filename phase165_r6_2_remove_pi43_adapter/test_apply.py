from pathlib import Path
import ast
import pytest
from apply import transform, install


def sample() -> str:
    return '''from phase165_r52_r23_existing_rule_adapter import expand_existing_pi43_rules

def shared_expansion_provider(bridge):
    def expand(goal):
        for provider in (
            common_provider,
            expand_existing_pi43_rules,
        ):
            provider(goal)
        return ()
    return expand
'''


def test_transform_removes_only_dedicated_path():
    result = transform(sample())
    ast.parse(result)
    assert "common_provider," in result
    assert "expand_existing_pi43_rules" not in result
    assert "phase165_r52_r23_existing_rule_adapter" not in result


def test_unknown_import_guard():
    with pytest.raises(ValueError):
        transform(sample().replace("import expand_existing_pi43_rules", "import another"))


def test_duplicate_reference_guard():
    with pytest.raises(ValueError):
        transform(sample().replace("            expand_existing_pi43_rules,", "            expand_existing_pi43_rules,\n            expand_existing_pi43_rules,"))


def test_missing_path_changes_nothing(tmp_path: Path):
    target = tmp_path / "phase165_r52_r9_shared_math.py"
    target.write_text(sample(), encoding="utf-8")
    with pytest.raises(FileNotFoundError):
        install(tmp_path)
    assert target.read_text(encoding="utf-8") == sample()


def test_install_quarantines_and_backs_up(tmp_path: Path):
    target = tmp_path / "phase165_r52_r9_shared_math.py"
    target.write_text(sample(), encoding="utf-8")
    adapter = tmp_path / "phase165_r52_r23_existing_rule_adapter.py"
    adapter.write_text("pass\n", encoding="utf-8")
    out = install(tmp_path)
    assert out["status"] == "REMOVED_FROM_PRODUCTION"
    assert not adapter.exists()
    assert (tmp_path / "phase165_r52_r23_existing_rule_adapter.py.r6_2_removed.bak").exists()
    assert (tmp_path / "phase165_r52_r9_shared_math.py.r6_2_remove_pi43_before.bak").read_text(encoding="utf-8") == sample()
    assert "expand_existing_pi43_rules" not in target.read_text(encoding="utf-8")


def test_reinstall_refuses_without_mutation(tmp_path: Path):
    target = tmp_path / "phase165_r52_r9_shared_math.py"
    target.write_text(sample(), encoding="utf-8")
    adapter = tmp_path / "phase165_r52_r23_existing_rule_adapter.py"
    adapter.write_text("pass", encoding="utf-8")
    install(tmp_path)
    before = target.read_bytes()
    with pytest.raises(FileNotFoundError):
        install(tmp_path)
    assert target.read_bytes() == before
