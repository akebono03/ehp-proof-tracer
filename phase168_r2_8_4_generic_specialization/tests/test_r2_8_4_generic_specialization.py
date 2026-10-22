from expression import Composition, GeneratorSymbol, HomotopyElement, ScalarSum, ScalarSymbol
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase168_r2_8_4_generic_specialization.specialization import specialize_registered_higher_stem
from proof import Relation, RelationType


def make_eta_statement():
    n = ScalarSymbol("n")
    x = HomotopyElement("eta_n", n, generator=GeneratorSymbol("η", n))
    y = HomotopyElement("eta_n_plus_1", ScalarSum(n, 1),
                        generator=GeneratorSymbol("η", ScalarSum(n, 1)))
    return Relation(TodaPrimaryGroup(ScalarSum(n, 2), n),
                    FiniteCyclicGroup(2, Composition(x, y)), RelationType.EQUALITY)


def make_nu_statement():
    n = ScalarSymbol("n")
    x = HomotopyElement("nu_n", n, generator=GeneratorSymbol("ν", n))
    return Relation(TodaPrimaryGroup(ScalarSum(n, 3), n),
                    FiniteCyclicGroup(8, x), RelationType.EQUALITY)


def test_higher_eta_squared_at_five():
    relation = specialize_registered_higher_stem(make_eta_statement(), 5)
    assert relation.lhs == TodaPrimaryGroup(7, 5)
    assert relation.rhs.order == 2
    assert isinstance(relation.rhs.generator, Composition)
    assert relation.rhs.generator.left.target == 5
    assert relation.rhs.generator.right.source == 7


def test_nu_at_six():
    relation = specialize_registered_higher_stem(make_nu_statement(), 6)
    assert relation.lhs == TodaPrimaryGroup(9, 6)
    assert relation.rhs.order == 8
    assert relation.rhs.generator.source == 9


def test_reject_lower_dimensions():
    assert specialize_registered_higher_stem(make_eta_statement(), 4) is None
    assert specialize_registered_higher_stem(make_nu_statement(), 5) is None


def test_reject_malformed_source():
    statement = make_nu_statement()
    wrong = Relation(statement.lhs, FiniteCyclicGroup(4, statement.rhs.generator), RelationType.EQUALITY)
    assert specialize_registered_higher_stem(wrong, 6) is None
    assert specialize_registered_higher_stem(make_eta_statement(), True) is None


def test_real_bridge_two_new_resolutions():
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    bridge = build_shared_typed_bridge()
    for n, k in ((5, 2), (6, 3)):
        goals = registered_group_goal_candidates(bridge, n=n, k=k)
        assert len(goals) == 1
        assert resolve_specialized_goal_citing_id(bridge, goals[0]) is not None


def test_real_bridge_previous_seven_resolutions():
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    bridge = build_shared_typed_bridge()
    for n, k in ((2, 2), (3, 2), (4, 2), (2, 3), (3, 3), (4, 3), (5, 3)):
        goals = registered_group_goal_candidates(bridge, n=n, k=k)
        assert len(goals) == 1
        assert resolve_specialized_goal_citing_id(bridge, goals[0]) is not None
