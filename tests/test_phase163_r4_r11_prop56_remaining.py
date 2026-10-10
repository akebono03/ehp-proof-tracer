from dataclasses import replace

import pytest

from expression import GeneratorSymbol, HomotopyElement, ScalarSum, ScalarSymbol, Suspension
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from phase163_r4_r11_prop56_remaining import (
    COMPONENT_KEYS,
    verify_prop56_remaining_component,
)
from phase163_r4_r7_representative_bindings import WitnessCandidate, bind_representative_witnesses
from phase163_r4_registry_bridge import build_registry_bridge
from proof import FoundationalReferenceIdentity, InferenceRule, LiteratureReference, ProofRule, ProofStep, Relation, RelationType
from scalar_rules import ScalarGreaterEqualStatement


def _nu(index=None, prime=False):
    return HomotopyElement(
        name="ν′" if prime else f"ν{index}",
        dimension=3,
        generator=GeneratorSymbol(family="ν", decoration="′" if prime else None, index=index),
    )


def _citation(witness, locator, component, expected):
    identity = FoundationalReferenceIdentity(
        key=f"literature:{locator}:{component}", label=locator
    )
    leaf = ProofStep(expected, (), ProofRule.GIVEN, foundational_reference=identity)
    return ProofStep(
        expected, (leaf,), ProofRule.INFERENCE,
        foundational_reference=identity,
        inference_rule=InferenceRule(
            name="phase162_verified_literature_citation",
            literature_reference=LiteratureReference(label="Toda " + locator, locator=locator),
        ),
    )


def _relation(dimension, sphere, group):
    return Relation(TodaPrimaryGroup(dimension, sphere), group, RelationType.EQUALITY)


def _sample():
    n = ScalarSymbol("n")
    contents = {
        "pi6_3_group_relation": _relation(6, 3, FiniteCyclicGroup(4, _nu(prime=True))),
        "pi7_4_group_relation": _relation(7, 4, DirectSumGroup((FreeCyclicGroup(_nu(4)), FiniteCyclicGroup(4, Suspension(_nu(prime=True)))))),
        "pi8_5_group_relation": _relation(8, 5, FiniteCyclicGroup(8, _nu(5))),
        "higher_nu_group_relation": _relation(ScalarSum(n, 3), n, FiniteCyclicGroup(8, _nu(n))),
    }
    return contents


def _snapshot(contents):
    premise = ProofStep("source", (), ProofRule.GIVEN)
    candidates = tuple(
        WitnessCandidate(
            "Proposition 5.6", key,
            ProofStep(contents[key], (premise,), ProofRule.INFERENCE),
            contents[key], "focused test",
        )
        for key in COMPONENT_KEYS
    )
    snapshot, attempts = bind_representative_witnesses(
        build_registry_bridge(), candidates, citation_builder=_citation
    )
    assert all(attempt.status == "STRUCTURED" for attempt in attempts)
    return snapshot


def test_r4_r11_registers_four_typed_generators_and_scope():
    contents = _sample()
    snapshot = _snapshot(contents)
    n = ScalarSymbol("n")
    range_fact = ScalarGreaterEqualStatement(n, 6)
    for key in COMPONENT_KEYS:
        result = verify_prop56_remaining_component(
            snapshot, key,
            higher_range=range_fact if key == "higher_nu_group_relation" else None,
        )
        assert result.generator is not None
        assert result.status.startswith("GENERATOR")
        assert snapshot.registry.assertion(f"boundary:Proposition 5.6:{key}").content == contents[key]
    assert verify_prop56_remaining_component(snapshot, COMPONENT_KEYS[-1], higher_range=range_fact).scope == "n >= 6"


def test_r4_r11_pi6_3_rejects_wrong_generator():
    contents = _sample()
    contents["pi6_3_group_relation"] = _relation(6, 3, FiniteCyclicGroup(4, _nu(3)))
    with pytest.raises(ValueError, match="generator"):
        verify_prop56_remaining_component(_snapshot(contents), COMPONENT_KEYS[0])


def test_r4_r11_pi7_4_rejects_lost_direct_sum():
    contents = _sample()
    contents["pi7_4_group_relation"] = _relation(7, 4, FiniteCyclicGroup(4, Suspension(_nu(prime=True))))
    with pytest.raises(ValueError, match="direct summands"):
        verify_prop56_remaining_component(_snapshot(contents), COMPONENT_KEYS[1])


def test_r4_r11_pi7_4_rejects_wrong_free_generator():
    contents = _sample()
    contents["pi7_4_group_relation"] = _relation(7, 4, DirectSumGroup((FreeCyclicGroup(_nu(5)), FiniteCyclicGroup(4, Suspension(_nu(prime=True))))))
    with pytest.raises(ValueError, match="free generator"):
        verify_prop56_remaining_component(_snapshot(contents), COMPONENT_KEYS[1])


def test_r4_r11_pi8_5_rejects_wrong_order():
    contents = _sample()
    contents["pi8_5_group_relation"] = _relation(8, 5, FiniteCyclicGroup(4, _nu(5)))
    with pytest.raises(ValueError, match="order"):
        verify_prop56_remaining_component(_snapshot(contents), COMPONENT_KEYS[2])


def test_r4_r11_higher_requires_range_fact():
    with pytest.raises(ValueError, match="scope"):
        verify_prop56_remaining_component(_snapshot(_sample()), COMPONENT_KEYS[3])


def test_r4_r11_higher_rejects_wrong_generator():
    contents = _sample()
    n = ScalarSymbol("n")
    contents["higher_nu_group_relation"] = _relation(ScalarSum(n, 3), n, FiniteCyclicGroup(8, _nu(5)))
    with pytest.raises(ValueError, match="generator"):
        verify_prop56_remaining_component(_snapshot(contents), COMPONENT_KEYS[3], higher_range=ScalarGreaterEqualStatement(n, 6))


def test_r4_r11_unstructured_snapshot_is_rejected():
    with pytest.raises(ValueError, match="STRUCTURED"):
        verify_prop56_remaining_component(build_registry_bridge(), COMPONENT_KEYS[0])
