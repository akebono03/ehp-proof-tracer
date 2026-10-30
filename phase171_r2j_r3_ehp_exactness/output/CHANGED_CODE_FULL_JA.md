# Phase 171 R2J-R3 — 変更コード全文

変更対象: `phase165_r52_r9_shared_math.py` の `shared_expansion_provider()`。
追加位置: R2J-R2 `expand_cited_cyclic_hopf_surjectivity` 呼出し直後。
モジュール冒頭の import 変更なし。新規ファイルの import は各全文に含む。

## 本番ファイルの冒頭 import 全文

```python
"""Shared Phase 165 typed backward-search path. Never replay saved proofs.

Typed source claims may be reused across goals; a source's role as a leaf
is not a license to use an untyped archive or an earlier derived proof.
"""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r14_r6_generic_iso import GeneratorImage, MapIsomorphism, expand_generic_iso_goal
from phase165_r14_r9_ehp_exactness import expand_generic_ehp_hopf_goal
from phase165_r14_r11_delta_zero import expand_delta_zero_from_suspension_iso
from phase165_r14_r14_diagonal_and_prop42 import expand_diagonal_suspension
from phase165_r14_r33_final_group import reverse_free_cyclic_transport_rule
from phase165_r3_recursive_search import GoalExpansion
from phase165_r6_2_unified_registry_r3_r4.context_provider_registry import build_context_expansion_provider_registry
from phase165_r6_2_unified_registry_r3_r3.provider_registry import build_shared_expansion_provider_registry
from phase165_r6_2_unified_registry_r1.unified_backward_rule_registry import build_unified_backward_rule_registry
from phase165_r52_r2_search_adapter import search_registered_partial_proof
from phase165_r52_partial_proof import GroupStructureStatus, ProofSearchStatus
from proof import ProofRule, ProofStep, Relation, RelationType
from unified_statement_registry import (
    AssertionOrigin, UnifiedStatementRegistry,
)



```

## 変更後の関数全文

```python
def shared_expansion_provider(bridge: RegistryBridgeResult, extra_providers: tuple = (), *, proof_target=None, prior_conclusions: tuple = ()):
    """Build backward proposals from typed source witnesses and common rules."""
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    # R4-4 stage4: exactness-map binding from cited fixed statements only.
    from phase165_r6_2_r4_r4_stage4_binding import build_exactness_binding_provider
    from phase165_r12_r11_prop42_unified import build_prop42_specialization_provider
    from phase165_r12_r12_ehp_consequences import expand_ehp_exactness_consequences
    from phase165_r12_r13_kernel_image import build_concrete_kernel_provider
    from phase165_r12_r26_map_candidates import build_cited_eta_quotient_provider
    extra_providers = (build_cited_eta_quotient_provider(bridge),) + tuple(extra_providers)
    from phase165_r12_r28_presentation_connection import expand_eta_presentation
    extra_providers = (expand_eta_presentation,) + tuple(extra_providers)
    from phase165_r12_r29_kernel_connection import expand_kernel_multiple_from_suspension
    extra_providers = (expand_kernel_multiple_from_suspension,) + tuple(extra_providers)
    from phase165_r12_r30_ehp_surjectivity import expand_ehp_whole_image
    extra_providers = (expand_ehp_whole_image,) + tuple(extra_providers)
    from phase165_r12_r31_proven_cyclic_reuse import expand_free_cyclic_structure_from_relation
    extra_providers = (expand_free_cyclic_structure_from_relation,) + tuple(extra_providers)
    extra_providers = (build_concrete_kernel_provider(bridge),) + tuple(extra_providers)
    extra_providers = (build_exactness_binding_provider(bridge), build_prop42_specialization_provider(bridge), expand_ehp_exactness_consequences) + tuple(extra_providers)
    # Phase 169 R3E: connect the pre-existing typed EHP goal expansions.
    # These propose subgoals only; no completed map property or proof leaf is inserted.
    from phase165_r14_r5_ehp_connection import (
        expand_registered_ehp_goal, expand_registered_ehp_terminal_goal,
        expand_cited_ehp_terminal_goal,
    )
    extra_providers = (expand_registered_ehp_goal,) + tuple(extra_providers)
    available = []
    for link in bridge.proof_links:
        if link.step is None or link.step.rule is not ProofRule.GIVEN:
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        if assertion.origin is AssertionOrigin.FIXED_STATEMENT:
            available.append(link.step.conclusion)

    from phase165_r12_r15_toda51 import expand_cited_toda51_zero
    from phase165_r12_r24_web_search_connection import expand_finite_cyclic_relation
    from phase165_r12_r20_eta_definition import expand_cited_eta_definition
    from phase165_r12_r21_eta_generator_chain import expand_cited_eta_generator
    from phase169_r10d2_general_family_definition.family_citation import (
        expand_cited_stable_family,
    )
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
    from phase165_r57_r26_generic_search_connection import (
        build_generic_backward_expansion_provider,
        merge_backward_expansions,
    )

    unified_registry, _unified_report = build_unified_backward_rule_registry()
    unified_rules = unified_registry.rules()
    generic_provider = build_generic_backward_expansion_provider(unified_rules)

    # R6-2 R4: cited source anchors bind otherwise unknown premise variables.
    from phase165_r6_2_r4_seeded_goals import generate_seeded_backward_goals
    seeded_rules = unified_rules
    seeded_steps = tuple(
        link.step for link in bridge.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and bridge.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
        and link.step.conclusion == bridge.registry.assertion(link.assertion_id).content
    )

    # R6-2 R3: use only cited GIVEN witnesses for verified inverse proposals.
    from phase165_r6_2_r2_verified_inverse import reverse_rules_from_witnesses
    witness_rules = unified_rules
    cited_witnesses = tuple(
        link.step for link in bridge.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and bridge.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
        and link.step.conclusion == bridge.registry.assertion(link.assertion_id).content
    )

    shared_provider_registry = build_shared_expansion_provider_registry(
        expand_generic_iso_goal=expand_generic_iso_goal,
        expand_generic_ehp_hopf_goal=expand_generic_ehp_hopf_goal,
        expand_delta_zero_from_suspension_iso=expand_delta_zero_from_suspension_iso,
        expand_diagonal_suspension=expand_diagonal_suspension,
        extra_providers=extra_providers,
    )

    context_provider_registry = build_context_expansion_provider_registry(
        available=tuple(available),
        prior_conclusions=prior_conclusions,
        expand_registered_toda45_finite_cyclic_goal=expand_registered_toda45_finite_cyclic_goal,
        expand_registered_eta_specialization=expand_registered_eta_specialization,
        expand_registered_delta_image_goal=expand_registered_delta_image_goal,
        expand_cited_general_specialization=expand_cited_general_specialization,
    )

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        # R10ET-R5: use the single, replayable Definition for every eligible
        # typed stable GeneratorImage, regardless of the generator's label.
        from phase169_r10eq_r1_universal_stable_definition.definition import (
            expand_defined_stable_element_image,
        )
        defined_options = expand_defined_stable_element_image(goal)
        if defined_options:
            return defined_options
        options = []
        from phase166_r3q_hopf_image_relation import expand_hopf_image_relation
        options.extend(expand_hopf_image_relation(goal, tuple(available)))
        from phase171_r2h_prop22_cited_hopf.source import (
            expand_cited_prop22_right_formula,
        )
        options.extend(expand_cited_prop22_right_formula(goal, tuple(available)))
        from phase171_r2i_eta_hopf_bridge.source import (
            expand_cited_eta_hopf_power,
        )
        options.extend(expand_cited_eta_hopf_power(goal, tuple(available)))
        from phase171_r2j_r2_cyclic_hopf_surjective.source import (
            expand_cited_cyclic_hopf_surjectivity,
        )
        options.extend(expand_cited_cyclic_hopf_surjectivity(
            goal, tuple(available), proof_target=proof_target,
        ))
        from phase171_r2j_r3_ehp_exactness.source import (
            expand_cited_ehp_surjectivity_consequences,
        )
        options.extend(expand_cited_ehp_surjectivity_consequences(goal))
        options.extend(expand_finite_cyclic_relation(goal))
        from phase169_r3o_stable_composite_rule import (
            expand_cited_toda45_composite_transport,
        )
        options.extend(expand_cited_toda45_composite_transport(
            goal, tuple(available),
        ))
        from phase169_r5b_pi75_prior_transport.rule import (
            expand_prior_cited_toda45_composite_transport,
        )
        legacy_one_step_options = expand_prior_cited_toda45_composite_transport(
            goal, tuple(available), bridge, proof_target=proof_target,
        )
        options.extend(legacy_one_step_options)
        from phase169_r6a_pi86_two_step_transport.rule import (
            expand_prior_two_step_eta_square_transport,
        )
        legacy_two_step_options = expand_prior_two_step_eta_square_transport(
            goal, tuple(available), bridge, proof_target=proof_target,
        )
        options.extend(legacy_two_step_options)
        # R10E1: one typed entry for zero, cyclic, free and direct-sum groups.
        # Previously verified finite-cyclic derivations retain their R7 adapter.
        # Neither DB results nor candidate generators become GIVEN proof leaves.
        from homotopy_groups import TodaPrimaryGroupZeroStatement
        from phase169_r10e1_general_group_transport.transport import (
            expand_prior_general_group_transport,
        )
        if (not legacy_one_step_options and not legacy_two_step_options
                and ((isinstance(goal, Relation)
                      and isinstance(goal.lhs, TodaPrimaryGroup)
                      and type(goal.lhs.group_dimension) is int
                      and type(goal.lhs.sphere_dimension) is int)
                     or isinstance(goal, TodaPrimaryGroupZeroStatement))):
            options.extend(expand_prior_general_group_transport(
                goal, tuple(available), bridge, proof_target=proof_target,
            ))
        options.extend(expand_registered_ehp_terminal_goal(goal, tuple(available)))
        # R3I: earlier cited GIVEN sources are valid inference premises.
        # Retain the historical inference-only proposal independently.
        options.extend(expand_cited_ehp_terminal_goal(goal, tuple(available)))
        from phase168_r2_toda52_transport import expand_toda52_finite_cyclic_goal
        options.extend(expand_toda52_finite_cyclic_goal(goal, tuple(available)))
        options.extend(expand_cited_toda51_zero(goal, tuple(available)))
        options.extend(expand_cited_eta_definition(goal, tuple(available)))
        eta_generator_options = expand_cited_eta_generator(goal)
        options.extend(eta_generator_options)
        cited_stable_options = expand_cited_stable_family(
            goal, tuple(available),
        )
        options.extend(cited_stable_options)
        composite_image_options = ()
        if not eta_generator_options:
            from phase169_r10e5_composite_generator_image.rule import (
                expand_composite_generator_image,
            )
            composite_image_options = expand_composite_generator_image(goal)
            options.extend(composite_image_options)
        from phase169_r4b_prop44_injectivity.rule import expand_cited_prop44_injectivity
        options.extend(expand_cited_prop44_injectivity(goal, tuple(available)))
        from phase169_r4c_pi64_suspension_iso.rule import expand_pi64_suspension_isomorphism
        options.extend(expand_pi64_suspension_isomorphism(goal))
        from phase166_r3ac_stable_notation import expand_stable_eta_notation
        options.extend(expand_stable_eta_notation(goal, tuple(available)))
        from phase166_r3v_generator_transport import expand_generator_transport_normalization
        options.extend(expand_generator_transport_normalization(goal, tuple(available)))
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
        for provider in context_provider_registry.providers():
            new = provider(goal)
            if not isinstance(new, tuple) or not all(isinstance(x, GoalExpansion) for x in new):
                raise TypeError("expansion provider contract violated")
            options.extend(new)
        for provider in shared_provider_registry.providers():
            new = provider(goal)
            if not isinstance(new, tuple) or not all(isinstance(x, GoalExpansion) for x in new):
                raise TypeError("expansion provider contract violated")
            options.extend(new)
        # R2 returns candidate Goals only; the recursive search still verifies ProofSteps.
        # Exhaustion is not equivalent to proof; preserve the older search proposals.
        try:
            witness_options = reverse_rules_from_witnesses(
                goal, witness_rules, cited_witnesses, max_combinations=2048,
            )
        except ValueError as exc:
            if str(exc) != "generic witness inverse search budget exceeded":
                raise
            witness_options = ()
        merged = merge_backward_expansions(
            merge_backward_expansions(tuple(options), generic_provider(goal)),
            witness_options,
        )
        try:
            seeded_options = generate_seeded_backward_goals(
                goal, seeded_rules, seeded_steps, max_candidates=2048,
            )
        except ValueError as exc:
            if str(exc) != "seeded backward search budget exceeded":
                raise
            seeded_options = ()
        merged = merge_backward_expansions(merged, seeded_options)
        return retain_ordered_root_expansions(proof_target, goal, merged)
    return expand

```

## 新規 source.py 全文

```python
"""Prove Delta=0 and E injective from already proved typed EHP premises.

No source or target group is assumed, and no new GIVEN is introduced.
An explicit, well-indexed Proposition 4.2 window is required at each step.
"""
from __future__ import annotations

from homotopy_groups import (
    TodaDeltaMap,
    TodaEHPExactnessWindow,
    TodaHopfInvariantMap,
    TodaPrimaryGroup,
    TodaSuspensionMap,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, ProofRule
from toda_rules import TodaDeltaZeroStatement, TodaProp42ExactnessStatement


def _h_delta_inputs(goal: object) -> tuple[MapSurjective, TodaProp42ExactnessStatement] | None:
    if not isinstance(goal, TodaDeltaZeroStatement) or not isinstance(goal.map, TodaDeltaMap):
        return None
    delta = goal.map
    group, target = delta.source_group, delta.target_group
    if not isinstance(group, TodaPrimaryGroup) or not isinstance(target, TodaPrimaryGroup):
        return None
    q, h_sphere, n = group.group_dimension, group.sphere_dimension, target.sphere_dimension
    if not all(type(x) is int for x in (q, h_sphere, n)):
        return None
    if n < 1 or h_sphere != 2 * n + 1 or target.group_dimension != q - 2:
        return None
    h_source = TodaPrimaryGroup(q, n + 1)
    exact = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=h_source, middle_term=group, target_term=target,
        first_map=EHP_H_MAP, second_map=EHP_DELTA_MAP,
    ))
    if prop42_exactness_indices(exact) is None:
        return None
    return MapSurjective(TodaHopfInvariantMap(h_source, group)), exact


def _delta_e_inputs(goal: object) -> tuple[TodaDeltaZeroStatement, TodaProp42ExactnessStatement] | None:
    if not isinstance(goal, MapInjective) or not isinstance(goal.map, TodaSuspensionMap):
        return None
    suspension = goal.map
    source, target = suspension.source_group, suspension.target_group
    if not isinstance(source, TodaPrimaryGroup) or not isinstance(target, TodaPrimaryGroup):
        return None
    q, n = source.group_dimension, source.sphere_dimension
    if not all(type(x) is int for x in (
        q, n, target.group_dimension, target.sphere_dimension,
    )) or n < 1 or target != TodaPrimaryGroup(q + 1, n + 1):
        return None
    previous = TodaPrimaryGroup(q + 2, 2 * n + 1)
    delta_zero = TodaDeltaZeroStatement(TodaDeltaMap(previous, source))
    exact = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=previous, middle_term=source, target_term=target,
        first_map=EHP_DELTA_MAP, second_map=EHP_E_MAP,
    ))
    if prop42_exactness_indices(exact) is None:
        return None
    return delta_zero, exact


def delta_zero_from_surjective_hopf_rule(goal: TodaDeltaZeroStatement) -> InferenceRule:
    """When im(H) is all of B=ker(Delta), Delta is the zero map."""
    inputs = _h_delta_inputs(goal)
    if inputs is None:
        raise ValueError("invalid typed H-Delta exactness goal")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and (premises[0].conclusion, premises[1].conclusion) == inputs
            and _h_delta_inputs(goal) == inputs
        )

    return InferenceRule(
        name="EHP H surjectivity and H-Delta exactness imply zero Delta",
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=MapSurjective),
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=TodaProp42ExactnessStatement),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def suspension_injective_from_zero_delta_rule(goal: MapInjective) -> InferenceRule:
    """Exactness im(Delta)=ker(E) and Delta=0 force E injective."""
    inputs = _delta_e_inputs(goal)
    if inputs is None:
        raise ValueError("invalid typed Delta-E exactness goal")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and (premises[0].conclusion, premises[1].conclusion) == inputs
            and _delta_e_inputs(goal) == inputs
        )

    return InferenceRule(
        name="EHP zero Delta and Delta-E exactness imply suspension injectivity",
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=TodaDeltaZeroStatement),
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=TodaProp42ExactnessStatement),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_cited_ehp_surjectivity_consequences(goal: object) -> tuple[GoalExpansion, ...]:
    """Generic backward goals only; actual premises must be reconstructed."""
    hd = _h_delta_inputs(goal)
    if hd is not None:
        return (GoalExpansion(delta_zero_from_surjective_hopf_rule(goal), hd),)
    de = _delta_e_inputs(goal)
    if de is not None:
        return (GoalExpansion(suspension_injective_from_zero_delta_rule(goal), de),)
    return ()

```

## 新規 audit.py 全文

```python
"""R2J-R3: replay H-surjectivity and both cited EHP windows, no GIVEN promotion."""
from __future__ import annotations

import json
from pathlib import Path

from homotopy_groups import (
    TodaDeltaMap, TodaHopfInvariantMap, TodaPrimaryGroup, TodaSuspensionMap,
)
from phase165_r12_r11_prop42_unified import (
    TodaProp42GeneralExactnessStatement, expand_cited_prop42_exactness,
)
from phase165_r12_r20_eta_definition import expand_cited_eta_definition
from phase165_r12_r21_eta_generator_chain import expand_cited_eta_generator
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase166_r3c_publication_order import precedes_citing_assertion
from phase171_r2h_prop22_cited_hopf.source import expand_cited_prop22_right_formula
from phase171_r2i_eta_hopf_bridge.audit import _available, _checked_chain, _screened_context
from phase171_r2i_eta_hopf_bridge.source import expand_cited_eta_hopf_power
from phase171_r2j_r2_cyclic_hopf_surjective.source import expand_cited_cyclic_hopf_surjectivity
from phase171_r2j_r3_ehp_exactness.source import (
    _delta_e_inputs, _h_delta_inputs, expand_cited_ehp_surjectivity_consequences,
)
from proof import ProofRule
from toda_rules import TodaDeltaZeroStatement, TodaProp42ExactnessStatement
from unified_statement_registry import AssertionOrigin

OUTPUT = Path(__file__).resolve().parent / "output"


def _goals():
    delta = TodaDeltaZeroStatement(TodaDeltaMap(
        TodaPrimaryGroup(7, 5), TodaPrimaryGroup(5, 2),
    ))
    e_injective = MapInjective(TodaSuspensionMap(
        TodaPrimaryGroup(5, 2), TodaPrimaryGroup(6, 3),
    ))
    return delta, e_injective


def _scoped_provider(available, proof_target):
    def expand(goal):
        return (
            expand_cited_ehp_surjectivity_consequences(goal)
            + expand_cited_prop42_exactness(goal, available)
            + expand_cited_cyclic_hopf_surjectivity(
                goal, available, proof_target=proof_target,
            )
            + expand_cited_eta_hopf_power(goal, available)
            + expand_cited_prop22_right_formula(goal, available)
            + expand_cited_eta_definition(goal, available)
            + expand_cited_eta_generator(goal)
        )
    return expand


def _walk(root):
    result = []
    seen = set()

    def visit(step):
        if id(step) in seen:
            return
        seen.add(id(step))
        result.append(step)
        for parent in step.premises:
            visit(parent)
    visit(root)
    return tuple(result)


def build_r2j_r3_proof():
    """Build the two zero/injective roots using one screened pi6^3 context."""
    screened, group_goal, citing = _screened_context()
    chain, available = _checked_chain(screened, citing)
    delta, injective = _goals()
    exact_sources = tuple(
        link for link in screened.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and type(link.step.conclusion) is TodaProp42GeneralExactnessStatement
    )
    if len(exact_sources) != 1:
        raise RuntimeError("one citation-screened Proposition 4.2 general source required")
    entry = exact_sources[0]
    if (screened.registry.assertion(entry.assertion_id).origin is not AssertionOrigin.FIXED_STATEMENT
            or not precedes_citing_assertion(screened, entry.assertion_id, citing)):
        raise RuntimeError("Proposition 4.2 not positioned before the group goal")
    if _h_delta_inputs(delta) is None or _delta_e_inputs(injective) is None:
        raise RuntimeError("EHP consecutive windows have invalid indices")
    if _h_delta_inputs(delta)[0] != MapSurjective(TodaHopfInvariantMap(
            TodaPrimaryGroup(7, 3), TodaPrimaryGroup(7, 5))):
        raise RuntimeError("the H-Delta window uses a wrong Hopf map")
    if _delta_e_inputs(injective)[0] != delta:
        raise RuntimeError("the two EHP windows do not share the same Delta")
    public = shared_expansion_provider(screened, proof_target=group_goal)
    for target in (delta, injective):
        if not any(option.subgoals == expand_cited_ehp_surjectivity_consequences(target)[0].subgoals
                   and option.rule.name == expand_cited_ehp_surjectivity_consequences(target)[0].rule.name
                   for option in public(target)):
            raise RuntimeError("R2J-R3 is not connected to the public shared provider")
    expand = _scoped_provider(available, group_goal)
    delta_root = reconstruct_registered_goal(
        delta, screened, citing, expand, lookup_mode="typed_reference_publication",
    )
    injective_root = reconstruct_registered_goal(
        injective, screened, citing, expand, lookup_mode="typed_reference_publication",
    )
    if (delta_root.rule is not ProofRule.INFERENCE
            or injective_root.rule is not ProofRule.INFERENCE
            or delta_root.conclusion != delta
            or injective_root.conclusion != injective):
        raise RuntimeError("the two EHP conclusions were not inferred")
    ancestry = _walk(injective_root)
    if not any(step.conclusion == chain.conclusion and step.rule is ProofRule.INFERENCE
               for step in ancestry):
        raise RuntimeError("R2I Hopf image is not an inferred ancestor")
    if not any(step.conclusion == delta and step.rule is ProofRule.INFERENCE
               for step in ancestry):
        raise RuntimeError("Delta=0 was not inferred")
    if not any(step.conclusion == _h_delta_inputs(delta)[0]
               and step.rule is ProofRule.INFERENCE for step in ancestry):
        raise RuntimeError("R2J-R2 surjectivity was not inferred")
    expected_windows = (_h_delta_inputs(delta)[1], _delta_e_inputs(injective)[1])
    for window in expected_windows:
        matches = tuple(step for step in ancestry if step.conclusion == window)
        if (len(matches) != 1 or matches[0].rule is not ProofRule.INFERENCE
                or not any(parent.conclusion == entry.step.conclusion
                           and parent.rule is ProofRule.GIVEN for parent in matches[0].premises)):
            raise RuntimeError("specialized exactness lacks the cited universal source")
    leaves = tuple(step for step in ancestry if step.rule is ProofRule.GIVEN)
    permitted = tuple(link.step.conclusion for link in screened.proof_links
                      if link.step is not None and link.step.rule is ProofRule.GIVEN)
    if (len(leaves) != 5
            or any(leaf.conclusion not in permitted or leaf.premises for leaf in leaves)
            or sum(leaf.conclusion == entry.step.conclusion for leaf in leaves) != 1):
        raise RuntimeError("wrong number or content of citation-screened GIVEN leaves")
    forbidden = (delta, injective, _h_delta_inputs(delta)[0])
    if any(step.conclusion in forbidden and step.rule is ProofRule.GIVEN for step in ancestry):
        raise RuntimeError("EHP result was promoted into GIVEN")
    if any(step.conclusion == group_goal for step in ancestry):
        raise RuntimeError("pi6^3 target group prematurely imported")
    return delta_root, injective_root, ancestry, entry


def run():
    delta_root, injective_root, ancestry, ref = build_r2j_r3_proof()
    report = {
        "result": "PASS_CITED_DELTA_ZERO_AND_E_INJECTIVE_ONLY",
        "delta_zero": repr(delta_root.conclusion),
        "e_injective": repr(injective_root.conclusion),
        "proposition42_assertion_id": ref.assertion_id,
        "inferences": sum(step.rule is ProofRule.INFERENCE for step in ancestry),
        "given_leaves": sum(step.rule is ProofRule.GIVEN for step in ancestry),
        "given_added": 0,
        "pi63_proven": False,
        "full_pytest": False,
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    report_path = OUTPUT / "audit.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R2J_R3_H_SURJECTIVE_ANCESTRY=PASS", flush=True)
    print("PHASE171_R2J_R3_H_DELTA_EXACTNESS=PASS", flush=True)
    print("PHASE171_R2J_R3_DELTA_ZERO=PASS", flush=True)
    print("PHASE171_R2J_R3_DELTA_E_EXACTNESS=PASS", flush=True)
    print("PHASE171_R2J_R3_E_INJECTIVE=PASS", flush=True)
    print("PHASE171_R2J_R3_INFERENCES=" + str(report["inferences"]), flush=True)
    print("PHASE171_R2J_R3_GIVEN_LEAVES=" + str(report["given_leaves"]), flush=True)
    print("PHASE171_R2J_R3_PI63_PROVEN=False", flush=True)
    print("PHASE171_R2J_R3_RESULT=" + report["result"], flush=True)
    print("PHASE171_R2J_R3_REPORT=" + str(report_path), flush=True)


if __name__ == "__main__":
    run()

```

## 新規テスト 全文

```python
"""Proven H-surjectivity and cited exactness must justify Delta=0 and E injective."""
from __future__ import annotations

from homotopy_groups import (
    TodaDeltaMap, TodaHopfInvariantMap, TodaPrimaryGroup, TodaSuspensionMap,
)
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase171_r2j_r3_ehp_exactness.audit import _goals, build_r2j_r3_proof
from phase171_r2j_r3_ehp_exactness.source import (
    _delta_e_inputs, _h_delta_inputs, delta_zero_from_surjective_hopf_rule,
    expand_cited_ehp_surjectivity_consequences,
    suspension_injective_from_zero_delta_rule,
)
from proof import ProofRule, ProofStep, find_inference_matches_for_rule
from toda_rules import TodaDeltaZeroStatement


def test_full_proof_replays_h_and_both_exactness_windows():
    delta_root, injective_root, nodes, reference = build_r2j_r3_proof()
    assert delta_root.rule is ProofRule.INFERENCE
    assert injective_root.rule is ProofRule.INFERENCE
    assert injective_root.premises[0].conclusion == delta_root.conclusion
    assert sum(node.rule is ProofRule.GIVEN for node in nodes) == 5
    assert sum(node.rule is ProofRule.INFERENCE for node in nodes) >= 18
    assert reference.step.rule is ProofRule.GIVEN


def test_consecutive_ehp_windows_are_well_typed():
    delta, injective = _goals()
    hopf_surj, h_delta = _h_delta_inputs(delta)
    zero, delta_e = _delta_e_inputs(injective)
    assert zero == delta
    assert hopf_surj == MapSurjective(TodaHopfInvariantMap(
        TodaPrimaryGroup(7, 3), TodaPrimaryGroup(7, 5),
    ))
    assert prop42_exactness_indices(h_delta) == (2, 7, "h_delta")
    assert prop42_exactness_indices(delta_e) == (2, 6, "delta_e")
    assert len(expand_cited_ehp_surjectivity_consequences(delta)) == 1
    assert len(expand_cited_ehp_surjectivity_consequences(injective)) == 1


def test_forged_given_surjectivity_and_exactness_are_rejected():
    delta, _ = _goals()
    surj, exact = _h_delta_inputs(delta)
    rule = delta_zero_from_surjective_hopf_rule(delta)
    forged = (ProofStep(surj, (), ProofRule.GIVEN), ProofStep(exact, (), ProofRule.GIVEN))
    assert find_inference_matches_for_rule(rule, forged) == ()
    assert find_inference_matches_for_rule(rule, (
        ProofStep(surj, (), ProofRule.INFERENCE), forged[1],
    )) == ()


def test_forged_given_delta_and_exactness_are_rejected():
    delta, injective = _goals()
    zero, exact = _delta_e_inputs(injective)
    assert delta == zero
    rule = suspension_injective_from_zero_delta_rule(injective)
    forged = (ProofStep(zero, (), ProofRule.GIVEN), ProofStep(exact, (), ProofRule.GIVEN))
    assert find_inference_matches_for_rule(rule, forged) == ()
    assert find_inference_matches_for_rule(rule, (
        ProofStep(zero, (), ProofRule.INFERENCE), forged[1],
    )) == ()


def test_wrong_delta_and_suspension_indices_fail_closed():
    delta, injective = _goals()
    invalid = TodaDeltaZeroStatement(TodaDeltaMap(
        TodaPrimaryGroup(7, 5), TodaPrimaryGroup(6, 2),
    ))
    assert _h_delta_inputs(invalid) is None
    assert expand_cited_ehp_surjectivity_consequences(invalid) == ()
    wrong = MapInjective(TodaSuspensionMap(
        TodaPrimaryGroup(5, 2), TodaPrimaryGroup(6, 4),
    ))
    assert _delta_e_inputs(wrong) is None
    assert expand_cited_ehp_surjectivity_consequences(wrong) == ()
    assert _h_delta_inputs(delta) is not None
    assert _delta_e_inputs(injective) is not None


def test_unrelated_exactness_window_cannot_substitute():
    delta, _ = _goals()
    surj, exact = _h_delta_inputs(delta)
    other = TodaDeltaZeroStatement(TodaDeltaMap(
        TodaPrimaryGroup(8, 5), TodaPrimaryGroup(6, 2),
    ))
    _, other_exact = _h_delta_inputs(other)
    rule = delta_zero_from_surjective_hopf_rule(delta)
    premises = (
        ProofStep(surj, (), ProofRule.INFERENCE),
        ProofStep(other_exact, (), ProofRule.INFERENCE),
    )
    assert find_inference_matches_for_rule(rule, premises) == ()
    assert exact != other_exact

```

## インストーラー回帰テスト 全文

```python
"""The R2J-R3 installer changes only the reviewed R2J-R2 hook boundary."""
from __future__ import annotations

import pytest

from phase171_r2j_r3_ehp_exactness.install import ANCHOR, ADDITION, _insert_hook


def _sample(newline: str = "\n") -> bytes:
    code = (
        "def shared_expansion_provider():\n"
        "    def expand(goal):\n"
        + ANCHOR
        + "        return ()\n"
        + "    return expand\n"
    )
    return code.replace("\n", newline).encode("utf-8")


def test_installer_preserves_exact_unrelated_code():
    original = _sample()
    result = _insert_hook(original)
    assert result == original.replace(ANCHOR.encode(), (ANCHOR + ADDITION).encode())


def test_installer_preserves_windows_crlf():
    original = _sample("\r\n")
    result = _insert_hook(original)
    assert b"\r\n" in result
    assert result.replace(b"\r\n", b"\n") == _insert_hook(_sample())


def test_installer_rejects_duplicate_apply_and_missing_anchor():
    original = _sample()
    with pytest.raises(RuntimeError):
        _insert_hook(_insert_hook(original))
    with pytest.raises(RuntimeError):
        _insert_hook(b"def unrelated():\n    return 1\n")

```

## コミット済み基準回帰テスト 全文

```python
"""R2J-R3 installer regressions for a committed R2J-R2 baseline.

These tests are deliberately self-contained and require neither a GitHub
connection nor the earlier transient R2J-R2 install.py module.
"""
from __future__ import annotations

import subprocess
from types import SimpleNamespace

import pytest

from phase171_r2j_r3_ehp_exactness import install


def _baseline() -> bytes:
    return (
        "def shared_expansion_provider():\n"
        "    def expand(goal):\n"
        + install.ANCHOR
        + "        return ()\n"
        + "    return expand\n"
    ).encode("utf-8")


def _fixture(monkeypatch, tmp_path, *, eol="\n"):
    baseline = _baseline()
    target = tmp_path / "phase165_r52_r9_shared_math.py"
    content = baseline.replace(b"\n", eol.encode("ascii"))
    target.write_bytes(content)
    output = tmp_path / "output"
    monkeypatch.setattr(install, "ROOT", tmp_path)
    monkeypatch.setattr(install, "TARGET", target)
    monkeypatch.setattr(install, "BACKUP", output / "before.py")
    monkeypatch.setattr(install, "STATE", output / "state.json")
    monkeypatch.setattr(install, "R2J_R2_SHARED_BLOB", install._git_blob_sha(baseline))
    monkeypatch.setattr(install, "_git_bytes", lambda *args: baseline)
    monkeypatch.setattr(install, "_git", lambda *args: (
        "develop" if args == ("branch", "--show-current") else
        "future-head" if args == ("rev-parse", "HEAD") else
        install.R2J_R2_SHARED_BLOB if args == (
            "rev-parse", "HEAD:phase165_r52_r9_shared_math.py"
        ) else ""
    ))
    monkeypatch.setattr(
        install.subprocess, "run",
        lambda *args, **kwargs: SimpleNamespace(returncode=0),
    )
    return target, baseline


def test_committed_r2j_r2_is_available_without_transient_installer(monkeypatch, tmp_path):
    target, baseline = _fixture(monkeypatch, tmp_path)
    assert install._exact_r2j_r2_baseline() == baseline
    observed, installed = install.preflight()
    assert observed == target.read_bytes()
    assert installed is False


def test_committed_r2j_r2_allows_crlf_checkout_without_rewriting_others(monkeypatch, tmp_path):
    target, baseline = _fixture(monkeypatch, tmp_path, eol="\r\n")
    observed, installed = install.preflight()
    assert installed is False
    modified = install._insert_hook(observed)
    assert b"\r\n" in modified
    assert modified.replace(b"\r\n", b"\n") == install._insert_hook(baseline)
    assert target.read_bytes() == observed


def test_committed_r2j_r2_rejects_unreviewed_worktree_change(monkeypatch, tmp_path):
    target, _ = _fixture(monkeypatch, tmp_path)
    target.write_bytes(target.read_bytes().replace(b"return ()", b"return (goal,)"))
    with pytest.raises(RuntimeError, match="unexpected shared-module bytes"):
        install.preflight()


def test_committed_r2j_r2_rejects_wrong_head_blob(monkeypatch, tmp_path):
    _fixture(monkeypatch, tmp_path)
    monkeypatch.setattr(install, "_git", lambda *args: (
        "develop" if args == ("branch", "--show-current") else
        "future-head" if args == ("rev-parse", "HEAD") else
        "unreviewed-blob" if args[0] == "rev-parse" else ""
    ))
    with pytest.raises(RuntimeError, match="committed shared module differs"):
        install.preflight()


def test_committed_r2j_r2_rejects_non_descendant_head(monkeypatch, tmp_path):
    _fixture(monkeypatch, tmp_path)
    monkeypatch.setattr(
        install.subprocess, "run",
        lambda *args, **kwargs: SimpleNamespace(returncode=1),
    )
    with pytest.raises(RuntimeError, match="HEAD does not contain"):
        install.preflight()


def test_committed_r2j_r2_rejects_wrong_source_blob(monkeypatch, tmp_path):
    _fixture(monkeypatch, tmp_path)
    monkeypatch.setattr(install, "_git_bytes", lambda *args: b"unreviewed git content")
    with pytest.raises(RuntimeError, match="audited R2J-R2 Git blob changed"):
        install.preflight()


def test_committed_r2j_r2_accepts_already_installed_r2j_r3(monkeypatch, tmp_path):
    target, _ = _fixture(monkeypatch, tmp_path)
    target.write_bytes(install._insert_hook(target.read_bytes()))
    _, installed = install.preflight()
    assert installed is True

```

## 新規 install.py 全文

```python
"""Safe R2J-R3 installer from a committed, audited R2J-R2 baseline."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
OUTPUT = HERE / "output"
BACKUP = OUTPUT / "phase165_r52_r9_shared_math.py.before_r2j_r3"
STATE = OUTPUT / "state.json"
R2J_R2_COMMIT = "8b8deb6ef064e11a230b420d8ae4ae54704e6078"
R2J_R2_SHARED_BLOB = "912b5f4cd03b7bded097bedf8f7b4cbd36b5207b"
ANCHOR = (
    "        options.extend(expand_cited_cyclic_hopf_surjectivity(\n"
    "            goal, tuple(available), proof_target=proof_target,\n"
    "        ))\n"
)
HOOK = "expand_cited_ehp_surjectivity_consequences"
ADDITION = (
    "        from phase171_r2j_r3_ehp_exactness.source import (\n"
    "            expand_cited_ehp_surjectivity_consequences,\n"
    "        )\n"
    "        options.extend(expand_cited_ehp_surjectivity_consequences(goal))\n"
)


def _git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, check=True, capture_output=True,
        encoding="utf-8", errors="replace",
    ).stdout.strip()


def _git_bytes(*args: str) -> bytes:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, check=True, capture_output=True,
    ).stdout


def _git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _insert_hook(before: bytes) -> bytes:
    source = before.decode("utf-8-sig")
    normalized = source.replace("\r\n", "\n")
    if normalized.count(ANCHOR) != 1 or HOOK in normalized:
        raise RuntimeError("R2J-R2 anchor absent, duplicated, or R2J-R3 already present")
    updated = normalized.replace(ANCHOR, ANCHOR + ADDITION)
    ast.parse(updated)
    newline = "\r\n" if b"\r\n" in before else "\n"
    return (b"\xef\xbb\xbf" if before.startswith(b"\xef\xbb\xbf") else b"") + updated.replace("\n", newline).encode("utf-8")


def _exact_r2j_r2_baseline() -> bytes:
    """Read the audited committed file; never import a transient package installer."""
    original = _git_bytes(
        "show", R2J_R2_COMMIT + ":phase165_r52_r9_shared_math.py"
    )
    if _git_blob_sha(original) != R2J_R2_SHARED_BLOB:
        raise RuntimeError("audited R2J-R2 Git blob changed")
    normalized = original.decode("utf-8-sig").replace("\r\n", "\n")
    if normalized.count(ANCHOR) != 1 or HOOK in normalized:
        raise RuntimeError("committed R2J-R2 baseline has an unexpected hook boundary")
    return original


def _same_audited_content(local: bytes, source: bytes) -> bool:
    """Allow only checkout EOL normalization; preserve the local encoding/EOL."""
    return (
        local.startswith(b"\xef\xbb\xbf") == source.startswith(b"\xef\xbb\xbf")
        and local.decode("utf-8-sig").replace("\r\n", "\n")
        == source.decode("utf-8-sig").replace("\r\n", "\n")
    )


def _changed_function(source: str) -> str:
    tree = ast.parse(source)
    nodes = [node for node in tree.body
             if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
             and node.name == "shared_expansion_provider"]
    if len(nodes) != 1:
        raise RuntimeError("shared_expansion_provider was not unique")
    lines = source.splitlines()
    return "\n".join(lines[nodes[0].lineno - 1:nodes[0].end_lineno]) + "\n"


def _full_code(shared: str) -> str:
    marker = "def build_shared_typed_bridge("
    if shared.count(marker) != 1:
        raise RuntimeError("shared import boundary changed")
    additions = (
        ("新規 source.py", HERE / "source.py"),
        ("新規 audit.py", HERE / "audit.py"),
        ("新規テスト", HERE / "tests" / "test_r2j_r3_exactness.py"),
        ("インストーラー回帰テスト", HERE / "tests" / "test_installer.py"),
        ("コミット済み基準回帰テスト", HERE / "tests" / "test_r2j_r3_committed_baseline.py"),
        ("新規 install.py", HERE / "install.py"),
    )
    chunks = [
        "# Phase 171 R2J-R3 — 変更コード全文\n",
        "変更対象: `phase165_r52_r9_shared_math.py` の `shared_expansion_provider()`。",
        "追加位置: R2J-R2 `expand_cited_cyclic_hopf_surjectivity` 呼出し直後。",
        "モジュール冒頭の import 変更なし。新規ファイルの import は各全文に含む。",
        "\n## 本番ファイルの冒頭 import 全文\n\n```python\n" + shared[:shared.index(marker)] + "\n```",
        "\n## 変更後の関数全文\n\n```python\n" + _changed_function(shared) + "\n```",
    ]
    for label, path in additions:
        chunks.append("\n## " + label + " 全文\n\n```python\n" + path.read_text(encoding="utf-8") + "\n```")
    chunks.append("\n## 新規 PowerShell 全文\n\n```powershell\n" + (HERE / "run.ps1").read_text(encoding="utf-8") + "\n```")
    return "\n".join(chunks) + "\n"


def preflight() -> tuple[bytes, bool]:
    branch = _git("branch", "--show-current")
    head = _git("rev-parse", "HEAD")
    print("PHASE171_R2J_R3_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R3_HEAD=" + head, flush=True)
    if branch != "develop":
        raise RuntimeError("develop branch required; never checkout/reset")
    ancestor = subprocess.run(
        ("git", "merge-base", "--is-ancestor", R2J_R2_COMMIT, "HEAD"),
        cwd=ROOT, check=False, capture_output=True,
    )
    if ancestor.returncode != 0:
        raise RuntimeError("HEAD does not contain the audited R2J-R2 commit")
    if _git("rev-parse", "HEAD:phase165_r52_r9_shared_math.py") != R2J_R2_SHARED_BLOB:
        raise RuntimeError("committed shared module differs from audited R2J-R2 blob")
    expected = _exact_r2j_r2_baseline()
    if not TARGET.is_file():
        raise RuntimeError("shared module missing")
    current = TARGET.read_bytes()
    if _same_audited_content(current, expected):
        if _git("diff", "--", "phase165_r52_r9_shared_math.py"):
            raise RuntimeError("existing uncommitted shared-module edit; preserve and audit")
        _insert_hook(current)
        applied = False
    elif _same_audited_content(current, _insert_hook(expected)):
        applied = True
    else:
        raise RuntimeError("unexpected shared-module bytes; preserve local changes and re-audit")
    if not applied and (BACKUP.exists() or STATE.exists()):
        raise RuntimeError("previous R2J-R3 backup exists: inspect before applying")
    print("PHASE171_R2J_R3_R2J_R2_PRESERVED=PASS", flush=True)
    print("PHASE171_R2J_R3_PREFLIGHT=PASS", flush=True)
    print("PHASE171_R2J_R3_ALREADY_INSTALLED=" + str(applied), flush=True)
    return current, applied


def apply(dry_run: bool) -> None:
    raw, installed = preflight()
    if dry_run:
        print("PHASE171_R2J_R3_RESULT=PASS_DRY_RUN", flush=True)
        return
    if installed:
        print("PHASE171_R2J_R3_RESULT=PASS_ALREADY_APPLIED", flush=True)
        return
    altered = _insert_hook(raw)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    BACKUP.write_bytes(raw)
    try:
        TARGET.write_bytes(altered)
        revised = altered.decode("utf-8-sig").replace("\r\n", "\n")
        (OUTPUT / "CHANGED_CODE_FULL_JA.md").write_text(_full_code(revised), encoding="utf-8")
        STATE.write_text(json.dumps({
            "before_sha256": _sha256(raw), "after_sha256": _sha256(altered),
        }, indent=2) + "\n", encoding="utf-8")
    except Exception:
        if TARGET.read_bytes() == altered:
            TARGET.write_bytes(raw)
        raise
    print("PHASE171_R2J_R3_PATCHED=" + TARGET.name, flush=True)
    print("PHASE171_R2J_R3_BACKUP=" + str(BACKUP), flush=True)
    print("PHASE171_R2J_R3_CHANGED_CODE=" + str(OUTPUT / "CHANGED_CODE_FULL_JA.md"), flush=True)
    print("PHASE171_R2J_R3_RESULT=PASS_APPLY", flush=True)


def restore() -> None:
    if not BACKUP.is_file() or not STATE.is_file():
        raise RuntimeError("no verified backup")
    previous = json.loads(STATE.read_text(encoding="utf-8"))
    before = BACKUP.read_bytes()
    if (_sha256(before) != previous["before_sha256"]
            or _sha256(TARGET.read_bytes()) != previous["after_sha256"]):
        raise RuntimeError("current file or backup no longer matches; manual inspection needed")
    TARGET.write_bytes(before)
    STATE.unlink()
    print("PHASE171_R2J_R3_RESULT=PASS_RESTORE", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--dry-run", action="store_true")
    actions.add_argument("--restore", action="store_true")
    args = parser.parse_args()
    if args.restore:
        restore()
    else:
        apply(args.dry_run)


if __name__ == "__main__":
    main()

```

## 新規 PowerShell 全文

```powershell
param([switch]$DryRun)
$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $Root
try {
    $Package = ".\phase171_r2j_r3_ehp_exactness"
    & python "$Package\install.py" --dry-run
    if ($LASTEXITCODE -ne 0) { throw "R2J-R3 preflight failed" }
    if ($DryRun) {
        Write-Output "PHASE171_R2J_R3_RUN=PASS_DRY_RUN"
        return
    }
    $Target = Join-Path $Root "phase165_r52_r9_shared_math.py"
    $WasInstalled = [bool](Select-String -Path $Target -Pattern "expand_cited_ehp_surjectivity_consequences" -Quiet)
    & python "$Package\install.py"
    if ($LASTEXITCODE -ne 0) { throw "R2J-R3 installation failed" }
    try {
        & python -m pytest -p no:cacheprovider -q `
            "$Package\tests\test_installer.py" `
            "$Package\tests\test_r2j_r3_exactness.py" `
            ".\phase171_r2j_r2_cyclic_hopf_surjective\tests\test_cited_cyclic_hopf.py" `
            ".\phase171_r2i_eta_hopf_bridge\tests\test_cited_eta_hopf.py" `
            ".\phase171_r2j_r1_prop53_ehp_audit\tests\test_audit.py"
        if ($LASTEXITCODE -ne 0) { throw "R2J-R3 focused pytest failed" }
        Write-Output "PHASE171_R2J_R3_FOCUSED_PYTEST=PASS"
        & python -m phase171_r2j_r3_ehp_exactness.audit
        if ($LASTEXITCODE -ne 0) { throw "R2J-R3 proof tree audit failed" }
    } catch {
        if (-not $WasInstalled) {
            & python "$Package\install.py" --restore
            if ($LASTEXITCODE -ne 0) { throw "R2J-R3 rollback failed: inspect backup" }
        }
        throw
    }
    Write-Output "PHASE171_R2J_R3_RUN=PASS"
} finally {
    Pop-Location
}

```
