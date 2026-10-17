"""Scope check for the typed symbolic higher-eta clause of Toda Proposition 5.1.

Only the exact typed family with eta_n is recognized. Other symbolic
statements retain existing behavior. The n >= 4 limit is adopted scope data.
"""
from expression import ScalarSum, ScalarSymbol, GeneratorSymbol, HomotopyElement
from homotopy_groups import TodaPrimaryGroup, FiniteCyclicGroup
from proof import Relation, RelationType


def is_prop51_higher_eta_family(statement: object) -> bool:
    if not isinstance(statement, Relation) or statement.relation_type is not RelationType.EQUALITY:
        return False
    group, structure = statement.lhs, statement.rhs
    if not isinstance(group, TodaPrimaryGroup) or not isinstance(structure, FiniteCyclicGroup):
        return False
    n = group.sphere_dimension
    eta = structure.generator
    return (
        isinstance(n, ScalarSymbol)
        and group.group_dimension == ScalarSum(left=n, right=1)
        and structure.order == 2
        and isinstance(eta, HomotopyElement)
        and eta.dimension == n
        and eta.source == ScalarSum(left=n, right=1)
        and eta.target == n
        and isinstance(eta.generator, GeneratorSymbol)
        and eta.generator.family == 'η'
        and eta.generator.index == n
    )


def allows_typed_specialization(source: object, bindings: dict[str, int]) -> bool:
    """Enforce the adopted domain of Proposition 5.1 higher-eta clause."""
    if not is_prop51_higher_eta_family(source):
        return True
    n = bindings.get(source.lhs.sphere_dimension.name)
    return type(n) is int and n >= 4
