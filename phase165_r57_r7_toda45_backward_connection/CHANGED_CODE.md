# R57-R7 変更コード全文

## 変更対象

- 既存 `phase165_r52_r9_shared_math.py` 内 `shared_expansion_provider`：関数全体の置換。import 変更なし。
- 新規 `phase165_r57_r7_stable_expansion.py`：ファイル全文で追加（全 import と新規関数を含む）。
- 新規 `phase165_r57_r7_toda45_backward_connection/test_phase165_r57_r7_toda45_backward_connection.py`：新規テスト全文。
- 新規 `install.py`、`run.ps1`。その他既存ファイルは変更しない。

## 変更後の shared_expansion_provider() 全文

```python
def shared_expansion_provider(bridge: RegistryBridgeResult, extra_providers: tuple = ()):
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
        return tuple(options)
    return expand
```

## 新規モジュール全文

```python
"""R57-R7: source-anchored backward expansions for Toda (4.5) transport.

No proof leaves, no generator normalization, and no group-number branches.
"""
from __future__ import annotations

from expression import IteratedSuspension
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion
from proof import Relation, RelationType
from toda_rules import Toda45IsomorphismStatement
from toda_stable_group_transport import (
    toda_45_generic_finite_cyclic_transport_inference_rule,
)


def expand_registered_toda45_finite_cyclic_goal(
    goal: object,
    available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Use only exact, already admissible typed Reference conclusions.

    The rule itself checks its premises again before deriving the conclusion.
    An IteratedSuspension is not silently identified with a named eta symbol.
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if not (
        isinstance(goal, Relation)
        and goal.relation_type is RelationType.EQUALITY
        and isinstance(goal.lhs, TodaPrimaryGroup)
        and isinstance(goal.rhs, FiniteCyclicGroup)
    ):
        return ()
    options = []
    for iso in available:
        if not isinstance(iso, Toda45IsomorphismStatement):
            continue
        transport_map = iso.map
        if transport_map.target_group != goal.lhs:
            continue
        for base in available:
            if not (
                isinstance(base, Relation)
                and base.relation_type is RelationType.EQUALITY
                and isinstance(base.lhs, TodaPrimaryGroup)
                and isinstance(base.rhs, FiniteCyclicGroup)
                and base.lhs == transport_map.source_group
                and base.rhs.order == goal.rhs.order
            ):
                continue
            expected_generator = IteratedSuspension(
                expression=base.rhs.generator,
                exponent=transport_map.exponent,
            )
            if goal.rhs.generator != expected_generator:
                continue
            candidate = GoalExpansion(
                toda_45_generic_finite_cyclic_transport_inference_rule(),
                (base, iso),
            )
            if not any(item.subgoals == candidate.subgoals for item in options):
                options.append(candidate)
    return tuple(options)
```

## 新規テスト全文

```python
"""Targeted R57-R7 tests (no legacy proof replay)."""
from dataclasses import replace
from pathlib import Path
import ast
import pytest

from expression import GeneratorSymbol, HomotopyElement, IteratedSuspension
from homotopy_groups import FiniteCyclicGroup, TodaIteratedSuspensionMap, TodaPrimaryGroup
from phase165_r57_r7_stable_expansion import expand_registered_toda45_finite_cyclic_goal
from proof import ProofRule, ProofStep, Relation, RelationType
from toda_rules import Toda45IsomorphismStatement
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase163_r4_registry_bridge import RegistryBridgeResult
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)


def _typed_case():
    source = TodaPrimaryGroup(4, 3)
    target = TodaPrimaryGroup(5, 4)
    eta3 = HomotopyElement(name="η₃", dimension=3, source=4, target=3,
                           generator=GeneratorSymbol(family="η", index=3))
    base = Relation(source, FiniteCyclicGroup(2, eta3), RelationType.EQUALITY)
    suspension = TodaIteratedSuspensionMap(exponent=1, source_group=source, target_group=target)
    iso = Toda45IsomorphismStatement(map=suspension)
    goal = Relation(target, FiniteCyclicGroup(2, IteratedSuspension(expression=eta3, exponent=1)), RelationType.EQUALITY)
    return base, iso, goal


def _bridge(statements):
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(reference_id="r", kind=ReferenceKind.PROPOSITION,
                                           locator="Test source", source_id="typed-fixture"))
    links = []
    for i, statement in enumerate(statements):
        identifier = "test:" + str(i)
        registry.add_assertion(AssertionEntry(assertion_id=identifier, reference_id="r",
                 kind=AssertionKind.STATEMENT, content=statement, origin=AssertionOrigin.FIXED_STATEMENT))
        links.append(ProofStepLink(assertion_id=identifier, step=ProofStep(
                    conclusion=statement, premises=(), rule=ProofRule.GIVEN)))
    return RegistryBridgeResult(registry, (), tuple(links))


def test_typed_source_and_iso_produce_existing_toda45_expansion():
    base, iso, goal = _typed_case()
    options = expand_registered_toda45_finite_cyclic_goal(goal, (base, iso))
    assert len(options) == 1
    assert options[0].subgoals == (base, iso)
    assert "Toda 4.5" in options[0].rule.name


def test_no_isomorphism_or_base_never_creates_source_evidence():
    base, iso, goal = _typed_case()
    assert expand_registered_toda45_finite_cyclic_goal(goal, (base,)) == ()
    assert expand_registered_toda45_finite_cyclic_goal(goal, (iso,)) == ()
    assert expand_registered_toda45_finite_cyclic_goal(goal, ()) == ()


def test_named_eta_is_not_assumed_equal_to_suspension():
    base, iso, goal = _typed_case()
    eta4 = HomotopyElement(name="η₄", dimension=4, source=5, target=4,
                           generator=GeneratorSymbol(family="η", index=4))
    named = replace(goal, rhs=FiniteCyclicGroup(2, eta4))
    assert expand_registered_toda45_finite_cyclic_goal(named, (base, iso)) == ()


def test_shared_provider_exposes_typed_transport_only_with_source():
    base, iso, goal = _typed_case()
    assert any(option.subgoals == (base, iso) for option in shared_expansion_provider(_bridge((base, iso)))(goal))
    assert not any(option.subgoals == (base, iso) for option in shared_expansion_provider(_bridge((base,)))(goal))


def test_targeted_unregistered_toda45_not_given_by_connection():
    source = Path(__file__).resolve().parents[1] / "phase165_r52_r9_shared_math.py"
    body = ast.parse(source.read_text(encoding="utf-8"))
    function = next(x for x in body.body if isinstance(x, ast.FunctionDef) and x.name == "shared_expansion_provider")
    assert any(isinstance(node, ast.Name) and node.id == "expand_registered_toda45_finite_cyclic_goal"
               for node in ast.walk(function))
    assert not any(isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "ProofStep"
                   for node in ast.walk(function))
```

## 実行と完了条件

`run.ps1` は本番接続を一度だけ適用し、対象 pytest のみ実行する。ProofStep に未登録命題を混入させず、型付き命題が揃った場合に `GoalExpansion` を返すこと。次の段階で一般形の (4.5) 型付き特殊化、基点の型付き証明、生成元同定、および Web 候補探索を実装する。今回そこまでの機能を先取りしない。
