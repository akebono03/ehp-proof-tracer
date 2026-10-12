"""Phase 163 R4-R70: read-only batch queue for 237 pending TeX candidates.

Heuristic buckets are lexical hints, never mathematical classifications.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def lexical_bucket(excerpt: str) -> str:
    if any(token in excerpt for token in (":=", r"\coloneqq", r"\stackrel{\mathrm{def}}{=}")):
        return "DEFINITION_SYNTAX_REVIEW"
    if any(token in excerpt for token in (r"\longrightarrow", r"\rightarrow", r"\mapsto", r"\xrightarrow")):
        return "MAP_SYNTAX_REVIEW"
    if any(token in excerpt for token in ("=", r"\cong", r"\subset", r"\in", r"\leq", r"\geq")):
        return "RELATION_SYNTAX_REVIEW"
    return "OTHER_DISPLAY_REVIEW"


def audit_pending(r51: dict, r69: dict) -> dict:
    if r51.get("phase") != "163 R4-R51" or r69.get("phase") != "163 R4-R69":
        raise ValueError("Unexpected upstream phase")
    if r51.get("original_candidate_count") != 316 or len(r51.get("review_queue", [])) != 316:
        raise ValueError("R51 candidate inventory changed")
    if r51.get("pending_mathematical_review_count") != 237:
        raise ValueError("R51 pending count changed")
    if r69.get("reference_candidate_count") != 17 or r69.get("assertion_candidate_count") != 23:
        raise ValueError("R69 reference inventory changed")
    for d in (r51, r69):
        if d.get("proof_search_connected") is not False:
            raise ValueError("An upstream input claims proof-search mutation")
    if r51.get("registration_applied") is not False or r51.get("ids_allocated") is not False:
        raise ValueError("R51 input is not read-only")
    if r69.get("production_registry_modified") is not False or r69.get("production_ids_allocated") is not False:
        raise ValueError("R69 input is not read-only")
    references = r69.get("records", [])
    if len(references) != 17 or len({r["editorial_key"] for r in references}) != 17:
        raise ValueError("R69 records missing or duplicated")
    for ref in references:
        if not 1 <= ref["start_line"] <= ref["end_line"] or ref["publication_position"] is not None:
            raise ValueError("R69 range or verified publication position changed")
    queue = r51["review_queue"]
    identifiers = [r["r48_index"] for r in queue]
    if sorted(identifiers) != list(range(1, 317)):
        raise ValueError("R51 row identity duplicated or missing")
    pending = [r for r in queue if r.get("role_decision") == "PENDING_MATHEMATICAL_REVIEW"]
    if len(pending) != 237:
        raise ValueError("R51 pending-role cardinality differs")
    output = []
    for item in pending:
        if item.get("review_level") != "PENDING" or item.get("registration_decision") != "NOT_APPLIED":
            raise ValueError("A pending item was already classified or registered")
        chapter = item["chapter"]
        line = item["source_line"]
        excerpt = item["excerpt"]
        if not 1 <= chapter <= 5 or not isinstance(line, int) or line < 1 or not excerpt.strip():
            raise ValueError("Invalid pending candidate source locator")
        if item.get("original_edition_verified") is not False:
            raise ValueError("Unexpected original-edition verification")
        same_chapter = [r for r in references if r["chapter"] == chapter]
        overlapping = sorted(r["editorial_key"] for r in same_chapter if r["start_line"] <= line <= r["end_line"])
        nearby = sorted(r["editorial_key"] for r in same_chapter if
                        line < r["start_line"] and r["start_line"] - line <= 5 or
                        line > r["end_line"] and line - r["end_line"] <= 5)
        bucket = lexical_bucket(excerpt)
        output.append({
            "r48_index": item["r48_index"],
            "chapter": chapter,
            "source_file": item["source_anchor"]["file"],
            "source_line": line,
            "review_group_id": item.get("review_group_id"),
            "original_triage_status": item["triage_status"],
            "lexical_bucket": bucket,
            "excerpt_sha256": hashlib.sha256(excerpt.encode("utf-8")).hexdigest(),
            "excerpt": excerpt,
            "context": item["context"],
            "overlapping_r69_keys": overlapping,
            "nearby_r69_keys_within_five_lines": nearby,
            "candidate_identity_decision": "NOT_ASSESSED",
            "mathematical_role_verified": False,
            "production_reference_id": None,
            "production_assertion_ids": [],
            "registration_action": "NONE",
        })
    output.sort(key=lambda r: (r["chapter"], r["source_line"], r["r48_index"]))
    role_counts = dict(sorted(Counter(r["lexical_bucket"] for r in output).items()))
    chapter_counts = {str(i): sum(r["chapter"] == i for r in output) for i in range(1, 6)}
    return {
        "phase": "163 R4-R70",
        "mode": "READ_ONLY_237_CANDIDATE_BATCH_TRIAGE",
        "input_r51_source_sha256": r51["source_sha256"],
        "pending_candidate_count": len(output),
        "comparison_reference_count": len(references),
        "lexical_bucket_counts": role_counts,
        "chapter_counts": chapter_counts,
        "overlap_candidate_count": sum(bool(r["overlapping_r69_keys"]) for r in output),
        "nearby_candidate_count": sum(bool(r["nearby_r69_keys_within_five_lines"]) for r in output),
        "mathematical_role_verified_count": 0,
        "semantic_duplicate_verified_count": 0,
        "publication_position_verified_count": 0,
        "production_registry_modified": False,
        "production_ids_allocated": False,
        "proof_search_connected": False,
        "full_suite_run": False,
        "records": output,
    }


def write_reports(report: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "pending_batch_audit.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    columns = ["r48_index", "chapter", "source_file", "source_line", "lexical_bucket",
               "original_triage_status", "overlapping_r69_keys", "nearby_r69_keys_within_five_lines",
               "excerpt_sha256", "excerpt", "candidate_identity_decision"]
    with (output / "pending_batch_audit.csv").open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for row in report["records"]:
            writer.writerow({**row, "overlapping_r69_keys": ";".join(row["overlapping_r69_keys"]),
                             "nearby_r69_keys_within_five_lines": ";".join(row["nearby_r69_keys_within_five_lines"])})
    lines = ["# Phase 163 R4-R70：未判定237候補の一括整理", "",
             "R51 の未判定候補だけを抽出。字句分類は Definition / Proposition / ProofStep 等の数学的判定ではない。", "",
             "|分類|件数|", "|---|---:|"]
    lines.extend(f"|{k}|{v}|" for k, v in report["lexical_bucket_counts"].items())
    lines.extend(["", "|章|件数|", "|---:|---:|"])
    lines.extend(f"|{k}|{v}|" for k, v in report["chapter_counts"].items())
    lines.extend(["", f"R69 範囲内のアンカー: {report['overlap_candidate_count']}件",
                  f"R69 から5行以内のアンカー: {report['nearby_candidate_count']}件", "",
                  "## 全237候補", "", "|R48 index|章|行|字句分類|R69との近接|", "|---:|---:|---:|---|---|"])
    for r in report["records"]:
        labels = r["overlapping_r69_keys"] + r["nearby_r69_keys_within_five_lines"]
        lines.append(f"|{r['r48_index']}|{r['chapter']}|{r['source_line']}|{r['lexical_bucket']}|{', '.join(labels) or '—'}|")
    lines.extend(["", "原本照合・数学的同一性・文献掲載順位・正式 ID・登録・証明探索への接続は行わない。",
                  "全体 pytest は Phase 163 の最後に実施する。", ""])
    (output / "report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Read-only R4-R70 batch audit")
    parser.add_argument("--r51", required=True, type=Path)
    parser.add_argument("--r69", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    report = audit_pending(load_json(args.r51), load_json(args.r69))
    write_reports(report, args.output)
    print(json.dumps({k: v for k, v in report.items() if k != "records"}, ensure_ascii=False, indent=2))
    print("R4-R70 read-only 237-candidate batch audit complete. Full pytest not run.")


if __name__ == "__main__":
    main()
