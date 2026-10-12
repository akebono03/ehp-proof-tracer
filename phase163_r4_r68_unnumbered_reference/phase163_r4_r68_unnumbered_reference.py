"""Phase 163 R4-R68: read-only proposals for unnumbered literature references.

Keeps numbered/unnumbered literature references distinct from assertions.
No production identifiers, semantic approval, or registry mutation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXISTENCE_KEY = "extension_coextension_existence_conditions"
EXISTENCE_START = 1118
EXISTENCE_END = 1121
EXISTENCE_MARKERS = (r"\alpha\circ \beta=0", r"\beta\circ\gamma=0")


def load_inputs(decisions_path: Path, context_path: Path) -> tuple[dict, dict]:
    decisions = json.loads(decisions_path.read_text(encoding="utf-8"))
    context = json.loads(context_path.read_text(encoding="utf-8"))
    if decisions.get("phase") != "163 R4-R66" or decisions.get("reference_policy") != "ONE_REFERENCE_MULTIPLE_ASSERTIONS_ALLOWED":
        raise ValueError("R4-R66 multi-assertion decisions required")
    if context.get("phase") != "163 R4-R67" or context.get("reference_policy") != "ONE_REFERENCE_MULTIPLE_ASSERTIONS_ALLOWED":
        raise ValueError("R4-R67 source context required")
    for source in (decisions, context):
        if source.get("production_registry_modified") is not False or source.get("production_ids_allocated") is not False:
            raise ValueError("Read-only inputs required")
        if source.get("mathematical_boundary_verified_count") != 0 or source.get("semantic_registration_allowed_count") != 0:
            raise ValueError("Unverified source input required")
    return decisions, context


def build_proposals(decisions: dict, context: dict) -> dict:
    originals = decisions.get("records", [])
    if len(originals) != 16 or len({r["editorial_key"] for r in originals}) != 16:
        raise ValueError("Expected 16 distinct R66 references")
    if sum(len(r["assertions"]) for r in originals) != 21:
        raise ValueError("Expected 21 R66 assertions")
    contexts = {r["editorial_key"]: r for r in context.get("records", [])}
    if len(contexts) != 10 or "coextension" not in contexts:
        raise ValueError("Expected ten R67 context records including coextension")
    c = contexts["coextension"]
    if c.get("source_span_sha256_verified") is not True or c.get("source_file") != "Toda_01_corrected.tex":
        raise ValueError("Unverified coextension source")
    extracted = {line["line"]: line for line in c["surrounding_lines"] if EXISTENCE_START <= line["line"] <= EXISTENCE_END}
    if set(extracted) != set(range(EXISTENCE_START, EXISTENCE_END + 1)):
        raise ValueError("Missing existence-condition source lines")
    if any(extracted[number]["region"] != "AFTER" for number in extracted):
        raise ValueError("Existence conditions not separated from definitions")
    text = "\n".join(extracted[number]["text"] for number in range(EXISTENCE_START, EXISTENCE_END + 1))
    if not all(marker in text for marker in EXISTENCE_MARKERS):
        raise ValueError("Existence-condition text differs from reviewed TeX")
    if "必要十分条件" not in text:
        raise ValueError("Existence-condition equivalence missing")
    original_keys = {r["editorial_key"] for r in originals}
    if EXISTENCE_KEY in original_keys:
        raise ValueError("Existence reference already present")
    refs = []
    for r in originals:
        if r.get("registration_action") != "NONE" or r.get("production_reference_id") is not None:
            raise ValueError("An existing reference was registered")
        assertions = r["assertions"]
        if any(a.get("mathematical_verification") != "NOT_VERIFIED" for a in assertions):
            raise ValueError("Existing assertions unexpectedly verified")
        refs.append({
            "editorial_key": r["editorial_key"], "chapter": r["chapter"],
            "source_file": r["source_file"], "start_line": r["start_line"], "end_line": r["end_line"],
            "source_text_sha256": r["source_text_sha256"],
            "source_numbering_status": "NOT_ASSESSED", "reference_kind_proposal": "DEFINITION",
            "assertions": [{
                "component_position_proposal": a["component_position_proposal"],
                "editorial_subject_unverified": a["editorial_subject_unverified"],
                "assertion_kind_proposal": "DEFINITION",
                "source_marker": a["source_marker"],
                "mathematical_verification": "NOT_VERIFIED",
            } for a in assertions],
            "dependencies_review_required": bool(r["review_flags"]),
            "mathematical_boundary_verified": False,
            "publication_position": None, "production_reference_id": None,
            "production_assertion_ids": [], "registration_action": "NONE",
        })
    refs.append({
        "editorial_key": EXISTENCE_KEY, "chapter": 1,
        "source_file": c["source_file"], "start_line": EXISTENCE_START, "end_line": EXISTENCE_END,
        "source_text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "source_numbering_status": "UNNUMBERED_PROPOSAL", "reference_kind_proposal": "REMARK",
        "source_text": text,
        "assertions": [
            {"component_position_proposal": 1,
             "editorial_subject_unverified": "extension exists iff alpha circ beta equals zero",
             "assertion_kind_proposal": "STATEMENT", "source_marker": EXISTENCE_MARKERS[0],
             "mathematical_verification": "NOT_VERIFIED"},
            {"component_position_proposal": 2,
             "editorial_subject_unverified": "coextension exists iff beta circ gamma equals zero",
             "assertion_kind_proposal": "STATEMENT", "source_marker": EXISTENCE_MARKERS[1],
             "mathematical_verification": "NOT_VERIFIED"},
        ],
        "dependencies_review_required": True,
        "dependency_editorial_keys": ["extension", "coextension"],
        "mathematical_boundary_verified": False,
        "publication_position": None, "production_reference_id": None,
        "production_assertion_ids": [], "registration_action": "NONE",
    })
    refs.sort(key=lambda r: (r["chapter"], r["start_line"], r["editorial_key"]))
    assert_count = sum(len(r["assertions"]) for r in refs)
    if len(refs) != 17 or assert_count != 23:
        raise ValueError("Unexpected R68 proposal totals")
    return {
        "phase": "163 R4-R68",
        "mode": "READ_ONLY_UNNUMBERED_REFERENCE_POLICY_PROPOSAL",
        "reference_policy": "ONE_REFERENCE_MULTIPLE_ASSERTIONS_ALLOWED",
        "unnumbered_reference_policy": "INDEPENDENT_UNNUMBERED_REFERENCE_WITH_STATEMENT_ASSERTIONS",
        "reference_proposal_count": len(refs),
        "assertion_proposal_count": assert_count,
        "additional_unnumbered_reference_proposal_count": 1,
        "additional_statement_assertion_proposal_count": 2,
        "mathematical_boundary_verified_count": 0,
        "semantic_registration_allowed_count": 0,
        "original_edition_verified": False,
        "production_registry_modified": False,
        "production_ids_allocated": False,
        "proof_search_connected": False,
        "full_suite_run": False,
        "records": refs,
    }


def write_reports(result: dict, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    (out / "unnumbered_reference_proposals.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rows = ["# Phase 163 R4-R68：番号なし Reference と Assertion の分離", "",
            "定義と数学的性質は別 Assertion。独立した文献番号のない性質は、番号なし Reference 候補へ対応させる。",
            "編集上の案であり、原本確認、数学的承認、正式 ID、Registry 変更はしていない。", "",
            "|章|出典行|Reference 候補|番号の扱い|Assertion 数|種類|",
            "|---:|---|---|---|---:|---|"]
    for ref in result["records"]:
        kinds = ", ".join(a["assertion_kind_proposal"] for a in ref["assertions"])
        rows.append(f"|{ref['chapter']}|{ref['start_line']}–{ref['end_line']}|`{ref['editorial_key']}`|{ref['source_numbering_status']}|{len(ref['assertions'])}|{kinds}|")
    rows += ["", "## 追加した番号なし Reference 候補", "",
             "第1章 1118–1121行：extension が存在する必要十分条件 `alpha circ beta = 0`、",
             "coextension が存在する必要十分条件 `beta circ gamma = 0`。",
             "同一の無番号 Reference 候補に二つの STATEMENT Assertion を保持する。", "",
             "**未確定:** 原本掲載位置、独立番号の有無の最終照合、数学的意味と前提、既存登録との重複。", "",
             "全体 pytest は Phase 163 終了時のみ行う。", ""]
    (out / "unnumbered_reference_proposals.md").write_text("\n".join(rows), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--decisions", type=Path, required=True)
    parser.add_argument("--context", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = build_proposals(*load_inputs(args.decisions, args.context))
    write_reports(result, args.output)
    print(json.dumps({k: v for k, v in result.items() if k != "records"}, ensure_ascii=False, indent=2))
    print("R4-R68 read-only unnumbered reference proposals complete. Full pytest not run.")


if __name__ == "__main__":
    main()
