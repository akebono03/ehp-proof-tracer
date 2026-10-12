"""Phase 163 R4-R71: context-cue review queue, read only.

Cues indicate review priority, never mathematical role or registration approval.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

EXPECTED_BUCKETS = {
    "DEFINITION_SYNTAX_REVIEW": 7,
    "MAP_SYNTAX_REVIEW": 49,
    "OTHER_DISPLAY_REVIEW": 22,
    "RELATION_SYNTAX_REVIEW": 159,
}


def load_input(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def context_cues(context: str) -> tuple[str, ...]:
    """Extract textual cues without treating them as semantic classifications."""
    found: list[str] = []
    if re.search(r"\\textbf\{Proof\.|\\qed|証明|\\begin\{proof\}", context, re.I):
        found.append("PROOF_MARKER_IN_WINDOW")
    if re.search(r"定義する|定める|と置く|と書く|と呼ぶ|で表す", context):
        found.append("DEFINITION_WORD_IN_WINDOW")
    if re.search(r"成り立つ|従う|得られる|示される|同型である|準同型である|必要十分条件", context):
        found.append("ASSERTION_WORD_IN_WINDOW")
    if re.search(r"(?:Prop|Lem|Th|Cor)(?:\.?\s*\\ref|\.?\s*\d)|\\ref\{", context, re.I):
        found.append("CITATION_IN_WINDOW")
    return tuple(found)


def audit_queue(source: dict) -> dict:
    if source.get("phase") != "163 R4-R70" or source.get("mode") != "READ_ONLY_237_CANDIDATE_BATCH_TRIAGE":
        raise ValueError("R70 audit required")
    rows = source.get("records")
    if not isinstance(rows, list) or len(rows) != 237 or source.get("pending_candidate_count") != 237:
        raise ValueError("237 source records required")
    if source.get("lexical_bucket_counts") != EXPECTED_BUCKETS:
        raise ValueError("unexpected lexical buckets")
    if any(source.get(k) is not False for k in ("production_registry_modified", "production_ids_allocated", "proof_search_connected", "full_suite_run")):
        raise ValueError("upstream safety assertion failed")
    seen: set[int] = set()
    result: list[dict] = []
    for r in rows:
        idx = r["r48_index"]
        if not isinstance(idx, int) or idx in seen:
            raise ValueError("duplicate or invalid R48 identity")
        seen.add(idx)
        snippet = r["excerpt"]
        digest = hashlib.sha256(snippet.encode("utf-8")).hexdigest()
        if digest != r["excerpt_sha256"]:
            raise ValueError(f"excerpt hash mismatch at {idx}")
        overlap = r["overlapping_r69_keys"]
        nearby = r["nearby_r69_keys_within_five_lines"]
        if not isinstance(overlap, list) or not isinstance(nearby, list):
            raise ValueError("overlap arrays required")
        cues = context_cues(r["context"])
        if overlap:
            tier = "T0_EXISTING_REFERENCE_SPAN"
        elif nearby:
            tier = "T1_ADJACENT_REFERENCE"
        elif r["lexical_bucket"] == "DEFINITION_SYNTAX_REVIEW":
            tier = "T2_DEFINITION_NOTATION"
        elif "DEFINITION_WORD_IN_WINDOW" in cues or "ASSERTION_WORD_IN_WINDOW" in cues:
            tier = "T3_PROSE_CUE"
        else:
            tier = "T4_NO_PROSE_CUE"
        result.append({
            "r48_index": idx,
            "chapter": r["chapter"],
            "source_file": r["source_file"],
            "source_line": r["source_line"],
            "lexical_bucket": r["lexical_bucket"],
            "review_tier": tier,
            "textual_cues": list(cues),
            "overlapping_r69_keys": overlap,
            "nearby_r69_keys_within_five_lines": nearby,
            "excerpt_sha256": digest,
            "excerpt": snippet,
            "context": r["context"],
            "review_decision": "NEEDS_MATHEMATICAL_REVIEW",
            "mathematical_role_verified": False,
            "semantic_duplicate_verified": False,
            "production_reference_id": None,
            "registration_action": "NONE",
        })
    result.sort(key=lambda x: (int(x["review_tier"][1]), x["chapter"], x["source_line"], x["r48_index"]))
    counts = dict(sorted(Counter(x["review_tier"] for x in result).items()))
    assert sum(counts.values()) == 237
    return {
        "phase": "163 R4-R71",
        "mode": "READ_ONLY_CONTEXT_CUE_REVIEW_QUEUE",
        "source_phase": "163 R4-R70",
        "pending_candidate_count": len(result),
        "review_tier_counts": counts,
        "overlap_review_count": sum(bool(x["overlapping_r69_keys"]) for x in result),
        "nearby_review_count": sum(bool(x["nearby_r69_keys_within_five_lines"]) for x in result),
        "mathematical_role_verified_count": 0,
        "registration_allowed_count": 0,
        "production_registry_modified": False,
        "production_ids_allocated": False,
        "proof_search_connected": False,
        "full_suite_run": False,
        "records": result,
    }


def write_reports(report: dict, folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "semantic_review_queue.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fields = ["r48_index", "chapter", "source_file", "source_line", "lexical_bucket", "review_tier", "textual_cues", "overlapping_r69_keys", "nearby_r69_keys_within_five_lines", "excerpt", "context", "review_decision"]
    with (folder / "semantic_review_queue.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for record in report["records"]:
            row = dict(record)
            for key in ("textual_cues", "overlapping_r69_keys", "nearby_r69_keys_within_five_lines"):
                row[key] = "; ".join(row[key])
            writer.writerow(row)
    lines = ["# Phase 163 R4-R71：237候補の文脈付き一括確認", "", "字句・周辺文章の手掛かりで確認順を並べた資料。数学的な分類・登録承認ではない。", "", "|確認区分|件数|", "|---|---:|"]
    for k, v in report["review_tier_counts"].items():
        lines.append(f"|{k}|{v}|")
    lines += ["", "## 優先確認一覧", "", "|順序|第|行|R48 ID|対象|", "|---:|---:|---:|---:|---|"]
    for position, r in enumerate(report["records"], 1):
        lines.append(f'|{position}|{r["chapter"]}|{r["source_line"]}|{r["r48_index"]}|{r["review_tier"]}|')
    lines += ["", "T0 は既存候補に含まれる箇所で、独立 Reference の追加は保留する。", "文献掲載順・原本照合・意味的同一性・正式 ID・証明接続は未確認。", "全体 pytest は実施しない。"]
    (folder / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = audit_queue(load_input(args.input))
    write_reports(report, args.output)
    print(json.dumps({key: value for key, value in report.items() if key != "records"}, ensure_ascii=False, indent=2))
    print("R71 read-only queue generated. Full pytest not run.")


if __name__ == "__main__":
    main()
