"""R12-R19: inspect established eta-family definitions without adding facts."""
from __future__ import annotations

from dataclasses import dataclass

from proof import ProofRule, ProofStep
from unified_statement_registry import AssertionOrigin


@dataclass(frozen=True)
class DefinitionAudit:
    status: str
    matching_count: int
    assertion_ids: tuple[str, ...]


def inspect_fixed_definition_links(bridge: object, statement_type: type) -> DefinitionAudit:
    """Accept only exact, reference-backed fixed GIVEN statement links."""
    accepted: list[str] = []
    for link in bridge.proof_links:
        step = link.step
        if not isinstance(step, ProofStep) or type(step.conclusion) is not statement_type:
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        if step.rule is not ProofRule.GIVEN or step.conclusion != assertion.content:
            continue
        reference = bridge.registry.reference(assertion.reference_id)
        if not reference.locator:
            continue
        accepted.append(assertion.assertion_id)
    return DefinitionAudit(
        status="FIXED_DEFINITION_LINKS_FOUND" if accepted else "NO_FIXED_DEFINITION_LINK",
        matching_count=len(accepted),
        assertion_ids=tuple(accepted),
    )


def inspect_eta_runtime() -> dict[str, object]:
    """Report existing schema and real shared registry; do not certify an eta equation."""
    from dataclasses import fields, is_dataclass
    from toda_rules import TodaEtaFamilyDefinitionStatement, toda_eta_family_definition_statement
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    kind = TodaEtaFamilyDefinitionStatement
    item = toda_eta_family_definition_statement(3)
    if not isinstance(item, kind):
        raise TypeError("eta definition factory does not return its declared statement")
    bridge = build_shared_typed_bridge()
    fixed = inspect_fixed_definition_links(bridge, kind)
    return {
        "phase": "165 R12-R19",
        "existing_eta_definition_class": True,
        "existing_eta_definition_factory": True,
        "eta3_definition_type_verified": True,
        "eta_definition_fields": [field.name for field in fields(kind)] if is_dataclass(kind) else [],
        "eta3_definition_repr": repr(item),
        "eligible_fixed_definition_link_count": fixed.matching_count,
        "eligible_fixed_definition_assertion_ids": list(fixed.assertion_ids),
        "eta3_specialization_proof_certified": False,
        "generator_image_proof_certified": False,
        "pi43_proof_certified": False,
        "full_pytest_run": False,
        "status": "ETA_DEFINITION_REGISTRY_AUDITED_NOT_CERTIFIED",
    }
