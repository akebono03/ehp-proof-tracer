from pathlib import Path
import pytest
from phase165_r14_r27_scope_delta import (
    inspect_scope_context, conditional_exactness_step, audit_r27
)

def test_absent_context_does_not_approve_n1():
    e=inspect_scope_context(None)
    assert not e.explicit_n1_permitted

def test_missing_tex_fails(tmp_path):
    with pytest.raises(FileNotFoundError):
        inspect_scope_context(tmp_path/"missing.tex")

def test_detect_explicit_exclusion_in_context(tmp_path):
    text=r"Assume n\geq 2. "+r"\begin{proposition}[]\label{prop:4.2} exact \end{proposition}"
    path=tmp_path/"sample.tex"
    path.write_text(text,encoding="utf8")
    e=inspect_scope_context(path)
    assert e.explicit_n1_excluded and not e.explicit_n1_permitted

def test_conditional_step_requires_explicit_scope():
    assert conditional_exactness_step(False) is None

def test_explicit_conditional_premise_matches_target():
    step=conditional_exactness_step(True)
    assert step.conclusion.window.source_term.group_dimension==3
    assert step.conclusion.window.middle_term.group_dimension==1

def test_production_remains_fail_closed():
    r=audit_r27()
    assert not r["n1_scope_confirmed"]
    assert not r["production_delta_zero_proved"]
