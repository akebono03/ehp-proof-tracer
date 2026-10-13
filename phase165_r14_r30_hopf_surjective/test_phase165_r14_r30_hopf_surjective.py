from pathlib import Path
import pytest
from dataclasses import replace

from phase165_r14_r29_delta_derived import (
    Prop42ApplicationPolicy, derive_adopted_tex_delta_zero,
)
from phase165_r14_r30_hopf_surjective import (
    pi32_hopf_surjectivity_goal, prop42_h_delta_exactness_step,
    derive_hopf_surjectivity_from_steps,
    derive_adopted_tex_hopf_surjectivity, audit_r30,
)
from homotopy_groups import TodaPrimaryGroup
from proof import ProofRule

TEX = Path(__file__).with_name("toda_51_complete.tex")
POLICY = Prop42ApplicationPolicy(use_unrestricted_statement_as_written=True)


def test_h_delta_window_is_correct():
    w = prop42_h_delta_exactness_step(POLICY).conclusion.window
    assert w.source_term == TodaPrimaryGroup(3, 2)
    assert w.middle_term == TodaPrimaryGroup(3, 3)
    assert w.target_term == TodaPrimaryGroup(1, 1)


def test_scope_policy_required():
    with pytest.raises(ValueError):
        prop42_h_delta_exactness_step(Prop42ApplicationPolicy())


def test_exclusion_blocks_exactness():
    with pytest.raises(ValueError):
        prop42_h_delta_exactness_step(Prop42ApplicationPolicy(
            use_unrestricted_statement_as_written=True,
            chapter_wide_exclusion_found=True,
        ))


def test_existing_inference_derives_surjectivity():
    _, _, delta = derive_adopted_tex_delta_zero(TEX, POLICY)
    exactness = prop42_h_delta_exactness_step(POLICY)
    derived = derive_hopf_surjectivity_from_steps(delta, exactness)
    assert derived.conclusion == pi32_hopf_surjectivity_goal()
    assert derived.rule is ProofRule.INFERENCE
    assert len(derived.premises) == 2


def test_wrong_window_rejected():
    _, delta_e, delta = derive_adopted_tex_delta_zero(TEX, POLICY)
    with pytest.raises(ValueError, match="do not match"):
        derive_hopf_surjectivity_from_steps(delta, delta_e)


def test_full_adopted_tex_chain():
    result = derive_adopted_tex_hopf_surjectivity(TEX, POLICY)
    assert result[4].conclusion == pi32_hopf_surjectivity_goal()
    assert result[2] in result[4].premises


def test_audit_keeps_strict_boundary():
    report = audit_r30(TEX)
    assert report["h_surjective_proof_step_created"]
    assert not report["strict_registry_citation_approved"]
    assert not report["pi32_proved"]
