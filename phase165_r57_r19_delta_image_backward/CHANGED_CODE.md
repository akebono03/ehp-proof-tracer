# 変更コード全文

## 変更一覧

- `phase165_r52_r9_shared_math.py`：`shared_expansion_provider()` 全体を置換。import 変更なし。
- 新規 `phase165_r57_r19_delta_image_backward.py`：root 直下へ追加。
- 新規 `phase165_r57_r19_delta_image_backward/test_phase165_r57_r19_delta_image_backward.py`：テスト6件。
- `phase165_r57_r19_delta_image_backward/install.py`：インストーラー。
- Renderer や文献命題には変更なし。

## shared_expansion_provider() 全体

```python
def shared_expansion_provider(bridge: RegistryBridgeResult, extra_providers: tuple = (), *, proof_target=None, prior_conclusions: tuple = ()):
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

    if not isinstance(prior_conclusions, tuple):
        raise TypeError("prior_conclusions must be a tuple")

    from phase165_r57_r7_stable_expansion import (
        expand_registered_toda45_finite_cyclic_goal,
    )
    from phase165_r57_r8_eta_specialization import (
        expand_registered_eta_specialization,
    )

    from phase165_r57_r11_proof_order_gate import retain_ordered_root_expansions
    from phase165_r57_r19_delta_image_backward import expand_registered_delta_image_goal

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
        options.extend(expand_registered_toda45_finite_cyclic_goal(goal, tuple(available) + prior_conclusions))
        options.extend(expand_registered_eta_specialization(goal, tuple(available)))
        options.extend(expand_registered_delta_image_goal(goal, tuple(available)))
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

## 新規モジュール全体（import を含む）

```python
"""R57-R19: reverse existing free-cyclic Delta image rule over cited typed leaves.

No group-specific result or unverified GIVEN is generated. Exact statement
identity, including generator expressions, is required for a proposal.
"""
from __future__ import annotations

from homotopy_groups import FreeCyclicGroup
from phase165_r3_recursive_search import GoalExpansion
from proof import Relation, RelationType
from toda_delta_image_rules import free_cyclic_generator_delta_image_inference_rule
from toda_rules import TodaDeltaImageFreeCyclicStatement, TodaDeltaImageUpToSignStatement


def expand_registered_delta_image_goal(
    goal: object, available_statements: tuple[object, ...]
) -> tuple[GoalExpansion, ...]:
    """Reverse the existing rule using only screened signed-Delta references.

    The source's group relation is an independent proof subgoal, not a GIVEN.
    Ambiguous signed-source witnesses fail closed rather than being guessed.
    """
    if not isinstance(available_statements, tuple):
        raise TypeError("available_statements must be a tuple")
    if not isinstance(goal, TodaDeltaImageFreeCyclicStatement):
        return ()
    if not isinstance(goal.image_group, FreeCyclicGroup):
        return ()
    witnesses = tuple(
        statement for statement in available_statements
        if isinstance(statement, TodaDeltaImageUpToSignStatement)
        and statement.map == goal.map
        and statement.positive_value == goal.image_group.generator
    )
    if len(witnesses) != 1:
        return ()
    witness = witnesses[0]
    source_relation = Relation(
        lhs=goal.map.source_group,
        rhs=FreeCyclicGroup(generator=witness.element),
        relation_type=RelationType.EQUALITY,
    )
    return (GoalExpansion(
        rule=free_cyclic_generator_delta_image_inference_rule(),
        subgoals=(source_relation, witness),
    ),)

```

## 新規テスト全体（import を含む）

```python
"""Focused R57-R19 mathematical and search integration checks."""
from __future__ import annotations

from expression import GeneratorSymbol, HomotopyElement, Multiple
from homotopy_groups import FreeCyclicGroup, TodaDeltaMap, TodaPrimaryGroup
from phase165_r57_r19_delta_image_backward import expand_registered_delta_image_goal
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule
from phase164_r8_proofstep_factory import derive_inference_proof_step
from toda_rules import TodaDeltaImageFreeCyclicStatement, TodaDeltaImageUpToSignStatement


def _case():
    source = TodaPrimaryGroup(5, 5)
    target = TodaPrimaryGroup(3, 2)
    delta = TodaDeltaMap(source, target)
    iota = HomotopyElement(name="ι_5", dimension=5,
                           generator=GeneratorSymbol(family="ι", index=5))
    eta = HomotopyElement(name="η₂", dimension=2, source=3, target=2,
                          generator=GeneratorSymbol(family="η", index=2))
    multiple = Multiple(coefficient=2, expression=eta)
    witness = TodaDeltaImageUpToSignStatement(map=delta, element=iota, positive_value=multiple)
    goal = TodaDeltaImageFreeCyclicStatement(map=delta, image_group=FreeCyclicGroup(multiple))
    group = Relation(source, FreeCyclicGroup(iota), relation_type=RelationType.EQUALITY)
    return goal, witness, group


def test_r19_reverse_requires_exact_cited_signed_delta():
    goal, witness, source = _case()
    expansion = expand_registered_delta_image_goal(goal, (witness,))
    assert len(expansion) == 1
    assert expansion[0].subgoals == (source, witness)


def test_r19_forward_rule_derives_exact_target_from_proved_premises():
    goal, witness, source = _case()
    expansion = expand_registered_delta_image_goal(goal, (witness,))[0]
    premises = (ProofStep(conclusion=source, premises=(), rule=ProofRule.GIVEN),
                ProofStep(conclusion=witness, premises=(), rule=ProofRule.GIVEN))
    matches = find_inference_matches_for_rule(expansion.rule, premises)
    assert len(matches) == 1
    step = derive_inference_proof_step(matches[0])
    assert step.conclusion == goal
    assert step.rule is ProofRule.INFERENCE


def test_r19_no_signed_reference_no_expansion():
    goal, witness, source = _case()
    assert expand_registered_delta_image_goal(goal, ()) == ()
    assert expand_registered_delta_image_goal(goal, (source,)) == ()


def test_r19_ambiguous_signed_references_fail_closed():
    goal, witness, _ = _case()
    assert expand_registered_delta_image_goal(goal, (witness, witness)) == ()


def test_r19_unrelated_image_is_not_derived():
    goal, witness, _ = _case()
    wrong = TodaDeltaImageFreeCyclicStatement(goal.map, FreeCyclicGroup(witness.element))
    assert expand_registered_delta_image_goal(wrong, (witness,)) == ()


def test_r19_shared_provider_uses_only_registered_delta_witness():
    bridge = build_shared_typed_bridge()
    goal, witness, source = _case()
    available = tuple(link.step.conclusion for link in bridge.proof_links
                      if link.step is not None and link.step.rule is ProofRule.GIVEN)
    options = shared_expansion_provider(bridge, proof_target=goal)(goal)
    matches = tuple(option for option in options if getattr(option.rule, "name", "") == "free cyclic generator Delta image")
    if witness in available:
        assert len(matches) == 1
        assert matches[0].subgoals == (source, witness)
    else:
        assert matches == ()

```

## 完了条件・次の境界

登録済みの符号付き Delta 命題があるときだけ逆展開し、自由生成の前提は別 Goal として残す。対象 pytest が成功すること。残る完全性などは次の段階。
