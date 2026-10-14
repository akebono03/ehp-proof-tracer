from dataclasses import replace

import pytest

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r52_r18_proof_order import ProofUseOrder, restrict_by_proof_use_order
from proof import ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry, AssertionKind, LiteratureEntry, ProofStepLink,
    ReferenceKind, UnifiedStatementRegistry,
)


def _bridge():
    registry = UnifiedStatementRegistry()
    for key, position in (("earlier", 77), ("current", 78), ("later", 79)):
        registry.add_reference(LiteratureEntry(
            key, ReferenceKind.PROPOSITION, key,
            source_id="Toda translated TeX", publication_position=position,
        ))
    data = (
        ("previous", "earlier", "prior fact"),
        ("pi3", "current", "pi3 group"),
        ("hopf", "current", "H eta2"),
        ("delta", "current", "Delta iota5"),
        ("pi4", "current", "pi4 group"),
        ("future", "later", "future fact"),
    )
    links = []
    for key, reference, content in data:
        registry.add_assertion(AssertionEntry(
            key, reference, AssertionKind.STATEMENT, content,
        ))
        links.append(ProofStepLink(key, step=ProofStep(content, (), ProofRule.GIVEN)))
    return RegistryBridgeResult(registry, (), tuple(links))


def _ids(bridge):
    return tuple(link.assertion_id for link in bridge.proof_links)


def test_pi3_uses_later_printed_hopf_but_not_own_conclusion():
    result = restrict_by_proof_use_order(
        _bridge(), goal="pi3 group",
        policy=ProofUseOrder("pi3", ("hopf",)),
    )
    assert _ids(result) == ("previous", "hopf")


def test_pi4_uses_pi3_and_delta_but_not_pi4():
    result = restrict_by_proof_use_order(
        _bridge(), goal="pi4 group",
        policy=ProofUseOrder("pi4", ("pi3", "delta")),
    )
    assert _ids(result) == ("previous", "pi3", "delta")


def test_later_reference_can_use_previous_reference_regardless_of_stem():
    result = restrict_by_proof_use_order(
        _bridge(), goal="future fact", policy=ProofUseOrder("future"),
    )
    assert _ids(result) == ("previous", "pi3", "hopf", "delta", "pi4")


def test_unknown_order_does_not_authorize_reference():
    bridge = _bridge()
    registry = bridge.registry
    registry._references["earlier"] = replace(registry.reference("earlier"), publication_position=None)
    result = restrict_by_proof_use_order(bridge, goal="pi3 group", policy=ProofUseOrder("pi3", ("hopf",)))
    assert _ids(result) == ("hopf",)


def test_same_reference_prerequisite_requires_explicit_permission():
    result = restrict_by_proof_use_order(_bridge(), goal="pi3 group", policy=ProofUseOrder("pi3"))
    assert _ids(result) == ("previous",)


def test_invalid_self_or_cross_reference_permissions_rejected():
    with pytest.raises(ValueError, match="self citation"):
        ProofUseOrder("pi3", ("pi3",))
    with pytest.raises(ValueError, match="another reference"):
        restrict_by_proof_use_order(_bridge(), goal="pi3 group", policy=ProofUseOrder("pi3", ("previous",)))


def test_does_not_promote_a_missing_or_r16_rejected_link():
    bridge = _bridge()
    screened = replace(bridge, proof_links=tuple(link for link in bridge.proof_links if link.assertion_id != "hopf"))
    result = restrict_by_proof_use_order(screened, goal="pi3 group", policy=ProofUseOrder("pi3", ("hopf",)))
    assert "hopf" not in _ids(result)
