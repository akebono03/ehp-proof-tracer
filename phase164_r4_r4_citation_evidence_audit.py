"""Phase 164 R4-R4: fail-closed evidence assessment for two fixed Toda references.

Only translated source identity and existing typed correspondence are established.
Neither source-text order nor an existing inferred ProofStep is proof of
original-edition verification, citation completion order, or mathematical truth.
This module never mutates the registry or grants citation eligibility.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from phase164_r4_r1_source_crosswalk import audit_current_repository
from phase164_r4_r3_independent_semantic_audit import assess_typed_clauses


CLAUSE_NAMES = {
    "prop51_finite_dimensional": (
        "pi3_2_free_cyclic_eta2",
        "eta2_hopf_iota3",
        "delta_iota5_up_to_sign_twice_eta2",
        "higher_eta_symbolic_family_structure",
    ),
    "nu_prime_hopf": ("nu_prime_hopf_eta5",),
}


REQUIRED_EVIDENCE = (
    "original_edition_statement_checked",
    "typed_clause_semantics_independently_reviewed",
    "application_scope_reviewed",
    "reference_availability_independently_established",
    "citing_context_position_established",
    "proof_root_trust_boundary_reviewed",
)


def assess_citation_evidence(
    crosswalk: dict[str, Any],
    typed_report: dict[str, Any],
    *,
    external_evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Record evidence gaps without treating unverified assertions as citations.

    Caller evidence is described but deliberately never promoted automatically.
    Independent verification and authorization require a later separate phase.
    """
    if not isinstance(crosswalk, dict) or not isinstance(typed_report, dict):
        raise TypeError("crosswalk and typed_report must be dict")
    if crosswalk.get("source_manifest_verified") is not True:
        raise ValueError("source manifest not verified")
    if crosswalk.get("source_archive_proof_eligible_count") != 0:
        raise ValueError("source archive proof eligibility changed")
    if typed_report.get("translated_source_clauses_structurally_consistent") is not True:
        raise ValueError("typed clause structural audit missing")
    if typed_report.get("typed_checks_passed") != 5 or typed_report.get("citation_eligible") is not False:
        raise ValueError("R4-R3 report is not fail closed")
    if typed_report.get("independent_original_edition_verified") is not False:
        raise ValueError("original edition verification unexpectedly claimed")
    if typed_report.get("publication_and_availability_verified") is not False:
        raise ValueError("availability unexpectedly claimed")
    if typed_report.get("typed_registry_binding_written") is not False:
        raise ValueError("typed registry binding unexpectedly written")
    if external_evidence is not None and not isinstance(external_evidence, dict):
        raise TypeError("external_evidence must be a dict or None")
    rows = crosswalk.get("leaves", ())
    if not isinstance(rows, list) or len(rows) != 2:
        raise ValueError("expected exactly two source rows")
    if set(typed_report.get("typed_checks", {})) != {
        clause for clauses in CLAUSE_NAMES.values() for clause in clauses
    } or not all(typed_report["typed_checks"].values()):
        raise ValueError("typed clause checks incomplete")
    if external_evidence is not None:
        if set(external_evidence) != set(CLAUSE_NAMES):
            raise ValueError("external evidence keys must match both leaves")
        for name, item in external_evidence.items():
            if not isinstance(item, dict) or set(item) != set(REQUIRED_EVIDENCE):
                raise ValueError("evidence fields incomplete for " + name)
            if any(not isinstance(value, bool) for value in item.values()):
                raise TypeError("evidence flags must be bool")
    result_rows = []
    seen = set()
    for row in rows:
        name = row.get("legacy_name")
        if name not in CLAUSE_NAMES or name in seen:
            raise ValueError("ambiguous source leaf names")
        seen.add(name)
        if (row.get("source_identity_match") is not True
                or row.get("source_publication_position_scope") != "SOURCE_TEX_ORDER_NOT_ORIGINAL_EDITION"
                or row.get("citation_eligible") is not False
                or row.get("exact_semantic_equivalence_verified") is not False
                or row.get("original_edition_verified") is not False):
            raise ValueError("R4-R1 evidence boundary changed: " + name)
        source_text = row.get("source_text")
        if not isinstance(source_text, str) or hashlib.sha256(source_text.encode("utf-8")).hexdigest() != row.get("source_text_sha256"):
            raise ValueError("source text hash mismatch: " + name)
        clauses = CLAUSE_NAMES[name]
        checks = {clause: typed_report["typed_checks"][clause] for clause in clauses}
        recorded = external_evidence[name] if external_evidence is not None else {field: False for field in REQUIRED_EVIDENCE}
        result_rows.append({
            "leaf": name,
            "source_statement_id": row["source_statement_id"],
            "source_locator": row["source_locator"],
            "source_file": row["source_file"],
            "source_start_line": row["source_start_line"],
            "source_sha256": row["source_text_sha256"],
            "translated_source_position": row["source_publication_position"],
            "translated_position_scope": row["source_publication_position_scope"],
            "typed_clause_checks": checks,
            "typed_structure_consistent": all(checks.values()),
            "recorded_external_evidence_not_authenticated": recorded,
            "unverified_prerequisites": [field for field in REQUIRED_EVIDENCE],
            "citing_context": "pi_5^3 backward reconstruction; not a verified literature publication position",
            "reference_available_after_position": None,
            "citation_status": "BLOCKED_PENDING_INDEPENDENT_EVIDENCE",
        })
    if set(seen) != set(CLAUSE_NAMES):
        raise ValueError("source leaf names incomplete")
    return {
        "phase": "164 R4-R4",
        "mode": "READ_ONLY_CITATION_EVIDENCE_GAPS",
        "status": "BLOCKED_PENDING_ORIGINAL_SCOPE_AND_AVAILABILITY_EVIDENCE",
        "source_archive_proof_eligible_count": 0,
        "typed_checks_passed": 5,
        "source_locator_candidates": 2,
        "evidence_authenticated_count": 0,
        "original_edition_verified": False,
        "publication_and_availability_verified": False,
        "typed_binding_written": False,
        "citation_eligible": False,
        "proof_search_connected": False,
        "production_modified": False,
        "full_pytest_run": False,
        "leaves": result_rows,
    }


def audit_current(manifest_path: Path) -> dict[str, Any]:
    from proof import ProofRule
    from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
    from toda_rules import TodaProp42ExactnessStatement

    crosswalk = audit_current_repository(manifest_path)
    leaves = tuple(
        step for step in build_phase59_3_data()["premise_steps"]
        if step.rule is ProofRule.INFERENCE
        and not isinstance(step.conclusion, TodaProp42ExactnessStatement)
    )
    typed_report = assess_typed_clauses(crosswalk, leaves)
    return assess_citation_evidence(crosswalk, typed_report)


def write_report(report: dict[str, Any], output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Phase 164 R4-R4 — 引用資格の証拠監査", "",
        "## 結論", "",
        "- 翻訳 TeX の出典 ID と既存の型付き構造は2件とも照合できた。",
        "- 原本版との照合・数学的意味の独立確認・引用可能位置は未認証。",
        "- 既存の推論結果は Reference の原本確認を代替しない。",
        "- source archive の117主張は証明に使用可能として昇格させない。", "",
        "## 前提ごとの確認状況", "",
    ]
    for row in report["leaves"]:
        lines.extend([
            f"### {row['source_locator']} — {row['leaf']}", "",
            f"- Statement ID: `{row['source_statement_id']}`",
            f"- 翻訳 TeX: `{row['source_file']}` {row['source_start_line']}行",
            f"- 翻訳 TeX 内の掲載順: {row['translated_source_position']}（原本位置ではない）",
            "- 対応する型付き構造: " + ", ".join(f"`{name}`" for name in row["typed_clause_checks"]),
            "- 引用可能位置: 未認証（ProofStep の目標は文献の掲載位置ではない）",
            "- 不足する確認事項: " + ", ".join(f"`{x}`" for x in row["unverified_prerequisites"]),
            "- 引用資格: BLOCKED", "",
        ])
    lines.extend([
        "## 次の境界", "",
        "原本の該当箇所の独立照合、変数範囲と引用条件の確認、",
        "対象証明に対する依存関係・利用可能位置の特定を先に行う。",
        "その証拠が得られるまで Typed Binding を本登録せず、R2 の許可リストにも加えない。", "",
        "全体 pytest は Phase 164 終了時のみ実行する。", "",
    ])
    (output / "report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = audit_current(args.manifest)
    write_report(report, args.output)
    print(json.dumps({key: report[key] for key in (
        "phase", "status", "source_locator_candidates", "typed_checks_passed",
        "evidence_authenticated_count", "citation_eligible", "proof_search_connected", "full_pytest_run",
    )}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
