"""Verified citation boundaries for existing ProofStep ancestry.

A proof may be collapsed only after its complete ancestry has been validated.
The resulting GIVEN is wrapped in a verified INFERENCE for existing matchers.
"""
from __future__ import annotations

from dataclasses import replace

from proof import (
    FoundationalReferenceIdentity, InferenceRule, LiteratureReference,
    PremisePattern, ProofRule, ProofStep, apply_inference_match,
    find_inference_match,
)
from phase161_r7_premise_provenance_validation import validate_phase161_r7_provenance
from toda_literature_statement_boundary import get_toda_fixed_statement_component


def _trusted_given_ancestors(root: ProofStep) -> tuple[ProofStep, ...]:
    roots = {}
    visiting = set()
    seen = set()

    def visit(step: ProofStep) -> None:
        identity = id(step)
        if identity in seen:
            return
        if identity in visiting:
            raise ValueError("Cyclic citation ancestry")
        visiting.add(identity)
        for premise in step.premises:
            if not isinstance(premise, ProofStep):
                raise ValueError("Non-ProofStep citation premise")
            visit(premise)
        visiting.remove(identity)
        seen.add(identity)
        if step.rule is ProofRule.GIVEN:
            if step.premises:
                raise ValueError("GIVEN citation ancestor has premises")
            roots[identity] = step

    visit(root)
    return tuple(roots.values())


def cite_verified_fixed_statement(
    witness: ProofStep,
    reference_locator: str,
    component_key: str,
    expected_conclusion: object,
) -> ProofStep:
    """Collapse verified ancestry at a registered citation boundary.

    The caller must identify the exact fixed statement and pass the mathematical
    conclusion it claims. A registered component is necessary, not sufficient,
    to establish the external truth of that mathematical citation.
    """
    if not isinstance(witness, ProofStep):
        raise TypeError("witness must be a ProofStep")
    if witness.rule is not ProofRule.INFERENCE or not witness.premises:
        raise ValueError("Citation witness must be a derived inference")
    if witness.conclusion != expected_conclusion:
        raise ValueError("Citation statement does not match verified witness")
    component = get_toda_fixed_statement_component(reference_locator, component_key)
    if component.reference_locator != reference_locator or component.component_key != component_key:
        raise ValueError("Registered component mismatch")
    validate_phase161_r7_provenance((witness,), _trusted_given_ancestors(witness))
    citation_identity = FoundationalReferenceIdentity(
        key=f"literature:{reference_locator}:{component_key}",
        label=reference_locator,
    )
    citation_leaf = ProofStep(
        conclusion=witness.conclusion,
        premises=(),
        rule=ProofRule.GIVEN,
        foundational_reference=citation_identity,
    )
    citation_rule = InferenceRule(
        name="phase162_verified_literature_citation",
        description="Use a verified fixed literature statement",
        premise_patterns=(PremisePattern(proof_rule=ProofRule.GIVEN),),
        match_guard=lambda premises, bindings=(): (
            len(premises) == 1
            and premises[0].foundational_reference == citation_identity
            and premises[0].conclusion == expected_conclusion
        ),
        conclusion_builder=lambda premises: premises[0].conclusion,
        literature_reference=LiteratureReference(
            label="Toda " + reference_locator,
            locator=reference_locator,
        ),
    )
    match = find_inference_match(citation_rule, (citation_leaf,))
    if match is None:
        raise ValueError("Citation inference failed to match the trusted leaf")
    result = apply_inference_match(match)
    return replace(result, foundational_reference=citation_identity)



def validate_cited_fixed_statement(
    step: ProofStep,
    reference_locator: str,
    component_key: str,
    expected_conclusion: object,
) -> None:
    """Fail closed for an unrecognized or incorrectly attributed citation."""
    component = get_toda_fixed_statement_component(reference_locator, component_key)
    expected_key = f"literature:{reference_locator}:{component_key}"
    if (
        not isinstance(step, ProofStep)
        or step.rule is not ProofRule.INFERENCE
        or step.conclusion != expected_conclusion
        or step.inference_rule is None
        or step.inference_rule.name != "phase162_verified_literature_citation"
        or step.foundational_reference is None
        or step.foundational_reference.key != expected_key
        or step.foundational_reference.label != component.reference_locator
        or len(step.premises) != 1
        or not isinstance(step.premises[0], ProofStep)
        or step.premises[0].rule is not ProofRule.GIVEN
        or step.premises[0].premises
        or step.premises[0].conclusion != expected_conclusion
        or step.premises[0].foundational_reference != step.foundational_reference
    ):
        raise ValueError("Invalid fixed-statement citation boundary")
