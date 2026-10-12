"""Phase 164 R4-R6: limited typed bindings for two user-confirmed Toda references.

An explicit user confirmation applies to source transcription, not automatic
mathematical certification or publication-order availability. The two existing
INFERENCE witnesses remain unchanged. Nothing is installed into the global
production registry or submitted to proof search by this module.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path

from phase163_r3_registry_validation import audit_dependencies
from phase163_r4_registry_bridge import (
    MigrationRecord,
    MigrationStatus,
    RegistryBridgeResult,
)
from phase164_r4_r1_source_crosswalk import audit_current_repository
from phase164_r4_r3_independent_semantic_audit import assess_typed_clauses
from proof import ProofRule, ProofStep
from toda_rules import TodaProp42ExactnessStatement
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    LiteratureEntry,
    ProofStepLink,
    ReferenceKind,
    UnifiedStatementRegistry,
)


@dataclass(frozen=True)
class ConfirmedSourceBinding:
    """Source-confirmed binding; never an R2 citation approval token."""

    assertion_id: str
    source_statement_id: str
    locator: str
    step: ProofStep
    coverage: str
    verification_basis: str


@dataclass(frozen=True)
class TypedBindingRegistration:
    bridge: RegistryBridgeResult
    bindings: tuple[ConfirmedSourceBinding, ...]
    user_source_confirmation_recorded: bool
    citation_eligible: bool = False
    proof_search_connected: bool = False


_TARGETS = (
    ("prop51_finite_dimensional", "Proposition 5.1", "toda:tex:ch5:0002",
     "toda:typed:ch5:prop5.1:finite_dimensional_subset", ReferenceKind.PROPOSITION,
     "Four typed components only; excludes stable (G_1;2) clause."),
    ("nu_prime_hopf", "(5.3)", "toda:tex:ch5:0005",
     "toda:typed:ch5:eq5.3:hopf", ReferenceKind.EQUATION,
     "H(nu-prime)=eta_5 only; excludes membership and twice-nu relation."),
)


def register_phase164_r4_r6_typed_bindings(
    crosswalk: dict,
    literature_leaves: tuple[ProofStep, ...],
    *,
    user_confirmed_original: bool,
) -> TypedBindingRegistration:
    """Build an isolated typed bridge after validating R4-R1 and R4-R3 contracts.

    Original confirmation is recorded as user attestation. A source text hash,
    typed shape, and recorded attestation cannot establish when a proposition
    became available in the original work or a new proof's citation context.
    """
    if type(user_confirmed_original) is not bool or not user_confirmed_original:
        raise ValueError("explicit user original-source confirmation required")
    if not isinstance(crosswalk, dict) or not isinstance(literature_leaves, tuple):
        raise TypeError("crosswalk dict and literature_leaves tuple required")
    if (crosswalk.get("source_manifest_verified") is not True
            or crosswalk.get("source_archive_proof_eligible_count") != 0
            or len(literature_leaves) != 2
            or any(type(s) is not ProofStep or s.rule is not ProofRule.INFERENCE
                   for s in literature_leaves)):
        raise ValueError("source manifest or existing literature leaf contract invalid")
    typed = assess_typed_clauses(crosswalk, literature_leaves)
    if (typed.get("typed_checks_passed") != 5
            or typed.get("citation_eligible") is not False
            or typed.get("typed_registry_binding_written") is not False):
        raise ValueError("R4-R3 contract changed")
    rows = crosswalk.get("leaves")
    if not isinstance(rows, list) or len(rows) != 2:
        raise ValueError("R4-R1 source rows missing")
    registry = UnifiedStatementRegistry()
    records = []
    links = []
    bindings = []
    for index, (name, locator, source_id, assertion_id, kind, coverage) in enumerate(_TARGETS):
        source = rows[index]
        if (source.get("legacy_name") != name
                or source.get("source_locator") != locator
                or source.get("source_statement_id") != source_id
                or source.get("source_identity_match") is not True
                or source.get("source_publication_position_scope") != "SOURCE_TEX_ORDER_NOT_ORIGINAL_EDITION"):
            raise ValueError("source-to-leaf pairing mismatch: " + name)
        step = literature_leaves[index]
        reference_id = "toda:" + locator
        registry.add_reference(LiteratureEntry(
            reference_id=reference_id,
            kind=kind,
            locator=locator,
            source_id="Toda:1962:user-checked",
            publication_position=None,
        ))
        registry.add_assertion(AssertionEntry(
            assertion_id=assertion_id,
            reference_id=reference_id,
            kind=AssertionKind.STATEMENT,
            content=step.conclusion,
            origin=AssertionOrigin.FIXED_STATEMENT,
            scope=coverage,
            component_position=None,
            available_after_position=None,
            dependencies=(),
        ))
        records.append(MigrationRecord(
            source="phase164_r4_r6_user_confirmed_typed",
            source_key=source_id,
            assertion_id=assertion_id,
            status=MigrationStatus.STRUCTURED,
            detail="Existing INFERENCE witness bound; external verification and availability remain distinct",
        ))
        links.append(ProofStepLink(assertion_id=assertion_id, step=step))
        bindings.append(ConfirmedSourceBinding(
            assertion_id=assertion_id,
            source_statement_id=source_id,
            locator=locator,
            step=step,
            coverage=coverage,
            verification_basis="user_confirmed_original_correspondence",
        ))
    bridge = RegistryBridgeResult(registry, tuple(records), tuple(links))
    if not audit_dependencies(registry).valid:
        raise ValueError("typed binding dependencies are invalid")
    return TypedBindingRegistration(
        bridge=bridge, bindings=tuple(bindings),
        user_source_confirmation_recorded=True,
    )


def audit_current(manifest_path: Path) -> dict:
    from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
    crosswalk = audit_current_repository(manifest_path)
    leaves = tuple(
        step for step in build_phase59_3_data()["premise_steps"]
        if step.rule is ProofRule.INFERENCE
        and not isinstance(step.conclusion, TodaProp42ExactnessStatement)
    )
    registration = register_phase164_r4_r6_typed_bindings(
        crosswalk, leaves, user_confirmed_original=True,
    )
    return {
        "phase": "164 R4-R6",
        "mode": "ISOLATED_TYPED_BINDING_USER_SOURCE_CONFIRMATION",
        "status": "TWO_TYPED_BINDINGS_REGISTERED_CITATION_AVAILABILITY_PENDING",
        "typed_binding_count": len(registration.bindings),
        "source_statement_ids": [b.source_statement_id for b in registration.bindings],
        "typed_assertion_ids": [b.assertion_id for b in registration.bindings],
        "coverage": [b.coverage for b in registration.bindings],
        "user_original_confirmation_recorded": registration.user_source_confirmation_recorded,
        "independent_edition_check_claimed": False,
        "availability_position_established": False,
        "citation_eligible": registration.citation_eligible,
        "proof_search_connected": registration.proof_search_connected,
        "source_archive_promoted": False,
        "production_registry_modified": False,
        "full_pytest_run": False,
    }


def write_report(report: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Phase 164 R4-R6 — 2件の型付き対応付け", "",
        "- 状態: " + report["status"],
        "- 型付き Assertion: 2件。元の ProofStep の INFERENCE 祖先は維持。",
        "- 原著対応: ユーザー確認済みとして記録（独立機械照合とは区別）。",
        "- Proposition 5.1: 既存4成分だけを登録。安定群の節は未収録。",
        "- (5.3): Hopf 等式だけを登録。他の節は未収録。",
        "- 文献掲載順・引用可能位置: 未確定。R2 による許可はまだ行わない。",
        "- 既存の全域 Registry・Proof Search・Renderer・Source Archive は変更しない。",
        "- 全体 pytest は Phase 164 の最終段階のみ。", "",
    ]
    (output / "report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = audit_current(args.manifest)
    write_report(report, args.output)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
