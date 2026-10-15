# R57-R20 変更コード全文

変更対象：

- `phase165_r52_r9_shared_math.py` の `build_shared_typed_bridge()` 全体と `shared_expansion_provider()` 全体。import 部分の変更なし。
- `phase165_r57_r11_proof_order_gate.py` の `is_unordered_root_structure_specialization()` 全体。import 部分の変更なし。
- 新規 `phase165_r57_r20_general_specialization.py`：プロジェクト root に追加。
- 新規 `phase165_r57_r20_general_specialization/test_phase165_r57_r20_general_specialization.py`：テスト7件。
- インストーラー `phase165_r57_r20_general_specialization/install.py`、Windows 実行 `run.ps1`。

## build_shared_typed_bridge() 全体

```python
def build_shared_typed_bridge(*, sources: tuple[RegistryBridgeResult, ...] | None = None) -> RegistryBridgeResult:
    """Merge eligible typed statements without importing derived group proofs.

    The R38 adopted-Tex *source assertions* are currently the first available
    rigorously linked typed leaves. They are shared with every query, not
    selected because the requested group is pi3^2.
    """
    if sources is None:
        from phase165_r9_production_wiring import discover_goal_search_inputs
        from phase165_r14_r38_direct_registry import build_adopted_typed_reference_registry
        production = discover_goal_search_inputs().bridge
        adopted_tex = Path(__file__).resolve().with_name("phase165_r14_r39_toda51.tex")
        from phase165_r52_r13_reference_registration import build_adopted_prop51_reference
        from phase165_r52_r27_r5_literature import build_typed_literature_bridge
        from phase165_r57_r20_general_specialization import build_adopted_toda51_diagonal_reference
        literature = build_typed_literature_bridge(production)
        sources = (production, build_adopted_typed_reference_registry(adopted_tex),
                   build_adopted_prop51_reference(),
                   build_adopted_toda51_diagonal_reference(adopted_tex)) + (literature,)
    registry = UnifiedStatementRegistry()
    links = []
    records = []
    for index, source in enumerate(sources):
        if not isinstance(source, RegistryBridgeResult):
            raise TypeError("source must be RegistryBridgeResult")
        prefix = f"shared:{index}:"
        for ref in source.registry._references.values():
            registry.add_reference(replace(ref, reference_id=prefix + ref.reference_id))
        for assertion in source.registry._assertions.values():
            if assertion.origin is AssertionOrigin.PROOF_INTERNAL:
                continue
            registry.add_assertion(replace(
                assertion, assertion_id=prefix + assertion.assertion_id,
                reference_id=prefix + assertion.reference_id,
                dependencies=tuple(prefix + dep for dep in assertion.dependencies),
            ))
        eligible_ids = {
            a.assertion_id for a in source.registry._assertions.values()
            if a.origin is AssertionOrigin.FIXED_STATEMENT
        }
        for link in source.proof_links:
            if link.assertion_id not in eligible_ids:
                continue
            if link.step is not None and (
                link.step.rule is not ProofRule.GIVEN
                or link.step.conclusion != source.registry.assertion(link.assertion_id).content
            ):
                raise ValueError("source link is not a typed fixed Reference")
            links.append(replace(link, assertion_id=prefix + link.assertion_id))
        records.extend(
            replace(record, assertion_id=prefix + record.assertion_id)
            if record.assertion_id is not None else record
            for record in source.records
        )
    from phase165_r52_r12_component_bridge import expand_cited_given_components
    return expand_cited_given_components(
        RegistryBridgeResult(registry, tuple(records), tuple(links))
    )
```

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
    from phase165_r57_r20_general_specialization import expand_cited_general_specialization

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
        options.extend(expand_cited_general_specialization(goal, tuple(available)))
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

## is_unordered_root_structure_specialization() 全体

```python
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
    # A cited diagonal source (5.1) is a foundational *earlier* formula,
    # unlike the target-group higher-eta clause of Proposition 5.1.
    # Its use still requires screening of the exact fixed Reference leaf.
    if (getattr(expansion.rule, "name", None) == "generic cited typed scalar specialization"
            and len(expansion.subgoals) == 1
            and root_goal.lhs.group_dimension == root_goal.lhs.sphere_dimension
            and isinstance(expansion.subgoals[0], Relation)):
        premise = expansion.subgoals[0]
        if (isinstance(premise.lhs, TodaPrimaryGroup)
                and premise.lhs.group_dimension == premise.lhs.sphere_dimension
                and isinstance(premise.rhs, FreeCyclicGroup)):
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
```

## 新規モジュール全体（import を含む）

```python
"""R57-R20: generic typed scalar specialization with cited source provenance.

The mathematical source is the adopted Toda (5.1) TeX. This module can only
instantiate already-screened symbolic statements: it never treats matching a
goal as evidence and never turns an uncited source into a proof leaf.
"""
from __future__ import annotations

from dataclasses import fields, is_dataclass, replace
from pathlib import Path

from expression import GeneratorSymbol, HomotopyElement, ScalarProduct, ScalarSum, ScalarSymbol
from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, LiteratureReference, PremisePattern, ProofRule, ProofStep, Relation, RelationType
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)


def _contains_symbol(value: object) -> bool:
    if isinstance(value, ScalarSymbol):
        return True
    if isinstance(value, tuple):
        return any(_contains_symbol(item) for item in value)
    if is_dataclass(value) and not isinstance(value, type):
        return any(_contains_symbol(getattr(value, field.name)) for field in fields(value))
    return False


def _scalar_value(value: object, bindings: dict[str, int]) -> int | None:
    if type(value) is int:
        return value
    if isinstance(value, ScalarSymbol):
        return bindings.get(value.name)
    if isinstance(value, ScalarSum):
        left, right = _scalar_value(value.left, bindings), _scalar_value(value.right, bindings)
        return left + right if left is not None and right is not None else None
    if isinstance(value, ScalarProduct):
        left, right = _scalar_value(value.left, bindings), _scalar_value(value.right, bindings)
        return left * right if left is not None and right is not None else None
    return None


def _bind(pattern: object, concrete: object, bindings: dict[str, int]) -> bool:
    if isinstance(pattern, ScalarSymbol):
        if type(concrete) is not int or concrete < 1:
            return False
        old = bindings.setdefault(pattern.name, concrete)
        return old == concrete
    if isinstance(pattern, (ScalarSum, ScalarProduct)) and type(concrete) is int:
        resolved = _scalar_value(pattern, bindings)
        if resolved is not None:
            return resolved == concrete
        if isinstance(pattern, ScalarSum):
            if isinstance(pattern.left, ScalarSymbol) and type(pattern.right) is int:
                return _bind(pattern.left, concrete - pattern.right, bindings)
            if isinstance(pattern.right, ScalarSymbol) and type(pattern.left) is int:
                return _bind(pattern.right, concrete - pattern.left, bindings)
        return False
    if isinstance(pattern, HomotopyElement) and isinstance(concrete, HomotopyElement):
        if not isinstance(pattern.name, str):
            return False
        if not _bind(pattern.dimension, concrete.dimension, bindings):
            return False
        if not _bind(pattern.source, concrete.source, bindings):
            return False
        if not _bind(pattern.target, concrete.target, bindings):
            return False
        if not _bind(pattern.generator, concrete.generator, bindings):
            return False
        name = _substitute_name(pattern.name, bindings)
        return name == concrete.name
    if type(pattern) is not type(concrete):
        return False
    if isinstance(pattern, tuple):
        return len(pattern) == len(concrete) and all(
            _bind(p, c, bindings) for p, c in zip(pattern, concrete)
        )
    if is_dataclass(pattern) and not isinstance(pattern, type):
        return all(_bind(getattr(pattern, field.name), getattr(concrete, field.name), bindings)
                   for field in fields(pattern))
    return pattern == concrete


def _substitute_name(name: str, bindings: dict[str, int]) -> str:
    # Source notation uses a literal underscore: ι_n -> ι_5.
    for symbol, value in sorted(bindings.items(), key=lambda item: -len(item[0])):
        name = name.replace("_" + symbol, "_" + str(value))
    return name


def _instantiate(value: object, bindings: dict[str, int]) -> object:
    if isinstance(value, (ScalarSymbol, ScalarSum, ScalarProduct)):
        actual = _scalar_value(value, bindings)
        if actual is None:
            raise ValueError("unbound scalar in source template")
        return actual
    if isinstance(value, tuple):
        return tuple(_instantiate(x, bindings) for x in value)
    if isinstance(value, HomotopyElement):
        return replace(value, name=_substitute_name(value.name, bindings),
                       dimension=_instantiate(value.dimension, bindings),
                       source=_instantiate(value.source, bindings),
                       target=_instantiate(value.target, bindings),
                       generator=_instantiate(value.generator, bindings))
    if is_dataclass(value) and not isinstance(value, type):
        return replace(value, **{field.name: _instantiate(getattr(value, field.name), bindings)
                                 for field in fields(value)})
    return value


def specialize_typed_statement(source: object, goal: object) -> tuple[tuple[str, int], ...] | None:
    """Find explicit scalar bindings with exact instantiated-goal equality."""
    if not _contains_symbol(source):
        return None
    bindings: dict[str, int] = {}
    if not _bind(source, goal, bindings):
        return None
    if _instantiate(source, bindings) != goal:
        return None
    return tuple(sorted(bindings.items()))


def _specialization_rule(source: object, goal: object) -> InferenceRule:
    def guard(premises, bindings):
        return (len(premises) == 1
                and type(premises[0].conclusion) is type(source)
                and premises[0].conclusion == source
                and specialize_typed_statement(source, goal) is not None)

    def conclusion(premises):
        binding = specialize_typed_statement(premises[0].conclusion, goal)
        if binding is None:
            raise ValueError("unmatched symbolic source")
        return _instantiate(premises[0].conclusion, dict(binding))

    return InferenceRule(
        name="generic cited typed scalar specialization",
        premise_patterns=(PremisePattern(statement_type=type(source)),),
        match_guard=guard, conclusion_builder=conclusion,
    )


def expand_cited_general_specialization(
    goal: object, available: tuple[object, ...]
) -> tuple[GoalExpansion, ...]:
    """Expand only from screened typed source leaves, never from source archives."""
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    seen: list[object] = []
    output: list[GoalExpansion] = []
    for source in available:
        if source in seen:
            continue
        if specialize_typed_statement(source, goal) is not None:
            seen.append(source)
            output.append(GoalExpansion(_specialization_rule(source, goal), (source,)))
    return tuple(output)


def build_adopted_toda51_diagonal_reference(tex_path: Path) -> RegistryBridgeResult:
    """Register the cited symbolic diagonal clause of the adopted (5.1) TeX.

    Only the exact existing source sentence authorizes this schema. It is a
    fixed literature assertion (and hence may be a GIVEN leaf), not a derived
    group result, and it carries the original Toda (5.1) citation.
    """
    tex = Path(tex_path).read_text(encoding="utf8")
    expected = r"\pi^{n}_{n}=\gen{\iota_n}\cong \mathbb Z"
    if expected not in tex:
        raise ValueError("adopted Toda (5.1) diagonal clause missing or changed")
    n = ScalarSymbol("n")
    statement = Relation(
        lhs=TodaPrimaryGroup(group_dimension=n, sphere_dimension=n),
        rhs=FreeCyclicGroup(HomotopyElement(
            name="ι_n", dimension=n,
            generator=GeneratorSymbol(family="ι", index=n),
        )),
        relation_type=RelationType.EQUALITY,
    )
    registry = UnifiedStatementRegistry()
    reference_id = "adopted:toda51:diagonal"
    assertion_id = "adopted:assertion:toda51:diagonal"
    registry.add_reference(LiteratureEntry(
        reference_id=reference_id, kind=ReferenceKind.EQUATION,
        locator="(5.1)", source_id="Toda translated TeX:(5.1) (adopted; original edition unverified)",
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id=assertion_id, reference_id=reference_id,
        kind=AssertionKind.STATEMENT, content=statement,
        origin=AssertionOrigin.FIXED_STATEMENT,
        scope=("symbolic_diagonal", "n_positive"),
    ))
    cited_step = ProofStep(
        conclusion=statement, premises=(), rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(
            name="Toda (5.1) diagonal cyclic source",
            literature_reference=LiteratureReference(label="Toda (5.1)", locator="(5.1)"),
        ),
    )
    return RegistryBridgeResult(
        registry, (), (ProofStepLink(assertion_id=assertion_id, step=cited_step),)
    )
```

## テスト全体（import を含む）

```python
"""R57-R20: typed universal-source instantiation and proof-use-order checks."""
from __future__ import annotations

from pathlib import Path

import pytest

from expression import GeneratorSymbol, HomotopyElement, ScalarSymbol
from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from phase165_r57_r20_general_specialization import (
    build_adopted_toda51_diagonal_reference,
    expand_cited_general_specialization,
    specialize_typed_statement,
)
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r57_r11_proof_order_gate import retain_ordered_root_expansions
from proof import ProofRule, Relation, RelationType, find_inference_matches_for_rule
from phase164_r8_proofstep_factory import derive_inference_proof_step
from unified_statement_registry import AssertionOrigin


def _tex_path() -> Path:
    return Path(__file__).resolve().parent.parent / "phase165_r14_r39_toda51.tex"


def _diagonal_goal(n: int) -> Relation:
    return Relation(
        lhs=TodaPrimaryGroup(n, n),
        rhs=FreeCyclicGroup(HomotopyElement(
            name="ι_" + str(n), dimension=n,
            generator=GeneratorSymbol(family="ι", index=n),
        )),
        relation_type=RelationType.EQUALITY,
    )


def _source():
    bridge = build_adopted_toda51_diagonal_reference(_tex_path())
    link, = bridge.proof_links
    return bridge, link.step


def test_r20_cited_symbolic_diagonal_has_exact_toda_51_provenance():
    bridge, step = _source()
    assertion, = bridge.registry._assertions.values()
    assert assertion.origin is AssertionOrigin.FIXED_STATEMENT
    assert bridge.registry.reference(assertion.reference_id).locator == "(5.1)"
    assert step.rule is ProofRule.GIVEN
    assert step.conclusion == assertion.content
    assert isinstance(step.conclusion.lhs.sphere_dimension, ScalarSymbol)


def test_r20_single_general_template_works_for_arbitrary_positive_n():
    _, step = _source()
    for n in (1, 3, 5, 10, 100):
        goal = _diagonal_goal(n)
        assert specialize_typed_statement(step.conclusion, goal) == (("n", n),)
        expansion, = expand_cited_general_specialization(goal, (step.conclusion,))
        matches = find_inference_matches_for_rule(expansion.rule, (step,))
        assert len(matches) == 1
        derived = derive_inference_proof_step(matches[0])
        assert derived.rule is ProofRule.INFERENCE
        assert derived.conclusion == goal


def test_r20_missing_cited_source_never_yields_specialization():
    goal = _diagonal_goal(5)
    assert expand_cited_general_specialization(goal, ()) == ()
    assert specialize_typed_statement(goal, goal) is None


def test_r20_wrong_dimensions_and_generator_are_rejected():
    _, step = _source()
    bad_dimension = Relation(TodaPrimaryGroup(6, 5), _diagonal_goal(5).rhs)
    bad_generator = Relation(TodaPrimaryGroup(5, 5), FreeCyclicGroup(
        HomotopyElement("ι_5", dimension=5, generator=GeneratorSymbol("η", 5)),
    ))
    for goal in (bad_dimension, bad_generator, _diagonal_goal(0)):
        assert expand_cited_general_specialization(goal, (step.conclusion,)) == ()


def test_r20_missing_or_changed_original_clause_rejected(tmp_path: Path):
    source = tmp_path / "toda.tex"
    source.write_text(r"\pi^{n}_{n}=\mathbb Z", encoding="utf8")
    with pytest.raises(ValueError):
        build_adopted_toda51_diagonal_reference(source)


def test_r20_screened_shared_expansion_preserves_diagonal_order_boundary():
    bridge = build_shared_typed_bridge()
    diagonal = _diagonal_goal(5)
    proposals = shared_expansion_provider(bridge, proof_target=diagonal)(diagonal)
    matching = tuple(x for x in proposals
                     if getattr(x.rule, "name", "") == "generic cited typed scalar specialization")
    assert len(matching) == 1
    assert matching[0].subgoals[0].lhs.group_dimension == ScalarSymbol("n")
    assert retain_ordered_root_expansions(diagonal, diagonal, matching) == matching


def test_r20_higher_eta_root_still_blocked_by_order_gate():
    from phase165_r57_r8_eta_specialization import specialize_eta_group_relation
    from phase165_r52_r13_reference_registration import build_adopted_prop51_reference
    from phase165_r57_r8_eta_specialization import _fixed_typed_relations
    bridge = build_adopted_prop51_reference()
    source, = _fixed_typed_relations(bridge)
    goal = specialize_eta_group_relation(source, 4)
    from phase165_r57_r8_eta_specialization import expand_registered_eta_specialization
    expansion, = expand_registered_eta_specialization(goal, (source,))
    assert retain_ordered_root_expansions(goal, goal, (expansion,)) == ()
```

## 完了条件・次の Phase との境界

文献 (5.1) の一般形を引用できる状態で、任意の正整数 n の対角群構造を共通エンジンが ProofStep で具体化できること。引用の欠落と誤った型・範囲は拒否する。対象 pytest に成功すること。ほかの一般命題の個別資料登録、π₄³ の残る未解決 Goal と Renderer は今後の対象とする。

## 実行時監査スクリプト全体

```python
"""Read-only check of the cited (5.1) specialization through shared search."""
from __future__ import annotations

import json
from pathlib import Path

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from phase165_r52_r9_shared_math import build_shared_typed_bridge, search_shared_group_goal
from phase165_r52_partial_proof import ProofSearchStatus


def main() -> None:
    bridge = build_shared_typed_bridge()
    generator = HomotopyElement(
        name="ι_5", dimension=5,
        generator=GeneratorSymbol(family="ι", index=5),
    )
    result = search_shared_group_goal(
        n=5, k=0, group_structure=FreeCyclicGroup(generator), bridge=bridge,
    )
    state = getattr(result.status, "value", str(result.status))
    report = {
        "phase": "165 R57-R20",
        "target": "pi_5^5",
        "status": state,
        "proven_step_count": len(result.proven_steps),
        "open_goals": [repr(goal) for goal in result.open_goals],
        "diagnostics": list(result.diagnostics),
        "full_pytest_run": False,
    }
    dest = Path(__file__).with_name("specialization_audit.json")
    dest.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf8")
    print("R57-R20 pi_5^5 search status:", state)
    print("R57-R20 proven steps:", len(result.proven_steps))
    print("R57-R20 unresolved goals:", len(result.open_goals))
    print("R57-R20 audit:", dest)


if __name__ == "__main__":
    main()

```
