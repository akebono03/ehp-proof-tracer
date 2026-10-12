"""Phase 163 R4-R65: read-only review packets for 16 definition boundaries."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def review_packets(proposals: dict, boundaries: dict) -> dict:
    if proposals.get("phase") != "163 R4-R64" or boundaries.get("phase") != "163 R4-R63":
        raise ValueError("Expected R64 proposals and R63 boundaries")
    if proposals.get("production_registry_modified") is not False or boundaries.get("production_registry_modified") is not False:
        raise ValueError("Read-only provenance required")
    refs = proposals.get("records", [])
    sources = boundaries.get("records", [])
    if len(refs) != 16 or len(sources) != 16:
        raise ValueError("Expected 16 candidate records")
    source_map = {item["editorial_key"]: item for item in sources}
    if len(source_map) != 16 or {r["editorial_key"] for r in refs} != set(source_map):
        raise ValueError("Source and proposal keys must match uniquely")
    result = []
    for ref in refs:
        key = ref["editorial_key"]
        src = source_map[key]
        excerpt = src["source_span_text"]
        digest = hashlib.sha256(excerpt.encode("utf-8")).hexdigest()
        if digest != ref["source_text_sha256"] or ref["source_file_sha256"] != src["source_file_sha256"]:
            raise ValueError(f"Source evidence checksum mismatch: {key}")
        if src["proposed_start_line"] != ref["start_line"] or src["proposed_end_line"] != ref["end_line"]:
            raise ValueError(f"Source span mismatch: {key}")
        if ref["production_reference_id"] is not None or ref["registration_action"] != "NONE":
            raise ValueError(f"Production registration forbidden: {key}")
        if any(a["production_assertion_id"] is not None or a["semantic_verification"] != "NOT_VERIFIED" for a in ref["assertions"]):
            raise ValueError(f"Unexpected semantic approval: {key}")
        if any(a["source_marker"] not in excerpt for a in ref["assertions"]):
            raise ValueError(f"Assertion marker outside evidence: {key}")
        context = ref["external_context_review_required"]
        adjacent = ref["adjacent_notation_review_required"]
        if context and adjacent:
            category = "CONTEXT_AND_ADJACENCY_REVIEW"
        elif context:
            category = "CONTEXT_REVIEW"
        elif adjacent:
            category = "ADJACENT_NOTATION_REVIEW"
        else:
            category = "SOURCE_LOCAL_REVIEW"
        result.append({
            "editorial_key": key,
            "chapter": ref["chapter"],
            "source_file": ref["source_file"],
            "start_line": ref["start_line"],
            "end_line": ref["end_line"],
            "review_category": category,
            "source_span_text": excerpt,
            "assertions": [{"component_position_proposal": a["component_position_proposal"],
                            "editorial_subject_unverified": a["editorial_subject_unverified"],
                            "source_marker": a["source_marker"]} for a in ref["assertions"]],
            "mathematical_verification": "PENDING",
            "original_edition_verification": "PENDING",
            "decision": "NEEDS_REVIEW",
        })
    result.sort(key=lambda x: (x["chapter"], x["start_line"], x["editorial_key"]))
    if sum(len(x["assertions"]) for x in result) != 21:
        raise ValueError("Expected 21 assertion proposals")
    categories = {kind: sum(r["review_category"] == kind for r in result) for kind in
                  ("SOURCE_LOCAL_REVIEW", "CONTEXT_REVIEW", "ADJACENT_NOTATION_REVIEW", "CONTEXT_AND_ADJACENCY_REVIEW")}
    if categories != {"SOURCE_LOCAL_REVIEW": 9, "CONTEXT_REVIEW": 5, "ADJACENT_NOTATION_REVIEW": 2, "CONTEXT_AND_ADJACENCY_REVIEW": 0}:
        raise ValueError("Unexpected review classification")
    return {"phase": "163 R4-R65", "mode": "READ_ONLY_BOUNDARY_REVIEW_PACKET",
            "candidate_count": 16, "assertion_proposal_count": 21,
            "category_counts": categories, "mathematical_boundary_verified_count": 0,
            "semantic_registration_allowed_count": 0, "production_registry_modified": False,
            "production_ids_allocated": False, "full_suite_run": False, "records": result}


def write_reports(data: dict, folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "review_packets.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Phase 163 R4-R65 境界確認パケット", "",
             "暫定的な原文抜粋です。数学的確認・原本照合・正式登録は実施していません。", "",
             "分類: 通常9件／外部文脈5件／隣接記法2件。", ""]
    labels = (("CONTEXT_REVIEW", "外部文脈の確認が必要"),
              ("ADJACENT_NOTATION_REVIEW", "隣接する記法との境界確認が必要"),
              ("SOURCE_LOCAL_REVIEW", "原文の当該範囲内で確認可能な候補"))
    for category, label in labels:
        lines.extend(["## " + label, ""])
        for item in data["records"]:
            if item["review_category"] != category:
                continue
            lines.extend([f"### {item['editorial_key']}（第{item['chapter']}章、{item['source_file']}:{item['start_line']}–{item['end_line']}）", "",
                          "Assertion 候補: " + ", ".join(x["editorial_subject_unverified"] for x in item["assertions"]), "",
                          "```tex", item["source_span_text"], "```", "",
                          "判定: 未確認。確認事項: Reference の境界と Assertion 分割が数学的に妥当か。", ""])
    lines.extend(["正式 ID、証明探索との接続は次段階以降。", "全体 pytest は Phase 終了時のみ実施。", ""])
    (folder / "review_packets.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--r64", required=True, type=Path)
    parser.add_argument("--r63", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    data = review_packets(json.loads(args.r64.read_text(encoding="utf-8")),
                          json.loads(args.r63.read_text(encoding="utf-8")))
    write_reports(data, args.output)
    print(json.dumps({k: v for k, v in data.items() if k != "records"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
