"""Register one explicitly adopted, earlier Toda (5.3) Hopf equality.

The source must be a matching archival text row, never mere metadata.
Registration grants a cited GIVEN and does not claim an INFERENCE proof.
"""
from __future__ import annotations

from hashlib import sha256

from expression import GeneratorSymbol, HomotopyElement, MapApplication
from map_facts import EHP_H_MAP
from phase163_r4_registry_bridge import (
    MigrationRecord,
    MigrationStatus,
    RegistryBridgeResult,
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


SOURCE_ID = "toda:tex:ch5:0005"
SOURCE_SHA256 = "f949b19909fdd4f60f562b1daa4b121a621a4e7a32b5461f770e1e80ada6d3f2"
REFERENCE_ID = "toda:(5.3)"
ASSERTION_ID = "toda:adopted:eq5.3:nu_prime_hopf_relation"


def build_adopted_toda53_hopf_reference(
    source_bridge: RegistryBridgeResult,
) -> RegistryBridgeResult:
    """Adopt precisely H(nu-prime)=eta_5 from documented equation (5.3).

    A matching, immutable archive source is required. No other clause from
    (5.3) is registered. The exact reference ID is used by the existing
    Phase 163 publication-position manifest, not a guessed source order.
    """
    if not isinstance(source_bridge, RegistryBridgeResult):
        raise TypeError("source_bridge must be RegistryBridgeResult")

    candidates = tuple(
        assertion for assertion in source_bridge.registry._assertions.values()
        if assertion.origin is AssertionOrigin.SOURCE_ARCHIVE
        and isinstance(assertion.content, dict)
        and assertion.content.get("source_statement_id") == SOURCE_ID
    )
    if len(candidates) != 1:
        raise ValueError("(5.3) must have exactly one archived source")

    source = candidates[0].content
    source_text = source.get("source_text")
    if (not isinstance(source_text, str)
            or source.get("source_sha256") != SOURCE_SHA256
            or sha256(source_text.encode("utf-8")).hexdigest() != SOURCE_SHA256
            or r"\begin{equation}\label{eq:5.3}" not in source_text
            or r"H(\nu')=\eta_5" not in source_text
            or r"\nu'\in\pi_6^3" not in source_text
            or r"2\nu'=\eta_3\circ\eta_4\circ\eta_5" not in source_text):
        raise ValueError("(5.3) archived source content does not match reviewed text")

    relation = Relation(
        lhs=MapApplication(
            map=EHP_H_MAP,
            expression=HomotopyElement(
                name="ν′", dimension=3, source=6, target=3,
                generator=GeneratorSymbol(family="ν", decoration="′"),
            ),
        ),
        rhs=HomotopyElement(
            name="η₅", dimension=5, source=6, target=5,
            generator=GeneratorSymbol(family="η", index=5),
        ),
        relation_type=RelationType.EQUALITY,
    )
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id=REFERENCE_ID, kind=ReferenceKind.EQUATION,
        locator="(5.3)", source_id=SOURCE_ID,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id=ASSERTION_ID,
        reference_id=REFERENCE_ID,
        kind=AssertionKind.STATEMENT,
        content=relation,
        origin=AssertionOrigin.FIXED_STATEMENT,
        scope=("adopted (5.3) Hopf equality only",),
    ))
    step = ProofStep(
        conclusion=relation,
        premises=(),
        rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(
            name="Toda (5.3) Hopf identity",
            literature_reference=LiteratureReference(
                label="Toda (5.3)", locator="(5.3)",
            ),
        ),
    )
    return RegistryBridgeResult(
        registry,
        (MigrationRecord(
            "phase169_r3h", "(5.3):nu_prime_hopf_relation",
            ASSERTION_ID, MigrationStatus.STRUCTURED,
            "adopted source-verified Hopf equality; original edition unverified",
        ),),
        (ProofStepLink(assertion_id=ASSERTION_ID, step=step),),
    )
