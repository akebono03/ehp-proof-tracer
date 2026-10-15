# R57-R12 変更コード全文

変更関数は両方とも `phase165_r52_r9_shared_math.py` 内の同名関数を置換。import 部分の変更はありません。新規クラス・関数は `phase165_r57_r12_ordered_proofs.py` の先頭に追加。

## shared_expansion_provider
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

## search_shared_group_goal
```python
def search_shared_group_goal(*, n: int, k: int, group_structure: object,
                              bridge: RegistryBridgeResult | None = None,
                              expansion_provider=None,
                              citing_assertion_id: str | None = None,
                              verified_assertion_ids: tuple[str, ...] = (), completed_internal_proofs: tuple = (), proof_use_order=None,
                              ordered_completed_proofs: tuple = (), target_order: int | None = None):
    """Run canonical search under a screened Reference context.

    Older calls retain their signature. R15 ordering is applied to sources
    outside the explicitly adopted-Tex policy; no IDs are auto-verified.
    """
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r57_r12_ordered_proofs import validate_prior_internal_proofs

    prior = validate_prior_internal_proofs(
        ordered_completed_proofs, target_order, completed_internal_proofs
    )
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
        expansion_provider = shared_expansion_provider(
            proof_context, proof_target=goal,
            prior_conclusions=tuple(item.root.conclusion for item in prior),
        )
    return search_registered_partial_proof(
        n=n, k=k, goal=goal, bridge=proof_context,
        citing_assertion_id=context_id,
        expansion_provider=expansion_provider,
        lookup_mode="typed_reference",
        structure_status=GroupStructureStatus.UNKNOWN,
        completed_internal_proofs=prior,
    )

```

## 新規ファイル全文
```python
"""R57-R12: explicit proof-use ordering for prior internal proof ancestry.

This class does not assert the chosen positions are historically verified.
The caller must supply reviewed order indices, not simply sort discovered facts.
"""
from __future__ import annotations

from dataclasses import dataclass

from phase165_r52_r17_internal_dependency import CompletedInternalProof, validate_ancestry
from proof import ProofStep


@dataclass(frozen=True)
class OrderedCompletedProof:
    proof: CompletedInternalProof
    order: int

    def __post_init__(self) -> None:
        if not isinstance(self.proof, CompletedInternalProof):
            raise TypeError("proof must be CompletedInternalProof")
        if isinstance(self.order, bool) or not isinstance(self.order, int) or self.order < 0:
            raise ValueError("order must be nonnegative integer")
        validate_ancestry(self.proof.root)


def validate_prior_internal_proofs(
    ordered: tuple[OrderedCompletedProof, ...],
    target_order: int | None,
    legacy_unordered: tuple = (),
) -> tuple[CompletedInternalProof, ...]:
    """Admit only explicitly ordered, earlier inference proofs; fail closed.

    A caller-supplied rank alone is not a certification of its correctness.
    The registry's proof-order metadata must eventually provide that evidence.
    """
    if not isinstance(ordered, tuple) or not isinstance(legacy_unordered, tuple):
        raise TypeError("proof collections must be tuples")
    if legacy_unordered:
        raise ValueError("unranked completed_internal_proofs are forbidden by proof-use ordering")
    if not ordered:
        if target_order is not None and (
            isinstance(target_order, bool) or not isinstance(target_order, int) or target_order < 0
        ):
            raise ValueError("target_order must be nonnegative integer")
        return ()
    if isinstance(target_order, bool) or not isinstance(target_order, int) or target_order < 0:
        raise ValueError("target_order is required for ordered proof reuse")
    result = []
    seen = []
    for item in ordered:
        if not isinstance(item, OrderedCompletedProof):
            raise TypeError("ordered proofs must contain OrderedCompletedProof")
        if item.order >= target_order:
            raise ValueError("internal proof order must precede the current target")
        root = item.proof.root
        validate_ancestry(root)
        if any(type(root.conclusion) is type(x) and root.conclusion == x for x in seen):
            raise ValueError("duplicate internal proof conclusion")
        seen.append(root.conclusion)
        result.append(item.proof)
    return tuple(result)

```

## テスト全文
```python
"""R57-R12: ordered prior proofs only; no fabricated stable isomorphism."""
import pytest

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r52_r17_internal_dependency import CompletedInternalProof
from phase165_r57_r12_ordered_proofs import OrderedCompletedProof, validate_prior_internal_proofs
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase165_r52_r12_component_bridge import expand_cited_given_components
from phase165_r52_r13_reference_registration import build_adopted_prop51_reference
from proof import InferenceRule, PremisePattern, ProofRule, ProofStep, Relation, RelationType


def _earlier_proof():
    eta3 = HomotopyElement(name="η_3", dimension=3, source=4, target=3,
        generator=GeneratorSymbol(family="η", index=3))
    conclusion = Relation(TodaPrimaryGroup(4, 3), FiniteCyclicGroup(2, eta3), RelationType.EQUALITY)
    given = ProofStep(conclusion="registered premise", premises=(), rule=ProofRule.GIVEN)
    rule = InferenceRule(name="test prior inference", premise_patterns=(PremisePattern(statement_type=str),),
        conclusion_builder=lambda premises: conclusion)
    root = ProofStep(conclusion=conclusion, premises=(given,), rule=ProofRule.INFERENCE, inference_rule=rule)
    return OrderedCompletedProof(CompletedInternalProof(root), 1)


def test_prior_proof_requires_strictly_earlier_position():
    prior = _earlier_proof()
    assert validate_prior_internal_proofs((prior,), 2) == (prior.proof,)
    with pytest.raises(ValueError, match="precede"):
        validate_prior_internal_proofs((prior,), 1)
    with pytest.raises(ValueError, match="precede"):
        validate_prior_internal_proofs((prior,), 0)


def test_unknown_order_and_unranked_proofs_fail_closed():
    prior = _earlier_proof()
    with pytest.raises(ValueError, match="target_order"):
        validate_prior_internal_proofs((prior,), None)
    with pytest.raises(ValueError, match="unranked"):
        validate_prior_internal_proofs((), 2, (prior.proof,))


def test_invalid_order_metadata_is_rejected():
    prior = _earlier_proof()
    with pytest.raises(ValueError):
        OrderedCompletedProof(prior.proof, True)
    with pytest.raises(ValueError):
        validate_prior_internal_proofs((prior, prior), 5)


def test_shared_provider_without_registered_toda45_does_not_invent_transport():
    bridge = expand_cited_given_components(build_adopted_prop51_reference())
    earlier = _earlier_proof().proof.root.conclusion
    provider = shared_expansion_provider(bridge, prior_conclusions=(earlier,))
    eta4 = HomotopyElement(name="η_4", dimension=4, source=5, target=4,
        generator=GeneratorSymbol(family="η", index=4))
    target = Relation(TodaPrimaryGroup(5,4), FiniteCyclicGroup(2, eta4), RelationType.EQUALITY)
    expansions = provider(target)
    assert not any("Toda 4.5" in x.rule.name for x in expansions)


def test_shared_search_rejects_unranked_prior_without_running_exploration():
    from phase165_r52_r9_shared_math import search_shared_group_goal
    prior = _earlier_proof()
    with pytest.raises(ValueError, match="unranked"):
        search_shared_group_goal(n=4, k=1, group_structure=prior.proof.root.conclusion.rhs,
            completed_internal_proofs=(prior.proof,))

```
