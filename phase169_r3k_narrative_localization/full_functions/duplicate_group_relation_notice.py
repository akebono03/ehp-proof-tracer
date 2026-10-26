def duplicate_group_relation_notice(model, step_index: int, previous_latex: set[str]) -> str | None:
    """Replace a repeated *display* with its source tags, never a new proof.

    Only typed cyclic group relations are eligible, and the root is preserved.
    The caller records a formula in previous_latex only after it has been shown.
    """
    from web_group_proof_common import _group_proof_statement_latex
    step = model.steps[step_index]
    fact = step.conclusion
    if (model.root_index == step_index
            or not isinstance(fact, Relation)
            or fact.relation_type is not RelationType.EQUALITY
            or not isinstance(fact.lhs, TodaPrimaryGroup)
            or not isinstance(fact.rhs, FiniteCyclicGroup)):
        return None
    latex, fallback = _group_proof_statement_latex(fact)
    if fallback is not None or not latex or latex not in previous_latex:
        return None
    numbers = model.step_citation_numbers[step_index]
    if not numbers:
        return ""
    references = ", ".join(f"[R{number}]" for number in numbers)
    return references + "による導出も同じ群構造を示す."
