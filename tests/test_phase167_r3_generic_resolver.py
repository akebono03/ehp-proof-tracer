from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import (
    registered_group_goal_candidates,
    search_group_from_registered_goal,
)
from phase165_r52_partial_proof import ProofSearchStatus
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase166_r3c_publication_order import precedes_citing_assertion
from proof import ProofRule


def test_phase167_r3_registered_goals_resolve_without_dimension_gate():
    bridge = build_shared_typed_bridge()
    for n in (2, 3):
        candidates = registered_group_goal_candidates(bridge, n=n, k=1)
        assert len(candidates) == 1
        citing_id = resolve_specialized_goal_citing_id(bridge, candidates[0])
        assert citing_id is not None
        assert bridge.registry.assertion(citing_id).content == candidates[0]


def test_phase167_r3_completed_proofs_use_only_preceding_givens():
    bridge = build_shared_typed_bridge()
    for n in (2, 3):
        result = search_group_from_registered_goal(n=n, k=1, bridge=bridge)
        assert result.status is ProofSearchStatus.COMPLETE
        citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
        assert citing_id is not None
        givens = [step for step in result.proven_steps if step.rule is ProofRule.GIVEN]
        assert givens
        for step in givens:
            assert step.conclusion != result.conclusion
            assert any(
                assertion.content == step.conclusion
                and precedes_citing_assertion(bridge, assertion.assertion_id, citing_id)
                for assertion in bridge.registry._assertions.values()
            ), (n, step.conclusion)


def test_phase167_r3_invalid_generic_specialization_returns_none():
    from types import SimpleNamespace
    from expression import GeneratorSymbol, HomotopyElement, ScalarSum, ScalarSymbol
    from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
    from proof import Relation
    from unified_statement_registry import AssertionOrigin

    n = ScalarSymbol("n")
    general = Relation(
        TodaPrimaryGroup(ScalarSum(n, 1), n),
        FiniteCyclicGroup(2, HomotopyElement(
            name="eta_n", dimension=n, source=ScalarSum(n, 1),
            target=n, generator=GeneratorSymbol(family="η", index=n)
        )),
    )
    assertion = SimpleNamespace(
        origin=AssertionOrigin.FIXED_STATEMENT, assertion_id="general",
        content=general, component_position=100, reference_id="reference",
    )
    registry = SimpleNamespace(
        _assertions={"general": assertion},
        reference=lambda rid: SimpleNamespace(publication_position=7800),
    )
    bridge = SimpleNamespace(registry=registry)
    goal = Relation(TodaPrimaryGroup(4, 3), FiniteCyclicGroup(
        2, HomotopyElement(name="η_3", dimension=3, source=4, target=3,
                          generator=GeneratorSymbol(family="η", index=3)),
    ))
    assert resolve_specialized_goal_citing_id(bridge, goal) is None
