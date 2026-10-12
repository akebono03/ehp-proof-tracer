"""Phase 164 R4-R3: independent typed-clause audit; read-only and fail-closed.

This establishes component-level correspondence of the existing typed objects
with the translated Toda TeX. It does NOT verify the original edition,
publication/availability order, or independent mathematical truth, and it
cannot grant citation eligibility.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from phase164_r4_r1_source_crosswalk import audit_current_repository
from phase164_r4_r2_semantic_structure import compare_structured_leaves


EXPECTED_SOURCES = {
    "prop51_finite_dimensional": ("toda:tex:ch5:0002", "Proposition 5.1"),
    "nu_prime_hopf": ("toda:tex:ch5:0005", "(5.3)"),
}


def _element(value: object, family: str, index: int, source: int, target: int) -> bool:
    from expression import HomotopyElement
    return (isinstance(value, HomotopyElement)
            and getattr(value, "source", None) == source
            and getattr(value, "target", None) == target
            and getattr(getattr(value, "generator", None), "family", None) == family
            and getattr(getattr(value, "generator", None), "index", None) == index)


def _group(value: object, dimension: int, sphere: int) -> bool:
    from homotopy_groups import TodaPrimaryGroup
    return (isinstance(value, TodaPrimaryGroup)
            and value.group_dimension == dimension
            and value.sphere_dimension == sphere)


def _source_row(crosswalk: dict, name: str) -> dict:
    selected = [row for row in crosswalk.get("leaves", ()) if row.get("legacy_name") == name]
    if len(selected) != 1:
        raise ValueError("missing or ambiguous source leaf: " + name)
    row = selected[0]
    expected_id, expected_locator = EXPECTED_SOURCES[name]
    if (row.get("source_statement_id") != expected_id
            or row.get("source_locator") != expected_locator
            or row.get("source_identity_match") is not True
            or row.get("source_publication_position_scope") != "SOURCE_TEX_ORDER_NOT_ORIGINAL_EDITION"):
        raise ValueError("unverified source identity: " + name)
    return row


def assess_typed_clauses(crosswalk: dict, leaves: tuple[object, ...]) -> dict:
    """Verify concrete typed claims; decline unproved universal/general claims."""
    from expression import HomotopyElement, MapApplication, Multiple
    from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup
    from map_facts import EHP_H_MAP
    from proof import ProofRule, Relation, RelationType
    from toda_rules import TodaDeltaImageUpToSignStatement, TodaProp51FiniteDimensionalStatement

    if len(leaves) != 2 or any(getattr(s, "rule", None) is not ProofRule.INFERENCE for s in leaves):
        raise ValueError("expected two existing INFERENCE leaves")
    prior = compare_structured_leaves(crosswalk, leaves)
    if not (prior["prop51"]["all_four_components_structurally_present"]
            and prior["nu_prime_hopf"]["source_tokens_all_present"]):
        raise ValueError("R4-R2 structural audit not satisfied")
    prop_source = _source_row(crosswalk, "prop51_finite_dimensional")["source_text"]
    hopf_source = _source_row(crosswalk, "nu_prime_hopf")["source_text"]
    prop = leaves[0].conclusion
    hopf = leaves[1].conclusion
    if not isinstance(prop, TodaProp51FiniteDimensionalStatement):
        raise ValueError("unexpected Prop 5.1 conclusion type")

    g = prop.pi3_2_group_relation
    g_ok = (isinstance(g, Relation) and g.relation_type is RelationType.EQUALITY
            and _group(g.lhs, 3, 2) and isinstance(g.rhs, FreeCyclicGroup)
            and _element(g.rhs.generator, "η", 2, 3, 2)
            and all(token in prop_source for token in (r"\pi^{2}_{3}", r"\gen{\eta_2}", r"\mathbb Z")))

    h = prop.eta2_hopf_relation
    h_ok = (isinstance(h, Relation) and h.relation_type is RelationType.EQUALITY
            and isinstance(h.lhs, MapApplication) and h.lhs.map == EHP_H_MAP
            and _element(h.lhs.expression, "η", 2, 3, 2)
            and isinstance(h.rhs, HomotopyElement)
            and h.rhs.name == "ι_3"
            and h.rhs.dimension == 3
            and r"H(\eta_2)=\iota_3" in prop_source)

    delta = prop.delta_iota5_relation
    positive = getattr(delta, "positive_value", None)
    delta_ok = (isinstance(delta, TodaDeltaImageUpToSignStatement)
                and _group(getattr(delta.map, "source_group", None), 5, 5)
                and _group(getattr(delta.map, "target_group", None), 3, 2)
                and isinstance(delta.element, HomotopyElement)
                and delta.element.name == "ι_5"
                and isinstance(positive, Multiple)
                and positive.coefficient == 2
                and _element(positive.expression, "η", 2, 3, 2)
                and r"\Delta(\iota_5)=\pm 2\,\eta_2" in prop_source)

    higher = prop.higher_eta_group_relation
    higher_concrete = (isinstance(higher, Relation)
                       and higher.relation_type is RelationType.EQUALITY
                       and isinstance(higher.rhs, FiniteCyclicGroup)
                       and higher.rhs.order == 2
                       and hasattr(higher.lhs, "sphere_dimension")
                       and hasattr(higher.lhs, "group_dimension")
                       and higher.lhs.sphere_dimension >= 3
                       and higher.lhs.group_dimension == higher.lhs.sphere_dimension + 1
                       and _element(higher.rhs.generator, "η", higher.lhs.sphere_dimension,
                                    higher.lhs.sphere_dimension + 1, higher.lhs.sphere_dimension)
                       and r"\pi^{n}_{n+1}" in prop_source and r"(n\ge3)" in prop_source)

    relation_ok = (isinstance(hopf, Relation)
                   and hopf.relation_type is RelationType.EQUALITY
                   and isinstance(hopf.lhs, MapApplication)
                   and hopf.lhs.map == EHP_H_MAP
                   and isinstance(hopf.lhs.expression, HomotopyElement)
                   and hopf.lhs.expression.name == "ν′"
                   and (hopf.lhs.expression.source, hopf.lhs.expression.target) == (6, 3)
                   and _element(hopf.rhs, "η", 5, 6, 5)
                   and r"\nu'\in\pi_6^3" in hopf_source
                   and r"H(\nu')=\eta_5" in hopf_source)
    checks = {
        "pi3_2_free_cyclic_eta2": bool(g_ok),
        "eta2_hopf_iota3": bool(h_ok),
        "delta_iota5_up_to_sign_twice_eta2": bool(delta_ok),
        "higher_eta_specific_instance": bool(higher_concrete),
        "nu_prime_hopf_eta5": bool(relation_ok),
    }
    if not all(checks.values()):
        raise ValueError("typed mathematical clause mismatch: " + ", ".join(k for k, v in checks.items() if not v))
    return {
        "phase": "164 R4-R3",
        "mode": "READ_ONLY_INDEPENDENT_TYPED_CLAUSE_AUDIT",
        "status": "TYPED_CLAUSE_CONSISTENCY_CONFIRMED_AUTHORIZATION_BLOCKED",
        "source_statement_ids": [EXPECTED_SOURCES[k][0] for k in EXPECTED_SOURCES],
        "typed_checks": checks,
        "typed_checks_passed": len(checks),
        "proposition_5_1_universal_range_verified": False,
        "proposition_5_1_stable_clause_covered": False,
        "equation_5_3_double_nu_clause_covered": False,
        "translated_source_clauses_structurally_consistent": True,
        "independent_original_edition_verified": False,
        "independent_mathematical_truth_verified": False,
        "publication_and_availability_verified": False,
        "typed_registry_binding_written": False,
        "citation_eligible": False,
        "proof_search_connected": False,
        "production_modified": False,
        "full_pytest_run": False,
    }


def audit_current(manifest: Path) -> dict:
    from proof import ProofRule
    from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
    from toda_rules import TodaProp42ExactnessStatement
    crosswalk = audit_current_repository(manifest)
    leaves = tuple(s for s in build_phase59_3_data()["premise_steps"]
                   if s.rule is ProofRule.INFERENCE
                   and not isinstance(s.conclusion, TodaProp42ExactnessStatement))
    return assess_typed_clauses(crosswalk, leaves)


def write_report(report: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Phase 164 R4-R3 — 数学的内容の独立構造監査", "",
        "## 確認できたこと", "",
        "既存の構造化された前提と翻訳 TeX に記録された個別の式の整合性を確認した。", "",
    ]
    lines.extend(f"- `{key}`: {'PASS' if value else 'FAIL'}" for key, value in report["typed_checks"].items())
    lines.extend([
        "", "## 未検証の境界", "",
        "- Proposition 5.1 の $n\\ge3$ 全範囲を個別例だけから証明したわけではない。",
        "- Proposition 5.1 の $(G_1;2)$ の節は今回の4成分に含めない。",
        "- (5.3) の $2\\nu'=\\eta_3\\eta_4\\eta_5$ は今回の Hopf 等式とは別である。",
        "- Toda 原本版との照合、数学的真偽の独立証明、引用可能位置は未確認。",
        "- Typed Binding の本登録・引用資格付与・Backward Search の本接続は行わない。",
        "- 原本転記117主張の `proof_eligible_count=0` を維持する。",
        "- 全体 pytest は Phase 164 終了時まで実行しない。", "",
        "## 次の境界", "",
        "独立した原本・利用可能位置の根拠が確立されてから、限定された Typed Binding を検討する。", "",
    ])
    (output / "report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = audit_current(args.manifest)
    write_report(report, args.output)
    print(json.dumps({key: report[key] for key in ("phase", "status", "typed_checks_passed", "citation_eligible", "proof_search_connected", "full_pytest_run")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
