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
    prior = [
        link.step.conclusion for link in screened.proof_links
        if link.step is not None
        and isinstance(link.step.conclusion, Relation)
        and link.step.conclusion.lhs == TodaPrimaryGroup(4, 3)
        and isinstance(link.step.conclusion.rhs, FiniteCyclicGroup)
        and link.step.conclusion.rhs.order == 2
    ]
    assert prior, "the registered prior pi4^3 group was not screened in"
    assert any(
        getattr(item.rhs.generator, "generator", None)
        == witness.source_generator.generator
        and getattr(item.rhs.generator, "dimension", None)
        == witness.source_generator.dimension
        and getattr(item.rhs.generator, "source", None)
        == witness.source_generator.source
        and getattr(item.rhs.generator, "target", None)
        == witness.source_generator.target
        for item in prior
    ), "typed eta3 data do not match the prior group"
    # The prior generator is the exact registered one (η_3), not the
    # differently spelled η₃ element returned by the definition factory.
    options = shared_expansion_provider(screened, proof_target=named)(named)
    candidates = [
        option for option in options
        if option.rule.name == "proved generator suspension normalizes transported cyclic group"
        and len(option.subgoals) == 2
        and option.subgoals[1] == witness
    ]
    assert candidates, "registered prior did not produce the R3-V normalization"
    assert any(
        isinstance(option.subgoals[0], Relation)
        and option.subgoals[0].lhs == named.lhs
        and isinstance(option.subgoals[0].rhs, FiniteCyclicGroup)
        and option.subgoals[0].rhs.order == 2
        and any(
            option.subgoals[0].rhs.generator == IteratedSuspension(item.rhs.generator, 1)
            for item in prior
        )
        for option in candidates
    ), "R3-V transport must use the registered generator without inventing a source"
    assert all(
        option.rule.match_guard(
            (
                ProofStep(option.subgoals[0], (), ProofRule.GIVEN),
                ProofStep(option.subgoals[1], (), ProofRule.GIVEN),
            ),
            {},
        )
        for option in candidates
    ), "R3-V inference rule must accept the actual typed premises"
