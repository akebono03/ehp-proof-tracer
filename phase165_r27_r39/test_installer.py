from pathlib import Path
import ast
import tempfile
import pytest

from apply import MODULE, rewrite_imports, plan


def test_extracts_function_without_removing_other_type_imports():
    source = "from repository_element_presentation import (\n    render_repository_conclusion_latex,\n    RepositoryGeneratorOccurrencePresentation,\n)\n"
    result, changed = rewrite_imports(source)
    assert changed
    assert f"from {MODULE} import render_repository_conclusion_latex" in result
    assert "from repository_element_presentation import RepositoryGeneratorOccurrencePresentation" in result
    ast.parse(result)


def test_unrelated_import_is_preserved():
    source = "from repository_element_presentation import RepositoryGeneratorOccurrencePresentation\n"
    assert rewrite_imports(source) == (source, False)


def test_aliased_import_is_preserved():
    source = "from repository_element_presentation import render_repository_conclusion_latex as render\n"
    output, changed = rewrite_imports(source)
    assert changed
    assert f"from {MODULE} import render_repository_conclusion_latex as render" in output


def test_new_module_source_is_syntax_valid():
    source = (Path(__file__).parent / f"{MODULE}.py").read_text(encoding="utf-8")
    ast.parse(source)
    assert "from repository_element_" not in source


def test_plan_reports_missing_optional_targets():
    source = (Path(__file__).parent / f"{MODULE}.py").read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "repository_element_presentation.py").write_text("pass\n", encoding="utf-8")
        p = plan(root, source)
        assert p["new_module"]
        assert not p["modified"]
        assert p["skipped"]


def test_plan_rejects_renderer_conflicts():
    source = (Path(__file__).parent / f"{MODULE}.py").read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "repository_element_presentation.py").write_text("pass\n", encoding="utf-8")
        (root / f"{MODULE}.py").write_text("pass\n", encoding="utf-8")
        with pytest.raises(RuntimeError, match="different shared renderer"):
            plan(root, source)
