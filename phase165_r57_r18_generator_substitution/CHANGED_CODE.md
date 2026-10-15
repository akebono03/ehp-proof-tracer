# R57-R18 変更コード全文

## 変更・追加対象

- `phase165_r52_r23_existing_rule_adapter.py` の `expand_existing_pi43_rules()` 全体。import に変更なし。
- `phase165_r57_r11_proof_order_gate.py` クラスなし・関数全文（import 全文）置換。
- 新規 `phase165_r57_r18_generator_substitution.py` をリポジトリ直下に追加。
- 新規テスト `test_phase165_r57_r18_generator_substitution.py` を配布ディレクトリ内に追加。

## expand_existing_pi43_rules
```python
def expand_existing_pi43_rules(goal: object) -> tuple[GoalExpansion, ...]:
    """Reverse existing rules, without supplying unverified theorem premises.

    For the final named generator, substitute using a *proved* generator
    equality, not a mere textual spelling equivalence. Accept the registry's
    eta_3 display spelling when its typed GeneratorSymbol is eta(3).
    """
    source, target, delta_source, e, delta, eta2, eta3, twice = _objects()
    if isinstance(goal, Relation) and goal.relation_type is RelationType.EQUALITY:
        if goal.lhs == target and isinstance(goal.rhs, FiniteCyclicGroup):
            generator = goal.rhs.generator
            symbol = getattr(generator, "generator", None)
            if (goal.rhs.order == 2
                    and isinstance(generator, HomotopyElement)
                    and getattr(symbol, "family", None) == "η"
                    and getattr(symbol, "index", None) == 3
                    and getattr(symbol, "decoration", None) is None
                    and generator.dimension == eta3.dimension
                    and generator.source == eta3.source
                    and generator.target == eta3.target
                    and generator.name in (eta3.name, "η_3")):
                from phase165_r57_r18_generator_substitution import (
                    finite_cyclic_generator_substitution_rule,
                )
                suspended = Suspension(expression=eta2)
                return (GoalExpansion(
                    finite_cyclic_generator_substitution_rule(),
                    (
                        Relation(target, FiniteCyclicGroup(2, suspended)),
                        Relation(generator, suspended),
                    ),
                ),)
        if goal.lhs == target and goal.rhs == FiniteCyclicGroup(2, Suspension(expression=eta2)):
            return (GoalExpansion(
                rules.toda_pi4_3_finite_cyclic_inference_rule(),
                (
                    Relation(source, FreeCyclicGroup(eta2)),
                    rules.TodaSuspensionKernelFreeCyclicStatement(
                        map=e, kernel_group=FreeCyclicGroup(twice),
                    ),
                    rules.TodaSuspensionSurjectiveStatement(map=e),
                ),
            ),)
    if isinstance(goal, rules.TodaSuspensionKernelFreeCyclicStatement):
        if goal.map == e and goal.kernel_group == FreeCyclicGroup(twice):
            return (GoalExpansion(
                rules.toda_pi4_3_exactness_delta_image_to_suspension_kernel_inference_rule(),
                (
                    rules.TodaDeltaImageFreeCyclicStatement(
                        map=delta, image_group=FreeCyclicGroup(twice),
                    ),
                    rules.TodaProp42ExactnessStatement(
                        TodaEHPExactnessWindow(
                            source_term=delta_source, middle_term=source,
                            target_term=target, first_map=EHP_DELTA_MAP,
                            second_map=EHP_E_MAP,
                        ),
                    ),
                ),
            ),)
    if isinstance(goal, rules.TodaSuspensionSurjectiveStatement):
        if goal.map == e:
            return (GoalExpansion(
                rules.toda_pi4_3_zero_right_implies_suspension_surjective_inference_rule(),
                (
                    TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(4, 5)),
                    rules.TodaProp42ExactnessStatement(
                        TodaEHPExactnessWindow(
                            source_term=source, middle_term=target,
                            target_term=TodaPrimaryGroup(4, 5),
                            first_map=EHP_E_MAP, second_map=EHP_H_MAP,
                        ),
                    ),
                ),
            ),)
    return ()

```

## phase165_r57_r11_proof_order_gate.py
```python
"""R57-R11: fail closed when a root group cites its own structure.

R57-R18 permits *derived* cyclic-generator substitution backed by a separately
proved equality, but never accepts an unproved symbolic structure as a root.
"""
from __future__ import annotations

from expression import Suspension
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion
from proof import Relation, RelationType


def _proved_generator_substitution_shape(root_goal: object, expansion: GoalExpansion) -> bool:
    """Only exempt substitution from an explicitly equal intermediate generator."""
    if getattr(expansion.rule, "name", None) != "generic finite cyclic generator substitution from proved equality":
        return False
    if len(expansion.subgoals) != 2:
        return False
    structure, equality = expansion.subgoals
    if not (isinstance(root_goal, Relation)
            and isinstance(root_goal.rhs, FiniteCyclicGroup)
            and isinstance(structure, Relation)
            and isinstance(structure.rhs, FiniteCyclicGroup)
            and isinstance(equality, Relation)
            and structure.relation_type is RelationType.EQUALITY
            and equality.relation_type is RelationType.EQUALITY):
        return False
    return (
        structure.lhs == root_goal.lhs
        and structure.rhs.order == root_goal.rhs.order
        and isinstance(structure.rhs.generator, Suspension)
        and equality.lhs == root_goal.rhs.generator
        and equality.rhs == structure.rhs.generator
    )


def is_unordered_root_structure_specialization(
    root_goal: object, current_goal: object, expansion: GoalExpansion,
) -> bool:
    """Reject a group-structure root derived from its own structural theorem.

    A generator substitution with a proved equality has independently
    checkable premises, unlike direct self-specialization of a source claim.
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
    if _proved_generator_substitution_shape(root_goal, expansion):
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
    """Retain genuinely derived root steps; reject self-structure specialization."""
    if not isinstance(expansions, tuple):
        raise TypeError("expansions must be a tuple")
    return tuple(
        option for option in expansions
        if not is_unordered_root_structure_specialization(root_goal, current_goal, option)
    )

```

## phase165_r57_r18_generator_substitution.py
```python
"""R57-R18: replace a finite cyclic generator using a proved equality.

No family-specific group result and no GIVEN proof leaf are created.
"""
from __future__ import annotations

from homotopy_groups import FiniteCyclicGroup
from proof import InferenceRule, PremisePattern, Relation, RelationType


def _matching_generator_substitution(premises, bindings):
    source, equality = (step.conclusion for step in premises)
    if not isinstance(source, Relation) or not isinstance(equality, Relation):
        return False
    if source.relation_type is not RelationType.EQUALITY or equality.relation_type is not RelationType.EQUALITY:
        return False
    if not isinstance(source.rhs, FiniteCyclicGroup):
        return False
    return source.rhs.generator == equality.rhs


def _build_generator_substitution(premises):
    source, equality = (step.conclusion for step in premises)
    return Relation(
        lhs=source.lhs,
        rhs=FiniteCyclicGroup(order=source.rhs.order, generator=equality.lhs),
        relation_type=RelationType.EQUALITY,
    )


def finite_cyclic_generator_substitution_rule():
    """Transport a finite cyclic presentation along a proved generator identity."""
    return InferenceRule(
        name="generic finite cyclic generator substitution from proved equality",
        premise_patterns=(
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY),
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY),
        ),
        match_guard=_matching_generator_substitution,
        conclusion_builder=_build_generator_substitution,
    )

```

## test_phase165_r57_r18_generator_substitution.py
```python
"""Focused R57-R18 runtime checks. Run against the installed project."""
from __future__ import annotations

from expression import GeneratorSymbol, HomotopyElement, Suspension
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion
from phase165_r52_r23_existing_rule_adapter import expand_existing_pi43_rules
from phase165_r57_r11_proof_order_gate import retain_ordered_root_expansions
from phase165_r57_r18_generator_substitution import finite_cyclic_generator_substitution_rule
from proof import ProofRule, ProofStep, Relation, find_inference_matches_for_rule
from phase164_r8_proofstep_factory import derive_inference_proof_step


def eta(index: int, name: str) -> HomotopyElement:
    return HomotopyElement(name=name, dimension=index, source=index + 1, target=index,
                           generator=GeneratorSymbol(family="η", index=index))


def test_r18_registered_eta3_spelling_has_root_expansion():
    goal = Relation(TodaPrimaryGroup(4, 3), FiniteCyclicGroup(2, eta(3, "η_3")))
    candidates = expand_existing_pi43_rules(goal)
    assert len(candidates) == 1
    assert len(retain_ordered_root_expansions(goal, goal, candidates)) == 1
    assert candidates[0].subgoals[1].lhs == goal.rhs.generator


def test_r18_canonical_eta3_spelling_has_root_expansion():
    goal = Relation(TodaPrimaryGroup(4, 3), FiniteCyclicGroup(2, eta(3, "η₃")))
    assert len(expand_existing_pi43_rules(goal)) == 1


def test_r18_unrelated_generator_is_not_accepted():
    goal = Relation(TodaPrimaryGroup(4, 3), FiniteCyclicGroup(2, eta(4, "η_4")))
    assert expand_existing_pi43_rules(goal) == ()


def test_r18_generator_substitution_requires_proved_identity():
    target = TodaPrimaryGroup(4, 3)
    old = Suspension(expression=eta(2, "η₂"))
    new = eta(3, "η_3")
    first = ProofStep(conclusion=Relation(target, FiniteCyclicGroup(2, old)),
                      premises=(), rule=ProofRule.GIVEN)
    second = ProofStep(conclusion=Relation(new, old), premises=(), rule=ProofRule.GIVEN)
    matches = find_inference_matches_for_rule(finite_cyclic_generator_substitution_rule(), (first, second))
    assert len(matches) == 1
    derived = derive_inference_proof_step(matches[0])
    assert derived.conclusion == Relation(target, FiniteCyclicGroup(2, new))
    assert derived.rule is ProofRule.INFERENCE


def test_r18_root_gate_continues_rejecting_self_specialization():
    root = Relation(TodaPrimaryGroup(4, 3), FiniteCyclicGroup(2, eta(3, "η_3")))
    expansion = GoalExpansion(finite_cyclic_generator_substitution_rule(), (root,))
    assert retain_ordered_root_expansions(root, root, (expansion,)) == ()


def test_r18_rejects_generator_substitution_without_matching_equality():
    old = Suspension(expression=eta(2, "η₂"))
    first = ProofStep(conclusion=Relation(TodaPrimaryGroup(4, 3), FiniteCyclicGroup(2, old)),
                      premises=(), rule=ProofRule.GIVEN)
    second = ProofStep(conclusion=Relation(eta(3, "η_3"), eta(3, "η₃")),
                       premises=(), rule=ProofRule.GIVEN)
    matches = find_inference_matches_for_rule(finite_cyclic_generator_substitution_rule(), (first, second))
    assert matches == () or len(matches) == 0

```

## 新規 `audit_r18.py` 全文（監査スクリプト）

```python
"""Read-only verification of the root expansions after R57-R18 installation."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates


def run() -> dict:
    bridge = build_shared_typed_bridge()
    records = []
    for n, k in ((2, 1), (3, 1), (4, 1)):
        goals = registered_group_goal_candidates(bridge, n=n, k=k)
        item = {"n": n, "k": k, "candidate_count": len(goals)}
        if len(goals) == 1:
            goal = goals[0]
            provider = shared_expansion_provider(bridge, proof_target=goal)
            expansions = provider(goal)
            item["root_expansion_count"] = len(expansions)
            item["expansion_rules"] = [getattr(x.rule, "name", repr(x.rule)) for x in expansions]
            item["required_subgoals"] = [[repr(g) for g in x.subgoals] for x in expansions]
        records.append(item)
    return {"phase": "165 R57-R18", "mode": "READ_ONLY_ROOT_AUDIT", "targets": records,
            "no_proof_certification": True, "full_pytest_run": False}


def main() -> None:
    result = run()
    destination = Path(__file__).with_name("root_expansions.json")
    destination.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf8")
    for item in result["targets"]:
        print(f"pi_{item['n'] + item['k']}^{item['n']}: root_expansions={item.get('root_expansion_count', 'unknown')}")
        for name in item.get("expansion_rules", ()):
            print("  rule:", name)
    print("R57-R18 root audit written:", destination)


if __name__ == "__main__":
    main()

```
