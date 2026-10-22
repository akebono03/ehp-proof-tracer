from __future__ import annotations

from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from proof import ProofRule


def _context(locator: str, key: str):
    bridge = build_shared_typed_bridge()
    assertion_id = f'shared:0:boundary:{locator}:{key}'
    goal = bridge.registry.assertion(assertion_id).content
    screened = screen_shared_proof_context(
        bridge,
        goal=goal,
        citing_assertion_id=assertion_id,
        explicit_publication_target=True,
    )
    return bridge, screened


def test_r2_7_prop53_excludes_metadata_but_retains_typed_toda52():
    bridge, screened = _context('Proposition 5.3', 'higher_eta_squared_group_relation')
    contents = []
    for link in screened.proof_links:
        assert link.step is not None
        assert link.step.rule is ProofRule.GIVEN
        assertion = bridge.registry.assertion(link.assertion_id)
        assert type(assertion.content).__name__ != 'TodaFixedStatementComponent'
        assert link.step.conclusion == assertion.content
        contents.append(type(assertion.content).__name__)
    assert 'Toda52UniversalStatement' in contents
    assert 'Relation' in contents


def test_r2_7_prop56_excludes_metadata_but_retains_typed_toda45():
    bridge, screened = _context('Proposition 5.6', 'higher_nu_group_relation')
    names = [type(link.step.conclusion).__name__ for link in screened.proof_links]
    assert 'TodaFixedStatementComponent' not in names
    assert 'Toda45IsomorphismStatement' in names


def test_r2_7_no_target_self_given():
    bridge, screened = _context('Proposition 5.3', 'higher_eta_squared_group_relation')
    target_id = 'shared:0:boundary:Proposition 5.3:higher_eta_squared_group_relation'
    assert all(link.assertion_id != target_id for link in screened.proof_links)


def test_r2_7_typed_prop51_group_maintained():
    bridge, screened = _context('Proposition 5.3', 'higher_eta_squared_group_relation')
    assert any(
        bridge.registry.reference(bridge.registry.assertion(link.assertion_id).reference_id).locator == 'Proposition 5.1'
        and type(link.step.conclusion).__name__ == 'Relation'
        for link in screened.proof_links
    )
