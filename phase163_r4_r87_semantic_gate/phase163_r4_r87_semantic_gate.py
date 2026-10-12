"""Phase 163 R4-R87: source-grounded semantic registration gate.

No automatic mathematical certification, permanent IDs, or proof eligibility.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


CLAIM_REVIEW = {
    "prop:1-6:last_argument_additivity": (
        "Toda bracket の第3変数に関する包含関係",
        ("共有変数の型指定", "n>=1 または W=E W'", "包含関係（等号としない）"),
        "第1章訂正TeXと原本の突合が必要",
    ),
    "prop:1-6:middle_argument_additivity": (
        "Toda bracket の第2変数に関する加法等式",
        ("共有変数の型指定", "n>=1 または gamma=E gamma'（空間の懸垂条件を含む）"),
        "共通の変数定義の継承と原本照合が必要",
    ),
    "prop:1-6:first_argument_additivity": (
        "Toda bracket の第1変数に関する包含関係",
        ("共有変数の型指定", "n>=1 または beta=E beta' かつ gamma=E gamma'", "包含関係（等号としない）"),
        "第三項の開始境界と原本照合が必要",
    ),
    "thm:2.4:odd_dimension_case": (
        "m が奇数かつ p=2 の場合の h_* の全次数同型",
        ("p は素数", "m>1", "指定された写像 h", "m は奇数", "p=2", "全ての i"),
        "参照文献との対応と写像の仮定の数学的確認が必要",
    ),
    "thm:2.4:even_dimension_range_isomorphism": (
        "m が偶数の場合の指定次数範囲での h_* の同型",
        ("p は素数", "m>1", "指定された写像 h", "m は偶数", "i<(p+1)m-1"),
        "写像の仮定と次数範囲の数学的確認が必要",
    ),
    "thm:2.4:even_dimension_p_primary_isomorphism": (
        "m が偶数の場合の h_* による全次数の p-成分の同型",
        ("p は素数", "m>1", "指定された写像 h", "m は偶数", "全ての i", "p-成分に限定"),
        "参照先写像と p-成分の数学的意味の確認が必要",
    ),
    "prop:2.5:delta_composition": (
        "Delta と合成の包含関係、および追加条件下の等号",
        ("alpha, beta の型", "通常は包含", "m が奇数または j<3m-1 または関係する元が 2-primary のとき等号"),
        "共通の等号成立条件と型の確認が必要",
    ),
    "prop:2.5:whitehead_product_case": (
        "二重懸垂に対する Delta と Whitehead product の関係、および追加条件下の等号",
        ("gamma の型と Whitehead product の定義", "通常は包含", "m が奇数または j<3m-1 または関係する元が 2-primary のとき等号"),
        "共通の等号成立条件と符号・型の確認が必要",
    ),
    "prop:4.2:ehp_exact_sequence": (
        "EHP 完全列 (4.4) の完全性",
        ("E, H, Delta の定義と添字", "(4.4) は Proposition 4.2 内の式のラベルであり重複 Reference を生成しない"),
        "適用次元の範囲と式 (4.4) の別名関係を確定する必要がある",
    ),
}


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def build_gate(source: dict) -> dict:
    if source.get("phase") != "163 R4-R86":
        raise ValueError("R86 review catalog required")
    records = source.get("records")
    if not isinstance(records, list) or len(records) != 9:
        raise ValueError("expected exactly nine review units")
    seen = set()
    grouped = defaultdict(list)
    proposed = []
    for item in records:
        review_id = item["review_unit_id"]
        if not review_id.startswith("review:r86:") or review_id in seen:
            raise ValueError("duplicate or invalid review unit id")
        seen.add(review_id)
        key = review_id.removeprefix("review:r86:")
        if key not in CLAIM_REVIEW:
            raise ValueError("unrecognized review unit")
        if sha256_text(item["claim_text"]) != item["claim_sha256"]:
            raise ValueError(f"claim text tampered: {key}")
        if not item.get("source_fragment_verified"):
            raise ValueError("source fragment not verified")
        if (item.get("mathematical_semantics_verified") is not False
                or item.get("original_edition_verified") is not False
                or item.get("proof_eligible") is not False
                or item.get("permanent_id_allocated") is not False):
            raise ValueError("source must remain non-certified")
        if not item["source_file"].endswith(".tex") or not item["source_excerpt_sha256"]:
            raise ValueError("missing source provenance")
        grouped[item["source_owner"]].append((item["component_position"], item["subposition"]))
        label, constraints, blocker = CLAIM_REVIEW[key]
        if key.startswith("prop:2.5:"):
            clause = item.get("inherited_equality_conditions") or ""
            if not all(t in clause for t in ("m$ が奇数", "j<3m-1", "primary")):
                raise ValueError("shared equality conditions missing")
        if key == "thm:2.4:even_dimension_p_primary_isomorphism" and "成分" not in item["claim_text"]:
            raise ValueError("p-primary claim lost")
        if key == "prop:4.2:ehp_exact_sequence" and "label{4.4}" not in item["claim_text"]:
            raise ValueError("equation alias lost")
        proposed.append({
            "review_unit_id": review_id,
            "reference_locator": item["reference_locator"],
            "source_owner": item["source_owner"],
            "component_position": item["component_position"],
            "subposition": item["subposition"],
            "mathematical_description_proposal_jp": label,
            "required_scope_conditions_jp": list(constraints),
            "source_file": item["source_file"],
            "source_lines": item["source_lines"],
            "claim_sha256": item["claim_sha256"],
            "source_excerpt_sha256": item["source_excerpt_sha256"],
            "origin": "SOURCE_ARCHIVE",
            "source_fragment_verified": True,
            "mathematical_semantics_verified": False,
            "original_edition_verified": False,
            "proof_eligible": False,
            "semantic_registration_allowed": False,
            "blocking_reason_jp": blocker,
        })
    if set(CLAIM_REVIEW) != {x.removeprefix('review:r86:') for x in seen}:
        raise ValueError("missing review unit")
    for owner, positions in grouped.items():
        if positions != sorted(positions) or len(positions) != len(set(positions)):
            raise ValueError(f"invalid component order: {owner}")
    counts = Counter(r["source_owner"] for r in proposed)
    if dict(counts) != {"prop:1-6": 3, "thm:2.4": 3, "prop:2.5": 2, "prop:4.2": 1}:
        raise ValueError("unexpected claims per reference")
    return {
        "phase": "163 R4-R87", "mode": "SOURCE_GROUNDED_SEMANTIC_REGISTRATION_GATE",
        "review_unit_count": len(proposed),
        "source_fragment_verified_count": len(proposed),
        "description_proposal_count": len(proposed),
        "mathematical_semantics_verified_count": 0,
        "original_edition_verified": False,
        "semantic_registration_allowed_count": 0,
        "proof_eligible_count": 0,
        "production_registry_modified": False,
        "production_ids_allocated": False,
        "proof_search_connected": False,
        "full_suite_run": False,
        "records": proposed,
    }


def write_outputs(result: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "semantic_registration_gate.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Phase 163 R4-R87：数学的主張の正式登録ゲート", "",
             "出典の9確認単位について、数学的内容の**提案**と必要条件を整理する。原本照合・数学的認定は未実施。", "",
             "| Reference | 順序 | 主張の解釈案 | 正式登録 |", "|---|---|---|---|"]
    for item in result["records"]:
        lines.append(f"| {item['reference_locator']} | {item['component_position']}.{item['subposition']} | {item['mathematical_description_proposal_jp']} | 保留 |")
    lines += ["", "## 登録前の要件", ""]
    for item in result["records"]:
        lines += [f"### {item['review_unit_id']}", "", "必要条件：" + "、".join(item['required_scope_conditions_jp']), "", "未解決：" + item['blocking_reason_jp'], ""]
    lines += ["本番 Registry は未変更。原本照合と数学的な適用条件の確認が完了するまで、正式登録 ID・証明探索には接続しない。", ""]
    (output / "report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = build_gate(json.loads(args.input.read_text(encoding="utf-8")))
    write_outputs(result, args.output)
    print(json.dumps({k: v for k, v in result.items() if k != "records"}, ensure_ascii=False, indent=2))
    print("R87 semantic registration gate complete. No production changes; full pytest not run.")


if __name__ == "__main__":
    main()
