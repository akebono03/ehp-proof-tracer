"""Phase 163 R4-R66: read-only editorial decisions for multi-assertion references.

No original-book verification, semantic approval, IDs, or registry changes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

# Editorial choices: one source Reference may contain several ordered Assertions.
# Review flags are deliberately conservative, not claims about mathematical truth.
REVIEW_FLAGS = {
    "pointed_homotopy_classes": ("TRAILING_SENTENCE_OUTSIDE_SPAN",),
    "composition_homotopy_classes": ("CONTEXT_FOR_COMPOSITION",),
    "secondary_composition": ("PRECEDING_CONSTRUCTION_REQUIRED",),
    "extension": ("ATTACHING_SPACE_CONTEXT_REQUIRED",),
    "coextension": ("ATTACHING_SPACE_CONTEXT_REQUIRED",),
    "stable_toda_bracket": ("DEFINITION_HYPOTHESES_AND_INDETERMINACY",),
    "nu4_generator_notation": ("PRIOR_CHOICES_ALPHA_STAR_U_S",),
    "nu_n_notation": ("ADJACENT_NOTATION_BLOCK",),
    "eta_n_cubed_notation": ("ADJACENT_NOTATION_BLOCK",),
    "stable_homotopy_group": ("SOURCE_ENDS_AT_DISPLAY",),
}

# Informational classification only. Do not infer proof status from these labels.
SPLIT_RULES = {
    "addition_inverse_suspension": "TWO_DEFINITIONS_IN_ONE_BLOCK",
    "stable_homotopy_group": "GROUP_AND_MAP_IN_ONE_BLOCK",
    "nu_n_notation": "UNSTABLE_AND_STABLE_SYMBOLS",
    "eta_n_cubed_notation": "UNSTABLE_AND_STABLE_SYMBOLS",
    "nu_n_squared_notation": "UNSTABLE_AND_STABLE_SYMBOLS",
}


def build_review(data: dict) -> dict:
    if data.get("phase") != "163 R4-R65" or data.get("mode") != "READ_ONLY_BOUNDARY_REVIEW_PACKET":
        raise ValueError("R65 review input required")
    if data.get("production_registry_modified") is not False or data.get("production_ids_allocated") is not False:
        raise ValueError("Input must be read-only")
    if data.get("mathematical_boundary_verified_count") != 0 or data.get("semantic_registration_allowed_count") != 0:
        raise ValueError("Unexpected semantic approval in input")
    records = data.get("records", [])
    if len(records) != 16 or len({r["editorial_key"] for r in records}) != 16:
        raise ValueError("Exactly 16 distinct references required")
    if not set(REVIEW_FLAGS).issubset({r["editorial_key"] for r in records}):
        raise ValueError("Expected review subjects missing")
    result = []
    for ref in records:
        key = ref["editorial_key"]
        assertions = ref["assertions"]
        if not assertions or ref.get("mathematical_verification") != "PENDING" or ref.get("decision") != "NEEDS_REVIEW":
            raise ValueError(f"Unreviewed input required: {key}")
        positions = [a["component_position_proposal"] for a in assertions]
        if positions != list(range(1, len(assertions) + 1)):
            raise ValueError(f"Invalid component order: {key}")
        if any(a["source_marker"] not in ref["source_span_text"] for a in assertions):
            raise ValueError(f"Missing evidence: {key}")
        if ref["start_line"] > ref["end_line"]:
            raise ValueError(f"Invalid source range: {key}")
        result.append({
            "editorial_key": key,
            "chapter": ref["chapter"],
            "source_file": ref["source_file"],
            "start_line": ref["start_line"],
            "end_line": ref["end_line"],
            "source_text_sha256": hashlib.sha256(ref["source_span_text"].encode("utf-8")).hexdigest(),
            "reference_policy": "ONE_REFERENCE_MULTIPLE_ASSERTIONS_ALLOWED",
            "reference_count_proposed": 1,
            "assertion_count_proposed": len(assertions),
            "split_rationale": SPLIT_RULES.get(key, "SINGLE_ASSERTION"),
            "assertions": [{
                "component_position_proposal": a["component_position_proposal"],
                "editorial_subject_unverified": a["editorial_subject_unverified"],
                "source_marker": a["source_marker"],
                "mathematical_verification": "NOT_VERIFIED",
            } for a in assertions],
            "review_flags": list(REVIEW_FLAGS.get(key, ())),
            "boundary_status": "REQUIRES_CONTEXT_OR_SPAN_REVIEW" if key in REVIEW_FLAGS else "LOCAL_EDITORIAL_PROPOSAL",
            "original_edition_verified": False,
            "mathematical_boundary_verified": False,
            "publication_position": None,
            "production_reference_id": None,
            "production_assertion_ids": [],
            "registration_action": "NONE",
        })
    result.sort(key=lambda x: (x["chapter"], x["source_file"], x["start_line"], x["editorial_key"]))
    if sum(x["assertion_count_proposed"] for x in result) != 21:
        raise ValueError("Expected 21 assertions")
    if sum(x["assertion_count_proposed"] > 1 for x in result) != 5:
        raise ValueError("Expected five multi-assertion references")
    return {
        "phase": "163 R4-R66",
        "mode": "READ_ONLY_MULTI_ASSERTION_BOUNDARY_DECISIONS",
        "reference_policy": "ONE_REFERENCE_MULTIPLE_ASSERTIONS_ALLOWED",
        "reference_proposal_count": 16,
        "assertion_proposal_count": 21,
        "multi_assertion_reference_count": 5,
        "context_or_span_review_count": sum(bool(r["review_flags"]) for r in result),
        "local_editorial_proposal_count": sum(not r["review_flags"] for r in result),
        "mathematical_boundary_verified_count": 0,
        "original_edition_verified": False,
        "semantic_registration_allowed_count": 0,
        "production_registry_modified": False,
        "production_ids_allocated": False,
        "proof_search_connected": False,
        "full_suite_run": False,
        "records": result,
    }


def write_reports(report: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "boundary_decisions.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Phase 163 R4-R66 登録単位の暫定判定", "",
             "**採用方針:** 文献上の Reference は原則1項目、複数の独立した定義があれば Assertion を個別に番号付けする。",
             "この判定は編集上の区分のみ。原本照合・数学的検証・正式登録・ID採番・証明探索への接続はしていない。", "",
             "|章|候補|Reference|Assertion|区分|要確認事項|", "|---:|---|---:|---:|---|---|"]
    for r in report["records"]:
        flags = ", ".join(r["review_flags"]) or "なし（原本照合は別途必要）"
        lines.append(f"|{r['chapter']}|`{r['editorial_key']}`|1|{r['assertion_count_proposed']}|{r['split_rationale']}|{flags}|")
    lines.extend(["", "## R4-R67 の対象", "",
                  "出典範囲の切れ目と前提条件の不足を優先して見直す。必要なら Reference の出典範囲のみ拡張する。",
                  "数学的な検証結果なしに `mathematical_boundary_verified` を真にしない。", "",
                  "## 限定テスト", "", "`python -m pytest -q phase163_r4_r66_multi_assertion_boundary/tests/test_phase163_r4_r66_multi_assertion_boundary.py`", "",
                  "全体 pytest は Phase 163 の最後に実施する。", ""])
    (output / "boundary_decisions.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--r65", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    report = build_review(json.loads(arguments.r65.read_text(encoding="utf-8")))
    write_reports(report, arguments.output)
    print(json.dumps({k: v for k, v in report.items() if k != "records"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
