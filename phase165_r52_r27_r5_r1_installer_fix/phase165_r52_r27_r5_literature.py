"""Typed universal literature claims with strict adopted-source identity checks.

These are reference statements, not theorems about a specific substituted map.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

from phase163_r4_registry_bridge import RegistryBridgeResult, MigrationRecord, MigrationStatus
from proof import ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)


@dataclass(frozen=True)
class TodaProp44UniversalStatement:
    """For n, alpha: H(alpha)=±iota_(2n-1) implies the sum map is an isomorphism."""
    source_condition: str = "alpha in pi_(2n-1)^n; H(alpha)=+/-iota_(2n-1)"
    isomorphism_map: str = "(beta,gamma)->E(beta)+alpha o gamma"
    source_group: str = "pi_(i-1)^(n-1) + pi_i^(2n-1)"
    target_group: str = "pi_i^n"
    quantifiers: tuple[str, ...] = ("n", "i", "alpha")
    includes_suspension_injectivity: bool = True


@dataclass(frozen=True)
class Toda52UniversalStatement:
    """Composition by eta2 defines pi_i^3 ~= pi_i^2 for every integer i>=3."""
    map_formula: str = "alpha -> eta_2 o alpha"
    source_group: str = "pi_i^3"
    target_group: str = "pi_i^2"
    variable: str = "i"
    minimum_i: int = 3


_SOURCES = (
    (
        "Proposition 4.4", "toda:tex:ch4:0010", "5a98acdac4748472b3007f10ae8ff13b3530dcb24ea4757d3929aa6e72a00d73",
        ("H(\\alpha)=\\pm\\iota_{2n-1}", "\\pit{i-1}{n-1}", "\\pit{i}{2n-1}", "\\alpha\\circ\\gamma", "\\end{proposition}"),
        TodaProp44UniversalStatement(), ReferenceKind.PROPOSITION,
    ),
    (
        "(5.2)", "toda:tex:ch5:0003", "7f82293d6787d78f0ab075d7a93ae10710295bfe08487831f060ac6d1835d024",
        ("\\eta_2\\circ", "\\pi^{3}_{i}", "\\pi^{2}_{i}", "i\\ge3", "\\end{equation}"),
        Toda52UniversalStatement(), ReferenceKind.EQUATION,
    ),
)


def build_typed_literature_bridge(source_bridge: RegistryBridgeResult) -> RegistryBridgeResult:
    """Produce two fixed, source-bound general claims; never promote other archive rows."""
    registry = UnifiedStatementRegistry()
    links = []
    records = []
    for locator, source_id, digest, tokens, claim, kind in _SOURCES:
        candidates = [
            a for a in source_bridge.registry._assertions.values()
            if a.origin is AssertionOrigin.SOURCE_ARCHIVE
            and isinstance(a.content, dict)
            and a.content.get("source_statement_id") == source_id
        ]
        if len(candidates) != 1:
            raise ValueError(f"unique source archive entry required: {locator}")
        archive = candidates[0].content
        text = archive.get("source_text")
        if (not isinstance(text, str) or archive.get("source_sha256") != digest
                or any(token not in text for token in tokens)):
            raise ValueError(f"source content does not match reviewed scope: {locator}")
        ref_id = f"typed_literature:{source_id}"
        assertion_id = f"typed_literature:assertion:{source_id}"
        registry.add_reference(LiteratureEntry(ref_id, kind, locator, source_id=source_id))
        registry.add_assertion(AssertionEntry(
            assertion_id, ref_id, AssertionKind.STATEMENT, claim,
            origin=AssertionOrigin.FIXED_STATEMENT,
        ))
        links.append(ProofStepLink(assertion_id, step=ProofStep(
            conclusion=claim, premises=(), rule=ProofRule.GIVEN,
        )))
        records.append(MigrationRecord(
            "phase165_r52_r27_r5", locator, assertion_id,
            MigrationStatus.STRUCTURED, "typed universal literature claim; specialization not certified",
        ))
    return RegistryBridgeResult(registry, tuple(records), tuple(links))
