from expression import Composition, GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r52_r27_r5_literature import Toda52UniversalStatement
from phase168_r2_toda52_transport import expand_toda52_finite_cyclic_goal
from proof import Relation, RelationType


def _goal():
    eta2 = HomotopyElement(name="η₂", dimension=2, source=3, target=2,
                           generator=GeneratorSymbol(family="η", index=2))
    eta3 = HomotopyElement(name="η₃", dimension=3, source=4, target=3,
                           generator=GeneratorSymbol(family="η", index=3))
    return Relation(TodaPrimaryGroup(4, 2), FiniteCyclicGroup(2, Composition(eta2, eta3)),
                    RelationType.EQUALITY)


def test_toda52_requires_screened_theorem():
    assert expand_toda52_finite_cyclic_goal(_goal(), ()) == ()


def test_toda52_yields_two_proof_goals():
    result = expand_toda52_finite_cyclic_goal(_goal(), (Toda52UniversalStatement(),))
    assert len(result) == 1
    assert len(result[0].subgoals) == 2
    assert result[0].subgoals[0].lhs == TodaPrimaryGroup(4, 3)
    assert result[0].subgoals[1] == Toda52UniversalStatement()


def test_toda52_rejects_wrong_target():
    assert expand_toda52_finite_cyclic_goal(
        Relation(TodaPrimaryGroup(5, 3), _goal().rhs, RelationType.EQUALITY),
        (Toda52UniversalStatement(),),
    ) == ()
