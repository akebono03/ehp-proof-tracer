"""Phase 169 R3G focused audit tests: reject provenance shortcuts."""
from pathlib import Path

from homotopy_groups import TodaDeltaMap, TodaHopfInvariantMap, TodaPrimaryGroup
from phase165_r14_r5_ehp_connection import expand_registered_ehp_terminal_goal
from phase165_r52_r13_reference_registration import build_adopted_prop51_reference
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from proof import ProofRule, Relation
from toda_rules import TodaDeltaInjectiveStatement, TodaHopfInvariantSurjectiveStatement


def _source_composite():
    bridge = build_adopted_prop51_reference()
    return bridge.registry.assertion("toda:adopted:prop5.1:finite_dimensional").content


def test_r3g_historical_terminal_requires_inference_provenance():
    available = (_source_composite(),)
    hopf = TodaHopfInvariantSurjectiveStatement(
        TodaHopfInvariantMap(TodaPrimaryGroup(6, 3), TodaPrimaryGroup(6, 5)),
    )
    delta = TodaDeltaInjectiveStatement(
        TodaDeltaMap(TodaPrimaryGroup(5, 5), TodaPrimaryGroup(3, 2)),
    )
    hopf_options = expand_registered_ehp_terminal_goal(hopf, available)
    delta_options = expand_registered_ehp_terminal_goal(delta, available)
    assert len(hopf_options) == len(delta_options) == 1
    assert tuple(p.proof_rule for p in hopf_options[0].rule.premise_patterns) == (
        ProofRule.INFERENCE, ProofRule.INFERENCE,
    )
    assert tuple(p.proof_rule for p in delta_options[0].rule.premise_patterns) == (
        ProofRule.INFERENCE,
    )
    assert isinstance(hopf_options[0].subgoals[0], Relation)
    assert hopf_options[0].subgoals[1] == delta_options[0].subgoals[0]


def test_r3g_the_hopf_formula_is_from_53_before_prop53():
    source = Path(__file__).resolve().parents[2] / "sources" / "toda" / "Toda_05_2.tex"
    text = source.read_text(encoding="utf-8")
    eq = text.index(r"\label{eq:5.3}")
    prop = text.index(r"\label{prop:5.3}")
    assert eq < prop
    assert r"H(\nu')=\eta_5" in text[eq:prop]


def test_r3g_source_registration_is_not_an_inference_step():
    bridge = build_adopted_prop51_reference()
    link, = bridge.proof_links
    assert link.assertion_id == "toda:adopted:prop5.1:finite_dimensional"
    assert link.step is not None
    assert link.step.rule is ProofRule.GIVEN
    assert link.step.premises == ()


def test_r3g2_database_goal_uses_production_citing_resolution():
    # The selected database goal can use a different generator spelling from
    # the registered fixed statement. Do not require raw Relation equality.
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=3, k=2)
    assert len(goals) == 1
    citing_id = resolve_specialized_goal_citing_id(bridge, goals[0])
    assert citing_id is not None
    assert citing_id == "shared:0:boundary:Proposition 5.3:pi5_3_group_relation"
    assertion = bridge.registry.assertion(citing_id)
    assert bridge.registry.reference(assertion.reference_id).locator == "Proposition 5.3"
