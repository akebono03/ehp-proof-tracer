from expression import IteratedSuspension
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r57_r7_stable_expansion import expand_registered_toda45_finite_cyclic_goal
from phase166_r3v_generator_transport import expand_generator_transport_normalization
from proof import ProofRule, Relation
from toda_rules import toda_eta_family_definition_statement

TARGET = 'shared:2:toda:adopted:prop5.1:higher_eta_group_relation'


def _screen():
    named = Relation(TodaPrimaryGroup(5,4), FiniteCyclicGroup(2,toda_eta_family_definition_statement(4).element))
    bridge = build_shared_typed_bridge()
    screened = screen_shared_proof_context(bridge,goal=named,citing_assertion_id=TARGET,explicit_publication_target=True)
    available = tuple(link.step.conclusion for link in screened.proof_links if link.step is not None and link.step.rule is ProofRule.GIVEN)
    return named,screened,available


def test_r3w_screened_prior_generator_enables_toda45():
    named,_,available = _screen()
    candidates = expand_generator_transport_normalization(named,available)
    assert candidates
    transported,witness = candidates[0].subgoals
    assert isinstance(transported.rhs.generator,IteratedSuspension)
    assert transported.rhs.generator.expression.name == 'η_3'
    assert witness.source_generator.name == 'η₃'
    assert expand_registered_toda45_finite_cyclic_goal(transported,available)


def test_r3w_screened_shared_providers_keep_both_expansions():
    named,screened,available = _screen()
    options = shared_expansion_provider(screened,proof_target=named)(named)
    candidates = expand_generator_transport_normalization(named,available)
    assert any(option.subgoals == candidates[0].subgoals for option in options)
    transported = candidates[0].subgoals[0]
    options2 = shared_expansion_provider(screened,proof_target=named)(transported)
    assert any('Toda (4.5)' in option.rule.name or 'transport' in option.rule.name for option in options2)


def test_r3w_web_underscore_eta_target_uses_registered_base():
    from expression import GeneratorSymbol, HomotopyElement
    _,screened,available = _screen()
    named_eta = HomotopyElement('η_4',4,5,4,GeneratorSymbol('η',4))
    goal = Relation(TodaPrimaryGroup(5,4),FiniteCyclicGroup(2,named_eta))
    candidates = expand_generator_transport_normalization(goal,available)
    assert len(candidates) == 1
    assert candidates[0].rule.conclusion_builder is not None
    assert any(x.subgoals == candidates[0].subgoals for x in shared_expansion_provider(screened,proof_target=goal)(goal))


def test_r3w_no_uncited_base_no_fabricated_transport():
    named,_,available = _screen()
    other = tuple(x for x in available if not (isinstance(x,Relation) and x.lhs==TodaPrimaryGroup(4,3)))
    assert expand_generator_transport_normalization(named,other)==()
