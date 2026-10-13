import pytest

from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from phase165_r14_r2_toda51 import (
    TODA_51_SCHEMAS,
    Toda51Clause,
    instantiate_toda51_clause,
)
from proof import Relation


def test_toda51_general_schemas_have_explicit_ranges():
    assert len(TODA_51_SCHEMAS) == 2
    assert [(c.bound_variable, c.minimum, c.strict) for c in TODA_51_SCHEMAS] == [
        ("i", 1, True), ("n", 1, False)
    ]
    assert all(not c.proof_eligible for c in TODA_51_SCHEMAS)


def test_toda51_sphere_one_zero_is_general():
    for i in (2, 3, 8):
        result = instantiate_toda51_clause(TODA_51_SCHEMAS[0], i)
        assert isinstance(result, Relation)
        assert result.lhs == TodaPrimaryGroup(group_dimension=i, sphere_dimension=1)
        assert result.rhs == 0


def test_toda51_diagonal_is_general():
    for n in (1, 2, 3, 9):
        result = instantiate_toda51_clause(TODA_51_SCHEMAS[1], n)
        assert result.lhs == TodaPrimaryGroup(group_dimension=n, sphere_dimension=n)
        assert isinstance(result.rhs, FreeCyclicGroup)
        assert result.rhs.generator.generator.index == n


@pytest.mark.parametrize("clause,index", [
    (0, 1), (0, 0), (1, 0), (0, -2), (1, -2), (0, True)
])
def test_toda51_rejects_out_of_scope(clause, index):
    with pytest.raises(ValueError):
        instantiate_toda51_clause(TODA_51_SCHEMAS[clause], index)


def test_toda51_cannot_self_authorize():
    with pytest.raises(ValueError, match="promoted"):
        Toda51Clause("sphere_one_zero", "i", 1, True, proof_eligible=True)
