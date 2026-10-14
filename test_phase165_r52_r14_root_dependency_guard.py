"""R52-R14 targeted regressions: fixed claims are not their own proofs."""
from pathlib import Path

from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from hopf_facts import ETA_2
from phase165_r14_r38_direct_registry import build_adopted_typed_reference_registry
from phase165_r52_r13_reference_registration import build_adopted_prop51_reference
from phase165_r52_r9_shared_math import build_shared_typed_bridge, search_shared_group_goal
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r3_recursive_search import _typed_reference_steps
from proof import ProofRule, Relation


def _bridge():
    adopted = Path(__file__).resolve().with_name("phase165_r14_r39_toda51.tex")
    return build_shared_typed_bridge(sources=(
        build_adopted_typed_reference_registry(adopted),
        build_adopted_prop51_reference(),
    ))


def test_r14_prop51_is_registered_but_pi32_not_used_as_own_leaf():
    bridge = _bridge()
    goal = Relation(TodaPrimaryGroup(3, 2), FreeCyclicGroup(ETA_2))
    assert len(_typed_reference_steps(bridge, goal)) == 1
    result = search_shared_group_goal(n=2, k=1, group_structure=FreeCyclicGroup(ETA_2), bridge=bridge)
    assert result.status is ProofSearchStatus.COMPLETE
    roots = [step for step in result.proven_steps if step.conclusion == goal]
    assert len(roots) == 1
    assert roots[0].rule is ProofRule.INFERENCE
    assert not any(step.rule is ProofRule.GIVEN and step.conclusion == goal for step in result.proven_steps)
    assert len(_typed_reference_steps(bridge, goal)) == 1


def test_r14_same_reference_available_for_different_goal():
    bridge = _bridge()
    statement = next(a.content for a in bridge.registry._assertions.values()
                     if getattr(a.content, "delta_iota5_relation", None) is not None)
    goal = statement.pi3_2_group_relation
    assert len(_typed_reference_steps(bridge, goal)) == 1
    assert len(_typed_reference_steps(bridge, statement.delta_iota5_relation)) == 1


def test_r14_direct_root_reference_without_inference_is_not_a_proof():
    from phase165_r52_r13_reference_registration import register_adopted_composite_reference
    from dataclasses import dataclass
    from phase165_r52_r12_component_bridge import expand_cited_given_components
    @dataclass(frozen=True)
    class Claims:
        target: object
        auxiliary: str
    goal = Relation(TodaPrimaryGroup(3, 2), FreeCyclicGroup(ETA_2))
    source = register_adopted_composite_reference(
        assertion_id="r14:toy", locator="Proposition toy", source_id="adopted",
        content=Claims(goal, "aux"),
    )
    bridge = build_shared_typed_bridge(sources=(source,))
    result = search_shared_group_goal(n=2, k=1, group_structure=FreeCyclicGroup(ETA_2),
                                      bridge=bridge, expansion_provider=lambda goal: ())
    assert result.status is ProofSearchStatus.SEARCH_FAILED
    assert result.conclusion is None
