from dataclasses import replace
from pathlib import Path

import pytest

from phase165_r14_r29_delta_derived import Prop42ApplicationPolicy
from phase165_r14_r30_hopf_surjective import derive_adopted_tex_hopf_surjectivity
from phase165_r14_r31_hopf_injective import derive_adopted_tex_hopf_injectivity
from phase165_r14_r32_hopf_isomorphism import (
    derive_hopf_isomorphism_from_steps,
    derive_adopted_tex_hopf_isomorphism,
    audit_r32,
)
from phase165_r14_r6_generic_iso import MapIsomorphism
from proof import ProofRule

TEX = Path(__file__).with_name("toda_51_complete.tex")
POLICY = Prop42ApplicationPolicy(use_unrestricted_statement_as_written=True)


def test_existing_branches_derive_same_hopf_map():
    _, _, _, _, surj = derive_adopted_tex_hopf_surjectivity(TEX, POLICY)
    _, _, inj = derive_adopted_tex_hopf_injectivity(TEX, POLICY)
    assert inj.conclusion.map == surj.conclusion.map


def test_generic_inference_derives_hopf_isomorphism():
    inj, surj, iso = derive_adopted_tex_hopf_isomorphism(TEX, POLICY)
    assert iso.conclusion == MapIsomorphism(inj.conclusion.map)
    assert iso.rule is ProofRule.INFERENCE
    assert iso.premises == (inj, surj)


def test_swapped_premises_rejected():
    inj, surj, _ = derive_adopted_tex_hopf_isomorphism(TEX, POLICY)
    with pytest.raises(ValueError):
        derive_hopf_isomorphism_from_steps(surj, inj)


def test_incorrect_second_map_rejected():
    inj, surj, _ = derive_adopted_tex_hopf_isomorphism(TEX, POLICY)
    bad_surj = replace(surj, conclusion=replace(surj.conclusion, map=object()))
    with pytest.raises(ValueError):
        derive_hopf_isomorphism_from_steps(inj, bad_surj)


def test_unapproved_scope_rejected():
    with pytest.raises(ValueError):
        derive_adopted_tex_hopf_isomorphism(
            TEX, Prop42ApplicationPolicy(),
        )


def test_chapter_exclusion_rejected():
    with pytest.raises(ValueError):
        derive_adopted_tex_hopf_isomorphism(
            TEX, Prop42ApplicationPolicy(
                use_unrestricted_statement_as_written=True,
                chapter_wide_exclusion_found=True,
            ),
        )


def test_audit_has_no_claim_of_final_proof():
    report = audit_r32(TEX)
    assert report["hopf_isomorphism_proof_step_created"]
    assert report["hopf_isomorphism_premises"] == 2
    assert not report["strict_registry_citation_approved"]
    assert not report["pi32_proved"]
