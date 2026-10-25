def verify_proof_tree_for_narrative(
    result: PartialProofResult,
    bridge: RegistryBridgeResult,
    *,
    citing_assertion_id: str,
) -> tuple[int, int]:
    """Check source leaves and replay existing inference matches, or reject.

    The citing ID must be resolved from the unscreened registered goal, not
    constructed from a displayed group label. The supplied bridge must be the
    screened bridge actually used by canonical backward search.

    All nested premises are visited, including premises of earlier internal
    proofs. Neither the result nor the bridge is modified. The result is only
    a count for diagnostics and MUST NOT be treated as a transferable seal.
    """
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    if not isinstance(citing_assertion_id, str) or not citing_assertion_id:
        raise ValueError("citing_assertion_id must identify a positioned goal")
    bridge.registry.assertion(citing_assertion_id)

    checked: set[int] = set()
    active: set[int] = set()
    inference_count = 0
    given_count = 0

    def visit(step: ProofStep) -> None:
        nonlocal inference_count, given_count
        if not isinstance(step, ProofStep):
            raise UnverifiedProofTree("a proof premise is not a ProofStep")
        identity = id(step)
        if identity in checked:
            return
        if identity in active:
            raise UnverifiedProofTree("cyclic proof ancestry")
        active.add(identity)
        try:
            if step.rule is ProofRule.GIVEN:
                if step.premises:
                    raise UnverifiedProofTree("GIVEN has unproved premises")
                accepted = False
                for link in bridge.proof_links:
                    if link.step is None or link.step != step:
                        continue
                    assertion = bridge.registry.assertion(link.assertion_id)
                    if (assertion.origin is AssertionOrigin.FIXED_STATEMENT
                            and type(assertion.content) is type(step.conclusion)
                            and assertion.content == step.conclusion
                            and precedes_citing_assertion(
                                bridge, link.assertion_id, citing_assertion_id
                            )):
                        accepted = True
                        break
                if not accepted:
                    raise UnverifiedProofTree("GIVEN is not screened, fixed and prior")
                given_count += 1
            elif step.rule is ProofRule.INFERENCE:
                if not isinstance(step.inference_rule, InferenceRule):
                    raise UnverifiedProofTree("inference has no typed rule")
                for premise in step.premises:
                    visit(premise)
                try:
                    matches = find_inference_matches_for_rule(
                        step.inference_rule, step.premises
                    )
                    accepted = any(
                        len(match.premises) == len(step.premises)
                        and all(a is b for a, b in zip(match.premises, step.premises))
                        and type(derived.conclusion) is type(step.conclusion)
                        and derived.conclusion == step.conclusion
                        for match in matches
                        for derived in (apply_inference_match(match),)
                    )
                except (TypeError, ValueError, AttributeError, IndexError) as exc:
                    raise UnverifiedProofTree("inference replay failed") from exc
                if not accepted:
                    raise UnverifiedProofTree("inference has no matching derivation")
                inference_count += 1
            else:
                raise UnverifiedProofTree("unsupported proof-step origin")
            checked.add(identity)
        finally:
            active.remove(identity)

    for step in result.proven_steps:
        visit(step)
    if result.status is ProofSearchStatus.COMPLETE:
        if result.conclusion is None or not any(
            type(step.conclusion) is type(result.conclusion)
            and step.conclusion == result.conclusion for step in result.proven_steps
        ):
            raise UnverifiedProofTree("completed proof has no matching conclusion")
    return inference_count, given_count
