"""Phase 164 R4-R1: read-only source-locator crosswalk for two pi_5^3 leaves.

Source transcription, source locator, structured conclusion, and independent
mathematical verification are deliberately different levels of evidence.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from phase163_r4_r95_phase_closure.r95_phase_closure import verify_manifest


SOURCE_TARGETS = (
    ("prop51_finite_dimensional", "Proposition 5.1", "toda:tex:ch5:0002"),
    ("nu_prime_hopf", "(5.3)", "toda:tex:ch5:0005"),
)


def _ancestors(step: object) -> tuple[object, ...]:
    found: dict[int, object] = {}
    active: set[int] = set()

    def walk(node: object) -> None:
        key = id(node)
        if key in active:
            raise ValueError("cyclic proof ancestry")
        if key in found:
            return
        active.add(key)
        for premise in node.premises:
            walk(premise)
        active.remove(key)
        found[key] = node

    walk(step)
    return tuple(found.values())


def source_crosswalk(manifest: dict, leaves: tuple[object, ...]) -> dict:
    """Compare source identities and legacy step contracts without eligibility promotion."""
    verify_manifest(manifest)
    if len(leaves) != 2:
        raise ValueError("expected two existing literature leaves")
    from proof import ProofRule
    from toda_rules import TodaProp51FiniteDimensionalStatement
    from proof import Relation, RelationType

    first, second = leaves
    if (first.rule is not ProofRule.INFERENCE
            or not isinstance(first.conclusion, TodaProp51FiniteDimensionalStatement)):
        raise ValueError("first literature leaf contract drift")
    if (second.rule is not ProofRule.INFERENCE
            or not isinstance(second.conclusion, Relation)
            or second.conclusion.relation_type is not RelationType.EQUALITY):
        raise ValueError("second literature leaf contract drift")
    if len({id(first), id(second)}) != 2:
        raise ValueError("duplicated literature leaves")

    rows = manifest["assertions"]
    output = []
    for index, ((label, locator, identifier), step) in enumerate(zip(SOURCE_TARGETS, leaves)):
        candidates = [row for row in rows if row.get("locator") == locator]
        if len(candidates) != 1 or candidates[0].get("statement_id") != identifier:
            raise ValueError("expected source ID/locator not uniquely present: " + locator)
        row = candidates[0]
        chain = _ancestors(step)
        roots = [node for node in chain if node.rule is ProofRule.GIVEN]
        rule_names = sorted({node.inference_rule.name for node in chain
                             if node.rule is ProofRule.INFERENCE
                             and node.inference_rule is not None})
        if not roots or not rule_names:
            raise ValueError("legacy inference ancestry missing")
        output.append({
            "leaf_index": index,
            "legacy_name": label,
            "legacy_conclusion_type": type(step.conclusion).__name__,
            "legacy_rule": step.rule.name,
            "legacy_step_ancestry_count": len(chain),
            "legacy_given_root_count": len(roots),
            "legacy_inference_rule_names": rule_names,
            "source_locator": locator,
            "source_statement_id": row["statement_id"],
            "source_reference_id": row["reference_id"],
            "source_file": row["source_file"],
            "source_start_line": row["start_line"],
            "source_publication_position": row["publication_position"],
            "source_publication_position_scope": manifest["publication_order_scope"],
            "source_text_sha256": row["source_sha256"],
            "source_text": row["source_text"],
            "source_identity_match": True,
            "mathematical_statement_type_match": False,
            "structured_assertion_connected": False,
            "exact_semantic_equivalence_verified": False,
            "original_edition_verified": False,
            "citation_eligible": False,
            "status": "LOCATOR_CANDIDATE_ONLY",
        })
    return {
        "phase": "164 R4-R1",
        "mode": "READ_ONLY_TWO_LEAF_SOURCE_CROSSWALK",
        "source_manifest_verified": True,
        "source_archive_assertion_count": manifest["assertion_count"],
        "source_archive_proof_eligible_count": manifest["proof_eligible_count"],
        "literature_leaf_count": 2,
        "source_locator_candidate_count": len(output),
        "mathematically_verified_bindings": 0,
        "proof_search_connected": False,
        "production_modified": False,
        "full_pytest_run": False,
        "status": "BLOCKED_PENDING_TYPED_BINDING_AND_INDEPENDENT_EVIDENCE",
        "leaves": output,
    }


def audit_current_repository(manifest_path: Path) -> dict:
    from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
    from proof import ProofRule
    from toda_rules import TodaProp42ExactnessStatement

    data = build_phase59_3_data()
    literature = tuple(step for step in data["premise_steps"]
                       if step.rule is ProofRule.INFERENCE
                       and not isinstance(step.conclusion, TodaProp42ExactnessStatement))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    return source_crosswalk(manifest, literature)


def write_reports(report: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Phase 164 R4-R1 — 2前提の実台帳対応監査", "",
        "## 判定", "",
        "- 文献名・原本転記 Statement ID の候補を2件特定した。",
        "- これは数学的な型一致・命題同値性・引用資格の承認ではない。",
        "- source publication position は TeX 内の順序であり原本掲載順ではない。",
        "- 実 Registry の typed assertion との接続は未確立。R3 の実データ実行は行わない。", "",
        "## 前提ごとの対応候補", "",
    ]
    for row in report["leaves"]:
        lines.extend([
            f"### {row['legacy_name']}", "",
            f"- 既存 ProofStep 結論型: `{row['legacy_conclusion_type']}`",
            f"- 登録出典: `{row['source_locator']}`",
            f"- Statement ID: `{row['source_statement_id']}`",
            f"- Reference ID: `{row['source_reference_id']}`",
            f"- TeX: `{row['source_file']}` {row['source_start_line']}行",
            f"- TeX の掲載順: {row['source_publication_position']}（原本掲載順未確認）",
            f"- 祖先ステップ: {row['legacy_step_ancestry_count']}、GIVEN 根: {row['legacy_given_root_count']}",
            "- 判定: LOCATOR_CANDIDATE_ONLY。数学的な対応証明と引用資格の独立検証が必要。", "",
        ])
    lines.extend([
        "## 次に必要な証拠", "",
        "1. Proposition 5.1 の複合的な主張と `TodaProp51FiniteDimensionalStatement` の各成分を対応付ける。",
        "2. (5.3) の `H(ν′)=η₅` と `Relation` を構造的に対応付ける。",
        "3. 文献原本の確認、命題の利用可能位置、独立した数学的検証を記録する。",
        "4. 既存の推論祖先が固定結果を展開したものか確認し、文献参照と内部証明を混同しない。", "",
        "## 境界", "",
        "Phase 164 R4-R1 は読み取り専用。Production、Registry、ProofStep、Renderer の変更はない。",
        "全体 pytest は Phase 164 の最後のみ。", "",
    ])
    (output_dir / "report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = audit_current_repository(args.manifest)
    write_reports(report, args.output)
    print(json.dumps({key: report[key] for key in (
        "phase", "status", "literature_leaf_count", "source_locator_candidate_count",
        "mathematically_verified_bindings", "proof_search_connected", "full_pytest_run"
    )}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
