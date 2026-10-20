"""Root gate recognizes a substantiated generator change, not an unproved self-relation."""
from expression import IteratedSuspension
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r57_r11_proof_order_gate import is_unordered_root_structure_specialization
from phase166_r3v_generator_transport import expand_generator_transport_normalization
from proof import Relation
from toda_rules import toda_eta_family_definition_statement
from phase165_r3_recursive_search import GoalExpansion


def test_r3v_generator_evidence_root_is_not_self_citation():
    source=toda_eta_family_definition_statement(3).element
    target=toda_eta_family_definition_statement(4).element
    goal=Relation(TodaPrimaryGroup(5,4),FiniteCyclicGroup(2,target))
    opts=expand_generator_transport_normalization(goal)
    assert len(opts)==1
    assert not is_unordered_root_structure_specialization(goal,goal,opts[0])
    transported,witness=opts[0].subgoals
    assert transported.rhs.generator==IteratedSuspension(source,1)
    assert isinstance(witness,GeneratorSuspension)
    assert witness.map==TodaSuspensionMap(TodaPrimaryGroup(4,3),goal.lhs)


def test_r3v_root_gate_rejects_missing_or_wrong_generator_evidence():
    source=toda_eta_family_definition_statement(3).element
    target=toda_eta_family_definition_statement(4).element
    goal=Relation(TodaPrimaryGroup(5,4),FiniteCyclicGroup(2,target))
    option=expand_generator_transport_normalization(goal)[0]
    wrong_witness=GeneratorSuspension(TodaSuspensionMap(TodaPrimaryGroup(4,3),goal.lhs),target,target)
    invalid=GoalExpansion(option.rule,(option.subgoals[0],wrong_witness))
    assert is_unordered_root_structure_specialization(goal,goal,invalid)
    cyclic=GoalExpansion(option.rule,(goal,option.subgoals[1]))
    assert is_unordered_root_structure_specialization(goal,goal,cyclic)
