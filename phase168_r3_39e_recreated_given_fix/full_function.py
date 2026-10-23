def screen_shared_proof_context(
    bridge: RegistryBridgeResult,
    *,
    goal: object,
    citing_assertion_id: str,
    verified_assertion_ids: tuple[str, ...] = (),
    explicit_publication_target: bool = False,
) -> RegistryBridgeResult:
    """Filter source statements by existing policies or explicit publication order.

    In explicit publication-order mode the registry is authoritative: a prior
    FIXED_STATEMENT needs no manually maintained ProofStepLink. The link is
    constructed uniformly from the registered typed assertion, independent of
    any pre-existing ProofStepLink. Legacy implicit-target mode is unchanged.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    if not isinstance(verified_assertion_ids, tuple):
        raise TypeError("verified_assertion_ids must be a tuple")
    bridge.registry.assertion(citing_assertion_id)
    accepted = []
    if explicit_publication_target:
        from dataclasses import is_dataclass, replace
        from phase166_r3c_publication_order import precedes_citing_assertion
        from proof import ProofStep, InferenceRule, LiteratureReference
        from unified_statement_registry import AssertionKind, ProofStepLink

        def registered_reference_step(assertion, step):
            """Retain provenance of an already screened fixed assertion only."""
            reference = bridge.registry.reference(assertion.reference_id)
            locator = reference.locator
            if not isinstance(locator, str) or not locator:
                return step
            if step.inference_rule is not None and step.inference_rule.literature_reference is not None:
                return step
            return replace(
                step,
                inference_rule=InferenceRule(
                    name="Registered fixed statement: " + locator,
                    literature_reference=LiteratureReference(
                        label="Toda " + locator,
                        locator=locator,
                    ),
                ),
            )

        for assertion in bridge.registry._assertions.values():
            if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
                continue
            if assertion.kind not in (AssertionKind.STATEMENT, AssertionKind.DEFINITION):
                continue
            if not is_dataclass(assertion.content) or isinstance(assertion.content, type):
                continue
            # Boundary component metadata is not a mathematical proof premise.
            if type(assertion.content).__name__ == "TodaFixedStatementComponent":
                continue
            if type(assertion.content) is type(goal) and assertion.content == goal:
                continue
            if not precedes_citing_assertion(
                bridge, assertion.assertion_id, citing_assertion_id
            ):
                continue
            # A concrete fixed assertion is not an independent GIVEN if the
            # same cited source already contains an eligible typed schema
            # whose established specialization rule derives that assertion.
            # Keep the registry entry for provenance; only the direct leaf is
            # suppressed. This applies uniformly to printed source locators.
            from phase165_r57_r20_general_specialization import specialize_typed_statement
            reference = bridge.registry.reference(assertion.reference_id)
            covered_by_schema = any(
                alternative.assertion_id != assertion.assertion_id
                and alternative.origin is AssertionOrigin.FIXED_STATEMENT
                and alternative.kind in (AssertionKind.STATEMENT, AssertionKind.DEFINITION)
                and bridge.registry.reference(alternative.reference_id).locator == reference.locator
                and precedes_citing_assertion(
                    bridge, alternative.assertion_id, citing_assertion_id
                )
                and specialize_typed_statement(alternative.content, assertion.content) is not None
                for alternative in bridge.registry._assertions.values()
            )
            if covered_by_schema:
                continue
            accepted.append(ProofStepLink(
                assertion_id=assertion.assertion_id,
                step=registered_reference_step(assertion, ProofStep(
                    conclusion=assertion.content,
                    premises=(),
                    rule=ProofRule.GIVEN,
                )),
            ))
        # Equivalent copies from the same printed position are one GIVEN,
        # not competing independent mathematical derivations. Preserve a
        # previously linked source when possible, including its provenance.
        unique = []
        for candidate in accepted:
            assertion = bridge.registry.assertion(candidate.assertion_id)
            reference = bridge.registry.reference(assertion.reference_id)
            identical_index = None
            for index, existing in enumerate(unique):
                other = bridge.registry.assertion(existing.assertion_id)
                other_reference = bridge.registry.reference(other.reference_id)
                if (
                    candidate.step.conclusion == existing.step.conclusion
                    and reference.publication_position == other_reference.publication_position
                    and assertion.component_position == other.component_position
                ):
                    identical_index = index
                    break
            original_links = tuple(
                link for link in bridge.proof_links
                if link.assertion_id == candidate.assertion_id
                and link.step is not None
                and link.step.rule is ProofRule.GIVEN
                and link.step.conclusion == candidate.step.conclusion
            )
            if len(original_links) == 1:
                candidate = ProofStepLink(
                    assertion_id=candidate.assertion_id,
                    step=registered_reference_step(assertion, original_links[0].step),
                )
            if identical_index is None:
                unique.append(candidate)
            else:
                existing = unique[identical_index]
                existing_linked = any(
                    link.assertion_id == existing.assertion_id
                    and link.step is not None
                    and link.step.rule is ProofRule.GIVEN
                    and link.step.conclusion == existing.step.conclusion
                    for link in bridge.proof_links
                )
                if len(original_links) == 1 and not existing_linked:
                    unique[identical_index] = candidate
        return RegistryBridgeResult(bridge.registry, bridge.records, tuple(unique))

    for link in bridge.proof_links:
        assertion = bridge.registry.assertion(link.assertion_id)
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        if type(assertion.content) is type(goal) and assertion.content == goal:
            continue
        step = link.step
        if step is None or step.rule is not ProofRule.GIVEN:
            continue
        if type(step.conclusion) is not type(assertion.content) or step.conclusion != assertion.content:
            raise ValueError("fixed reference has inconsistent GIVEN proof link")
        adopted = (
            assertion.assertion_id.startswith("shared:")
            and (
                ":adopted:assertion:" in assertion.assertion_id
                or ":toda:adopted:prop5.1:finite_dimensional" in assertion.assertion_id
                or assertion.assertion_id.endswith(":adopted:assertion:prop42:general")
            )
        )
        if adopted:
            accepted.append(link)
            continue
        decision = assess_phase164_r2_citation(
            bridge, assertion.assertion_id, citing_assertion_id,
            verified_assertion_ids=verified_assertion_ids,
        )
        if decision.usable:
            accepted.append(link)
    return RegistryBridgeResult(bridge.registry, bridge.records, tuple(accepted))
