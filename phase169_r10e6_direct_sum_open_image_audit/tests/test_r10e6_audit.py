"""Focused tests for the audit's observational (not proving) behavior."""
from __future__ import annotations

from expression import Composition, GeneratorSymbol, HomotopyElement
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, TodaPrimaryGroup
from phase169_r10e6_direct_sum_open_image_audit.audit import (
    _component_generators,
    _expected_component_audit,
    _observed_inferred,
)
from proof import ProofRule, ProofStep, Relation, RelationType


def _nu(n: int) -> HomotopyElement:
    return HomotopyElement(
        name=f"ν_{n}", dimension=n, source=n + 3, target=n,
        generator=GeneratorSymbol(family="ν", index=n),
    )


def _mu(n: int) -> HomotopyElement:
    return HomotopyElement(
        name=f"μ_{n}", dimension=n, source=n + 9, target=n,
        generator=GeneratorSymbol(family=r"\mu", index=n),
    )


def _cube(n: int) -> Composition:
    return Composition(_nu(n), Composition(_nu(n + 3), _nu(n + 6)))


def _group(n: int, k: int, generators: tuple) -> Relation:
    structure = DirectSumGroup(tuple(FiniteCyclicGroup(2, g) for g in generators))
    return Relation(
        TodaPrimaryGroup(n + k, n), structure, RelationType.EQUALITY,
    )


def test_r10e6_records_individual_direct_sum_components_without_claiming_proof():
    source = _group(11, 9, (_cube(11), _mu(11)))
    target = _group(15, 9, (_cube(15), _mu(15)))
    assert len(_component_generators(source)) == 2
    actual = _expected_component_audit(source, target, (), (), ())
    assert actual["typed_transport_compatible"] is True
    assert actual["suspension_exponent"] == 4
    assert actual["expected_image_count"] == 8
    assert len(actual["component_reports"]) == 2
    assert all(row["inferred_image_count"] == 0 for row in actual["component_reports"])
    assert all(not step["in_search_proven_steps_as_inference"]
               for row in actual["component_reports"] for step in row["images"])


def test_r10e6_never_counts_given_generator_image_as_inference():
    from homotopy_groups import TodaSuspensionMap
    from phase165_r14_r6_generic_iso import GeneratorImage
    image = GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(14, 11), TodaPrimaryGroup(15, 12)),
        _nu(11), _nu(12),
    )
    given = ProofStep(image, (), ProofRule.GIVEN)
    assert not _observed_inferred(image, (given,))
    assert _observed_inferred(image, (ProofStep(image, (), ProofRule.INFERENCE),))


def test_r10e6_structurally_requires_all_images_of_each_component():
    source = _group(11, 9, (_cube(11), _mu(11)))
    target = _group(15, 9, (_cube(15), _mu(15)))
    from phase169_r10e1_general_group_transport.transport import generator_images_for_group_transport
    obligations = generator_images_for_group_transport(source, target)
    assert obligations is not None and len(obligations) == 8
    steps = tuple(ProofStep(goal, (), ProofRule.INFERENCE) for goal in obligations[:4])
    actual = _expected_component_audit(source, target, steps, (), ())
    assert actual["component_reports"][0]["inferred_image_count"] == 4
    assert actual["component_reports"][1]["inferred_image_count"] == 0
