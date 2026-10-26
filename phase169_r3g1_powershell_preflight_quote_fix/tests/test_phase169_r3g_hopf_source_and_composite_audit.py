"""Phase 169 R3G focused audit tests: reject provenance shortcuts."""
from pathlib import Path

from homotopy_groups import TodaDeltaMap, TodaHopfInvariantMap, TodaPrimaryGroup
from phase165_r14_r5_ehp_connection import expand_registered_ehp_terminal_goal
from phase165_r52_r13_reference_registration import build_adopted_prop51_reference
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
