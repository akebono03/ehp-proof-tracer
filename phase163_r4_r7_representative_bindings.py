"""Phase 163 R4-R7: opt-in binding of real representative proof steps.

No witness is fabricated. Existing Phase 162 citation verification is required.
Unverified sources remain metadata-only. No search or renderer integration.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from phase162_reference_boundary import cite_verified_fixed_statement
from phase163_r4_r6_structured_binding import (
    FixedStatementBinding,
    bind_verified_fixed_statements,
)
from phase163_r4_registry_bridge import MigrationStatus, RegistryBridgeResult, build_registry_bridge
from proof import ProofRule, ProofStep


@dataclass(frozen=True)
class WitnessCandidate:
    reference_locator: str
    component_key: str
    witness: ProofStep
    expected_conclusion: object
    source_description: str

    def __post_init__(self) -> None:
        if not self.reference_locator or not self.component_key:
            raise ValueError("reference and component must be nonempty")
        if not isinstance(self.witness, ProofStep):
            raise TypeError("witness must be ProofStep")
        if self.expected_conclusion != self.witness.conclusion:
            raise ValueError("expected conclusion and witness must match")


@dataclass(frozen=True)
class BindingAttempt:
    reference_locator: str
    component_key: str
    status: str
    detail: str


def bind_representative_witnesses(
    base: RegistryBridgeResult,
    candidates: tuple[WitnessCandidate, ...],
    *,
    citation_builder: Callable[..., ProofStep] = cite_verified_fixed_statement,
) -> tuple[RegistryBridgeResult, tuple[BindingAttempt, ...]]:
    """Bind individually verified citations; preserve failures without promoting them.

    Passing a builder is only for controlled focused tests. Production defaults to
    Phase 162's verified-ancestry citation constructor.
    """
    if not isinstance(base, RegistryBridgeResult):
        raise TypeError("base must be RegistryBridgeResult")
    if not isinstance(candidates, tuple):
        raise TypeError("candidates must be a tuple")
    accepted: list[FixedStatementBinding] = []
    attempts: list[BindingAttempt] = []
    seen: set[tuple[str, str]] = set()
    eligible = {
        r.assertion_id for r in base.records
        if r.source == "boundary" and r.status is MigrationStatus.METADATA_ONLY
    }
    for candidate in candidates:
        if not isinstance(candidate, WitnessCandidate):
            raise TypeError("candidates must contain WitnessCandidate")
        locator, component = candidate.reference_locator, candidate.component_key
        key = (locator, component)
        if key in seen:
            raise ValueError(f"duplicate candidate: {key}")
        seen.add(key)
        assertion_id = f"boundary:{locator}:{component}"
        if assertion_id not in eligible:
            attempts.append(BindingAttempt(locator, component, "NOT_REGISTERED", "No metadata-only boundary entry"))
            continue
        if candidate.witness.rule is ProofRule.GIVEN:
            attempts.append(BindingAttempt(locator, component, "GIVEN_UNVERIFIED", "GIVEN is not a derived proof and cannot be promoted"))
            continue
        try:
            citation = citation_builder(
                candidate.witness, locator, component, candidate.expected_conclusion
            )
            binding = FixedStatementBinding(
                reference_locator=locator,
                component_key=component,
                citation_step=citation,
                expected_conclusion=candidate.expected_conclusion,
            )
            # The R6 validation is authoritative even for a custom builder.
            bind_verified_fixed_statements(base, (binding,))
        except (ValueError, TypeError, KeyError) as exc:
            attempts.append(BindingAttempt(locator, component, "VERIFICATION_FAILED", f"{type(exc).__name__}: {exc}"))
            continue
        accepted.append(binding)
        attempts.append(BindingAttempt(locator, component, "STRUCTURED", "Existing citation boundary validated; external literary truth not independently established"))
    result = bind_verified_fixed_statements(base, tuple(accepted))
    return result, tuple(attempts)


def representative_candidates() -> tuple[WitnessCandidate, ...]:
    """Use existing project builders unchanged; do not construct substitute proofs."""
    from probes.probe_phase58_capabilities import build_phase58_representative_result
    from probes.probe_phase65_capabilities import build_phase65_representative_result

    five_three = build_phase58_representative_result()
    five_six = build_phase65_representative_result()
    return (
        WitnessCandidate(
            "(5.3)", "nu_prime_bracket_definition",
            five_three["bracket_membership_step"],
            five_three["bracket_membership_step"].conclusion,
            "Phase58 bracket membership GIVEN: not independently verified",
        ),
        WitnessCandidate(
            "(5.3)", "nu_prime_hopf_relation",
            five_three["final_hopf_step"], five_three["expected_final_hopf"],
            "Phase58 final_hopf_step",
        ),
        WitnessCandidate(
            "(5.3)", "nu_prime_double_relation",
            five_three["final_double_step"], five_three["expected_final_double"],
            "Phase58 final_double_step",
        ),
        WitnessCandidate(
            "Proposition 5.6", "pi5_2_group_relation",
            five_six["pi5_2_step"], five_six["pi5_2_step"].conclusion,
            "Phase65 pi5_2_step",
        ),
    )


def run_audit(output_dir: Path) -> dict[str, object]:
    base = build_registry_bridge()
    candidates = representative_candidates()
    result, attempts = bind_representative_witnesses(base, candidates)
    structured = sum(r.status is MigrationStatus.STRUCTURED for r in result.records)
    counts = {status: sum(a.status == status for a in attempts)
              for status in sorted({a.status for a in attempts})}
    report = {
        "phase": "163 R4-R7",
        "status_counts": counts,
        "total_base_records": len(base.records),
        "structured_records": structured,
        "original_structured_records": sum(r.status is MigrationStatus.STRUCTURED for r in base.records),
        "notes": [
            "Citation ancestry check is not independent literature verification.",
            "Brackets represented by a GIVEN remain unverified unless a legitimate derivation exists.",
            "Nu-prime membership is not inferred from bracket membership automatically.",
            "Any failed candidate remains metadata-only; no invented theorem facts.",
            "No full pytest, no backward search or renderer changes.",
        ],
        "attempts": [
            {"reference_locator": a.reference_locator,
             "component_key": a.component_key,
             "status": a.status, "detail": a.detail}
            for a in attempts
        ],
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = ["# Phase 163 R4-R7 — 代表的な実 ProofStep 接続", "",
             "これは選択した4候補の結果であり、全命題数ではありません。", "",
             "| 文献 | component | 状態 | 理由 |", "|---|---|---|---|"]
    for a in attempts:
        lines.append(f"| {a.reference_locator} | `{a.component_key}` | {a.status} | {a.detail.replace('|', '/')} |")
    lines.extend(["", f"- Structured records: {structured}",
                  "- 全体 pytest: 未実施", "- 文献原本に対する数学的同一性の検証: 未完了", ""])
    (output_dir / "report.md").write_text("\n".join(lines), encoding="utf-8")
    return report


if __name__ == "__main__":
    audit = run_audit(Path("phase163_r4_r7_output"))
    print("Phase 163 R4-R7", audit["status_counts"])
    print("Saved phase163_r4_r7_output/report.md")
    print("Full pytest not run.")
