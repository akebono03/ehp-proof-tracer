import pytest
from proof import FoundationalReferenceIdentity, ProofRule, ProofStep
from phase164_r8_proofstep_factory import (
    annotate_derived_reference_step,
    project_reference_component_step,
)


def test_reference_annotation_preserves_ancestry_and_rule():
    root = ProofStep(conclusion='given', premises=(), rule=ProofRule.GIVEN)
    derived = ProofStep(conclusion='derived', premises=(root,), rule=ProofRule.INFERENCE)
    ref = FoundationalReferenceIdentity(key='literature:test', label='Test')
    annotated = annotate_derived_reference_step(derived, ref)
    assert annotated is not derived
    assert annotated.premises[0] is root
    assert annotated.conclusion is derived.conclusion
    assert annotated.rule is ProofRule.INFERENCE
    assert annotated.foundational_reference is ref


def test_reference_annotation_rejects_wrong_rule_or_reference():
    given = ProofStep(conclusion='given', premises=(), rule=ProofRule.GIVEN)
    with pytest.raises(TypeError):
        annotate_derived_reference_step(given, FoundationalReferenceIdentity(key='a', label='A'))
    derived = ProofStep(conclusion='derived', premises=(given,), rule=ProofRule.INFERENCE)
    with pytest.raises(TypeError):
        annotate_derived_reference_step(derived, 'unauthenticated-string')


def test_display_projection_is_temporary_and_preserves_source_rule():
    given = ProofStep(conclusion='source', premises=(), rule=ProofRule.GIVEN, note='original')
    component = object()
    projected = project_reference_component_step(given, component)
    assert projected is not given
    assert projected.conclusion is component
    assert projected.rule is given.rule
    assert projected.note == given.note
    assert projected.premises == ()
    assert given.conclusion == 'source'


def test_display_projection_rejects_non_step():
    with pytest.raises(TypeError):
        project_reference_component_step(object(), object())
