# R57-R11 変更対象とコード全文

1. `phase165_r52_r9_shared_math.py` — `shared_expansion_provider` 関数全体・`search_shared_group_goal` 関数全体を置換。import 部は変更なし。
2. `phase165_r57_r11_proof_order_gate.py` — 新規モジュール、すべての関数を追加。
3. `phase165_r57_r10_proofstep_fidelity/test_phase165_r57_r10_proofstep_fidelity.py` — 旧期待値を修正、import とテスト関数の全文置換。
4. `phase165_r57_r11_proof_order_gate/test_phase165_r57_r11_proof_order_gate.py` — 新規テスト全文。
5. `phase165_r57_r11_proof_order_gate/install.py`, `update_regression_test.py`, `run.ps1` — 新規。

## `shared_expansion_provider` 全文

```python
def shared_expansion_provider(bridge: RegistryBridgeResult, extra_providers: tuple = (), *, proof_target=None):
    """Build backward proposals from typed source witnesses and common rules."""
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    available = []
    for link in bridge.proof_links:
        if link.step is None or link.step.rule is not ProofRule.GIVEN:
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        if assertion.origin is AssertionOrigin.FIXED_STATEMENT:
            available.append(link.step.conclusion)

    from phase165_r57_r7_stable_expansion import (
        expand_registered_toda45_finite_cyclic_goal,
    )
    from phase165_r57_r8_eta_specialization import (
        expand_registered_eta_specialization,
    )

    from phase165_r57_r11_proof_order_gate import retain_ordered_root_expansions

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        options = []
        if (isinstance(goal, Relation)
                and goal.relation_type is RelationType.EQUALITY
                and isinstance(goal.rhs, FreeCyclicGroup)
                and isinstance(goal.lhs, TodaPrimaryGroup)):
            for image in available:
                if not isinstance(image, GeneratorImage):
                    continue
                if (getattr(image.map, "source_group", None) != goal.lhs
                        or image.source_generator != goal.rhs.generator):
                    continue
                options.append(GoalExpansion(
                    reverse_free_cyclic_transport_rule(),
                    (MapIsomorphism(image.map),
                     Relation(image.map.target_group,
                              FreeCyclicGroup(image.target_generator)),
                     image),
                ))
        options.extend(expand_registered_toda45_finite_cyclic_goal(goal, tuple(available)))
        options.extend(expand_registered_eta_specialization(goal, tuple(available)))
        for provider in (
            expand_generic_iso_goal,
            expand_generic_ehp_hopf_goal,
            expand_delta_zero_from_suspension_iso,
            expand_diagonal_suspension,
            expand_existing_pi43_rules,
            *extra_providers,
        ):
            new = provider(goal)
            if not isinstance(new, tuple) or not all(isinstance(x, GoalExpansion) for x in new):
                raise TypeError("expansion provider contract violated")
            options.extend(new)
        return retain_ordered_root_expansions(proof_target, goal, tuple(options))
    return expand
```

## `search_shared_group_goal` 全文

```python
def search_shared_group_goal(*, n: int, k: int, group_structure: object,
                              bridge: RegistryBridgeResult | None = None,
                              expansion_provider=None,
                              citing_assertion_id: str | None = None,
                              verified_assertion_ids: tuple[str, ...] = (), completed_internal_proofs: tuple = (), proof_use_order=None):
    """Run canonical search under a screened Reference context.

    Older calls retain their signature. R15 ordering is applied to sources
    outside the explicitly adopted-Tex policy; no IDs are auto-verified.
    """
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context

    if bridge is None:
        bridge = build_shared_typed_bridge()
    goal = Relation(TodaPrimaryGroup(n + k, n), group_structure)
    assertions = tuple(bridge.registry._assertions.values())
    if not assertions:
        raise ValueError("shared typed registry is empty")
    context_id = citing_assertion_id or assertions[0].assertion_id
    proof_context = screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=context_id,
        verified_assertion_ids=verified_assertion_ids,
    )
    if proof_use_order == "registered":
        from phase165_r52_r19_prop51_binding import resolve_registered_proof_use_order
        proof_use_order = resolve_registered_proof_use_order(proof_context, goal)
    if proof_use_order is not None:
        from phase165_r52_r18_proof_order import restrict_by_proof_use_order
        proof_context = restrict_by_proof_use_order(
            proof_context, goal=goal, policy=proof_use_order,
        )
    if expansion_provider is None:
        expansion_provider = shared_expansion_provider(proof_context, proof_target=goal)
    return search_registered_partial_proof(
        n=n, k=k, goal=goal, bridge=proof_context,
        citing_assertion_id=context_id,
        expansion_provider=expansion_provider,
        lookup_mode="typed_reference",
        structure_status=GroupStructureStatus.UNKNOWN,
        completed_internal_proofs=completed_internal_proofs,
    )
```

## 新規順序制約モジュール全文

```python
"""R57-R11: fail closed when a root group is only its own symbolic specialization.

This is a proof-use-order boundary, distinct from the publication order of
Toda references. It neither fabricates predecessor proofs nor GIVEN leaves.
"""
from __future__ import annotations

from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion
from proof import Relation, RelationType


def is_unordered_root_structure_specialization(
    root_goal: object, current_goal: object, expansion: GoalExpansion,
) -> bool:
    """Reject direct symbolic structural facts about the requested group.

    A symbolic group theorem may be used as a mathematical reference, but
    without reviewed proof-use ordering it is not accepted as the *derivation*
    of the same requested group's structure. Other inference branches survive.
    """
    structures = (FiniteCyclicGroup, FreeCyclicGroup, DirectSumGroup)
    if not isinstance(expansion, GoalExpansion):
        raise TypeError("expansion must be GoalExpansion")
    if not (
        isinstance(root_goal, Relation)
        and root_goal.relation_type is RelationType.EQUALITY
        and isinstance(root_goal.lhs, TodaPrimaryGroup)
        and isinstance(root_goal.rhs, structures)
        and isinstance(current_goal, Relation)
        and current_goal == root_goal
    ):
        return False
    for premise in expansion.subgoals:
        if not (
            isinstance(premise, Relation)
            and premise.relation_type is RelationType.EQUALITY
            and isinstance(premise.lhs, TodaPrimaryGroup)
            and isinstance(premise.rhs, structures)
        ):
            continue
        source_group = premise.lhs
        if source_group == root_goal.lhs:
            return True
        if not isinstance(source_group.sphere_dimension, int):
            return True
    return False


def retain_ordered_root_expansions(
    root_goal: object, current_goal: object,
    expansions: tuple[GoalExpansion, ...],
) -> tuple[GoalExpansion, ...]:
    """Retain only root derivations which do not self-cite a generic structure.

    This does not establish a global total ordering of all Toda groups. Such
    ordering needs registered predecessor metadata, and remains a separate gate.
    """
    if not isinstance(expansions, tuple):
        raise TypeError("expansions must be a tuple")
    return tuple(
        option for option in expansions
        if not is_unordered_root_structure_specialization(root_goal, current_goal, option)
    )
```

## 新規テスト全文

```python
"""R57-R11: target ordering is a proof-path constraint, not presentation."""
from __future__ import annotations

from phase165_r52_r12_component_bridge import expand_cited_given_components
from phase165_r52_r13_reference_registration import build_adopted_prop51_reference
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase165_r57_r8_eta_specialization import (
    _fixed_typed_relations, specialize_eta_group_relation,
)
from phase165_r57_r11_proof_order_gate import (
    is_unordered_root_structure_specialization, retain_ordered_root_expansions,
)
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from proof import Relation


def _proof_fixture():
    source_bridge = build_adopted_prop51_reference()
    source, = _fixed_typed_relations(source_bridge)
    bridge = expand_cited_given_components(source_bridge)
    goal = specialize_eta_group_relation(source, 4)
    return source, bridge, goal


def test_r11_root_cannot_use_same_group_symbolic_structure():
    source, bridge, goal = _proof_fixture()
    expansions = shared_expansion_provider(bridge)(goal)
    direct = tuple(x for x in expansions if x.subgoals == (source,))
    assert len(direct) == 1
    assert is_unordered_root_structure_specialization(goal, goal, direct[0])
    assert retain_ordered_root_expansions(goal, goal, direct) == ()


def test_r11_proof_target_is_wired_to_shared_provider():
    source, bridge, goal = _proof_fixture()
    expansions = shared_expansion_provider(bridge, proof_target=goal)(goal)
    assert not any(x.subgoals == (source,) for x in expansions)


def test_r11_nonroot_goal_preserves_generic_specialization_mechanism():
    source, bridge, goal = _proof_fixture()
    other = Relation(goal.lhs, goal.rhs)
    # No proof root supplied: the generic mathematical inference remains usable.
    assert any(x.subgoals == (source,) for x in shared_expansion_provider(bridge)(other))


def test_r11_public_target_does_not_claim_unordered_direct_proof():
    result = search_group_from_registered_goal(n=4, k=1)
    assert result.status is not ProofSearchStatus.COMPLETE
    assert result.conclusion is None
    assert result.open_goals
    assert not any("higher-eta specialization" in str(s.inference_rule) for s in result.proven_steps)


def test_r11_pi32_prerequisite_path_survives():
    result = search_group_from_registered_goal(n=2, k=1)
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.conclusion is not None
```

## 更新した R57-R10 テスト全文

```python
"""R57-R10 proof fidelity retained under the strict R57-R11 root order gate."""
from __future__ import annotations

from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r57_r10_step_narrative import has_transport_proof_ancestry


def test_r10_unordered_pi54_specialization_not_claimed_as_proved():
    result = search_group_from_registered_goal(n=4, k=1)
    assert result.status is not ProofSearchStatus.COMPLETE
    assert result.conclusion is None
    assert result.open_goals
    assert not any(has_transport_proof_ancestry(s) for s in result.proven_steps)


def test_r10_incomplete_proof_must_not_gain_conclusion_in_renderer():
    from phase165_r52_partial_proof import render_partial_proof_markdown
    text = render_partial_proof_markdown(search_group_from_registered_goal(n=4, k=1))
    assert "証明" in text
    assert "未解決" in text or "未完成" in text
    assert "[R1]を " not in text
    assert "以上より" not in text


def test_r10_existing_pi32_narrative_is_preserved():
    from phase165_r52_partial_proof import render_partial_proof_markdown
    text = render_partial_proof_markdown(search_group_from_registered_goal(n=2, k=1))
    assert "使用する結果" in text
    assert "証明" in text
    assert "□" in text


def test_r10_adapter_does_not_remove_legacy_renderer():
    text = Path(__file__).resolve().parent.parent.joinpath("toda_group_proof_narrative_renderer.py").read_text(encoding="utf-8")
    assert "_phase160_r7_render_stable_finite_cyclic_transport_narrative" in text
```
