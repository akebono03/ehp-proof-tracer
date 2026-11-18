"""Provider discovers the R4R10 signed source without creating a new GIVEN."""
from __future__ import annotations

from dataclasses import replace

from expression import Composition, MapApplication, Multiple, Zero
from map_facts import EHP_DELTA_MAP
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase175_r4r10_cited_58_prop25_public.audit import sample_delta_eta9
from phase175_r4r10_cited_58_prop25_public.source import (
    CitedToda58SignedDelta, canonical_toda58,
)
from phase175_r4r11_signed_eta_torsion_public.provider import (
    build_signed_eta_torsion_provider,
)
from phase175_r4r11_signed_eta_torsion_public.rule import RULE_NAME
from proof import ProofRule, ProofStep, Relation
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)


def cited_bridge(include_source: bool = True, duplicate: bool = False) -> RegistryBridgeResult:
    registry = UnifiedStatementRegistry()
    refs = []
    if include_source:
        refs.append(CitedToda58SignedDelta(canonical_toda58()))
        if duplicate:
            refs.append(CitedToda58SignedDelta(canonical_toda58()))
    refs.append(TodaEtaFamilyGeneralDefinition())
    links = []
    for i, item in enumerate(refs):
        aid = "test:cited:" + str(i)
        rid = "test:source:" + str(i)
        registry.add_reference(LiteratureEntry(
            rid, ReferenceKind.EQUATION, "cited fixture" + str(i),
        ))
        registry.add_assertion(AssertionEntry(
            aid, rid, AssertionKind.STATEMENT, item, AssertionOrigin.FIXED_STATEMENT,
        ))
        links.append(ProofStepLink(aid, step=ProofStep(item, (), ProofRule.GIVEN)))
    return RegistryBridgeResult(registry, (), tuple(links))


def exact_target() -> Relation:
    signed = sample_delta_eta9()
    source = canonical_toda58()
    return Relation(
        MapApplication(EHP_DELTA_MAP, signed.element),
        Composition(source.positive_value.right.expression, signed.positive_value.right),
    )


def test_source_backed_provider_requires_actual_cited_witness() -> None:
    target = exact_target()
    good = build_signed_eta_torsion_provider(cited_bridge())(target)
    assert len(good) == 1
    assert good[0].rule.name == RULE_NAME
    signed, order, definition = good[0].subgoals
    assert signed == sample_delta_eta9()
    assert order == Relation(Multiple(2, signed.positive_value.right), Zero())
    assert definition == TodaEtaFamilyGeneralDefinition()
    assert not build_signed_eta_torsion_provider(cited_bridge(False))(target)


def test_duplicate_source_is_not_a_new_proof_or_extra_branch() -> None:
    options = build_signed_eta_torsion_provider(cited_bridge(duplicate=True))(exact_target())
    assert len(options) == 1
    assert all(not isinstance(goal, ProofStep) for goal in options[0].subgoals)


def test_wrong_goal_or_unrelated_expression_does_not_propose() -> None:
    expand = build_signed_eta_torsion_provider(cited_bridge())
    exact = exact_target()
    assert not expand(replace(exact, rhs=sample_delta_eta9().positive_value))
    assert not expand(replace(exact, lhs=MapApplication("wrong map", exact.lhs.expression)))
    assert not expand("untyped Delta identity text")
    assert not expand(Relation(Multiple(2, sample_delta_eta9().element), Zero()))


def test_provider_does_not_registered_pi95_group_proof() -> None:
    options = build_signed_eta_torsion_provider(cited_bridge())(exact_target())
    assert len(options) == 1
    assert all(not hasattr(item, "group_dimension") for item in options[0].subgoals)
