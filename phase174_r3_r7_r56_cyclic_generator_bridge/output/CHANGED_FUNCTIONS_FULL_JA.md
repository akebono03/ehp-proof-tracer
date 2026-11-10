# R56 変更後の関数全文

## phase165_r52_r9_shared_math.py : shared_expansion_provider

```python
def shared_expansion_provider(bridge: RegistryBridgeResult, extra_providers: tuple = (), *, proof_target=None, prior_conclusions: tuple = ()):
    """Build backward proposals from typed source witnesses and common rules."""
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    # R41: retain DB-prior provenance and the actual cited source boundary.
    # This only proposes an inference; it never registers a proof or GIVEN.
    from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.provider import (
        build_public_adopted_zero_image_provider,
    )
    extra_providers = (
        build_public_adopted_zero_image_provider(
            bridge=bridge, proof_target=proof_target,
        ),
    ) + tuple(extra_providers)
    # R43: add only two source-dependent, conditional EHP map-property goals.
    # No citation, verified proof, or GIVEN is registered by these providers.
    from phase174_r3_r7_r5_zero_image_hopf_injective.rule import (
        expand_hopf_injective_from_zero_image,
    )
    from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import (
        expand_upper_delta_surjectivity,
    )
    extra_providers = (
        expand_hopf_injective_from_zero_image,
        expand_upper_delta_surjectivity,
    ) + tuple(extra_providers)
    # R56: two ordinary typed EHP consequences, shared by every root query.
    # Prefer the two-step generator route while preserving the old R37 rule.
    from phase174_r3_r7_r56_cyclic_generator_bridge.rule import (
        expand_cyclic_generator_from_hopf,
        expand_delta_surjectivity_from_generator,
    )
    extra_providers = (
        expand_delta_surjectivity_from_generator,
        expand_cyclic_generator_from_hopf,
    ) + tuple(extra_providers)
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
        from phase174_r3_r7_r30_prop27_public_provider_wiring.provider import (
            expand_public_cited_prop27_goal,
        )
        cited_prop27_options = expand_public_cited_prop27_goal(goal, bridge)
        if cited_prop27_options:
            return cited_prop27_options
        from phase174_r3_r7_r3_ehp_zero_rule.rule import (
            expand_ehp_zero_from_delta_surjectivity,
        )
        options.extend(expand_ehp_zero_from_delta_surjectivity(goal))
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
        from phase174_r3_r3_injective_delta_zero.rule import expand_delta_zero_from_injection
        options.extend(expand_delta_zero_from_injection(goal))
        from phase174_r3_r5_finite_cyclic_extension.rule import (
            expand_finite_index_two_cyclic_structure, expand_toda48_index_two,
        )
        options.extend(expand_toda48_index_two(goal))
        options.extend(expand_finite_index_two_cyclic_structure(goal))
        from phase174_r3_r6_source_extension.source import expand_cited_toda55_double
        options.extend(expand_cited_toda55_double(goal, tuple(available)))
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
        from phase174_r3_r7_r12_toda59_annihilator_source.rule import (
            expand_cited_annihilator_specialization,
        )
        options.extend(expand_cited_annihilator_specialization(goal, tuple(available)))
        composite_image_options = ()
        if not eta_generator_options:
            from phase169_r10e5_composite_generator_image.rule import (
                expand_composite_generator_image,
            )
            composite_image_options = expand_composite_generator_image(goal)
            options.extend(composite_image_options)
        from phase174_r3_r6_r2_prop44_lemma54.source import (
            expand_cited_preprop44_splitting,
        )
        options.extend(expand_cited_preprop44_splitting(goal, tuple(available)))
        from phase173_r4_r1_lemma54_source_bridge.source import (
            expand_cited_lemma54_hopf,
        )
        options.extend(expand_cited_lemma54_hopf(goal, tuple(available)))
        from phase169_r4b_prop44_injectivity.rule import expand_cited_prop44_injectivity
        conditional_prop44 = expand_cited_prop44_injectivity(goal, tuple(available))
        if conditional_prop44:
            return conditional_prop44
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

## phase165_r52_r9_shared_math.py : search_shared_group_goal

```python
def search_shared_group_goal(*, n: int, k: int, group_structure: object,
                              bridge: RegistryBridgeResult | None = None,
                              expansion_provider=None,
                              citing_assertion_id: str | None = None,
                              verified_assertion_ids: tuple[str, ...] = (), completed_internal_proofs: tuple = (), proof_use_order=None,
                              ordered_completed_proofs: tuple = (), target_order: int | None = None,
                              proof_order_catalog=None, recursive_proof_order_catalog=None, context_sink=None):
    """Run canonical search under a screened Reference context.

    Older calls retain their signature. R15 ordering is applied to sources
    outside the explicitly adopted-Tex policy; no IDs are auto-verified.
    """
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r57_r12_ordered_proofs import validate_prior_internal_proofs

    goal = Relation(TodaPrimaryGroup(n + k, n), group_structure)
    if proof_order_catalog is not None and recursive_proof_order_catalog is None:
        from phase165_r57_r13_proof_order_catalog import ProofOrderCatalog
        if not isinstance(proof_order_catalog, ProofOrderCatalog):
            raise TypeError("proof_order_catalog must be ProofOrderCatalog")
        if ordered_completed_proofs or completed_internal_proofs or target_order is not None:
            raise ValueError("catalog proof order cannot mix with caller-supplied proofs")
        if any(record.completed is not None for record in proof_order_catalog._records):
            raise ValueError("on-demand mode forbids registered completed proofs")
        recursive_proof_order_catalog = proof_order_catalog
        proof_order_catalog = None
    if recursive_proof_order_catalog is not None:
        from phase165_r57_r14_recursive_search import search_recursively_in_proof_order
        if (proof_order_catalog is not None or ordered_completed_proofs
                or completed_internal_proofs or target_order is not None):
            raise ValueError("recursive proof order cannot mix with saved or caller-supplied proofs")

        def search_one(statement, earlier, order):
            if (not isinstance(statement, Relation)
                    or not isinstance(statement.lhs, TodaPrimaryGroup)
                    or statement.relation_type is not RelationType.EQUALITY):
                raise TypeError("recursive catalog targets must be typed group relations")
            target = statement.lhs
            if (not isinstance(target.group_dimension, int)
                    or not isinstance(target.sphere_dimension, int)
                    or target.sphere_dimension < 2
                    or target.group_dimension < target.sphere_dimension):
                raise ValueError("recursive target must have concrete dimensions")
            return search_shared_group_goal(
                n=target.sphere_dimension,
                k=target.group_dimension - target.sphere_dimension,
                group_structure=statement.rhs,
                bridge=bridge,
                expansion_provider=expansion_provider,
                citing_assertion_id=citing_assertion_id,
                verified_assertion_ids=verified_assertion_ids,
                completed_internal_proofs=(),
                proof_use_order=proof_use_order,
                ordered_completed_proofs=earlier,
                target_order=order,
                context_sink=context_sink if statement == goal else None,
            )

        return search_recursively_in_proof_order(
            recursive_proof_order_catalog, goal, search_one,
        )
    if proof_order_catalog is not None:
        from phase165_r57_r13_proof_order_catalog import ProofOrderCatalog
        if not isinstance(proof_order_catalog, ProofOrderCatalog):
            raise TypeError("proof_order_catalog must be ProofOrderCatalog")
        if ordered_completed_proofs or completed_internal_proofs or target_order is not None:
            raise ValueError("catalog proof order cannot be mixed with caller order")
        prior, target_order = proof_order_catalog.select_prior(goal)
    else:
        prior = validate_prior_internal_proofs(
            ordered_completed_proofs, target_order, completed_internal_proofs
        )
    if bridge is None:
        bridge = build_shared_typed_bridge()
    if n == 4 and k == 3 and expansion_provider is None:
        from phase173_r4_r1_public_connection.route import (
            prepare_pi74_public_connection,
        )
        pi74_connection = prepare_pi74_public_connection(
            bridge=bridge, goal=goal, citing_assertion_id=citing_assertion_id,
            prior_conclusions=tuple(item.root.conclusion for item in prior),
        )
        if pi74_connection is not None:
            bridge, citing_assertion_id, expansion_provider = pi74_connection
    if citing_assertion_id is not None and expansion_provider is None:
        from phase174_r3_r6_r2_prop44_lemma54.source import (
            attach_earlier_verified_lemma54,
        )
        bridge = attach_earlier_verified_lemma54(bridge, citing_assertion_id)
    assertions = tuple(bridge.registry._assertions.values())
    if not assertions:
        raise ValueError("shared typed registry is empty")
    context_id = citing_assertion_id or assertions[0].assertion_id
    if citing_assertion_id is None:
        from phase169_r10e2_unpositioned_citation.source_first import (
            screen_independent_sources_for_derived_goal,
        )
        proof_context = screen_independent_sources_for_derived_goal(
            bridge, goal=goal,
        )
    else:
        proof_context = screen_shared_proof_context(
            bridge, goal=goal, citing_assertion_id=context_id,
            verified_assertion_ids=verified_assertion_ids,
            explicit_publication_target=True,
        )
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    proof_context = prefer_universal_prop42_derivation(proof_context)
    # Phase 173 R4-R8: reuse only the three isolated, source-verified Toda (5.6) roots.
    if n == 4 and k in (4, 5, 6) and expansion_provider is None and citing_assertion_id is None:
        from phase173_r4_r8_public_connection.route import (
            prepare_pi4_higher_public_connection,
        )
        pi4_higher_connection = prepare_pi4_higher_public_connection(
            bridge=bridge, goal=goal,
            prior_conclusions=tuple(item.root.conclusion for item in prior),
        )
        if pi4_higher_connection is not None:
            proof_context, expansion_provider = pi4_higher_connection
    if context_sink is not None:
        context_sink(proof_context)
    if expansion_provider is None:
        expansion_provider = shared_expansion_provider(
            proof_context, proof_target=goal,
            prior_conclusions=tuple(item.root.conclusion for item in prior),
        )
        # Every ordinary (nonzero) group search needs the same cited R53
        # source-bound kernel candidate already used by the zero-group route.
        # This is a candidate ordering wrapper, not a new premise or GIVEN.
        from phase174_r3_r7_r53_public_source_bound_kernel.provider import (
            build_public_source_bound_kernel_provider,
        )
        expansion_provider = build_public_source_bound_kernel_provider(
            expansion_provider, proof_context,
        )
    return search_registered_partial_proof(
        n=n, k=k, goal=goal, bridge=proof_context,
        citing_assertion_id=context_id,
        expansion_provider=expansion_provider,
        lookup_mode="typed_reference_publication" if citing_assertion_id is not None else "typed_reference",
        structure_status=GroupStructureStatus.UNKNOWN,
        completed_internal_proofs=prior,
    )

```
