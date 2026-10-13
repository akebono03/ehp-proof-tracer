from pathlib import Path
from dataclasses import replace
import pytest
from homotopy_groups import TodaPrimaryGroup
from proof import ProofRule
from phase165_r14_r29_delta_derived import Prop42ApplicationPolicy
from phase165_r14_r31_hopf_injective import (
    pi32_hopf_injective_goal,toda51_pi21_zero_step,
    prop42_e_h_exactness_step,derive_hopf_injectivity_from_steps,
    derive_adopted_tex_hopf_injectivity,audit_r31,
)
TEX=Path(__file__).with_name("toda_51_complete.tex")
POLICY=Prop42ApplicationPolicy(use_unrestricted_statement_as_written=True)

def test_toda51_pi21_zero_is_concrete():
    assert toda51_pi21_zero_step(TEX).conclusion.group==TodaPrimaryGroup(2,1)

def test_e_h_window_indices_are_exact():
    w=prop42_e_h_exactness_step(POLICY).conclusion.window
    assert (w.source_term,w.middle_term,w.target_term)==(
        TodaPrimaryGroup(2,1),TodaPrimaryGroup(3,2),TodaPrimaryGroup(3,3))

def test_missing_scope_policy_rejected():
    with pytest.raises(ValueError):
        prop42_e_h_exactness_step(Prop42ApplicationPolicy())

def test_explicit_exclusion_rejected():
    with pytest.raises(ValueError):
        prop42_e_h_exactness_step(Prop42ApplicationPolicy(
            use_unrestricted_statement_as_written=True,
            chapter_wide_exclusion_found=True))

def test_general_rule_derives_injectivity():
    zero,exact,injection=derive_adopted_tex_hopf_injectivity(TEX,POLICY)
    assert injection.conclusion==pi32_hopf_injective_goal()
    assert injection.rule is ProofRule.INFERENCE
    assert injection.premises==(zero,exact)

def test_wrong_exactness_window_rejected():
    zero=toda51_pi21_zero_step(TEX)
    exact=prop42_e_h_exactness_step(POLICY)
    bad=replace(exact,conclusion=replace(exact.conclusion,
        window=replace(exact.conclusion.window,source_term=TodaPrimaryGroup(4,1))))
    with pytest.raises(ValueError,match="premises do not match"):
        derive_hopf_injectivity_from_steps(zero,bad)

def test_audit_preserves_unverified_boundary():
    r=audit_r31(TEX)
    assert r["hopf_injective_proof_step_created"]
    assert not r["strict_registry_citation_approved"]
    assert not r["pi32_proved"]
