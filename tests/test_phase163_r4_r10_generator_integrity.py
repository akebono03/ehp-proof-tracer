import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase163_r4_r10_generator_integrity import (
    ASSERTION_ID,
    CANONICAL_LATEX,
    verify_prop56_pi5_2_generator,
)
from phase163_r4_r7_representative_bindings import (
    WitnessCandidate,
    bind_representative_witnesses,
)
from phase163_r4_registry_bridge import build_registry_bridge
from proof import (
    FoundationalReferenceIdentity,
    InferenceRule,
    LiteratureReference,
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
)


def _citation(witness, locator, component, expected):
    identity = FoundationalReferenceIdentity(
        key=f"literature:{locator}:{component}", label=locator
    )
    leaf = ProofStep(
        conclusion=expected,
        premises=(),
        rule=ProofRule.GIVEN,
        foundational_reference=identity,
    )
    return ProofStep(
        conclusion=expected,
        premises=(leaf,),
        rule=ProofRule.INFERENCE,
        foundational_reference=identity,
        inference_rule=InferenceRule(
            name="phase162_verified_literature_citation",
            literature_reference=LiteratureReference(
                label="Toda " + locator, locator=locator
            ),
        ),
    )


def _element(index):
    return HomotopyElement(
        name=f"η{index}",
        dimension=index,
        generator=GeneratorSymbol(family="η", index=index),
    )


def _snapshot(generator, order=2):
    conclusion = Relation(
        lhs=TodaPrimaryGroup(group_dimension=5, sphere_dimension=2),
        rhs=FiniteCyclicGroup(order=order, generator=generator),
        relation_type=RelationType.EQUALITY,
    )
    given = ProofStep(conclusion="premise", premises=(), rule=ProofRule.GIVEN)
    witness = ProofStep(
        conclusion=conclusion, premises=(given,), rule=ProofRule.INFERENCE
    )
    candidate = WitnessCandidate(
        "Proposition 5.6", "pi5_2_group_relation",
        witness, conclusion, "focused test",
    )
    base = build_registry_bridge()
    snapshot, attempts = bind_representative_witnesses(
        base, (candidate,), citation_builder=_citation
    )
    assert attempts[0].status == "STRUCTURED"
    assert base.registry.assertion(ASSERTION_ID).content != conclusion
    return snapshot


def test_r4_r10_preserves_full_generator_and_standard_notation():
    generator = Composition(_element(2), Composition(_element(3), _element(4)))
    result = verify_prop56_pi5_2_generator(_snapshot(generator))
    assert result.generator == generator
    assert result.order == 2
    assert result.canonical_latex == CANONICAL_LATEX
    assert result.status == "GENERATOR_PRESERVED"


def test_r4_r10_rejects_missing_generator():
    with pytest.raises(ValueError, match="Generator"):
        verify_prop56_pi5_2_generator(_snapshot(None))


def test_r4_r10_rejects_wrong_generator():
    generator = Composition(_element(2), Composition(_element(3), _element(5)))
    with pytest.raises(ValueError, match="Generator"):
        verify_prop56_pi5_2_generator(_snapshot(generator))


def test_r4_r10_requires_structured_registration():
    with pytest.raises(ValueError, match="STRUCTURED"):
        verify_prop56_pi5_2_generator(build_registry_bridge())


def test_r4_r10_rejects_wrong_order():
    generator = Composition(_element(2), Composition(_element(3), _element(4)))
    with pytest.raises(ValueError, match="order two"):
        verify_prop56_pi5_2_generator(_snapshot(generator, order=4))


def test_r4_r10_rejects_wrong_argument_type():
    with pytest.raises(TypeError, match="RegistryBridgeResult"):
        verify_prop56_pi5_2_generator(None)
