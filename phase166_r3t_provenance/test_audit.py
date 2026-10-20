"""Focused checks of the R3-T provenance traversal (no production mutation)."""
from dataclasses import dataclass

from proof import Relation
from homotopy_groups import TodaPrimaryGroup, FiniteCyclicGroup
from phase166_r3t_provenance.audit import relations_inside


@dataclass(frozen=True)
class Composite:
    statements: tuple[Relation, ...]


def test_relation_traversal_in_nested_registered_statement():
    goal = Relation(TodaPrimaryGroup(5, 4), FiniteCyclicGroup(2, 'eta4'))
    assert tuple(relations_inside(Composite((goal,)))) == (goal,)


def test_relation_traversal_has_no_implicit_proof_step():
    goal = Relation(TodaPrimaryGroup(4, 3), FiniteCyclicGroup(2, 'eta3'))
    assert tuple(relations_inside((Composite((goal,)),))) == (goal,)
