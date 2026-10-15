"""Read-only R1 audit tests; fixtures do not certify application mathematics."""
from pathlib import Path

import pytest

from audit import gather, is_production_path, parse_file, report_markdown


def test_r1_detects_duplicate_top_level_functions(tmp_path: Path) -> None:
    path = tmp_path / "web_group_proof.py"
    path.write_text("def render_partial_proof_markdown():\n    return 1\n\ndef render_partial_proof_markdown():\n    return 2\n", encoding="utf-8")
    result = gather(tmp_path)
    assert any(x["name"] == "render_partial_proof_markdown" for x in result["duplicate_production_functions"])


def test_r1_finds_legacy_imports_and_routes(tmp_path: Path) -> None:
    (tmp_path / "web_group_proof.py").write_text(
        "from toda_group_proof_generic_narrative_renderer import render_toda_partial_proof_narrative_markdown\n"
        "def build_standard_web_group_proof_view():\n    return render_toda_partial_proof_narrative_markdown(None)\n", encoding="utf-8")
    result = gather(tmp_path)
    assert result["counts"]["legacy_imports"] == 1
    assert result["public_route_definitions"]["build_standard_web_group_proof_view"]


def test_r1_reads_compatibility_package_without_mutating(tmp_path: Path) -> None:
    (tmp_path / "web_group_proof.py").write_text("pass\n", encoding="utf-8")
    package = tmp_path / "toda_group_proof_generic_narrative_renderer"
    package.mkdir()
    file = package / "__init__.py"
    file.write_text("from x import y\n", encoding="utf-8")
    before = file.read_bytes()
    result = gather(tmp_path)
    assert result["focus_exists"]["toda_group_proof_generic_narrative_renderer/__init__.py"] is True
    assert file.read_bytes() == before


def test_r1_excludes_archived_and_phase_installers_from_production(tmp_path: Path) -> None:
    assert not is_production_path(Path("archive/old.py"))
    assert not is_production_path(Path("phase165_r57_r21/install.py"))
    assert not is_production_path(Path("test_renderer.py"))
    assert is_production_path(Path("toda_group_proof_narrative_renderer.py"))


def test_r1_nested_definitions_do_not_count_as_top_level_duplicates(tmp_path: Path) -> None:
    path = tmp_path / "nested.py"
    path.write_text("def outer():\n    def helper():\n        return 1\n    return helper()\n", encoding="utf-8")
    result = parse_file(path, Path("nested.py"))
    assert result["duplicate_top_level_functions"] == []


def test_r1_report_is_readable_with_no_legacy_imports(tmp_path: Path) -> None:
    (tmp_path / "web_group_proof.py").write_text("def root():\n    return None\n", encoding="utf-8")
    result = gather(tmp_path)
    text = report_markdown(result)
    assert "Phase 165 Renderer R1" in text
    assert "R1 ではコードを変更しない" in text


def test_r1_rejects_wrong_project_root(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        gather(tmp_path)
