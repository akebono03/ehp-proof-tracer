"""Phase 164 R4: read-only real-registry and pi_5^3 proof boundary audit.

The Phase 163 R94 manuscript archive is never a mathematical premise.
No eligibility or proof is inferred from textual similarity or source order.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from phase161_r5_backward_proof_reconstruction import phase161_r5_target_goal
from phase161_r7_premise_provenance_validation import reconstruct_phase161_r7_validated_goal
from phase163_r4_registry_bridge import MigrationStatus, build_registry_bridge
from phase163_r4_r95_phase_closure.r95_phase_closure import verify_manifest
from phase162_validated_proof_presentation import (
    build_validated_backward_proof_presentation,
    render_validated_backward_proof_markdown,
)
from proof import ProofRule
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from toda_rules import TodaProp42ExactnessStatement


@dataclass(frozen=True)
class AuditResult:
    report: dict
    narrative: str


def _given_roots(steps: tuple) -> tuple:
    visited = set()
    roots = {}

    def visit(step):
        identity = id(step)
        if identity in visited:
            return
        visited.add(identity)
        if step.rule is ProofRule.GIVEN:
            roots[identity] = step
        for premise in step.premises:
            visit(premise)

    for step in steps:
        visit(step)
    return tuple(roots.values())


def _equal_conclusion(left: object, right: object) -> bool:
    if type(left) is not type(right):
        return False
    try:
        value = left == right
    except (TypeError, ValueError):
        return False
    return type(value) is bool and value


def audit_phase164_r4(manifest_path: Path) -> AuditResult:
    """Audit current real bridge; reconstruct only from independent legacy leaves.

    This function never inserts synthetic verification evidence into the real
    registry and never calls R3 with an invented citing Assertion ID.
    """
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    archival = verify_manifest(manifest)
    if (manifest.get("proof_eligible_count") != 0
            or manifest.get("original_edition_verified") is not False
            or manifest.get("mathematical_semantics_verified_count") != 0
            or manifest.get("publication_order_scope")
            != "SOURCE_TEX_ORDER_NOT_ORIGINAL_EDITION"):
        raise ValueError("archival proof-ineligibility contract changed")

    bridge = build_registry_bridge()
    data = build_phase59_3_data()
    leaves = data["premise_steps"]
    literature = tuple(step for step in leaves if step.rule is ProofRule.INFERENCE)
    exactness = tuple(
        step for step in leaves
        if isinstance(step.conclusion, TodaProp42ExactnessStatement)
    )
    if len(literature) != 2 or len(exactness) != 4:
        raise ValueError("pi5_3 baseline leaf inventory drift")

    by_id = {record.assertion_id: record for record in bridge.records
             if record.assertion_id is not None}
    matches = []
    for index, step in enumerate(literature):
        candidates = []
        for record in bridge.records:
            if record.assertion_id is None:
                continue
            entry = bridge.registry.assertion(record.assertion_id)
            if _equal_conclusion(entry.content, step.conclusion):
                candidates.append({
                    "assertion_id": entry.assertion_id,
                    "origin": entry.origin.value,
                    "migration_status": record.status.value,
                    "source": record.source,
                    "available_after_position": entry.available_after_position,
                    "publication_position": bridge.registry.reference(
                        entry.reference_id).publication_position,
                })
        matches.append({"leaf_index": index, "candidate_count": len(candidates),
                        "candidates": candidates})

    # This is a regression baseline, not a registry-licensed derivation.
    validated = reconstruct_phase161_r7_validated_goal(
        phase161_r5_target_goal(), leaves, _given_roots(leaves)
    )
    presentation = build_validated_backward_proof_presentation(validated)
    narrative = render_validated_backward_proof_markdown(presentation)
    if validated.reconstruction.final_step.conclusion != phase161_r5_target_goal():
        raise ValueError("baseline target mismatch")
    if len(validated.reconstruction.derived_steps) != 7:
        raise ValueError("baseline rule count drift")
    if not narrative.startswith("# Backward proof narrative\n") or not narrative.rstrip().endswith("□"):
        raise ValueError("baseline narrative contract drift")
    if render_validated_backward_proof_markdown(presentation) != narrative:
        raise ValueError("non-deterministic narrative")

    report = {
        "phase": "164 R4",
        "mode": "READ_ONLY_REAL_REGISTRY_AND_LEGACY_PROOF_AUDIT",
        "source_manifest": str(manifest_path),
        "source_manifest_verified": bool(archival),
        "source_archive_reference_count": manifest["reference_count"],
        "source_archive_assertion_count": manifest["assertion_count"],
        "source_archive_proof_eligible_count": 0,
        "source_archive_promoted": False,
        "bridge_record_count": len(bridge.records),
        "bridge_status_counts": {
            status.value: sum(record.status is status for record in bridge.records)
            for status in MigrationStatus
        },
        "literature_leaves": matches,
        "exactness_given_leaf_count": len(exactness),
        "trusted_given_root_count": len(_given_roots(leaves)),
        "legacy_reconstruction_success": True,
        "legacy_derived_step_count": len(validated.reconstruction.derived_steps),
        "legacy_provenance_verified_inferences": validated.provenance.verified_inferences,
        "legacy_narrative_rendered": True,
        "real_registry_r3_reconstruction_attempted": False,
        "real_registry_r3_status": "BLOCKED_PENDING_INDEPENDENT_CITATION_EVIDENCE",
        "mathematical_certification_claimed": False,
        "production_modified": False,
        "full_pytest_run": False,
    }
    return AuditResult(report, narrative)


def write_phase164_r4_report(result: AuditResult, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "report.json").write_text(
        json.dumps(result.report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Phase 164 R4 — 実登録と証明再構築の監査", "",
        "## 結論", "",
        "- 既存の π₅³ 証明は独立した既存前提から再構築し、既存 Renderer で表示できる。",
        "- これは実登録台帳による根拠承認を意味しない。",
        "- Phase 163 R94 の原本転記117主張は一切証明根拠へ昇格させない。",
        "- 実登録を用いた R3 接続は独立検証記録と掲載・利用可能位置の確認まで保留。", "",
        "## 観測値", "",
        f"- 実 Bridge レコード数: {result.report['bridge_record_count']}",
        f"- Bridge 分類: {result.report['bridge_status_counts']}",
        f"- 文献由来の既存前提: {len(result.report['literature_leaves'])}",
        f"- EHP 完全性の証人: {result.report['exactness_given_leaf_count']}",
        f"- 再構築した既存推論: {result.report['legacy_derived_step_count']}",
        "", "## 実登録との型・結論一致候補（引用資格の承認ではない）", "",
    ]
    for item in result.report["literature_leaves"]:
        lines.append(f"- 前提 {item['leaf_index'] + 1}: {item['candidate_count']} 件")
        for candidate in item["candidates"]:
            lines.append(f"  - `{candidate['assertion_id']}` [{candidate['migration_status']}, {candidate['origin']}]")
    lines.extend(["", "## 境界", "", "実登録の引用資格を証明できない場合でも、試験用の掲載順や許可 ID を補わない。", "全体 pytest は R5 のみ。", ""])
    (output_dir / "report.md").write_text("\n".join(lines), encoding="utf-8")
    (output_dir / "legacy_narrative.md").write_text(result.narrative, encoding="utf-8")
