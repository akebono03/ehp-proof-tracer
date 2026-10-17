from phase165_prop51_range_guard import allows_typed_specialization
from phase165_r52_r13_reference_registration import build_adopted_prop51_reference
from phase165_r57_r8_eta_specialization import specialize_eta_group_relation
from phase165_r57_r20_general_specialization import specialize_typed_statement
import pytest


def source_and_bridge():
    bridge = build_adopted_prop51_reference()
    source = next(iter(bridge.registry._assertions.values())).content.higher_eta_group_relation
    return source, bridge


def test_scope_metadata_registered():
    _, bridge = source_and_bridge()
    scope = next(iter(bridge.registry._assertions.values())).scope
    assert ('clause_ranges', (('higher_eta_group_relation','n',4),)) in scope


def test_lower_boundary_rejected_by_both_specializations():
    source, _ = source_and_bridge()
    # Concrete goal shape exists mathematically, but this fixed claim cannot justify it.
    from dataclasses import replace
    from expression import HomotopyElement, GeneratorSymbol
    from homotopy_groups import TodaPrimaryGroup, FiniteCyclicGroup
    target = replace(source, lhs=TodaPrimaryGroup(4,3), rhs=FiniteCyclicGroup(2, HomotopyElement(name='η_3',dimension=3,source=4,target=3,generator=GeneratorSymbol('η',3))))
    assert specialize_typed_statement(source,target) is None
    with pytest.raises(ValueError, match='n >= 4'):
        specialize_eta_group_relation(source,3)
    assert not allows_typed_specialization(source, {'n':3})


def test_n4_accepted():
    source, _ = source_and_bridge()
    goal = specialize_eta_group_relation(source,4)
    assert specialize_typed_statement(source,goal) == (('n',4),)
    assert allows_typed_specialization(source, {'n':4})
