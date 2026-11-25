"""Focused audit contracts; no fake accepted ProofSteps or source insertion."""
from dataclasses import replace

from expression import Composition, GeneratorSymbol, MapApplication
from phase176_r3r40r1_eta_notation_bridge.tests.test_notation import example
from phase176_r3r49_hopf_image_frontier.audit import plan_probe, preflight
from proof import Relation


def test_reviewed_local_dependencies_and_r48_present():
    assert len(preflight()) == 40


def test_actual_db_spelling_uses_strict_notation_transport_in_existing_fixture():
    transported, forward, available = example()
    canonical = Relation(transported.lhs, forward.lhs)
    control = plan_probe(canonical, available)
    assert control['exact_hopf_witness_count'] == 1
    assert control['public_plan_steps'] > 0
    alpha = canonical.lhs.expression.left
    db_alpha = replace(alpha, name="ν'", generator=GeneratorSymbol("\\nu'"))
    goal = Relation(MapApplication(canonical.lhs.map, Composition(db_alpha, canonical.lhs.expression.right)), canonical.rhs)
    actual = plan_probe(goal, available)
    assert actual['exact_hopf_witness_count'] == 0
    assert actual['public_plan_steps'] == control['public_plan_steps'] + 1
    assert actual['public_plan'][-1]['rule'] == (
        'transport proved Hopf equality across strict typed nu-prime notation'
    )
    assert actual['public_plan'][-1]['subgoals'] == [repr(canonical)]
    assert actual['canonical_quadruple_lhs_matches']


def test_missing_cited_source_blocks_existing_plan():
    transported, forward, available = example()
    goal = Relation(transported.lhs, forward.lhs)
    assert plan_probe(goal, ())['public_plan_steps'] == 0
    assert plan_probe(goal, ())['quadruple_candidate_count'] == 0
