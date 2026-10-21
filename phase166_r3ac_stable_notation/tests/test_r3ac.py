from expression import IteratedSuspension
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase166_r3ac_stable_notation import expand_stable_eta_notation, stable_eta_notation_rule
from proof import ProofStep, ProofRule, Relation, find_inference_matches_for_rule
from toda_rules import toda_eta_family_definition_statement


def _case(r):
    source = toda_eta_family_definition_statement(3).element
    target = toda_eta_family_definition_statement(3 + r).element
    earlier = Relation(TodaPrimaryGroup(4, 3), FiniteCyclicGroup(2, source))
    goal = Relation(TodaPrimaryGroup(4 + r, 3 + r), FiniteCyclicGroup(2, target))
    transported = Relation(goal.lhs, FiniteCyclicGroup(2, IteratedSuspension(source, r)))
    return earlier, goal, transported


def test_all_positive_iteration_counts_without_special_cases():
    for r in (2, 3, 4, 7):
        earlier, goal, transported = _case(r)
        options = expand_stable_eta_notation(goal, (earlier, TodaEtaFamilyGeneralDefinition()))
        assert len(options) == 1
        assert options[0].subgoals == (transported, TodaEtaFamilyGeneralDefinition())
        steps = (ProofStep(transported, (), ProofRule.GIVEN),
                 ProofStep(TodaEtaFamilyGeneralDefinition(), (), ProofRule.GIVEN))
        assert len(find_inference_matches_for_rule(stable_eta_notation_rule(goal), steps)) == 1


def test_no_uncited_notation_or_unrelated_stem():
    earlier, goal, transported = _case(2)
    assert expand_stable_eta_notation(goal, (earlier,)) == ()
    unrelated = Relation(TodaPrimaryGroup(7, 5), goal.rhs)
    assert expand_stable_eta_notation(unrelated, (earlier, TodaEtaFamilyGeneralDefinition())) == ()
