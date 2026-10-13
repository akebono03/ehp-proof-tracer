from pathlib import Path
import pytest
from phase165_r14_r28_scope_review import find_toda_tex, proposition_context


def test_missing_file_is_unverified(tmp_path):
    assert find_toda_tex(tmp_path) is None
    assert not proposition_context(None).n1_applicability_certified


def test_reads_normal_tex(tmp_path):
    path = tmp_path / "Toda_01.tex"
    path.write_text(r"Assume n\geq 2. \begin{proposition}[]\label{prop:4.2} exact \end{proposition}", encoding="utf8")
    ctx = proposition_context(path)
    assert ctx.found and ctx.n_ge_2_text_detected
    assert not ctx.n1_applicability_certified
    assert find_toda_tex(tmp_path) == path


def test_doubled_escape_fixture_is_readable(tmp_path):
    path = tmp_path / "sample.tex"
    path.write_text(r"Assume n\\geq 2. \\begin{proposition}[]\\label{prop:4.2} exact \\end{proposition}", encoding="utf8")
    ctx = proposition_context(path)
    assert ctx.found and ctx.n_ge_2_text_detected


def test_no_context_does_not_certify_n1(tmp_path):
    path = tmp_path / "sample.tex"
    path.write_text(r"\begin{proposition}[]\label{prop:4.2} exact \end{proposition}", encoding="utf8")
    ctx = proposition_context(path)
    assert ctx.found and not ctx.n1_applicability_certified


def test_positive_text_is_not_certification(tmp_path):
    path = tmp_path / "sample.tex"
    path.write_text(r"Assume n\geq 1. \begin{proposition}[]\label{prop:4.2} exact \end{proposition}", encoding="utf8")
    ctx = proposition_context(path)
    assert ctx.n_ge_1_text_detected
    assert not ctx.n1_applicability_certified


def test_malformed_environment_rejected(tmp_path):
    path = tmp_path / "sample.tex"
    path.write_text(r"\begin{proposition}[]\label{prop:4.2} exact", encoding="utf8")
    with pytest.raises(ValueError, match="closing"):
        proposition_context(path)
