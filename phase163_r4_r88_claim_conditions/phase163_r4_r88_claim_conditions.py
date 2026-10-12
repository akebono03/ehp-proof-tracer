"""Phase 163 R4-R88: source-derived scope checks, not mathematical certification."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

RULES = {
    "prop:1-6:last_argument_additivity": ("\\supset", "n\\ge 1", "W=\\Ex W'"),
    "prop:1-6:middle_argument_additivity": ("\\ =", "n\\ge 1", "\\gamma=\\Ex\\gamma'"),
    "prop:1-6:first_argument_additivity": ("\\supset", "n\\ge 1", "\\beta=\\Ex\\beta'", "\\gamma=\\Ex\\gamma'"),
    "thm:2.4:odd_dimension_case": ("m$ が奇数", "p=2", "全ての $i$", "h_*"),
    "thm:2.4:even_dimension_range_isomorphism": ("m$ が偶数", "i<(p+1)m-1", "h_*"),
    "thm:2.4:even_dimension_p_primary_isomorphism": ("全ての $i$", "$p$-成分"),
    "prop:2.5:delta_composition": ("\\Delta\\alpha", "\\subset", "\\beta\\in"),
    "prop:2.5:whitehead_product_case": ("\\Delta(E^2\\gamma)", "\\ni", "\\iota_m"),
    "prop:4.2:ehp_exact_sequence": ("\\label{4.4}", "\\xrightarrow{\\ H\\ }", "\\xrightarrow{\\ \\Delta\\ }"),
}

SCOPE_BLOCKERS = {
    "Proposition 1.6": "共通の変数型と各場合の懸垂条件について原著との照合が残る",
    "Theorem 2.4": "h の選択、p-primary 成分の意味、次数制限について文献確認が残る",
    "Proposition 2.5": "二つの包含関係に適用する等号条件と符号・次元の確認が残る",
    "Proposition 4.2": "EHP 完全列の定義域・次元条件と (4.4) の別名を確認する必要がある",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def tail_key(review_id: str) -> str:
    prefix = "review:r86:"
    if not review_id.startswith(prefix):
        raise AssertionError("invalid review unit ID")
    return review_id[len(prefix):]


def assess(r86: dict, r87: dict) -> dict:
    if r86.get("phase") != "163 R4-R86" or r87.get("phase") != "163 R4-R87":
        raise AssertionError("unexpected input phase")
    if r86.get("review_unit_count") != 9 or r87.get("review_unit_count") != 9:
        raise AssertionError("unexpected review unit count")
    if r86.get("records") is None or r87.get("records") is None:
        raise AssertionError("records missing")
    index = {row["review_unit_id"]: row for row in r87["records"]}
    if len(index) != 9 or len(r86["records"]) != 9:
        raise AssertionError("duplicate/missing rows")
    rows = []
    seen = set()
    by_owner = {}
    for source in r86["records"]:
        unit_id = source["review_unit_id"]
        key = tail_key(unit_id)
        if unit_id in seen or key not in RULES or unit_id not in index:
            raise AssertionError("unexpected/duplicate claim")
        seen.add(unit_id)
        gate = index[unit_id]
        for field in ("reference_locator", "source_file", "claim_sha256", "source_excerpt_sha256", "component_position", "subposition"):
            if gate[field] != source[field]:
                raise AssertionError(f"R86/R87 disagreement: {field}")
        if gate.get("origin") != "SOURCE_ARCHIVE" or any(gate.get(flag) is not False for flag in (
            "mathematical_semantics_verified", "original_edition_verified", "proof_eligible", "semantic_registration_allowed"
        )):
            raise AssertionError("approval flag unexpectedly enabled")
        text = source["claim_text"]
        if hashlib.sha256(text.encode("utf-8")).hexdigest() != source["claim_sha256"]:
            raise AssertionError("claim text checksum mismatch")
        missing = [token for token in RULES[key] if token not in text]
        if missing:
            raise AssertionError(f"claim condition not found in TeX: {key} {missing}")
        if not gate.get("required_scope_conditions_jp"):
            raise AssertionError("required conditions missing")
        locator = gate["reference_locator"]
        if locator not in SCOPE_BLOCKERS:
            raise AssertionError("unrecognized Reference")
        by_owner.setdefault(locator, []).append((source["component_position"], source["subposition"]))
        checks = ["CLAIM_TEX_MATCH", "R86_R87_IDENTICAL_SOURCE", "CONDITION_TOKENS_PRESENT"]
        if locator == "Proposition 1.6":
            if "source lines 967-968 define all typed variables" not in source["inherited_constraints"]:
                raise AssertionError("shared variables missing")
            checks.append("SHARED_VARIABLE_TYPES_PRESERVED")
        if locator == "Proposition 2.5":
            eq = source["inherited_equality_conditions"]
            if not isinstance(eq, str) or not all(v in eq for v in ("j<3m-1", "2\\)-primary", "等号")):
                raise AssertionError("shared equality conditions missing")
            checks.append("BOTH_FORMULAS_INHERIT_EQUALITY_CASES")
        if locator == "Proposition 4.2":
            if "(4.4)" not in source["shared_scope_note"]:
                raise AssertionError("equation alias missing")
            checks.append("EQUATION_44_IS_ALIAS_NOT_NEW_REFERENCE")
        rows.append({
            "review_unit_id": unit_id,
            "reference_locator": locator,
            "source_lines": source["source_lines"],
            "component_position": source["component_position"],
            "subposition": source["subposition"],
            "description_jp": gate["mathematical_description_proposal_jp"],
            "required_scope_conditions_jp": gate["required_scope_conditions_jp"],
            "verified_source_checks": checks,
            "remaining_mathematical_review_jp": SCOPE_BLOCKERS[locator],
            "source_scope_token_verified": True,
            "mathematical_semantics_verified": False,
            "original_edition_verified": False,
            "semantic_registration_allowed": False,
            "proof_eligible": False,
        })
    if set(RULES) != {tail_key(x) for x in seen}:
        raise AssertionError("claim coverage incomplete")
    expected = {
        "Proposition 1.6": [(1, 1), (2, 1), (3, 1)],
        "Theorem 2.4": [(1, 1), (2, 1), (2, 2)],
        "Proposition 2.5": [(1, 1), (2, 1)],
        "Proposition 4.2": [(1, 1)],
    }
    if by_owner != expected:
        raise AssertionError("publication order or scope split changed")
    return {
        "phase": "163 R4-R88",
        "mode": "SOURCE_SCOPE_TOKENS_VERIFIED_NOT_MATHEMATICAL_CERTIFICATION",
        "review_unit_count": len(rows),
        "source_scope_token_verified_count": len(rows),
        "shared_equality_condition_count": 2,
        "original_edition_verified": False,
        "mathematical_semantics_verified_count": 0,
        "semantic_registration_allowed_count": 0,
        "production_registry_modified": False,
        "production_ids_allocated": False,
        "proof_search_connected": False,
        "full_suite_run": False,
        "records": rows,
    }


def write_outputs(result: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "scope_conditions.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Phase 163 R4-R88：原文と適用条件の照合", "", "9件の TeX 文字列・適用条件・掲載順を検査。数学的正しさの証明や原著照合ではない。", "", "| Reference | 順序 | 主張の内容 | 残る確認 |", "|---|---|---|---|"]
    for row in result["records"]:
        lines.append(f"| {row['reference_locator']} | {row['component_position']}.{row['subposition']} | {row['description_jp']} | {row['remaining_mathematical_review_jp']} |")
    lines += ["", "全9件について出典の条件トークンを確認したが、原著と数学的内容の認定は0件。", "固定文献命題への昇格・正式 ID 採番・証明探索接続は実施しない。"]
    (output / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--r86", required=True, type=Path)
    parser.add_argument("--r87", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = assess(load(args.r86), load(args.r87))
    write_outputs(result, args.output)
    print(json.dumps({k: v for k, v in result.items() if k != "records"}, ensure_ascii=False, indent=2))
    print("R88 source-scope checks complete. Full pytest not run.")


if __name__ == "__main__":
    main()
