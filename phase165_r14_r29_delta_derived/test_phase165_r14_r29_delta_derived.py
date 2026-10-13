from pathlib import Path
import pytest

from phase165_r14_r29_delta_derived import (
    Prop42ApplicationPolicy, derive_adopted_tex_delta_zero, audit_r29,
)
from phase165_r14_r24_delta_connection import pi32_delta_goal
from proof import ProofRule

TEX = Path(__file__).with_name("toda_51_complete.tex")


def test_actual_r23_r26_steps_derive_delta_zero():
    iso, exactness, delta = derive_adopted_tex_delta_zero(
        TEX, Prop42ApplicationPolicy(True),
    )
    assert iso.rule is ProofRule.INFERENCE
    assert exactness.rule is ProofRule.GIVEN
    assert delta.rule is ProofRule.INFERENCE
    assert delta.conclusion == pi32_delta_goal()
    assert len(delta.premises) == 2


def test_scope_policy_is_mandatory():
    with pytest.raises(ValueError, match="not accepted"):
        derive_adopted_tex_delta_zero(TEX, Prop42ApplicationPolicy())


def test_explicit_chapter_exclusion_blocks_derivation():
    with pytest.raises(ValueError, match="excluded"):
        derive_adopted_tex_delta_zero(TEX, Prop42ApplicationPolicy(True, True))


def test_wrong_policy_rejected():
    with pytest.raises(TypeError):
        derive_adopted_tex_delta_zero(TEX, None)


def test_missing_toda51_source_fails():
    with pytest.raises(FileNotFoundError):
        derive_adopted_tex_delta_zero(
            TEX.parent / "absent.tex", Prop42ApplicationPolicy(True),
        )


def test_audit_reports_scope_and_citation_boundaries():
    result = audit_r29(TEX)
    assert result["delta_zero_proof_step_created"]
    assert result["delta_premise_count"] == 2
    assert not result["strict_registry_citation_approved"]
    assert not result["pi32_proved"]
