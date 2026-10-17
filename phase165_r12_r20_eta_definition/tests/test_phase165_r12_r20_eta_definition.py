from pathlib import Path
import pytest
from phase165_r12_r20_eta_definition import (TodaEtaFamilyGeneralDefinition, build_cited_eta_family_definition,
    expand_cited_eta_definition)
from toda_rules import toda_eta_family_definition_statement
from proof import ProofRule

def test_source_registration_and_citation():
    bridge = build_cited_eta_family_definition(Path("sources/toda/Toda_05_2.tex"))
    assert len(bridge.proof_links)==1
    assert bridge.proof_links[0].step.rule is ProofRule.GIVEN
    assert isinstance(bridge.proof_links[0].step.conclusion, TodaEtaFamilyGeneralDefinition)

def test_general_specialization_multiple_indices():
    available = (TodaEtaFamilyGeneralDefinition(),)
    for n in (2,3,4,8):
        goal = toda_eta_family_definition_statement(n)
        choices = expand_cited_eta_definition(goal, available)
        assert len(choices)==1 and choices[0].subgoals==available

def test_missing_source_does_not_specialize():
    assert expand_cited_eta_definition(toda_eta_family_definition_statement(3), ()) == ()

def test_invalid_source_is_rejected(tmp_path):
    f=tmp_path / "invalid.tex"
    f.write_text("eta", encoding="utf8")
    with pytest.raises(ValueError):
        build_cited_eta_family_definition(f)
