"""Typed shape and rejection fixtures, not fabricated accepted proofs."""
from types import SimpleNamespace

from expression import Composition, GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r52_partial_proof import ProofSearchStatus
from phase176_r3r55_equality_display_isolated.projection import (
    is_composition_transport, is_finite_cyclic_conversion, is_symmetry,
    is_transitivity, project_redundant_equalities,
)
from proof import Relation


def element(name, target, source):
    return HomotopyElement(name, target, source, target, GeneratorSymbol(name, target))


def test_exact_symmetry_not_matching_display():
    a, b, c = (element(name, 4, 5) for name in ('a', 'b', 'c'))
    assert is_symmetry(Relation(b,a), Relation(a,b))
    assert not is_symmetry(Relation(c,a), Relation(a,b))
    assert not is_symmetry(Relation(b,a), Relation(a,c))


def test_exact_transitivity_requires_shared_typed_middle():
    a, b, c, d = (element(name, 4, 5) for name in ('a', 'b', 'c', 'd'))
    assert is_transitivity(Relation(a,c), Relation(a,b), Relation(b,c))
    assert not is_transitivity(Relation(a,c), Relation(a,b), Relation(d,c))
    assert not is_transitivity(Relation(a,d), Relation(a,b), Relation(b,c))


def test_composition_transport_requires_unchanged_factor():
    a, b = (element(name, 4, 5) for name in ('a', 'b'))
    x, y = (element(name, 5, 6) for name in ('x', 'y'))
    assert is_composition_transport(Relation(Composition(a,x), Composition(b,x)), Relation(a,b))
    assert is_composition_transport(Relation(Composition(a,x), Composition(a,y)), Relation(x,y))
    assert not is_composition_transport(Relation(Composition(a,x), Composition(b,y)), Relation(a,b))


def test_finite_cyclic_conversion_requires_exact_order_group_generator():
    a, b = (element(name, 4, 5) for name in ('a', 'b'))
    g = TodaPrimaryGroup(5,4)
    structure = CyclicStructureStatement(g,a,2)
    assert is_finite_cyclic_conversion(structure, Relation(g,FiniteCyclicGroup(2,a)))
    assert not is_finite_cyclic_conversion(structure, Relation(g,FiniteCyclicGroup(4,a)))
    assert not is_finite_cyclic_conversion(structure, Relation(g,FiniteCyclicGroup(2,b)))
    assert not is_finite_cyclic_conversion(structure, Relation(TodaPrimaryGroup(6,5),FiniteCyclicGroup(2,a)))


def test_partial_and_invalid_models_do_not_project():
    assert project_redundant_equalities(SimpleNamespace(status=ProofSearchStatus.PARTIAL), ()) == {}
    assert project_redundant_equalities(SimpleNamespace(status=ProofSearchStatus.COMPLETE, open_goals=('pending',)), ()) == {}
    assert project_redundant_equalities(SimpleNamespace(status=ProofSearchStatus.COMPLETE), ()) == {}
