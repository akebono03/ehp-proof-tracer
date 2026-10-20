"""Focused contract for registered earlier literature claims without stored links."""
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from proof import ProofRule, ProofStep, Relation
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    LiteratureEntry,
    ReferenceKind,
    UnifiedStatementRegistry,
    ProofStepLink,
)


def _bridge():
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry('earlier', ReferenceKind.PROPOSITION, 'earlier', publication_position=10))
    registry.add_reference(LiteratureEntry('target', ReferenceKind.PROPOSITION, 'target', publication_position=11))
    registry.add_reference(LiteratureEntry('later', ReferenceKind.PROPOSITION, 'later', publication_position=12))
    claims = (
        ('earlier', Relation(TodaPrimaryGroup(4, 3), FiniteCyclicGroup(2, 'base'))),
        ('target', Relation(TodaPrimaryGroup(5, 4), FiniteCyclicGroup(2, 'goal'))),
        ('later', Relation(TodaPrimaryGroup(6, 5), FiniteCyclicGroup(2, 'later'))),
    )
    for identifier, claim in claims:
        registry.add_assertion(AssertionEntry(
            assertion_id=identifier, reference_id=identifier,
            kind=AssertionKind.STATEMENT, content=claim,
            origin=AssertionOrigin.FIXED_STATEMENT,
        ))
    return RegistryBridgeResult(registry, (), ())


def test_prior_registered_claim_becomes_given_without_manual_link():
    bridge = _bridge()
    screened = screen_shared_proof_context(
        bridge, goal=bridge.registry.assertion('target').content,
        citing_assertion_id='target', explicit_publication_target=True,
    )
    assert [link.assertion_id for link in screened.proof_links] == ['earlier']
    step = screened.proof_links[0].step
    assert step.rule is ProofRule.GIVEN
    assert step.premises == ()
    assert step.conclusion == bridge.registry.assertion('earlier').content
    assert bridge.proof_links == ()


def test_target_and_later_claim_not_given():
    bridge = _bridge()
    screened = screen_shared_proof_context(
        bridge, goal=bridge.registry.assertion('target').content,
        citing_assertion_id='target', explicit_publication_target=True,
    )
    assert not any(link.assertion_id in ('target', 'later') for link in screened.proof_links)


def test_legacy_context_retains_no_unlinked_claim():
    bridge = _bridge()
    screened = screen_shared_proof_context(
        bridge, goal=bridge.registry.assertion('target').content,
        citing_assertion_id='target',
    )
    assert screened.proof_links == ()


def test_preexisting_link_does_not_change_generated_step():
    bridge = _bridge()
    old_step = ProofStep(
        conclusion=bridge.registry.assertion('earlier').content,
        premises=(),
        rule=ProofRule.GIVEN,
    )
    with_link = RegistryBridgeResult(
        bridge.registry, bridge.records,
        (ProofStepLink(assertion_id='earlier', step=old_step),),
    )
    kwargs = dict(
        goal=bridge.registry.assertion('target').content,
        citing_assertion_id='target',
        explicit_publication_target=True,
    )
    plain = screen_shared_proof_context(bridge, **kwargs)
    linked = screen_shared_proof_context(with_link, **kwargs)
    assert plain.proof_links == linked.proof_links
    assert linked.proof_links[0].step is not old_step


def test_preexisting_link_for_later_claim_cannot_make_it_usable():
    bridge = _bridge()
    later_step = ProofStep(
        conclusion=bridge.registry.assertion('later').content,
        premises=(), rule=ProofRule.GIVEN,
    )
    with_link = RegistryBridgeResult(
        bridge.registry, bridge.records,
        (ProofStepLink(assertion_id='later', step=later_step),),
    )
    selected = screen_shared_proof_context(
        with_link, goal=bridge.registry.assertion('target').content,
        citing_assertion_id='target', explicit_publication_target=True,
    )
    assert [link.assertion_id for link in selected.proof_links] == ['earlier']
