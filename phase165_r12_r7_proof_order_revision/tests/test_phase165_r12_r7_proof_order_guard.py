from dataclasses import dataclass

import pytest

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r12_r7_proof_order_guard import OrderedClaim, restrict_ordered_claim_context
from proof import ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)


@dataclass(frozen=True)
class Composite:
    first: str
    second: str
    third: str
    fifth: str


def _fixture():
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry("prop", ReferenceKind.PROPOSITION, "Proposition X"))
    registry.add_reference(LiteratureEntry("external", ReferenceKind.LEMMA, "Lemma Y"))
    entries = (
        ("parent", "prop", Composite("group", "hopf", "delta", "future")),
        ("parent:component:first", "prop", "group"),
        ("parent:component:second", "prop", "hopf"),
        ("parent:component:third", "prop", "delta"),
        ("parent:component:fifth", "prop", "future"),
        ("external-claim", "external", "earlier literature"),
    )
    links = []
    for identifier, reference, value in entries:
        registry.add_assertion(AssertionEntry(
            identifier, reference, AssertionKind.STATEMENT, value,
            origin=AssertionOrigin.FIXED_STATEMENT,
        ))
        links.append(ProofStepLink(identifier, step=ProofStep(value, (), ProofRule.GIVEN)))
    return RegistryBridgeResult(registry, (), tuple(links))


def _claims():
    return (
        OrderedClaim(1, "first", "group"),
        OrderedClaim(2, "second", "hopf"),
        OrderedClaim(3, "third", "delta"),
        OrderedClaim(4, "fourth", "target"),
        OrderedClaim(5, "fifth", "future"),
    )


def _policy():
    return {"first": ("second",), "fourth": ("first", "second", "third")}


def _kept(target):
    return {link.assertion_id for link in restrict_ordered_claim_context(
        _fixture(), target=target, ordered_claims=_claims(),
        reference_id="prop", allowed_dependencies=_policy(),
    ).proof_links}


def test_pi32_can_use_later_printed_hopf_claim():
    assert _kept("group") == {"parent:component:second", "external-claim"}


def test_pi43_allows_only_three_reviewed_components():
    assert _kept("target") == {
        "parent:component:first", "parent:component:second",
        "parent:component:third", "external-claim",
    }


def test_no_compound_given_and_no_later_claim():
    kept = _kept("target")
    assert "parent" not in kept
    assert "parent:component:fifth" not in kept


def test_unregistered_target_rejected():
    with pytest.raises(ValueError, match="exactly one"):
        _kept("unknown")


def test_reject_duplicate_claim_positions():
    with pytest.raises(ValueError, match="duplicate claim position"):
        restrict_ordered_claim_context(
            _fixture(), target="target",
            ordered_claims=_claims() + (OrderedClaim(4, "extra", "other"),),
            reference_id="prop", allowed_dependencies=_policy(),
        )


def test_same_claim_cannot_authorize_itself():
    with pytest.raises(ValueError, match="invalid proof dependency"):
        restrict_ordered_claim_context(
            _fixture(), target="target", ordered_claims=_claims(),
            reference_id="prop", allowed_dependencies={"fourth": ("fourth",)},
        )
