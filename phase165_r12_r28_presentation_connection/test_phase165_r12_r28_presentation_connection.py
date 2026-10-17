from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r12_r2_quotient_rules import HomomorphismPresentationStatement
from phase165_r12_r28_presentation_connection import expand_eta_presentation
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from toda_rules import toda_eta_family_definition_statement


def make_goal(name="η_3", generator=None):
    domain, codomain = TodaPrimaryGroup(3, 2), TodaPrimaryGroup(4, 3)
    source = toda_eta_family_definition_statement(2).element
    expected = toda_eta_family_definition_statement(3).element
    target = HomotopyElement(name=name, dimension=3, source=4, target=3,
                             generator=expected.generator if generator is None else generator)
    return HomomorphismPresentationStatement(TodaSuspensionMap(domain, codomain),
                                            domain, codomain, source, target)


def test_r28_web_notation_creates_canonical_proof_obligation():
    options = expand_eta_presentation(make_goal())
    assert len(options) == 1
    assert len(options[0].subgoals) == 1
    assert isinstance(options[0].subgoals[0], GeneratorSuspension)
    assert options[0].subgoals[0].target_generator.name == "η₃"
    assert options[0].rule.conclusion_pattern == make_goal()


def test_r28_canonical_notation_supported():
    assert len(expand_eta_presentation(make_goal("η₃"))) == 1


def test_r28_unrelated_generator_is_not_assumed():
    assert expand_eta_presentation(make_goal("ν_3")) == ()
    assert expand_eta_presentation(make_goal("η_3", GeneratorSymbol("ν", 3))) == ()


def test_r28_wrong_map_is_not_assumed():
    goal = make_goal()
    wrong = HomomorphismPresentationStatement(goal.map, goal.codomain, goal.domain,
                                              goal.source_generator, goal.target_generator)
    assert expand_eta_presentation(wrong) == ()
