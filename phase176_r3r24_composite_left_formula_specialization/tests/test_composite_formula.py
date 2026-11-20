"""R3R24 focused regression for the actual cited Proposition 2.2 recognizer."""
from __future__ import annotations
from dataclasses import replace
from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication, Suspension
from map_facts import EHP_H_MAP
from phase171_r2h_prop22_cited_hopf.source import _formula_parts, TodaProp22RightFormula, expand_cited_prop22_right_formula
from proof import Relation, RelationType

def e(name: str, source: int, target: int) -> HomotopyElement:
    return HomotopyElement(name, target, source=source, target=target)

def formula(alpha: object, beta: HomotopyElement) -> Relation:
    return Relation(MapApplication(EHP_H_MAP, Composition(alpha, Suspension(beta))), Composition(MapApplication(EHP_H_MAP, alpha), Suspension(beta)), RelationType.EQUALITY)

def test_nested_left_factor_specializes_from_exact_cited_source() -> None:
    nu_prime = e('ν′', 6, 3)
    eta_6 = e('η₆', 7, 6)
    alpha = Composition(nu_prime, eta_6)
    goal = formula(alpha, eta_6)
    assert _formula_parts(goal) == (alpha, eta_6)
    assert expand_cited_prop22_right_formula(goal, ()) == ()
    choices = expand_cited_prop22_right_formula(goal, (TodaProp22RightFormula(),))
    assert len(choices) == 1
    assert choices[0].subgoals == (TodaProp22RightFormula(),)

def test_existing_single_factor_specialization_unchanged() -> None:
    alpha = e('ν′', 6, 3)
    eta_5 = e('η₅', 6, 5)
    assert _formula_parts(formula(alpha, eta_5)) == (alpha, eta_5)

def test_composite_wrong_middle_endpoint_rejected() -> None:
    alpha = Composition(e('ν′', 6, 3), e('η₆', 8, 6))
    beta = e('η₆', 7, 6)
    assert _formula_parts(formula(alpha, beta)) is None

def test_composite_wrong_outer_endpoint_rejected() -> None:
    alpha = Composition(e('ν′', 6, 3), e('η₆', 7, 6))
    beta = e('η₇', 8, 7)
    assert _formula_parts(formula(alpha, beta)) is None

def test_formula_wrong_rhs_and_no_source_rejected() -> None:
    alpha = Composition(e('ν′', 6, 3), e('η₆', 7, 6))
    beta = e('η₆', 7, 6)
    goal = formula(alpha, beta)
    assert _formula_parts(replace(goal, rhs=beta)) is None
    assert expand_cited_prop22_right_formula(goal, ()) == ()
