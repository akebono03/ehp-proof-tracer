"""Conservative typed specialization of registered higher-stem group clauses.

Only the already registered general eta-squared and nu clauses are supported.
No proof steps or assertions are created by this module.
"""
from __future__ import annotations

from expression import Composition, GeneratorSymbol, HomotopyElement, ScalarSum, ScalarSymbol
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase166_r3aj_structured_generator import structured_generator_from_ids
from proof import Relation, RelationType
from pathlib import Path


def _symbolic_index(value, variable, offset):
    if offset == 0:
        return value == variable
    return (isinstance(value, ScalarSum) and value.left == variable
            and value.right == offset)


def _symbolic_factor(value, variable, offset, family):
    return (isinstance(value, HomotopyElement)
            and _symbolic_index(value.dimension, variable, offset)
            and value.generator == GeneratorSymbol(family=family,
                index=variable if offset == 0 else ScalarSum(variable, offset)))


def _registered_clause_kind(statement):
    if not isinstance(statement, Relation) or statement.relation_type is not RelationType.EQUALITY:
        return None
    lhs, rhs = statement.lhs, statement.rhs
    if not isinstance(lhs, TodaPrimaryGroup) or not isinstance(rhs, FiniteCyclicGroup):
        return None
    variable = lhs.sphere_dimension
    if not isinstance(variable, ScalarSymbol):
        return None
    if rhs.order == 2 and _symbolic_index(lhs.group_dimension, variable, 2):
        generator = rhs.generator
        if (isinstance(generator, Composition)
                and _symbolic_factor(generator.left, variable, 0, "η")
                and _symbolic_factor(generator.right, variable, 1, "η")):
            return "eta_squared"
    if rhs.order == 8 and _symbolic_index(lhs.group_dimension, variable, 3):
        if _symbolic_factor(rhs.generator, variable, 0, "ν"):
            return "nu"
    return None


def specialize_registered_higher_stem(statement, sphere_dimension):
    """Return a checked concrete candidate or None; never assert a proof step."""
    if type(sphere_dimension) is not int:
        return None
    kind = _registered_clause_kind(statement)
    if kind == "eta_squared" and sphere_dimension >= 5:
        identifiers, stem = (2, 2), 2
    elif kind == "nu" and sphere_dimension >= 6:
        identifiers, stem = (4,), 3
    else:
        return None
    generator_csv = Path(__file__).resolve().parent.parent / "data" / "HyoujiGen.csv"
    if not generator_csv.is_file():
        return None
    generator = structured_generator_from_ids(
        ids=identifiers, start_dimension=sphere_dimension,
        generator_csv=generator_csv,
    )
    if generator is None:
        return None
    return Relation(
        TodaPrimaryGroup(sphere_dimension + stem, sphere_dimension),
        FiniteCyclicGroup(statement.rhs.order, generator),
        RelationType.EQUALITY,
    )
