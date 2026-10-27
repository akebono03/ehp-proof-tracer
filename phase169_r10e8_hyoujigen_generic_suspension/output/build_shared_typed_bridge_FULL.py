def build_shared_typed_bridge(*, sources: tuple[RegistryBridgeResult, ...] | None = None) -> RegistryBridgeResult:
    """Merge eligible typed statements without importing derived group proofs.

    The R38 adopted-Tex *source assertions* are currently the first available
    rigorously linked typed leaves. They are shared with every query, not
    selected because the requested group is pi3^2.
    """
    default_sources = sources is None
    if sources is None:
        from phase165_r9_production_wiring import discover_goal_search_inputs
        from phase165_r14_r38_direct_registry import build_adopted_typed_reference_registry
        production = discover_goal_search_inputs().bridge
        from phase168_r2_7_4_typed_registry_bridge.phase168_r2_7_4_literature_connection import (
            connect_explicit_literature_components,
        )
        production = connect_explicit_literature_components(production)
        adopted_tex = Path(__file__).resolve().with_name("phase165_r14_r39_toda51.tex")
        from phase165_r52_r13_reference_registration import build_adopted_prop51_reference
        from phase165_r52_r27_r5_literature import build_typed_literature_bridge
        from phase165_r57_r20_general_specialization import build_adopted_toda51_diagonal_reference
        literature = build_typed_literature_bridge(production)
        from phase165_r12_r11_prop42_unified import build_adopted_prop42_general_reference
        from phase165_r12_r15_toda51 import build_adopted_toda51_zero_reference
        from phase165_r12_r20_eta_definition import build_cited_eta_family_definition
        from phase169_r3h_source_registry import build_adopted_toda53_hopf_reference
        sources = (production, build_adopted_typed_reference_registry(adopted_tex),
                   build_adopted_prop51_reference(),
                   build_adopted_toda51_diagonal_reference(adopted_tex)) + (literature, build_adopted_prop42_general_reference(), build_adopted_toda51_zero_reference(adopted_tex), build_cited_eta_family_definition(Path(__file__).resolve().parent / 'sources' / 'toda' / 'Toda_05_2.tex'),
                   build_adopted_toda53_hopf_reference(production))
        from phase169_r10d2_general_family_definition.family_citation import (
            build_cited_stable_family_definitions,
        )
        from phase169_r10e8_hyoujigen_generic_suspension.chapter_vi_reference import (
            build_cited_chapter_vi_family_definitions,
        )
        sources = sources + (
            build_cited_stable_family_definitions(),
            build_cited_chapter_vi_family_definitions(),
        )
    registry = UnifiedStatementRegistry()
    links = []
    records = []
    for index, source in enumerate(sources):
        if not isinstance(source, RegistryBridgeResult):
            raise TypeError("source must be RegistryBridgeResult")
        # R3-C: reuse Phase 163 positions on original reference IDs before
        # shared: index namespacing. No locator or synthetic rank matching.
        from phase166_r3b_publication_order_binding.phase166_r3b_publication_order_binding import (
            connect_phase163_publication_order,
        )
        source, _publication_binding = connect_phase163_publication_order(source)
        prefix = f"shared:{index}:"
        for ref in source.registry._references.values():
            registry.add_reference(replace(ref, reference_id=prefix + ref.reference_id))
        for assertion in source.registry._assertions.values():
            if assertion.origin is AssertionOrigin.PROOF_INTERNAL:
                continue
            registry.add_assertion(replace(
                assertion, assertion_id=prefix + assertion.assertion_id,
                reference_id=prefix + assertion.reference_id,
                component_position=(
                    assertion.component_position * 100
                    if assertion.component_position is not None
                    and assertion.component_position < 100
                    else assertion.component_position
                ),
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
    from phase166_r3l_reference_order import connect_all_reference_orders
    joined = expand_cited_given_components(
        RegistryBridgeResult(registry, tuple(records), tuple(links))
    )
    # Leave archived assertion identities untouched. In the default context,
    # these four old concrete (5.1) GIVENs must be derived by the already
    # registered universal source instead of short-circuiting the Proof Tree.
    if default_sources:
        legacy_ids = {
            "shared:1:adopted:assertion:1",
            "shared:1:adopted:assertion:2",
            "shared:1:adopted:assertion:4",
            "shared:1:adopted:assertion:6",
        }
        joined = RegistryBridgeResult(
            joined.registry, joined.records,
            tuple(link for link in joined.proof_links
                  if link.assertion_id not in legacy_ids),
        )
    # Preserve registered mathematical statements/IDs, but keep one direct
    # GIVEN for the Hopf-image fact; relation views are derived by a rule.
    hopf_relation_ids = {
        "shared:2:toda:adopted:prop5.1:eta2_hopf_relation",
        "shared:2:toda:adopted:prop5.1:finite_dimensional:component:eta2_hopf_relation",
    }
    joined = RegistryBridgeResult(
        joined.registry,
        joined.records,
        tuple(link for link in joined.proof_links
              if link.assertion_id not in hopf_relation_ids),
    )
    ordered, _order_report = connect_all_reference_orders(joined)
    from phase166_r3p_position_binding import place_r3p_reference_positions
    return place_r3p_reference_positions(ordered)

