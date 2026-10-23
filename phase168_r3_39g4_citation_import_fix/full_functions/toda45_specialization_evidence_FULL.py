def toda45_specialization_evidence(step):
    """Return a general cited Toda (4.5) ancestor and checked scalar bindings.

    Only traverse existing ProofStep premises. The existing specialization
    validator supplies all equalities and stable-range checks.
    """
    from proof import ProofRule
    from toda_rules import Toda45IsomorphismStatement
    from phase165_r57_r20_general_specialization import specialize_typed_statement

    if (step is None or step.rule is not ProofRule.INFERENCE
            or not isinstance(step.conclusion, Toda45IsomorphismStatement)):
        return None

    visited = set()

    def find_source(node):
        if id(node) in visited:
            return None
        visited.add(id(node))
        for parent in node.premises:
            if (parent.rule is ProofRule.GIVEN
                    and isinstance(parent.conclusion, Toda45IsomorphismStatement)):
                bindings = specialize_typed_statement(parent.conclusion, step.conclusion)
                if bindings is not None and {"n", "m", "k"}.issubset(dict(bindings)):
                    return parent, bindings
            candidate = find_source(parent)
            if candidate is not None:
                return candidate
        return None

    return find_source(step)


