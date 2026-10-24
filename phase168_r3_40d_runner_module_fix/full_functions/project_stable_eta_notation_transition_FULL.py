def project_stable_eta_notation_transition(model, step_index):
    """Explain an existing cited eta renaming without inferring a new result.

    Both the transported group relation and the cited general eta definition
    must be actual premises of the typed stable-notation inference.
    """
    from expression import IteratedSuspension
    from homotopy_groups import FiniteCyclicGroup
    from proof import ProofRule, Relation, RelationType
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from phase166_r3ac_stable_notation import _stable_eta_renaming_shape
    from phase168_r3_3_proof_narrative_model import ProofNarrativeModel

    if not isinstance(model, ProofNarrativeModel):
        raise TypeError("model must be ProofNarrativeModel")
    if type(step_index) is not int or not 0 <= step_index < len(model.steps):
        raise ValueError("invalid proof-step index")
    step = model.steps[step_index]
    if step.rule is not ProofRule.INFERENCE or len(step.premises) != 2:
        return None
    transported_step, definition_step = step.premises
    transported = transported_step.conclusion
    if (not isinstance(transported, Relation)
            or transported.relation_type is not RelationType.EQUALITY
            or not isinstance(transported.rhs, FiniteCyclicGroup)
            or not isinstance(transported.rhs.generator, IteratedSuspension)
            or type(transported.rhs.generator.exponent) is not int
            or transported.rhs.generator.exponent < 2
            or definition_step.rule is not ProofRule.GIVEN
            or not isinstance(definition_step.conclusion, TodaEtaFamilyGeneralDefinition)
            or not _stable_eta_renaming_shape(transported, step.conclusion)):
        return None
    source = element_tex(transported.rhs.generator.expression)
    target = element_tex(step.conclusion.rhs.generator)
    if source is None or target is None:
        return None
    numbers = tuple(dict.fromkeys(
        number
        for index, candidate in enumerate(model.steps)
        if candidate == definition_step
        for number in model.step_citation_numbers[index]
    ))
    if not numbers:
        return None
    tags = ", ".join(f"[R{number}]" for number in numbers)
    exponent = transported.rhs.generator.exponent
    return rf"{tags}の $\eta$ 系列の定義より, $E^{{{exponent}}}{source}={target}$."
