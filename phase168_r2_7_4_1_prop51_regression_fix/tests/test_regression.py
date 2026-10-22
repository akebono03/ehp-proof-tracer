from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r9_production_wiring import discover_goal_search_inputs
from phase168_r2_7_4_typed_registry_bridge.phase168_r2_7_4_literature_connection import (
    connect_explicit_literature_components,
)
from proof import Relation
from toda_literature_statement_boundary import TodaFixedStatementComponent


def test_r2741_original_prop51_assertions_and_records_unchanged():
    base = discover_goal_search_inputs().bridge
    result = connect_explicit_literature_components(base)
    original_records = {r.assertion_id: r for r in base.records}
    result_records = {r.assertion_id: r for r in result.records}
    for assertion in base.registry._assertions.values():
        if assertion.assertion_id.startswith("boundary:Proposition 5.1:"):
            assert isinstance(assertion.content, TodaFixedStatementComponent)
            assert result.registry.assertion(assertion.assertion_id) == assertion
            assert result_records[assertion.assertion_id] == original_records[assertion.assertion_id]
    assert result.proof_links == base.proof_links


def test_r2741_new_prop53_and_prop56_relations_remain_registered():
    bridge = build_shared_typed_bridge()
    for locator, keys in (
        ("Proposition 5.3", (
            "pi4_2_group_relation", "pi5_3_group_relation", "pi6_4_group_relation",
            "higher_eta_squared_group_relation",
        )),
        ("Proposition 5.6", (
            "pi5_2_group_relation", "pi6_3_group_relation", "pi7_4_group_relation",
            "pi8_5_group_relation", "higher_nu_group_relation",
        )),
    ):
        for key in keys:
            assertion_id = f"shared:0:boundary:{locator}:{key}"
            assert isinstance(bridge.registry.assertion(assertion_id).content, Relation)


def test_r2741_shared_prop51_boundary_remains_metadata():
    bridge = build_shared_typed_bridge()
    for key in (
        "pi3_2_group_relation", "eta2_hopf_relation",
        "delta_iota5_relation", "higher_eta_group_relation",
    ):
        assertion_id = f"shared:0:boundary:Proposition 5.1:{key}"
        assert isinstance(bridge.registry.assertion(assertion_id).content, TodaFixedStatementComponent)
