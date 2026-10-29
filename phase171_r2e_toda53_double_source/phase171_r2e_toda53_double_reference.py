"""Adopt precisely the pre-existing Toda (5.3) double relation as a cited leaf.

This source statement is not a proof of a group presentation or of its order.
The independent archive/hash validation is delegated to the existing adopted
(5.3) Hopf-source verifier; it already checks the exact second clause.
"""
from __future__ import annotations

from expression import Composition, GeneratorSymbol, HomotopyElement, Multiple
from phase163_r4_registry_bridge import (
    MigrationRecord,
    MigrationStatus,
    RegistryBridgeResult,
)
from phase169_r3h_source_registry import (
    REFERENCE_ID,
    SOURCE_ID,
    build_adopted_toda53_hopf_reference,
)
from proof import (
    InferenceRule,
    LiteratureReference,
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
)
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    LiteratureEntry,
    ProofStepLink,
    ReferenceKind,
    UnifiedStatementRegistry,
)

ASSERTION_ID = "toda:adopted:eq5.3:nu_prime_double_relation"


def build_adopted_toda53_double_reference(
    source_bridge: RegistryBridgeResult,
) -> RegistryBridgeResult:
    """Register only 2 nu-prime = eta_3 o eta_4 o eta_5, with source ancestry.

    The existing adopted (5.3) verifier requires the uniquely identified source,
    its exact SHA-256 and the literal double relation; it rejects missing or
    changed source content. It is not legitimate to manufacture a GIVEN from
    an unverified group goal or Proposition 5.6 candidate.
    """
    verified = build_adopted_toda53_hopf_reference(source_bridge)
    if len(verified.proof_links) != 1:
        raise ValueError("existing (5.3) source verification is incomplete")

    nu_prime = HomotopyElement(
        name="ν′", dimension=3, source=6, target=3,
        generator=GeneratorSymbol(family="ν", decoration="′"),
    )
    eta3 = HomotopyElement(
        name="η₃", dimension=3, source=4, target=3,
        generator=GeneratorSymbol(family="η", index=3),
    )
    eta4 = HomotopyElement(
        name="η₄", dimension=4, source=5, target=4,
        generator=GeneratorSymbol(family="η", index=4),
    )
    eta5 = HomotopyElement(
        name="η₅", dimension=5, source=6, target=5,
        generator=GeneratorSymbol(family="η", index=5),
    )
    if (not Composition(eta4, eta5).is_type_compatible()
            or eta3.source != eta4.target):
        raise ValueError("ill-typed eta triple composition")
    relation = Relation(
        lhs=Multiple(2, nu_prime),
        rhs=Composition(eta3, Composition(eta4, eta5)),
        relation_type=RelationType.EQUALITY,
    )
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id=REFERENCE_ID,
        kind=ReferenceKind.EQUATION,
        locator="(5.3)",
        source_id=SOURCE_ID,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id=ASSERTION_ID,
        reference_id=REFERENCE_ID,
        kind=AssertionKind.STATEMENT,
        content=relation,
        origin=AssertionOrigin.FIXED_STATEMENT,
        scope=("adopted (5.3) double relation only",),
    ))
    step = ProofStep(
        conclusion=relation,
        premises=(),
        rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(
            name="Toda (5.3) double identity",
            literature_reference=LiteratureReference(
                label="Toda (5.3)", locator="(5.3)",
            ),
        ),
    )
    return RegistryBridgeResult(
        registry,
        (MigrationRecord(
            "phase171_r2e", "(5.3):nu_prime_double_relation", ASSERTION_ID,
            MigrationStatus.STRUCTURED,
            "adopted source-hash-verified double equality; original edition unverified",
        ),),
        (ProofStepLink(assertion_id=ASSERTION_ID, step=step),),
    )
