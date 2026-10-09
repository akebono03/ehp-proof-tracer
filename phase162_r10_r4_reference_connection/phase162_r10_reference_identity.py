"""Recognize an R10 fixed-statement citation from recorded ProofStep structure.

An arbitrary foundational_reference is not sufficient: its registered component,
provenance shape, label, and citation rule must agree. This is a structural
reference classifier, not a replacement for external mathematical verification.
"""
from __future__ import annotations

from proof import ProofRule, ProofStep


def fixed_citation_identity(step: ProofStep) -> tuple[str, str] | None:
    if not isinstance(step, ProofStep):
        raise TypeError("step must be a ProofStep")
    identity = step.foundational_reference
    if identity is None or not isinstance(identity.key, str):
        return None
    if not identity.key.startswith("literature:"):
        return None
    payload = identity.key[len("literature:"):]
    locator, separator, component_key = payload.rpartition(":")
    if not separator or not locator or not component_key or identity.label != locator:
        return None
    from toda_literature_statement_boundary import get_toda_fixed_statement_component
    try:
        component = get_toda_fixed_statement_component(locator, component_key)
    except (KeyError, ValueError, TypeError):
        return None
    if component is None or component.reference_locator != locator or component.component_key != component_key:
        return None
    if step.rule is ProofRule.GIVEN:
        if step.premises or step.inference_rule is not None:
            return None
        return locator, component_key
    if step.rule is not ProofRule.INFERENCE or len(step.premises) != 1:
        return None
    premise = step.premises[0]
    if not isinstance(premise, ProofStep) or premise is step:
        return None
    if (premise.rule is not ProofRule.GIVEN or premise.premises
            or premise.inference_rule is not None
            or premise.foundational_reference != identity
            or premise.conclusion != step.conclusion):
        return None
    rule = step.inference_rule
    if (rule is None or rule.name != "phase162_verified_literature_citation"
            or rule.literature_reference is None
            or rule.literature_reference.locator != locator):
        return None
    return locator, component_key


def is_cited_inference(step: ProofStep) -> bool:
    return step.rule is ProofRule.INFERENCE and fixed_citation_identity(step) is not None
