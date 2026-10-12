"""Phase 163 R4-R86: source-grounded claim review units, not proved assertions."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED = {
    "prop:1-6": 3,
    "thm:2.4": 2,
    "prop:2.5": 2,
    "prop:4.2": 1,
}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def split_units(catalog: dict) -> dict:
    if (catalog.get("schema") != "phase163-r83-source-archive-v1"
            or catalog.get("proof_eligible") is not False
            or catalog.get("original_edition_verified") is not False):
        raise ValueError("incompatible or promoted source catalog")
    rows = catalog.get("records")
    if not isinstance(rows, list) or len(rows) != 8:
        raise ValueError("eight source transcripts are required")
    grouped = {key: [] for key in EXPECTED}
    for row in rows:
        owner = row["owner"]
        if owner not in grouped:
            raise ValueError("unexpected source owner")
        text = row["claim_text"]
        if sha256_text(text) != row["source_claim_sha256"]:
            raise ValueError("altered source transcript")
        grouped[owner].append(row)
    for owner, count in EXPECTED.items():
        if [r["component_position"] for r in grouped[owner]] != list(range(1, count + 1)):
            raise ValueError("source component order drift")

    records = []
    common_prop25 = "上の「$\\subset$」および「$\\ni$」は"
    if common_prop25 not in grouped["prop:2.5"][1]["claim_text"]:
        raise ValueError("shared equality conditions missing")
    equality_conditions = grouped["prop:2.5"][1]["claim_text"].split(common_prop25, 1)[1]
    if not all(token in equality_conditions for token in ("m$ が奇数", "j<3m-1", "primary", "等号")):
        raise ValueError("shared equality conditions incomplete")
    for owner, source_rows in grouped.items():
        for row in source_rows:
            raw = row["claim_text"]
            parts = [(row["proposed_assertion_key"].split(":")[-1], raw)]
            if owner == "thm:2.4" and row["component_position"] == 2:
                marker = "さらに, 全ての $i$ に対して $p$-成分についての同型を与える."
                if raw.count(marker) != 1:
                    raise ValueError("cannot split even-dimensional theorem item")
                left, right = raw.split(marker)
                parts = [("even_dimension_range_isomorphism", left.strip()),
                         ("even_dimension_p_primary_isomorphism", marker)]
            if owner == "prop:1-6" and row["component_position"] == 3:
                prefix = "が成り立つ. "
                if not raw.startswith(prefix):
                    raise ValueError("unexpected third-claim leading boundary")
                parts = [(parts[0][0], raw[len(prefix):])]
            for subposition, (name, claim) in enumerate(parts, 1):
                if not claim.strip() or claim not in raw:
                    raise ValueError("split claim is not an exact source fragment")
                extra = []
                if owner == "prop:1-6":
                    extra.append("source lines 967-968 define all typed variables")
                if owner == "thm:2.4":
                    extra.append("source lines 485-490 define prime p, m>1 and map h")
                if owner == "prop:2.5":
                    extra.append("both inclusion relations share equality conditions from lines 971-974")
                if owner == "prop:4.2":
                    extra.append("equation (4.4) is an alias of the equation in Proposition 4.2")
                records.append({
                    "review_unit_id": f"review:r86:{owner}:{name}",
                    "reference_locator": {"prop:1-6": "Proposition 1.6", "thm:2.4": "Theorem 2.4",
                                          "prop:2.5": "Proposition 2.5", "prop:4.2": "Proposition 4.2"}[owner],
                    "source_owner": owner,
                    "component_position": row["component_position"],
                    "subposition": subposition,
                    "source_file": row["source_file"],
                    "source_lines": [row["start_line"], row["end_line"]],
                    "source_excerpt_sha256": row["source_claim_sha256"],
                    "claim_text": claim,
                    "claim_sha256": sha256_text(claim),
                    "shared_scope_note": row["shared_scope_note"],
                    "inherited_constraints": extra,
                    "inherited_equality_conditions": equality_conditions if owner == "prop:2.5" else None,
                    "boundary_issues": row["boundary_issues"],
                    "source_fragment_verified": True,
                    "mathematical_semantics_verified": False,
                    "original_edition_verified": False,
                    "proof_eligible": False,
                    "permanent_id_allocated": False,
                })
    expected_counts = {"prop:1-6": 3, "thm:2.4": 3, "prop:2.5": 2, "prop:4.2": 1}
    if len(records) != 9 or any(sum(r["source_owner"] == owner for r in records) != expected
                                for owner, expected in expected_counts.items()):
        raise ValueError("unexpected review unit partition")
    if len({r["review_unit_id"] for r in records}) != 9:
        raise ValueError("duplicate review unit")
    return {
        "phase": "163 R4-R86",
        "mode": "PERSISTED_SOURCE_GROUNDED_CLAIM_REVIEW",
        "source_record_count": 8,
        "review_unit_count": 9,
        "review_counts_by_owner": expected_counts,
        "split_item_count": 1,
        "mathematical_semantics_verified_count": 0,
        "original_edition_verified": False,
        "production_registry_modified": False,
        "production_ids_allocated": False,
        "proof_search_connected": False,
        "full_suite_run": False,
        "records": records,
    }


def write_outputs(result: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "claim_review_catalog.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    report = ["# Phase 163 R4-R86：主張境界の確認用台帳", "",
              "- 対象出典：8件", "- 主張の確認単位：9件", "- 命題本文の分割：Theorem 2.4 の偶数次元の場合を2件に分割", "",
              "| Reference | 確認単位 |", "|---|---:|"]
    for owner, count in result["review_counts_by_owner"].items():
        report.append(f"| {owner} | {count} |")
    report += ["", "出典 TeX 断片と継承条件を保持する。原本照合・数学的認定は未実施。",
               "本番 Registry・証明探索は変更しない。全体 pytest は未実施。"]
    (output / "report.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    result = split_units(catalog)
    write_outputs(result, args.output)
    print(json.dumps({key: value for key, value in result.items() if key != "records"}, ensure_ascii=False, indent=2))
    print("R86 source-grounded claim review complete. Full pytest not run.")


if __name__ == "__main__":
    main()
