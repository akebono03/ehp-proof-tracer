from dataclasses import replace

import pytest

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r52_r18_proof_order import restrict_by_proof_use_order
from phase165_r52_r19_prop51_binding import resolve_registered_proof_use_order
from proof import ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry, AssertionKind, LiteratureEntry, ProofStepLink,
    ReferenceKind, UnifiedStatementRegistry,
)


def _bridge():
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        "prior", ReferenceKind.EQUATION, "(5.1)",
        source_id="Toda", publication_position=77,
    ))
    registry.add_reference(LiteratureEntry(
        "prop51", ReferenceKind.PROPOSITION, "Proposition 5.1",
        source_id="Toda", publication_position=78,
    ))
    registry.add_reference(LiteratureEntry(
        "later", ReferenceKind.PROPOSITION, "Proposition 5.3",
        source_id="Toda", publication_position=79,
    ))
    items = (
        ("old", "prior", "earlier"),
        ("boundary:Proposition 5.1:pi3_2_group_relation", "prop51", "pi3"),
        ("boundary:Proposition 5.1:eta2_hopf_relation", "prop51", "hopf"),
        ("boundary:Proposition 5.1:delta_iota5_relation", "prop51", "delta"),
        ("new", "later", "later"),
    )
    links = []
    for identifier, ref, content in items:
        registry.add_assertion(AssertionEntry(
            identifier, ref, AssertionKind.STATEMENT, content,
        ))
        links.append(ProofStepLink(
            identifier, step=ProofStep(content, (), ProofRule.GIVEN),
        ))
    return RegistryBridgeResult(registry, (), tuple(links))


def test_prop51_registered_hopf_available_for_pi3():
    bridge = _bridge()
    policy = resolve_registered_proof_use_order(bridge, "pi3")
    assert policy is not None
    assert policy.target_assertion_id.endswith("pi3_2_group_relation")
    assert policy.same_reference_prerequisites == (
        "boundary:Proposition 5.1:eta2_hopf_relation",
    )
    usable = restrict_by_proof_use_order(bridge, goal="pi3", policy=policy)
    assert tuple(link.step.conclusion for link in usable.proof_links) == (
        "earlier", "hopf",
    )


def test_unknown_goal_has_no_invented_order():
    assert resolve_registered_proof_use_order(_bridge(), "pi4") is None


def test_missing_hopf_component_fails_closed():
    bridge = _bridge()
    registry = bridge.registry
    del registry._assertions["boundary:Proposition 5.1:eta2_hopf_relation"]
    with pytest.raises(ValueError, match="missing or ambiguous"):
        resolve_registered_proof_use_order(bridge, "pi3")


def test_different_source_does_not_inherit_prop51_policy():
    bridge = _bridge()
    bridge.registry._references["prop51"] = replace(
        bridge.registry.reference("prop51"), locator="Proposition 5.2",
    )
    assert resolve_registered_proof_use_order(bridge, "pi3") is None


def test_r18_filter_does_not_create_missing_proof_link():
    bridge = _bridge()
    bridge = replace(bridge, proof_links=tuple(
        link for link in bridge.proof_links
        if not link.assertion_id.endswith("eta2_hopf_relation")
    ))
    policy = resolve_registered_proof_use_order(bridge, "pi3")
    screened = restrict_by_proof_use_order(bridge, goal="pi3", policy=policy)
    assert tuple(link.step.conclusion for link in screened.proof_links) == ("earlier",)
