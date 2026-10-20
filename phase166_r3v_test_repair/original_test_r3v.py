from expression import GeneratorSymbol, HomotopyElement, IteratedSuspension
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase166_r3v_generator_transport import (expand_generator_transport_normalization,
                                               generator_transport_normalization_rule)
from phase165_r12_r21_eta_generator_chain import expand_cited_eta_generator
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule
from toda_rules import toda_eta_family_definition_statement


def _case():
    base = toda_eta_family_definition_statement(3).element
    target = toda_eta_family_definition_statement(4).element
    source_group = TodaPrimaryGroup(4, 3)
    target_group = TodaPrimaryGroup(5, 4)
    suspended = Relation(target_group, FiniteCyclicGroup(2, IteratedSuspension(base, 1)))
    named = Relation(target_group, FiniteCyclicGroup(2, target))
    witness = GeneratorSuspension(TodaSuspensionMap(source_group, target_group), base, target)
    return suspended, named, witness


def test_r3v_existing_eta_suspension_provable():
    _, _, witness = _case()
    options = expand_cited_eta_generator(witness)
    assert len(options) == 1
    assert len(options[0].subgoals) == 2


def test_r3v_named_goal_proposes_two_proved_subgoals():
    transported, named, witness = _case()
    options = expand_generator_transport_normalization(named)
    assert len(options) == 1
    assert options[0].subgoals == (transported, witness)
    steps = (ProofStep(transported, (), ProofRule.GIVEN), ProofStep(witness, (), ProofRule.GIVEN))
    rule = generator_transport_normalization_rule()
    matches = find_inference_matches_for_rule(rule, steps)
    assert len(matches) == 1
    assert rule.conclusion_builder(steps) == named


def test_r3v_no_unrelated_generator_and_no_other_stem_guess():
    transported, named, _ = _case()
    another = HomotopyElement(name='other', dimension=4, source=5, target=4,
                              generator=GeneratorSymbol(family='x', index=4))
    assert expand_generator_transport_normalization(Relation(named.lhs, FiniteCyclicGroup(2, another))) == ()
    assert expand_generator_transport_normalization(Relation(TodaPrimaryGroup(6, 4), FiniteCyclicGroup(2, named.rhs.generator))) == ()


def test_r3v_registered_prior_and_shared_search_connection():
    transported, named, witness = _case()
    bridge = build_shared_typed_bridge()
    target_id = 'shared:2:toda:adopted:prop5.1:higher_eta_group_relation'
    screened = screen_shared_proof_context(bridge, goal=named, citing_assertion_id=target_id,
                                            explicit_publication_target=True)
    assert any(link.step and link.step.conclusion == Relation(
        TodaPrimaryGroup(4, 3), FiniteCyclicGroup(2, witness.source_generator))
        for link in screened.proof_links)
    options = shared_expansion_provider(screened,proof_target=named)(named)
    assert any(option.subgoals == (transported, witness) for option in options)
