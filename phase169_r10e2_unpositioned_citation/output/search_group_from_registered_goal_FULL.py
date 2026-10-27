def search_group_from_registered_goal(*, n: int, k: int, bridge=None, proof_order_catalog=None, goal=None, context_sink=None):
    """Search typed goals. Zero goals use the same evidenced backward engine."""
    from homotopy_groups import TodaPrimaryGroupZeroStatement
    from phase166_r3af_goal_adapter import database_zero_group_goal_candidates

    target = TodaPrimaryGroup(n + k, n)
    make_partial_proof_result(n=n, k=k, status=ProofSearchStatus.NOT_SEARCHED)

    if goal is not None:
        valid_relation = (
            isinstance(goal, Relation)
            and goal.relation_type is RelationType.EQUALITY
            and goal.lhs == target
            and isinstance(goal.rhs, _GROUP_STRUCTURES)
        )
        valid_zero = (
            isinstance(goal, TodaPrimaryGroupZeroStatement)
            and goal.group == target
        )
        if not valid_relation and not valid_zero:
            raise ValueError("goal must be a typed group statement for the requested n,k")

    if goal is None:
        zeros = database_zero_group_goal_candidates(n=n, k=k)
        if len(zeros) == 1:
            candidate = zeros[0]
        else:
            if bridge is None:
                bridge = build_shared_typed_bridge()
            candidates = registered_group_goal_candidates(bridge, n=n, k=k)
            if len(candidates) != 1:
                explanation = (
                    "群構造・生成元の型付き証明目標を指定してください"
                    if not candidates else
                    "群構造の型付き候補が複数あり、証明目標を一意に選択できない"
                )
                return make_partial_proof_result(
                    n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED,
                    open_goals=(target,), diagnostics=(explanation,),
                )
            candidate = candidates[0]
    else:
        candidate = goal

    if bridge is None:
        bridge = build_shared_typed_bridge()

    if isinstance(candidate, TodaPrimaryGroupZeroStatement):
        from phase169_r10e2_unpositioned_citation.source_first import (
            screen_independent_sources_for_derived_goal,
        )
        from phase165_r52_r2_search_adapter import search_registered_partial_proof
        from phase165_r52_r9_shared_math import shared_expansion_provider
        assertions = tuple(bridge.registry._assertions.values())
        if not assertions:
            return make_partial_proof_result(
                n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED,
                open_goals=(candidate,), diagnostics=("型付き命題台帳が空です",),
            )
        # The DB target has no publication position. Cite only independently
        # positioned fixed source statements; invent no target citation ID.
        context_id = assertions[0].assertion_id
        screened = screen_independent_sources_for_derived_goal(
            bridge, goal=candidate,
        )
        if context_sink is not None:
            context_sink(screened)
        provider = shared_expansion_provider(
            screened, proof_target=candidate,
        )
        return search_registered_partial_proof(
            n=n, k=k, goal=candidate, bridge=screened,
            citing_assertion_id=context_id,
            expansion_provider=provider, lookup_mode="typed_reference",
        )

    if proof_order_catalog is None:
        from phase165_r57_r16_web_proof_order import resolve_reviewed_order_catalog
        proof_order_catalog, order_diagnostic = resolve_reviewed_order_catalog(
            bridge, n=n, k=k,
        )
        if order_diagnostic is not None:
            return make_partial_proof_result(
                n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED,
                open_goals=(candidate,), diagnostics=(order_diagnostic,),
            )
    citing_id = resolve_specialized_goal_citing_id(bridge, candidate)
    search_kwargs = dict(
        n=n, k=k, group_structure=candidate.rhs, bridge=bridge,
        proof_order_catalog=proof_order_catalog,
        context_sink=context_sink,
    )
    if citing_id is not None:
        search_kwargs["citing_assertion_id"] = citing_id
    result = search_shared_group_goal(**search_kwargs)
    if result.status is ProofSearchStatus.COMPLETE and result.conclusion == candidate:
        return replace(result, structure_status=GroupStructureStatus.KNOWN)
    return result
