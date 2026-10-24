"""Complete replacement functions for R3-41P3. No generated future-Phase features."""
from __future__ import annotations


RENDERER_HELPER = r'''
    def direct_given_premise_citation_numbers(step):
        """Use citations of an existing direct GIVEN premise, without replaying a rule.

        The Proof Tree is supplied by Backward Search. Citation ownership is
        already stored in the Narrative Model and is not re-inferred here.
        """
        if step.rule is not ProofRule.INFERENCE or len(step.premises) != 1:
            return ()
        given_step = step.premises[0]
        if given_step.rule is not ProofRule.GIVEN:
            return ()
        # Keep the old presentationally eligible typed statement families.
        # Proof validity itself was checked before this model was constructed.
        from homotopy_groups import TodaPrimaryGroupZeroStatement
        from phase165_r12_r15_toda51 import Toda51BelowDiagonalZeroStatement
        source, target = given_step.conclusion, step.conclusion
        is_direct_relation = isinstance(source, Relation) and isinstance(target, Relation)
        is_typed_zero = (
            isinstance(target, TodaPrimaryGroupZeroStatement)
            and isinstance(source, (TodaPrimaryGroupZeroStatement,
                                    Toda51BelowDiagonalZeroStatement))
        )
        if not (is_direct_relation or is_typed_zero):
            return ()
        return tuple(dict.fromkeys(
            number
            for source_index, candidate in enumerate(model.steps)
            if candidate is given_step or candidate == given_step
            for number in model.step_citation_numbers[source_index]
        ))
'''


TODA45_EVIDENCE = r'''
def toda45_specialization_evidence(step):
    """Project an existing cited Toda (4.5) premise and display parameters.

    The Proof Tree already contains the inference applying its typed general
    premise. This function does not re-run the specialization validator or
    decide whether Toda (4.5) applies. Numerical indices are projected from
    the already proven concrete suspension map for presentation only.
    """
    from proof import ProofRule
    from toda_rules import Toda45IsomorphismStatement
    from homotopy_groups import TodaIteratedSuspensionMap, TodaPrimaryGroup

    if (step is None or step.rule is not ProofRule.INFERENCE
            or not isinstance(step.conclusion, Toda45IsomorphismStatement)):
        return None
    mapping = step.conclusion.map
    if (not isinstance(mapping, TodaIteratedSuspensionMap)
            or not isinstance(mapping.source_group, TodaPrimaryGroup)
            or not isinstance(mapping.target_group, TodaPrimaryGroup)):
        return None
    n = mapping.source_group.sphere_dimension
    m = mapping.target_group.sphere_dimension
    source_dimension = mapping.source_group.group_dimension
    if any(type(index) is not int for index in (n, m, source_dimension)):
        return None
    # This is a display projection, not a validation of Toda's inequalities.
    bindings = (("n", n), ("m", m), ("k", source_dimension - n))
    visited = set()

    def find_source(node):
        if id(node) in visited:
            return None
        visited.add(id(node))
        for parent in node.premises:
            if (parent.rule is ProofRule.GIVEN
                    and isinstance(parent.conclusion, Toda45IsomorphismStatement)):
                return parent, bindings
            candidate = find_source(parent)
            if candidate is not None:
                return candidate
        return None

    return find_source(step)
'''
