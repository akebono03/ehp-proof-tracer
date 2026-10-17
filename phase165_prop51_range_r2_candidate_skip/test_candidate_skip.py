from pathlib import Path
import ast

from homotopy_groups import TodaPrimaryGroup
from phase165_r52_r13_reference_registration import build_adopted_prop51_reference
from phase165_r57_r8_eta_specialization import (
    _fixed_typed_relations,
    expand_registered_eta_specialization,
    specialize_eta_group_relation,
    specialized_eta_group_goal_candidates,
)
from phase165_r57_r20_general_specialization import specialize_typed_statement
from proof import Relation


def test_prop51_n3_is_not_a_registered_candidate():
    bridge = build_adopted_prop51_reference()
    assert specialized_eta_group_goal_candidates(TodaPrimaryGroup(4, 3), bridge) == ()


def test_prop51_n3_expansion_returns_empty_instead_of_raising():
    bridge = build_adopted_prop51_reference()
    source = _fixed_typed_relations(bridge)[0]
    from homotopy_groups import FiniteCyclicGroup
    from expression import HomotopyElement, GeneratorSymbol
    goal = Relation(TodaPrimaryGroup(4, 3), FiniteCyclicGroup(2, HomotopyElement(
        name="η_3", dimension=3, source=4, target=3,
        generator=GeneratorSymbol("η", 3))))
    assert expand_registered_eta_specialization(goal, (source,)) == ()
    assert specialize_typed_statement(source, goal) is None


def test_prop51_n4_remains_specializable():
    bridge = build_adopted_prop51_reference()
    group = TodaPrimaryGroup(5, 4)
    goals = specialized_eta_group_goal_candidates(group, bridge)
    assert len(goals) == 1
    source = _fixed_typed_relations(bridge)[0]
    assert specialize_eta_group_relation(source, 4) == goals[0]
    assert len(expand_registered_eta_specialization(goals[0], (source,))) == 1


def test_range_is_preserved_on_registered_composite():
    bridge = build_adopted_prop51_reference()
    assertion = next(iter(bridge.registry._assertions.values()))
    assert ("clause_ranges", (("higher_eta_group_relation", "n", 4),)) in assertion.scope


def test_source_functions_have_closed_n3_gate():
    module_path = Path(__file__).resolve().parent.parent / "phase165_r57_r8_eta_specialization.py"
    tree = ast.parse(module_path.read_text(encoding="utf-8"))
    for function_name in ("specialized_eta_group_goal_candidates", "expand_registered_eta_specialization"):
        function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == function_name)
        comparisons = [node for node in ast.walk(function) if isinstance(node, ast.Compare) and
                       isinstance(node.left, ast.Name) and node.left.id == "n" and
                       len(node.ops) == 1 and isinstance(node.ops[0], ast.Lt) and
                       len(node.comparators) == 1 and isinstance(node.comparators[0], ast.Constant)]
        assert any(node.comparators[0].value == 4 for node in comparisons)
