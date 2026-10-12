"""Phase 164 R4-R2: read-only, conservative structured-source comparison.

This is a component-level correspondence audit, NOT a mathematical proof, an
original-edition check, or a citation authorization. No production state changes.
"""
from __future__ import annotations

import argparse
from dataclasses import fields, is_dataclass
import json
from pathlib import Path

from phase164_r4_r1_source_crosswalk import audit_current_repository


PROP51_COMPONENTS = (
    ("pi3_2_group_relation", (r"\pi^{2}_{3}", r"\eta_2", r"\mathbb Z")),
    ("eta2_hopf_relation", (r"H(\eta_2)=\iota_3",)),
    ("delta_iota5_relation", (r"\Delta(\iota_5)=\pm 2", r"\eta_2")),
    ("higher_eta_group_relation", (r"\pi^{n}_{n+1}", r"\eta_n", r"n\ge3")),
)


def _find_row(report: dict, label: str) -> dict:
    matches = [item for item in report["leaves"] if item["legacy_name"] == label]
    if len(matches) != 1:
        raise ValueError("expected exactly one source crosswalk: " + label)
    return matches[0]


def compare_structured_leaves(crosswalk: dict, leaves: tuple[object, ...]) -> dict:
    """Audit actual field structure and source clauses, with fail-closed status.

    This deliberately does not infer that a token match establishes the same
    mathematical statement or that source archival records are proof eligible.
    """
    if len(leaves) != 2:
        raise ValueError("expected precisely two literature leaves")
    from proof import ProofRule, Relation, RelationType
    from expression import MapApplication, HomotopyElement
    from map_facts import EHP_H_MAP
    from toda_rules import TodaProp51FiniteDimensionalStatement

    prop_step, hopf_step = leaves
    prop_row = _find_row(crosswalk, "prop51_finite_dimensional")
    hopf_row = _find_row(crosswalk, "nu_prime_hopf")
    if (prop_row["source_statement_id"] != "toda:tex:ch5:0002"
            or hopf_row["source_statement_id"] != "toda:tex:ch5:0005"
            or not prop_row["source_identity_match"]
            or not hopf_row["source_identity_match"]):
        raise ValueError("source IDs or source identity changed")
    if (crosswalk.get("source_archive_proof_eligible_count") != 0
            or prop_step.rule is not ProofRule.INFERENCE
            or hopf_step.rule is not ProofRule.INFERENCE):
        raise ValueError("source archive eligibility or legacy provenance changed")
    prop = prop_step.conclusion
    if not isinstance(prop, TodaProp51FiniteDimensionalStatement) or not is_dataclass(prop):
        raise ValueError("Proposition 5.1 typed conclusion changed")
    actual_fields = {field.name for field in fields(prop)}
    expected_fields = {name for name, _ in PROP51_COMPONENTS}
    if actual_fields != expected_fields:
        raise ValueError("Proposition 5.1 component schema changed")
    prop_text = prop_row["source_text"]
    prop_components = []
    for name, tokens in PROP51_COMPONENTS:
        content = getattr(prop, name)
        present = {token: token in prop_text for token in tokens}
        prop_components.append({
            "name": name,
            "structured_type": type(content).__name__,
            "structured_value_present": content is not None,
            "source_tokens": present,
            "source_tokens_all_present": all(present.values()),
            "semantic_equivalence_verified": False,
        })
    # The text of Proposition 5.1 contains an additional stable group clause.
    # Do not pretend this is a fifth field of the existing finite-dimensional step.
    additional_stable_clause = r"(G_1;2)" in prop_text

    relation = hopf_step.conclusion
    if not isinstance(relation, Relation) or relation.relation_type is not RelationType.EQUALITY:
        raise ValueError("(5.3) existing conclusion no longer an equality Relation")
    lhs = relation.lhs
    rhs = relation.rhs
    if not isinstance(lhs, MapApplication) or lhs.map != EHP_H_MAP:
        raise ValueError("(5.3) existing conclusion is not an EHP Hopf image")
    nu = lhs.expression
    if not isinstance(nu, HomotopyElement) or not isinstance(rhs, HomotopyElement):
        raise ValueError("(5.3) expression types changed")
    if (getattr(nu, "name", None) != "ν′"
            or getattr(rhs, "name", None) != "η₅"
            or (getattr(nu, "source", None), getattr(nu, "target", None)) != (6, 3)
            or (getattr(rhs, "source", None), getattr(rhs, "target", None)) != (6, 5)):
        raise ValueError("(5.3) Hopf equality element typing changed")
    hopf_text = hopf_row["source_text"]
    hopf_tokens = {token: token in hopf_text for token in
                   (r"\nu'\in\pi_6^3", r"H(\nu')=\eta_5", r"2\nu'=\eta_3")}
    report = {
        "phase": "164 R4-R2",
        "mode": "READ_ONLY_COMPONENT_STRUCTURE_AUDIT",
        "status": "STRUCTURAL_CANDIDATES_ONLY_PENDING_INDEPENDENT_EVIDENCE",
        "source_archive_proof_eligible_count": 0,
        "source_publication_position_scope": "SOURCE_TEX_ORDER_NOT_ORIGINAL_EDITION",
        "prop51": {
            "statement_id": prop_row["source_statement_id"],
            "conclusion_type": type(prop).__name__,
            "components": prop_components,
            "all_four_components_structurally_present": all(
                item["structured_value_present"] and item["source_tokens_all_present"]
                for item in prop_components),
            "additional_stable_clause_in_source": additional_stable_clause,
            "semantic_equivalence_verified": False,
        },
        "nu_prime_hopf": {
            "statement_id": hopf_row["source_statement_id"],
            "conclusion_type": type(relation).__name__,
            "relation_type": relation.relation_type.name,
            "lhs_type": type(lhs).__name__,
            "map_is_ehp_h": True,
            "nu_prime_type": type(nu).__name__,
            "rhs_type": type(rhs).__name__,
            "source_tokens": hopf_tokens,
            "source_tokens_all_present": all(hopf_tokens.values()),
            "semantic_equivalence_verified": False,
        },
        "original_edition_verified": False,
        "independent_mathematical_verification": False,
        "typed_registry_binding_written": False,
        "citation_eligible": False,
        "proof_search_connected": False,
        "production_modified": False,
        "full_pytest_run": False,
    }
    if not (report["prop51"]["all_four_components_structurally_present"]
            and additional_stable_clause and report["nu_prime_hopf"]["source_tokens_all_present"]):
        raise ValueError("typed components and source clauses do not correspond")
    return report


def audit_current(manifest: Path) -> dict:
    from proof import ProofRule
    from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
    from toda_rules import TodaProp42ExactnessStatement
    crosswalk = audit_current_repository(manifest)
    leaves = tuple(step for step in build_phase59_3_data()["premise_steps"]
                   if step.rule is ProofRule.INFERENCE
                   and not isinstance(step.conclusion, TodaProp42ExactnessStatement))
    return compare_structured_leaves(crosswalk, leaves)


def write_report(report: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Phase 164 R4-R2 — 数学的内容の構造照合", "",
        "## 結論", "",
        "- Proposition 5.1 の既存4フィールドを原文の部分表現と対応検査した。",
        "- (5.3) の Relation について Hopf 写像・両辺の型と source/target を検査した。",
        "- 文字列トークン存在は数学的な意味一致の証明ではない。",
        "- TeX の掲載順は原本版の掲載順の認定ではない。",
        "- typed assertion の本登録、引用資格の承認、Backward Search の本接続は行わない。", "",
        "## Proposition 5.1", "",
        f"- Statement ID: `{report['prop51']['statement_id']}`", "",
    ]
    for item in report["prop51"]["components"]:
        lines.append(f"- `{item['name']}`: 型 `{item['structured_type']}`、構造存在={item['structured_value_present']}、出典トークン一致={item['source_tokens_all_present']}")
    lines.extend([
        f"- 安定群 $(G_1;2)$ の記述は原文に含まれる: {report['prop51']['additional_stable_clause_in_source']}",
        "- この安定群の節を4成分のいずれかと同一視しない。", "",
        "## (5.3)", "",
        f"- Statement ID: `{report['nu_prime_hopf']['statement_id']}`",
        "- 型 `Relation`、`EHP_H_MAP`、$\\nu'\\in\\pi_6^3$、$H(\\nu')=\\eta_5$ の構造を検査。",
        "- (5.3) の $2\\nu'=\\eta_3\\eta_4\\eta_5$ は別の主張であり、この Relation に含めない。", "",
        "## 継続条件", "",
        "- 原本確認と数学的な同値性の独立監査を実施する。",
        "- 利用可能位置を確定する。",
        "- 必要な場合だけ typed binding を別 Phase 操作で追加する。",
        "- 全体 pytest は Phase 164 終了時のみ。", "",
    ])
    (output_dir / "report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = audit_current(args.manifest)
    write_report(report, args.output)
    print(json.dumps({key: report[key] for key in (
        "phase", "status", "citation_eligible", "proof_search_connected", "full_pytest_run"
    )}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
