"""Focused non-regression checks for actual evidence-to-renderer bridge."""
from __future__ import annotations

from phase165_r12_r23_public_narrative import fixed_reference_locators, proof_nodes
from proof import ProofRule, ProofStep, InferenceRule, LiteratureReference


def test_proof_nodes_preserve_identity_without_duplication():
    leaf = ProofStep(conclusion='source', premises=(), rule=ProofRule.GIVEN)
    root = ProofStep(conclusion='root', premises=(leaf, leaf), rule=ProofRule.INFERENCE)
    steps = proof_nodes(root)
    assert steps == (leaf, root)
    assert steps[0] is leaf and steps[1] is root


def test_fixed_reference_locators_only_use_cited_given():
    leaf = ProofStep(
        conclusion='source', premises=(), rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(
            name='cited source', literature_reference=LiteratureReference(label='Toda', locator='(5.1)'),
        ),
    )
    root = ProofStep(conclusion='root', premises=(leaf,), rule=ProofRule.INFERENCE)
    assert fixed_reference_locators(root) == ('(5.1)',)


def test_no_invented_reference_for_uncited_given():
    step = ProofStep(conclusion='unknown', premises=(), rule=ProofRule.GIVEN)
    assert fixed_reference_locators(step) == ()
