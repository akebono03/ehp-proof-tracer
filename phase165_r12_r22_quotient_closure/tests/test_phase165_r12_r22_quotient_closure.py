"""R12-R22 small regression tests. No fabricated literature source."""
from __future__ import annotations

import pytest
from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from phase165_r12_r22_quotient_closure import (
    source_structure_from_proven_relation, proof_ancestors,
)
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from proof import InferenceRule, ProofRule, ProofStep, Relation
from toda_rules import toda_eta_family_definition_statement


def test_source_structure_is_inference_with_original_ancestor():
    source = TodaPrimaryGroup(3, 2)
    eta = toda_eta_family_definition_statement(2).element
    root = ProofStep(conclusion=Relation(source, FreeCyclicGroup(eta)), premises=(),
                     rule=ProofRule.GIVEN, inference_rule=InferenceRule(name="test fixture only"))
    derived = source_structure_from_proven_relation(root)
    assert derived.conclusion == CyclicStructureStatement(source, eta, None)
    assert derived.rule is ProofRule.INFERENCE
    assert proof_ancestors(derived, (root,))


def test_nonfree_structure_rejected():
    source = TodaPrimaryGroup(3, 2)
    root = ProofStep(conclusion=source, premises=(), rule=ProofRule.GIVEN)
    with pytest.raises(ValueError):
        source_structure_from_proven_relation(root)


def test_ancestry_rejects_missing_witness():
    source = TodaPrimaryGroup(3, 2)
    root = ProofStep(conclusion=source, premises=(), rule=ProofRule.GIVEN)
    missing = ProofStep(conclusion=TodaPrimaryGroup(4, 3), premises=(), rule=ProofRule.GIVEN)
    assert not proof_ancestors(root, (missing,))
