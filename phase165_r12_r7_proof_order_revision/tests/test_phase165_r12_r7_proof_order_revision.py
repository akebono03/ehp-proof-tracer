"""R12-R7 revised proof-use order; focused tests only."""
from dataclasses import dataclass

from phase165_prop51_claim_order import ordered_prop51_items, proof_ordered_prop51_items
from phase165_r12_r7_proof_order_guard import restrict_registered_ordered_claims
from phase163_r4_registry_bridge import RegistryBridgeResult
from proof import ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)


@dataclass(frozen=True)
class FiveClauses:
    pi3_2_group_relation: str = "pi3"
    eta2_hopf_relation: str = "hopf"
    delta_iota5_relation: str = "delta"
    higher_eta_group_relation: str = "higher"


def test_proof_order_swaps_first_two_without_changing_literature_order():
    source = FiveClauses()
    assert [x.component_key for x in ordered_prop51_items(source)][:2] == [
        "pi3_2_group_relation", "eta2_hopf_relation"]
    assert [x.component_key for x in proof_ordered_prop51_items(source)][:2] == [
        "eta2_hopf_relation", "pi3_2_group_relation"]
    assert len(proof_ordered_prop51_items(source)) == 5


def _bridge():
    from phase165_prop51_claim_order import pi4_3_goal
    from proof import Relation
    registry = UnifiedStatementRegistry()
    ref = "shared:0:adopted:toda:adopted:prop5.1:finite_dimensional"
    parent = "shared:0:toda:adopted:prop5.1:finite_dimensional"
    registry.add_reference(LiteratureEntry(ref, ReferenceKind.PROPOSITION, "Proposition 5.1"))
    content = FiveClauses()
    registry.add_assertion(AssertionEntry(parent, ref, AssertionKind.STATEMENT,
                                         content, origin=AssertionOrigin.FIXED_STATEMENT))
    links = [ProofStepLink(parent, step=ProofStep(content, (), ProofRule.GIVEN))]
    for key in ("pi3_2_group_relation", "eta2_hopf_relation",
                "delta_iota5_relation", "higher_eta_group_relation"):
        val = getattr(content, key)
        ident = parent + ":component:" + key
        registry.add_assertion(AssertionEntry(ident, ref, AssertionKind.STATEMENT,
                                             val, origin=AssertionOrigin.FIXED_STATEMENT))
        links.append(ProofStepLink(ident, step=ProofStep(val, (), ProofRule.GIVEN)))
    ident = parent + ":component:pi4_3_group_relation"
    target = pi4_3_goal()
    registry.add_assertion(AssertionEntry(ident, ref, AssertionKind.STATEMENT,
                                         target, origin=AssertionOrigin.FIXED_STATEMENT))
    links.append(ProofStepLink(ident, step=ProofStep(target, (), ProofRule.GIVEN)))
    return RegistryBridgeResult(registry, (), tuple(links))


def test_pi3_proof_uses_hopf_but_no_later_clause_or_parent():
    result = restrict_registered_ordered_claims(_bridge(), "pi3")
    contents = {link.step.conclusion for link in result.proof_links}
    assert contents == {"hopf"}


def test_pi43_proof_uses_only_first_three_and_never_composite():
    from phase165_prop51_claim_order import pi4_3_goal
    result = restrict_registered_ordered_claims(_bridge(), pi4_3_goal())
    contents = {link.step.conclusion for link in result.proof_links}
    assert contents == {"hopf", "pi3", "delta"}


def test_first_hopf_claim_uses_no_same_reference_given():
    result = restrict_registered_ordered_claims(_bridge(), "hopf")
    assert result.proof_links == ()
