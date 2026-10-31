# Phase 171 R20R11 — 完全な置換コード

対象: `phase171_r2j_r2_cyclic_hopf_surjective/source.py`、`phase165_r52_r9_shared_math.py`。

## source.py の変更後の import 全文

```python
from __future__ import annotations

from expression import Composition, HomotopyElement, IteratedSuspension, MapApplication, Suspension
from homotopy_groups import FiniteCyclicGroup, TodaHopfInvariantMap, TodaPrimaryGroup
from map_facts import EHP_H_MAP
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r3_recursive_search import GoalExpansion
from phase168_r2_8_3_generator_identity.identity import same_registered_group_presentation
from phase168_r2_8_4_generic_specialization.specialization import specialize_registered_higher_stem
from phase169_r10e4_ordered_db_prior.db_prior import admitted_db_step, verified_db_step
from phase171_r2i_eta_hopf_bridge.source import eligible_eta_hopf_chains
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType
```

## source.py の新規関数全文（既存 surjectivity rule の直後）

```python
def verified_prior_cyclic_generator_image_surjectivity_rule(
    goal: MapSurjective, group: Relation, image: Relation, *,
    proof_target: object, bridge: object,
) -> InferenceRule:
    """Reuse a *rechecked* earlier DB group, never an arbitrary GIVEN.

    The Hopf image remains a separately reconstructed INFERENCE.  The database
    admission is revalidated by the existing Phase 169 provenance gate on the
    *actual* ProofStep selected by canonical public recursion.
    """
    if not _valid_surjective_pair(goal, group, image):
        raise ValueError("typed cyclic Hopf generator image does not match")
    if admitted_db_step(group, proof_target=proof_target, bridge=bridge) is None:
        raise ValueError("cyclic group is not an eligible earlier database result")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and premises[0].rule is ProofRule.GIVEN
            and premises[1].rule is ProofRule.INFERENCE
            and bool(premises[1].premises)
            and premises[0].conclusion == group
            and premises[1].conclusion == image
            and verified_db_step(
                premises[0], proof_target=proof_target, bridge=bridge,
            )
            and _valid_surjective_pair(goal, group, image)
        )

    return InferenceRule(
        name="verified earlier database cyclic generator in Hopf image implies surjectivity",
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.GIVEN,
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=group,
            ),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=image,
            ),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )

```

## source.py の変更後の候補生成関数全文

```python
def expand_cited_cyclic_hopf_surjectivity(
    goal: object, available: tuple[object, ...], *,
    proof_target: object = None, bridge: object = None,
) -> tuple[GoalExpansion, ...]:
    """Propose only backed-up group specializations and R2I Hopf chains.

    Do not duplicate the group root's independent existing proof search.
    In subgoals of another proof, the specialized group schema remains a
    separate inference obligation; it is never inserted as a GIVEN.
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    sources = tuple(value for value in available if isinstance(value, Relation))
    if isinstance(goal, Relation):
        if proof_target is None or goal == proof_target:
            return ()
        proposals = []
        for source in sources:
            if _eligible_group_instance(source, goal):
                proposals.append(GoalExpansion(
                    cyclic_group_from_cited_general_rule(goal, source),
                    (source,),
                ))
        return tuple(proposals)
    if not isinstance(goal, MapSurjective) or not isinstance(goal.map, TodaHopfInvariantMap):
        return ()
    proposals = []
    for chain in eligible_eta_hopf_chains(available):
        for source in sources:
            target = goal.map.target_group
            if not isinstance(target, TodaPrimaryGroup):
                continue
            n = target.sphere_dimension
            if type(n) is not int:
                continue
            group = specialize_registered_higher_stem(source, n)
            if group is None or not _valid_surjective_pair(goal, group, chain.conclusion):
                continue
            candidate = GoalExpansion(
                cyclic_generator_image_surjectivity_rule(goal, group, chain.conclusion),
                (group, chain.conclusion),
            )
            if not any(x.subgoals == candidate.subgoals for x in proposals):
                proposals.append(candidate)
            if bridge is not None and proof_target is not None:
                prior = admitted_db_step(
                    group, proof_target=proof_target, bridge=bridge,
                )
                if prior is not None:
                    proposals.append(GoalExpansion(
                        verified_prior_cyclic_generator_image_surjectivity_rule(
                            goal, group, chain.conclusion,
                            proof_target=proof_target, bridge=bridge,
                        ),
                        (group, chain.conclusion),
                    ))
    return tuple(proposals)

```

## shared_math.py の変更後の関数全文

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
            bridge=bridge,
        ))
        from phase171_r2j_r3_ehp_exactness.source import (
            expand_cited_ehp_surjectivity_consequences,
        )
        options.extend(expand_cited_ehp_surjectivity_consequences(goal))
        options.extend(expand_finite_cyclic_relation(goal))
        from phase171_r2j_r4_r9_r7_public_cyclic_root.source import (
            expand_cited_double_cyclic_root,
        )
        options.extend(expand_cited_double_cyclic_root(goal, tuple(available)))
        from phase171_r2j_r4_r9_r8_public_cardinality.source import (
            expand_cited_ehp_middle_cardinality,
        )
        options.extend(expand_cited_ehp_middle_cardinality(goal, tuple(available)))
        from phase171_r2j_r4_r9_r9_public_cyclic_structure.source import (
            expand_cited_full_order_cyclic_structure,
        )
        options.extend(expand_cited_full_order_cyclic_structure(goal, tuple(available)))
        from phase171_r2j_r4_r7_nonzero_nu_order.source import (
            expand_public_order_four_from_nonzero_double,
        )
        options.extend(expand_public_order_four_from_nonzero_double(goal))
        from phase171_r2j_r4_r7_nonzero_nu_order.source import (
            expand_public_injected_generator_nonzero,
        )
        options.extend(expand_public_injected_generator_nonzero(goal, tuple(available)))
        from phase171_r2j_r4_r7_nonzero_nu_order.source import (
            expand_public_nonzero_double_from_cited_source,
        )
        options.extend(expand_public_nonzero_double_from_cited_source(goal, tuple(available)))
        from phase171_r2j_r4_r3_double_image_bridge.source import (
            expand_public_cited_double_image_equality,
        )
        options.extend(expand_public_cited_double_image_equality(goal, tuple(available)))
        from phase171_r2j_r4_r5_short_exact_sequence.source import expand_ehp_short_exact
        options.extend(expand_ehp_short_exact(goal))
        from phase171_r2j_r4_r9_r11_public_eta_symmetry.source import (
            expand_reverse_cited_eta_hopf_equalities,
        )
        directed = expand_reverse_cited_eta_hopf_equalities(goal, tuple(available))
        if directed:
            return directed
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

## 全ファイル

`full_replacements/source.py` と `full_replacements/phase165_r52_r9_shared_math.py` を参照。
実際の patch は元ファイルの改行コードを保持します。
