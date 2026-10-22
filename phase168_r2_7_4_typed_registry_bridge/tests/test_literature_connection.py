from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r9_production_wiring import discover_goal_search_inputs
from phase168_r2_7_4_typed_registry_bridge.phase168_r2_7_4_literature_connection import (
    connect_explicit_literature_components,
)
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from toda_literature_statement_boundary import TodaFixedStatementComponent
from proof import Relation, ProofRule


def test_r274_typed_nine_boundary_components_without_proof_links():
    base = discover_goal_search_inputs().bridge
    result = connect_explicit_literature_components(base)
    assert result.proof_links == base.proof_links
    assert sum(isinstance(result.registry.assertion(f"boundary:Proposition 5.3:{key}").content, Relation)
               for key in ("pi4_2_group_relation", "pi5_3_group_relation", "pi6_4_group_relation", "higher_eta_squared_group_relation")) == 4
    assert sum(isinstance(result.registry.assertion(f"boundary:Proposition 5.6:{key}").content, Relation)
               for key in ("pi5_2_group_relation", "pi6_3_group_relation", "pi7_4_group_relation", "pi8_5_group_relation", "higher_nu_group_relation")) == 5


def test_r274_shared_bridge_contains_both_typed_propositions():
    shared = build_shared_typed_bridge()
    assert isinstance(shared.registry.assertion("shared:0:boundary:Proposition 5.3:pi4_2_group_relation").content, Relation)
    assert isinstance(shared.registry.assertion("shared:0:boundary:Proposition 5.6:pi5_2_group_relation").content, Relation)


def test_r274_citing_target_cannot_derive_itself_as_given():
    bridge = build_shared_typed_bridge()
    target_id = "shared:0:boundary:Proposition 5.3:pi4_2_group_relation"
    target = bridge.registry.assertion(target_id).content
    screened = screen_shared_proof_context(
        bridge, goal=target, citing_assertion_id=target_id,
        explicit_publication_target=True,
    )
    assert all(link.step.conclusion != target for link in screened.proof_links)
    assert all(link.step.rule is ProofRule.GIVEN for link in screened.proof_links)
    assert all(not isinstance(link.step.conclusion, TodaFixedStatementComponent)
               for link in screened.proof_links)


def test_r274_same_proposition_prior_components_remain_available():
    bridge = build_shared_typed_bridge()
    target_id = "shared:0:boundary:Proposition 5.3:higher_eta_squared_group_relation"
    target = bridge.registry.assertion(target_id).content
    screened = screen_shared_proof_context(
        bridge, goal=target, citing_assertion_id=target_id,
        explicit_publication_target=True,
    )
    ids = {link.assertion_id for link in screened.proof_links}
    assert "shared:0:boundary:Proposition 5.3:pi4_2_group_relation" in ids
    assert target_id not in ids
