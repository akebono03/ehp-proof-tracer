from __future__ import annotations

from dataclasses import dataclass

from r4_probe import evaluate_goal, markdown


@dataclass(frozen=True)
class Expansion:
    subgoals: tuple


def test_matching_goal_is_proposal_not_proof():
    def factory(rules):
        def expand(goal):
            return (Expansion((goal,)),) if goal == 'registered' else ()
        return expand
    result = evaluate_goal(object(), 'registered', r8_factory=factory, generic_factory=factory)
    assert result['r8']['status'] == 'PROPOSED'
    assert result['r26']['premise_counts'] == [1]


def test_unmatched_goal_not_reported_as_success():
    def factory(rules):
        return lambda goal: ()
    result = evaluate_goal(object(), 'missing', r8_factory=factory, generic_factory=factory)
    assert result['r8']['status'] == 'NO_MATCH'
    assert result['r26']['count'] == 0


def test_provider_error_is_reported():
    def factory(rules):
        def fail(goal):
            raise ValueError('broken')
        return fail
    result = evaluate_goal(object(), 'goal', r8_factory=factory, generic_factory=factory)
    assert result['r8']['status'] == 'ERROR'


def test_markdown_does_not_claim_proof():
    report = markdown({'status':'OK','source_status':'REGISTERED_ASSERTION_CONTENT',
        'unique_goals_available':1,'goals_examined':1,'rules_with_r8_proposals':1,
        'rules_with_r26_proposals':1,'rules':[{'rule_id':'x.y','goal_probe_status':'PROPOSED',
        'r8_proposed':1,'r26_proposed':1}], 'limitations':[]})
    assert '完成証明確認: 0' in report
    assert 'x.y' in report


def test_python310_compile():
    from pathlib import Path
    compile(Path(__file__).with_name('r4_probe.py').read_text(encoding='utf-8'), 'r4_probe.py', 'exec')
