"""Phase 164 R4-R8: reconstruct pi_5^3 using two registered fixed references.

This is an explicit fixed-literature citation path, separate from R2's
same-document publication-order checker. No order or verified ID is invented.
The cited propositions are supplied as user-confirmed sources, not re-proved.
Existing INFERENCE steps and trusted GIVEN roots retain their provenance.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path

from phase161_r5_backward_proof_reconstruction import phase161_r5_target_goal
from phase161_r7_premise_provenance_validation import (
    ValidatedBackwardReconstruction,
    reconstruct_phase161_r7_validated_goal,
    validate_phase161_r7_provenance,
)
from phase163_r3_registry_validation import audit_dependencies
from phase163_r4_registry_bridge import MigrationStatus
from phase164_r4_r1_source_crosswalk import audit_current_repository
from phase164_r4_r6_typed_binding import register_phase164_r4_r6_typed_bindings
from phase164_r7_statement_resolution import resolve_registered_statement
from proof import ProofRule, ProofStep
from toda_rules import TodaProp42ExactnessStatement
from unified_statement_registry import AssertionOrigin


_EXPECTED_IDS = (
    "toda:typed:ch5:prop5.1:finite_dimensional_subset",
    "toda:typed:ch5:eq5.3:hopf",
)


@dataclass(frozen=True)
class RegistryBackedPi53Proof:
    validated: ValidatedBackwardReconstruction
    cited_assertion_ids: tuple[str, ...]
    used_source_ids: tuple[str, ...]
    exactness_leaf_count: int
    citation_mode: str = "confirmed_fixed_literature"


def reconstruct_phase164_r4_r8_pi5_3(
    crosswalk: dict,
    existing_leaves: tuple[ProofStep, ...],
    trusted_given_roots: tuple[ProofStep, ...],
    *,
    user_confirmed_original: bool,
) -> RegistryBackedPi53Proof:
    """Take *registered typed* premises through unchanged Phase 161 proof search.

    The fixed-literature path requires explicit source confirmation, exact
    registration and step identity, strict source coverage, and trusted proof
    ancestry. It does not claim a positive R2 same-document order decision.
    """
    if not isinstance(existing_leaves, tuple) or any(
        type(step) is not ProofStep for step in existing_leaves
    ):
        raise TypeError("existing_leaves must be a tuple of ProofStep")
    if not isinstance(trusted_given_roots, tuple) or any(
        type(step) is not ProofStep for step in trusted_given_roots
    ):
        raise TypeError("trusted_given_roots must be a tuple of ProofStep")
    if len(existing_leaves) != 6 or len({id(s) for s in existing_leaves}) != 6:
        raise ValueError("exactly six distinct existing proof leaves required")
    literature = tuple(
        step for step in existing_leaves
        if step.rule is ProofRule.INFERENCE
        and not isinstance(step.conclusion, TodaProp42ExactnessStatement)
    )
    exactness = tuple(
        step for step in existing_leaves
        if step.rule is ProofRule.GIVEN
        and isinstance(step.conclusion, TodaProp42ExactnessStatement)
    )
    if len(literature) != 2 or len(exactness) != 4:
        raise ValueError("two literature and four exactness witnesses required")
    if any(s.premises for s in exactness):
        raise ValueError("exactness witnesses must be premise-free")
    registration = register_phase164_r4_r6_typed_bindings(
        crosswalk, literature, user_confirmed_original=user_confirmed_original,
    )
    if not registration.user_source_confirmation_recorded:
        raise ValueError("source confirmation was not recorded")
    if len(registration.bindings) != 2 or len(registration.bridge.proof_links) != 2:
        raise ValueError("two typed bindings and two proof links required")
    if not audit_dependencies(registration.bridge.registry).valid:
        raise ValueError("invalid registered dependencies")

    selected = []
    for index, expected_id in enumerate(_EXPECTED_IDS):
        binding = registration.bindings[index]
        link = registration.bridge.proof_links[index]
        record = registration.bridge.records[index]
        if (binding.assertion_id != expected_id
                or link.assertion_id != expected_id
                or record.assertion_id != expected_id
                or record.status is not MigrationStatus.STRUCTURED
                or binding.step is not literature[index]
                or link.step is not literature[index]):
            raise ValueError("unexpected or altered registered proof binding")
        resolved = resolve_registered_statement(
            registration.bridge,
            expected_id,
            expected_conclusion=binding.step.conclusion,
            confirmed_fixed_step=binding.step,
            confirmed_source_locator=binding.locator,
            source_confirmation_recorded=registration.user_source_confirmation_recorded,
        )
        if (resolved.assertion.origin is not AssertionOrigin.FIXED_STATEMENT
                or resolved.proof_link is not link
                or resolved.reference.locator != binding.locator):
            raise ValueError("typed reference content or boundary changed")
        selected.append(resolved.proof_link.step)

    # Existing R7 validates the very same concrete INFERENCE ancestry and
    # separately supplied GIVEN trust boundary, rather than inventing roots.
    validate_phase161_r7_provenance(tuple(selected) + exactness, trusted_given_roots)
    validated = reconstruct_phase161_r7_validated_goal(
        phase161_r5_target_goal(), tuple(selected) + exactness,
        trusted_given_roots,
    )
    if len(validated.reconstruction.derived_steps) != 7:
        raise ValueError("expected seven production derivations")
    if validated.reconstruction.final_step.conclusion != phase161_r5_target_goal():
        raise ValueError("wrong reconstructed conclusion")
    if len(tuple(s for s in validated.reconstruction.leaf_steps
                 if isinstance(s.conclusion, TodaProp42ExactnessStatement))) != 4:
        raise ValueError("not all four exactness windows used")
    return RegistryBackedPi53Proof(
        validated=validated,
        cited_assertion_ids=tuple(_EXPECTED_IDS),
        used_source_ids=tuple(b.source_statement_id for b in registration.bindings),
        exactness_leaf_count=4,
    )


def _known_trusted_roots(steps: tuple[ProofStep, ...]) -> tuple[ProofStep, ...]:
    """Replay only: collect the established Phase 59 GIVEN objects for R7.

    Collecting a root does not independently certify its mathematical truth.
    Production callers must provide the reviewed roots explicitly.
    """
    found: dict[int, ProofStep] = {}
    seen: set[int] = set()

    def visit(step: ProofStep) -> None:
        identity = id(step)
        if identity in seen:
            return
        seen.add(identity)
        if step.rule is ProofRule.GIVEN:
            found[identity] = step
        for premise in step.premises:
            visit(premise)

    for step in steps:
        visit(step)
    return tuple(found.values())


def audit_current(manifest: Path) -> dict:
    from tests.test_phase59_n3_ehp_chain import build_phase59_3_data

    existing_leaves = build_phase59_3_data()["premise_steps"]
    crosswalk = audit_current_repository(manifest)
    validated = reconstruct_phase164_r4_r8_pi5_3(
        crosswalk, existing_leaves, _known_trusted_roots(existing_leaves),
        user_confirmed_original=True,
    )
    from phase162_validated_proof_presentation import (
        build_validated_backward_proof_presentation,
        render_validated_backward_proof_markdown,
    )
    presentation = build_validated_backward_proof_presentation(validated.validated)
    narrative = render_validated_backward_proof_markdown(presentation)
    if not narrative or "## 証明" not in narrative or "□" not in narrative:
        raise ValueError("validated narrative missing proof or end marker")
    return {
        "phase": "164 R4-R8",
        "status": "REGISTERED_FIXED_LITERATURE_PI5_3_RECONSTRUCTED",
        "typed_assertion_ids": list(validated.cited_assertion_ids),
        "source_statement_ids": list(validated.used_source_ids),
        "registry_backed_reconstruction_success": True,
        "derived_step_count": len(validated.validated.reconstruction.derived_steps),
        "exactness_leaf_count": validated.exactness_leaf_count,
        "provenance_verified_inferences": validated.validated.provenance.verified_inferences,
        "narrative_rendered": True,
        "narrative": narrative,
        "citation_mode": validated.citation_mode,
        "r2_same_document_order_approval_claimed": False,
        "user_original_confirmation_recorded": True,
        "independent_edition_check_claimed": False,
        "source_archive_promoted": False,
        "production_modified": False,
        "full_pytest_run": False,
    }


def write_report(report: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    public = {key: value for key, value in report.items() if key != "narrative"}
    (output / "report.json").write_text(
        json.dumps(public, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (output / "proof.md").write_text(report["narrative"], encoding="utf-8")
    lines = [
        "# Phase 164 R4-R8 — 登録済み文献命題による証明再構築", "",
        "- 状態: " + report["status"],
        "- 登録済み Assertion: " + ", ".join(report["typed_assertion_ids"]),
        "- 既存の7推論・4つの完全性の証人から証明を再構築した。",
        "- Reference の出典確認はユーザー確認済みとして記録する。",
        "- R2 の同一文献内掲載順判定を通過したという主張はしない。",
        "- 原本転記117件の一括昇格・本番 Registry の変更はしない。",
        "- 原本版の機械照合、GIVEN の数学的真偽は独立認定しない。",
        "- 全体 pytest は Phase 終了時のみ。", "",
    ]
    (output / "report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = audit_current(args.manifest)
    write_report(report, args.output)
    print(json.dumps({k: v for k, v in report.items() if k != "narrative"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
