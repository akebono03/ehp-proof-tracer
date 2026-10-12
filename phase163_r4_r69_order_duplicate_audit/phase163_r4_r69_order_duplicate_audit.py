"""Phase 163 R4-R69: read-only ordering and candidate duplicate audit.

Order is only among the supplied candidates, not verified publication position.
No statements, IDs or mathematical equivalences are approved by this module.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

EXPECTED_UNNUMBERED = "extension_coextension_existence_conditions"


def load_proposals(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("phase") != "163 R4-R68":
        raise ValueError("Expected Phase 163 R4-R68 input")
    if data.get("reference_policy") != "ONE_REFERENCE_MULTIPLE_ASSERTIONS_ALLOWED":
        raise ValueError("Reference / Assertion policy mismatch")
    if data.get("unnumbered_reference_policy") != "INDEPENDENT_UNNUMBERED_REFERENCE_WITH_STATEMENT_ASSERTIONS":
        raise ValueError("Unnumbered reference policy mismatch")
    if any(data.get(flag) is not False for flag in (
        "production_registry_modified", "production_ids_allocated", "proof_search_connected"
    )):
        raise ValueError("Input claims production mutations")
    if data.get("semantic_registration_allowed_count") != 0:
        raise ValueError("Input claims semantic approval")
    if data.get("reference_proposal_count") != 17 or data.get("assertion_proposal_count") != 23:
        raise ValueError("Unexpected R68 candidate totals")
    if not isinstance(data.get("records"), list) or len(data["records"]) != 17:
        raise ValueError("Expected exactly 17 reference records")
    return data


def audit_candidates(data: dict) -> dict:
    source = data["records"]
    keys = [item["editorial_key"] for item in source]
    if len(set(keys)) != len(keys):
        raise ValueError("Duplicate editorial keys")
    if keys.count(EXPECTED_UNNUMBERED) != 1:
        raise ValueError("Missing unnumbered existence reference")
    for item in source:
        if item.get("registration_action") != "NONE" or item.get("production_reference_id") is not None:
            raise ValueError("Candidate was promoted")
        if item.get("production_assertion_ids") != [] or item.get("mathematical_boundary_verified") is not False:
            raise ValueError("Candidate assertions were promoted or verified")
        if item.get("publication_position") is not None:
            raise ValueError("Unverified publication position unexpectedly assigned")
        if not isinstance(item.get("chapter"), int) or item["chapter"] < 1:
            raise ValueError("Invalid chapter")
        if not isinstance(item.get("start_line"), int) or not isinstance(item.get("end_line"), int):
            raise ValueError("Invalid source lines")
        if not 0 < item["start_line"] <= item["end_line"]:
            raise ValueError("Invalid source range")
        if not isinstance(item.get("source_file"), str) or not item["source_file"]:
            raise ValueError("Missing source file")
        if not isinstance(item.get("source_text_sha256"), str) or len(item["source_text_sha256"]) != 64:
            raise ValueError("Missing source digest")
        assertions = item.get("assertions")
        if not isinstance(assertions, list) or not assertions:
            raise ValueError("Missing assertions")
        if [a.get("component_position_proposal") for a in assertions] != list(range(1, len(assertions) + 1)):
            raise ValueError("Noncontiguous component order")
        for a in assertions:
            if a.get("assertion_kind_proposal") not in ("STATEMENT", "DEFINITION"):
                raise ValueError("Invalid assertion kind")
            if a.get("mathematical_verification") != "NOT_VERIFIED":
                raise ValueError("Unverified assertion was promoted")
    numbered = next(r for r in source if r["editorial_key"] == EXPECTED_UNNUMBERED)
    if (numbered.get("source_numbering_status") != "UNNUMBERED_PROPOSAL" or
        numbered.get("reference_kind_proposal") != "REMARK" or
        [a["assertion_kind_proposal"] for a in numbered["assertions"]] != ["STATEMENT", "STATEMENT"] or
        numbered.get("dependency_editorial_keys") != ["extension", "coextension"]):
        raise ValueError("Unnumbered existence candidate policy changed")
    if hashlib.sha256(numbered["source_text"].encode("utf-8")).hexdigest() != numbered["source_text_sha256"]:
        raise ValueError("Unnumbered source text checksum mismatch")

    sorted_records = sorted(source, key=lambda r: (r["chapter"], r["start_line"], r["end_line"], r["editorial_key"]))
    exact_groups = defaultdict(list)
    digest_groups = defaultdict(list)
    line_groups = defaultdict(list)
    for r in sorted_records:
        exact_groups[(r["chapter"], r["source_file"], r["start_line"], r["end_line"])].append(r["editorial_key"])
        digest_groups[(r["source_file"], r["source_text_sha256"])].append(r["editorial_key"])
        for a in r["assertions"]:
            line_groups[(r["editorial_key"], a["component_position_proposal"])].append(a["source_marker"])

    collisions = [dict(kind="IDENTICAL_SOURCE_RANGE", keys=v) for v in exact_groups.values() if len(v)>1]
    collisions.extend(dict(kind="IDENTICAL_SOURCE_TEXT_DIGEST", keys=v) for v in digest_groups.values() if len(v)>1)
    overlaps = []
    adjacent = []
    for index, a in enumerate(sorted_records):
        for b in sorted_records[index+1:]:
            if (a["chapter"], a["source_file"]) != (b["chapter"], b["source_file"]):
                continue
            if a["start_line"] <= b["end_line"] and b["start_line"] <= a["end_line"]:
                overlaps.append({"left":a["editorial_key"],"right":b["editorial_key"]})
            elif a["end_line"] + 1 == b["start_line"]:
                adjacent.append({"left":a["editorial_key"],"right":b["editorial_key"]})

    output = []
    for index, r in enumerate(sorted_records, start=1):
        flags=[]
        if any(r["editorial_key"] in hit["keys"] for hit in collisions):
            flags.append("EXACT_DUPLICATE_CANDIDATE")
        if any(r["editorial_key"] in (pair["left"],pair["right"]) for pair in overlaps):
            flags.append("OVERLAPPING_SPANS_REQUIRE_REVIEW")
        if r.get("source_numbering_status") == "NOT_ASSESSED":
            flags.append("SOURCE_NUMBERING_UNVERIFIED")
        if r["editorial_key"] == EXPECTED_UNNUMBERED:
            flags.append("UNNUMBERED_REFERENCE_PROPOSAL")
        output.append({
            "editorial_key": r["editorial_key"],
            "chapter": r["chapter"],
            "source_file": r["source_file"],
            "start_line": r["start_line"],
            "end_line": r["end_line"],
            "candidate_order": index,
            "publication_position": None,
            "publication_position_verified": False,
            "source_numbering_status": r["source_numbering_status"],
            "assertion_count": len(r["assertions"]),
            "component_positions": [a["component_position_proposal"] for a in r["assertions"]],
            "review_flags": flags,
            "registration_action": "NONE",
        })
    return {
        "phase":"163 R4-R69",
        "mode":"READ_ONLY_ORDER_DUPLICATE_AUDIT",
        "reference_candidate_count":len(output),
        "assertion_candidate_count":sum(r["assertion_count"] for r in output),
        "unnumbered_reference_candidate_count":sum(r["source_numbering_status"]=="UNNUMBERED_PROPOSAL" for r in output),
        "exact_duplicate_evidence_count":len(collisions),
        "overlapping_source_span_pair_count":len(overlaps),
        "adjacent_source_span_pair_count":len(adjacent),
        "candidate_order_assigned_count":len(output),
        "publication_position_verified_count":0,
        "semantic_duplicate_verified_count":0,
        "mathematical_boundary_verified_count":0,
        "pending_other_candidates_count":237,
        "production_registry_modified":False,
        "production_ids_allocated":False,
        "proof_search_connected":False,
        "full_suite_run":False,
        "records":output,"exact_duplicate_evidence":collisions,
        "overlapping_source_spans":overlaps,"adjacent_source_spans":adjacent,
    }


def write_reports(result: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "order_duplicate_audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (output_dir / "order_duplicate_audit.csv").open("w", encoding="utf-8-sig", newline="") as fp:
        fields=["candidate_order","chapter","source_file","start_line","end_line","editorial_key","assertion_count","source_numbering_status","publication_position_verified","review_flags"]
        writer=csv.DictWriter(fp,fieldnames=fields,extrasaction="ignore")
        writer.writeheader()
        for record in result["records"]:
            writer.writerow({**record,"review_flags":";".join(record["review_flags"])})
    lines=["# Phase 163 R4-R69：掲載順・重複候補の限定監査","",
           "掲載順は入力17候補内の暫定順位のみ。文献全体の掲載位置や数学的同一性の証明ではない。","",
           "|暫定順|章|出典行|候補|Assertion|注意|","|---:|---:|---|---|---:|---|"]
    for r in result["records"]:
        flags=", ".join(r["review_flags"]) or "—"
        lines.append(f'|{r["candidate_order"]}|{r["chapter"]}|{r["start_line"]}–{r["end_line"]}|`{r["editorial_key"]}`|{r["assertion_count"]}|{flags}|')
    lines += ["",f'厳密な出典重複証拠: {result["exact_duplicate_evidence_count"]}件',
              f'範囲重複: {result["overlapping_source_span_pair_count"]}組',
              f'隣接: {result["adjacent_source_span_pair_count"]}組（重複とは判定しない）',
              "", "未使用候補237件との照合は未実施。掲載順の正式採番、数学的同一性判定、正式登録は未実施。", "全体 pytest は未実施。", ""]
    (output_dir / "report.md").write_text("\n".join(lines),encoding="utf-8")


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--source",required=True,type=Path)
    parser.add_argument("--output",required=True,type=Path)
    args=parser.parse_args()
    result=audit_candidates(load_proposals(args.source))
    write_reports(result,args.output)
    print(json.dumps({k:v for k,v in result.items() if k not in ("records","exact_duplicate_evidence","overlapping_source_spans","adjacent_source_spans")},ensure_ascii=False,indent=2))
    print("Phase 163 R4-R69 read-only ordering audit complete. Full pytest not run.")


if __name__ == "__main__":
    main()
