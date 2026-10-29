"""R2E focused source-adoption and non-circularity regression tests."""
from __future__ import annotations

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, Multiple
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r9_production_wiring import discover_goal_search_inputs
from phase166_r3c_publication_order import precedes_citing_assertion
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase171_r2e_toda53_double_reference import (
    ASSERTION_ID, build_adopted_toda53_double_reference,
)
from proof import ProofRule, Relation, RelationType
from unified_statement_registry import AssertionOrigin, UnifiedStatementRegistry


def test_double_relation_is_one_exact_cited_given():
    production = discover_goal_search_inputs().bridge
    source = build_adopted_toda53_double_reference(production)
    assert len(source.proof_links) == 1
    assertion = source.registry.assertion(ASSERTION_ID)
    reference = source.registry.reference(assertion.reference_id)
    assert reference.locator == "(5.3)"
    assert reference.source_id == "toda:tex:ch5:0005"
    assert assertion.origin is AssertionOrigin.FIXED_STATEMENT
    assert isinstance(assertion.content, Relation)
    assert assertion.content.relation_type is RelationType.EQUALITY
    assert isinstance(assertion.content.lhs, Multiple)
    assert assertion.content.lhs.coefficient == 2
    nu_prime = assertion.content.lhs.expression
    assert nu_prime == HomotopyElement(
        name="ν′", dimension=3, source=6, target=3,
        generator=GeneratorSymbol(family="ν", decoration="′"),
    )
    rhs = assertion.content.rhs
    assert isinstance(rhs, Composition)
    assert rhs.left.source == rhs.right.left.target
    assert isinstance(rhs.right, Composition)
    assert rhs.right.is_type_compatible()
    assert tuple(x.generator.index for x in (
        rhs.left, rhs.right.left, rhs.right.right,
    )) == (3, 4, 5)
    link = source.proof_links[0]
    assert link.assertion_id == ASSERTION_ID
    assert link.step.rule is ProofRule.GIVEN
    assert link.step.premises == ()
    assert link.step.conclusion == assertion.content


def test_missing_archive_fails_closed():
    missing = RegistryBridgeResult(UnifiedStatementRegistry(), (), ())
    with pytest.raises(ValueError, match="exactly one archived source"):
        build_adopted_toda53_double_reference(missing)
    with pytest.raises(TypeError, match="RegistryBridgeResult"):
        build_adopted_toda53_double_reference(None)


def test_default_bridge_appends_source_without_renumbering_prior_ids():
    bridge = build_shared_typed_bridge()
    ids = tuple(a.assertion_id for a in bridge.registry._assertions.values()
                if a.assertion_id.endswith(":" + ASSERTION_ID))
    assert len(ids) == 1
    assertion_id = ids[0]
    assert assertion_id.startswith("shared:12:")
    assertion = bridge.registry.assertion(assertion_id)
    reference = bridge.registry.reference(assertion.reference_id)
    assert reference.locator == "(5.3)"
    assert reference.publication_position == 8100
    links = tuple(link for link in bridge.proof_links if link.assertion_id == assertion_id)
    assert len(links) == 1
    assert links[0].step.rule is ProofRule.GIVEN
    assert all(link.step.conclusion != assertion.content or link.assertion_id == assertion_id
               for link in bridge.proof_links)
    assert bridge.registry.assertion(
        "shared:8:toda:adopted:eq5.3:nu_prime_hopf_relation"
    ) is not None


def test_double_source_is_prior_to_pi63_target_and_not_root_proof():
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=3, k=3)
    assert len(goals) == 1
    target = goals[0]
    citing = resolve_specialized_goal_citing_id(bridge, target)
    assert citing == "shared:0:boundary:Proposition 5.6:pi6_3_group_relation"
    source_id = "shared:12:" + ASSERTION_ID
    assert precedes_citing_assertion(bridge, source_id, citing)
    assert all(link.step.conclusion != target for link in bridge.proof_links
               if link.step is not None)


def test_explicit_sources_are_not_modified():
    production = discover_goal_search_inputs().bridge
    source = build_adopted_toda53_double_reference(production)
    combined = build_shared_typed_bridge(sources=(source,))
    assert len(combined.proof_links) == 1
    assert combined.proof_links[0].step.rule is ProofRule.GIVEN
