def inspect_dimension(dimension: int, *, with_web: bool = True) -> dict:
    """Audit certified sources, and compare Web output to the model renderer."""
    if type(dimension) is not int or dimension not in (7, 8, 9, 10, 11):
        raise ValueError("R4-R13 concerns only five already-completed dimensions")
    bridge = build_shared_typed_bridge()
    contexts: list = []
    result = search_group_from_registered_goal(
        n=4, k=dimension - 4, bridge=bridge,
        context_sink=contexts.append,
    )
    if (result.status is not ProofSearchStatus.COMPLETE
            or result.open_goals or len(contexts) != 1):
        raise ValueError(f"pi_{dimension}^4 no longer has a completed screened proof")
    model = build_linked_proof_narrative_model(result, contexts[0])
    if model.root_index is None:
        raise ValueError("A complete proof lacks a narrative root")
    root = model.steps[model.root_index]
    name = getattr(getattr(root, "inference_rule", None), "name", None)
    expected_name = LEGACY_ROOT if dimension == 7 else (
        SOURCE_FIRST_ROOT if dimension in (8, 9, 10) else GENERIC_ROOT
    )
    if (root.rule is not ProofRule.INFERENCE
            or name != expected_name
            or root.conclusion != result.conclusion
            or root.inference_rule is None
            or len(root.premises) != 4
            or not root.inference_rule.match_guard(root.premises, {})):
        raise ValueError(f"Unexpected typed proof root for pi_{dimension}^4")
    if dimension > 7:
        theorem, left, right, hopf = root.premises
        first = exact_prior_database_result(3, dimension - 4)
        second = exact_prior_database_result(7, dimension - 7)
        if (left.conclusion != first or right.conclusion != second
                or not verified_db_step(left, proof_target=result.conclusion,
                                        bridge=contexts[0])
                or not verified_db_step(right, proof_target=result.conclusion,
                                        bridge=contexts[0])):
            raise ValueError("One or both adopted database priors lost certification")
        sources = (
            _source_number(model, theorem, locator="Proposition 4.4"),
            _source_number(model, left, db_prior=True),
            _source_number(model, right, db_prior=True),
            _source_number(model, hopf.premises[0], locator="Lemma 5.4"),
        )
        if len(set(sources)) != 4:
            raise ValueError("Cited source identities were conflated")
    from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
    ancestors = root_ancestor_step_indices(model.steps, model.root_index)
    citations = tuple({
        "number": citation.number,
        "locator": citation.reference.locator or citation.reference.label,
        "step_indices": list(citation.step_indices),
    } for citation in model.citations)
    if len(citations) != 4 or any(
        not set(citation["step_indices"]).issubset(ancestors)
        for citation in citations
    ):
        raise ValueError("Source references are not bound to the proof ancestry")
    base = render_model_backed_narrative_markdown(result, model)
    if ("使用する結果" not in base
            or base.count("\n証明\n") != 1
            or not base.endswith("□\n")):
        raise ValueError("Common narrative sections are missing or malformed")
    if with_web:
        from web_group_proof_common import _build_group_proof_rendered_lines
        view = build_standard_web_group_proof_view(
            n=4, k=dimension - 4,
            mode="narrative", citation_source="model",
        )
        if (view.key != "generic-complete-proof" or view.partial_result
                or not view.rendered_lines
                or view.rendered_lines != _build_group_proof_rendered_lines(base)):
            raise ValueError("Web narrative diverges from the verified model renderer")
    row = {
        "group": f"pi_{dimension}^4",
        "dimension": dimension,
        "root_rule": name,
        "source_verified": True,
        "source_reference_count": len(citations),
        "source_references": citations,
        "open_goals": len(result.open_goals),
        "web_verified": with_web,
        "narrative_markdown": base,
    }
    print(
        f"PHASE173_R4_R13_PI_{dimension}_4"
        f" ROOT_CERTIFIED=True REFERENCES={len(citations)}"
        f" OPEN=0 WEB_CHECKED={with_web}",
        flush=True,
    )
    return row
