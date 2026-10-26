def reconstruct_registered_goal(
    goal: object,
    bridge: RegistryBridgeResult,
    citing_assertion_id: str,
    expansion_provider: Callable[[object], tuple[GoalExpansion, ...]],
    *,
    verified_assertion_ids: tuple[str, ...] = (),
    lookup_mode: str = "legacy",
    progress_observer: Callable[[str, object, ProofStep | None], None] | None = None,
    completed_internal_proofs: tuple = (),
) -> ProofStep:
    """Derive a goal with optional read-only progress reporting.

    The observer receives ('proved', goal, step) only after an accepted unique
    derivation and ('unresolved', goal, None) for a failed search branch.
    Supplying no observer preserves the existing API and search semantics.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    if not callable(expansion_provider):
        raise TypeError("expansion_provider must be callable")
    if not isinstance(verified_assertion_ids, tuple):
        raise TypeError("verified_assertion_ids must be a tuple")
    if lookup_mode not in ("legacy", "typed_reference", "typed_reference_ordered", "typed_reference_publication"):
        raise ValueError("unknown lookup mode")
    if progress_observer is not None and not callable(progress_observer):
        raise TypeError("progress_observer must be callable or None")
    bridge.registry.assertion(citing_assertion_id)
    active: list[object] = []
    solved: list[tuple[object, ProofStep]] = []

    def report(kind: str, target: object, step: ProofStep | None = None) -> None:
        if progress_observer is not None:
            progress_observer(kind, target, step)

    def resolve(target: object) -> ProofStep:
        for earlier, step in solved:
            if type(earlier) is type(target) and earlier == target:
                return step
        if any(type(earlier) is type(target) and earlier == target for earlier in active):
            report("unresolved", target)
            raise RegisteredGoalUnresolved("cyclic proof dependency")
        active.append(target)
        try:
            if lookup_mode == "typed_reference_publication":
                from phase166_r3c_publication_order import precedes_citing_assertion
                options = []
                for assertion in bridge.registry._assertions.values():
                    if not precedes_citing_assertion(bridge, assertion.assertion_id, citing_assertion_id):
                        continue
                    if type(assertion.content) is not type(target) or assertion.content != target:
                        continue
                    links = tuple(link for link in bridge.proof_links if link.assertion_id == assertion.assertion_id)
                    if len(links) != 1 or links[0].step is None:
                        continue
                    step = links[0].step
                    if (not isinstance(step, ProofStep) or step.rule is not ProofRule.GIVEN
                            or type(step.conclusion) is not type(target) or step.conclusion != target):
                        raise ValueError("ordered reference has inconsistent ProofStep")
                    options.append(step)
            elif lookup_mode == "typed_reference_ordered":
                from phase165_r52_r15_ordered_citation import ordered_typed_reference_steps
                options = list(ordered_typed_reference_steps(
                    bridge, target, citing_assertion_id,
                    verified_assertion_ids=verified_assertion_ids,
                ))
            elif lookup_mode == "typed_reference":
                options = list(_typed_reference_steps(bridge, target))
            else:
                candidates = find_eligible_goal_candidates(
                    bridge, target, citing_assertion_id,
                    verified_assertion_ids=verified_assertion_ids,
                )
                options = [x.proof_step for x in candidates if x.proof_step is not None]
            # A uniquely registered fixed Reference is a complete proof leaf.
            # Do not count a second derivation of the same statement as ambiguity.
            # Multiple direct references remain ambiguous and are rejected below.
            if lookup_mode in ("typed_reference", "typed_reference_ordered", "typed_reference_publication") and len(options) == 1:
                step = options[0]
                solved.append((target, step))
                report("proved", target, step)
                return step
            # R3N: a positioned DB result needs no completed earlier proof.
            # Exact screened GIVEN sources were returned above. Only differing
            # registered generator presentations reach this guarded fallback.
            if lookup_mode == "typed_reference_publication" and not options:
                from phase169_r3n_prior_result_alias import resolve_prior_result_alias_step
                alias_step = resolve_prior_result_alias_step(
                    target, bridge, citing_assertion_id,
                )
                if alias_step is not None:
                    for prior_step in alias_step.premises:
                        report("proved", prior_step.conclusion, prior_step)
                    solved.append((target, alias_step))
                    report("proved", target, alias_step)
                    return alias_step
            # phase165_reference_stop_r3: direct eligible source before prior internal proof
            if completed_internal_proofs:
                from phase165_r52_r17_internal_dependency import find_reusable_internal_proof
                internal = find_reusable_internal_proof(target, goal, completed_internal_proofs)
                if internal is not None:
                    solved.append((target, internal))
                    report("proved", target, internal)
                    return internal
            expansions = expansion_provider(target)
            if not isinstance(expansions, tuple):
                raise TypeError("expansion provider must return a tuple")
            for expansion in expansions:
                if not isinstance(expansion, GoalExpansion):
                    raise TypeError("invalid inference expansion")
                try:
                    premises = tuple(resolve(child) for child in expansion.subgoals)
                except RegisteredGoalUnresolved:
                    continue
                matches = tuple(
                    match for match in find_inference_matches_for_rule(expansion.rule, premises)
                    if len(match.premises) == len(premises)
                    and all(a is b for a, b in zip(match.premises, premises))
                )
                for match in matches:
                    step = derive_inference_proof_step(match)
                    if type(step.conclusion) is type(target) and step.conclusion == target:
                        append_unique_verified_derivation(options, step)
            if len(options) != 1:
                report("unresolved", target)
                raise RegisteredGoalUnresolved(
                    f"expected one registered derivation for {target!r}, found {len(options)}"
                )
            step = options[0]
            solved.append((target, step))
            report("proved", target, step)
            return step
        finally:
            active.pop()

    return resolve(goal)

