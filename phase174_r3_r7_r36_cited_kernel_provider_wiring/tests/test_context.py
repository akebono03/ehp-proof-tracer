"""Historical four-provider contract and conditional R35 registration."""
from __future__ import annotations

from expression import Composition, GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaDeltaMap, TodaPrimaryGroup
from phase165_r6_2_unified_registry_r3_r4.context_provider_registry import (
    build_context_expansion_provider_registry,
)
from proof import Relation, RelationType
from toda_rules import TodaDeltaImageUpToSignStatement


def _noop(goal: object, available: tuple[object, ...]) -> tuple:
    return ()


def _registry(available: tuple[object, ...]):
    return build_context_expansion_provider_registry(
        available=available, prior_conclusions=(),
        expand_registered_toda45_finite_cyclic_goal=_noop,
        expand_registered_eta_specialization=_noop,
        expand_registered_delta_image_goal=_noop,
        expand_cited_general_specialization=_noop,
    )


def _typed_witnesses():
    delta = TodaDeltaMap(TodaPrimaryGroup(11, 11), TodaPrimaryGroup(9, 5))
    iota = HomotopyElement("iota_11", 11, 11, 11, GeneratorSymbol("ι", 11))
    nu = HomotopyElement("nu5", 5, 8, 5, GeneratorSymbol("ν", 5))
    eta = HomotopyElement("eta8", 8, 9, 8, GeneratorSymbol("η", 8))
    generator = Composition(nu, eta)
    group = Relation(delta.target_group, FiniteCyclicGroup(2, generator), RelationType.EQUALITY)
    image = TodaDeltaImageUpToSignStatement(delta, iota, generator)
    return group, image


def test_original_four_context_providers_unchanged_without_cited_witness() -> None:
    registry = _registry(("non-cited",))
    assert len(registry.entries()) == 4
    assert all(entry.origin == "SHARED_CITED_CONTEXT" for entry in registry.entries())


def test_one_missing_source_does_not_register_extra_provider() -> None:
    group, image = _typed_witnesses()
    assert len(_registry((group,)).entries()) == 4
    assert len(_registry((image,)).entries()) == 4


def test_mismatched_generator_rejects_registration() -> None:
    group, image = _typed_witnesses()
    wrong = TodaDeltaImageUpToSignStatement(image.map, image.element, image.element)
    assert len(_registry((group, wrong)).entries()) == 4


def test_real_cited_shape_adds_only_one_provider_in_original_order() -> None:
    group, image = _typed_witnesses()
    registry = _registry((group, image))
    entries = registry.entries()
    assert len(entries) == 5
    assert entries[-1].provider_id == (
        "phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule.expand_cyclic_delta_kernel"
    )
    assert [entry.provider_id.split(".")[-1] for entry in entries[:4]] == [
        "expand_registered_toda45_finite_cyclic_goal",
        "expand_registered_eta_specialization",
        "expand_registered_delta_image_goal",
        "expand_cited_general_specialization",
    ]
    assert all(entry.origin == "SHARED_CITED_CONTEXT" for entry in entries)


def test_extra_provider_returns_no_proof_for_unrelated_goal() -> None:
    group, image = _typed_witnesses()
    extra = _registry((group, image)).providers()[-1]
    assert extra("not a typed kernel goal") == ()
