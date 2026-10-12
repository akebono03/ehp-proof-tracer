"""R4-R62: read-only inventory of the remaining definition candidates."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

ALREADY_REVIEWED = frozenset({"delta_homomorphism", "inverse_delta", "pi_i_n_subgroup"})


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def audit_remaining(crosswalk, overlap, gate):
    """Cross-check source identity only; do not infer mathematical meanings."""
    if crosswalk.get("phase") != "163 R4-R52" or overlap.get("phase") != "163 R4-R53":
        raise ValueError("incorrect upstream phase")
    if gate.get("phase") != "163 R4-R61" or gate.get("candidate_count") != 3:
        raise ValueError("incorrect registration gate")
    if crosswalk.get("catalog_snapshot_sha256") != overlap.get("catalog_snapshot_sha256"):
        raise ValueError("catalog snapshots disagree")
    if crosswalk.get("source_sha256") != overlap.get("source_sha256"):
        raise ValueError("source hashes disagree")
    ca = crosswalk["candidates"]
    oa = overlap["candidates"]
    if len(ca) != 19 or len(oa) != 19 or gate.get("gate_blocked_count") != 3:
        raise ValueError("unexpected source candidate cardinality")
    key = lambda x: (x["r48_index"], x["chapter"], x["source_line"], x["editorial_key"])
    overlap_by_key = {key(x): x for x in oa}
    if len(overlap_by_key) != 19 or len({key(x) for x in ca}) != 19:
        raise ValueError("duplicate candidate identity")
    reviewed_keys = {key(x) for x in ca if x["editorial_key"] in ALREADY_REVIEWED}
    if len(reviewed_keys) != 3:
        raise ValueError("reviewed candidate set changed")
    gate_locators = {x["locator"] for x in gate["records"]}
    if gate_locators != {"(2.9)", "(2.10)", "(4.3)"}:
        raise ValueError("prior reviewed records changed")
    result = []
    for c in ca:
        k = key(c)
        if k not in overlap_by_key:
            raise ValueError("candidate missing from overlap audit")
        o = overlap_by_key[k]
        if c["source_file"] != o["source_file"] or c["excerpt"] != o["excerpt"]:
            raise ValueError("source evidence mismatch")
        if k in reviewed_keys:
            continue
        if o["tex_catalog_containment_status"] != "NO_DIRECT_CATALOG_UNIT" or o["matched_source_unit_id"] is not None or o["matched_locator"] is not None:
            raise ValueError("remaining candidate unexpectedly has catalog anchor")
        if c.get("direct_definition_reference_id") is not None or c.get("direct_definition_assertion_id") is not None:
            raise ValueError("candidate acquired registered definition")
        if c.get("original_edition_verified") or o.get("original_edition_verified"):
            raise ValueError("unexpected edition verification")
        result.append({
            "r48_index":c["r48_index"], "chapter":c["chapter"],
            "source_file":c["source_file"], "source_line":c["source_line"],
            "editorial_key":c["editorial_key"], "source_excerpt":c["excerpt"],
            "source_context":c["context"],
            "candidate_role":c["role_decision"],
            "catalog_containment":o["tex_catalog_containment_status"],
            "matched_source_unit_id":None, "matched_locator":None,
            "publication_position":None, "defined_symbol_verified":None,
            "candidate_definition_label":c["editorial_key"],
            "review_status":"SOURCE_EXCERPT_PRESENT_NO_DIRECT_CATALOG_UNIT",
            "registration_status":"NEEDS_SOURCE_BOUNDARY_AND_SEMANTIC_REVIEW",
            "source_boundaries_verified":False,
            "mathematical_semantics_verified":False,
            "original_edition_verified":False,
            "production_reference_id":None, "production_assertion_id":None,
        })
    result.sort(key=lambda x:(x["chapter"],x["source_line"],x["r48_index"]))
    if len(result)!=16 or any(x["editorial_key"] in ALREADY_REVIEWED for x in result):
        raise ValueError("expected exactly 16 untouched candidates")
    return {
        "phase":"163 R4-R62", "mode":"READ_ONLY_REMAINING_DEFINITION_EVIDENCE_INVENTORY",
        "upstream_candidate_count":19,"previously_reviewed_count":3,
        "remaining_definition_candidate_count":len(result),
        "no_direct_catalog_unit_count":sum(x["matched_source_unit_id"] is None for x in result),
        "verified_publication_position_count":0,
        "verified_defined_symbol_count":0,
        "semantic_registration_approved_count":0,
        "original_edition_verified":False,
        "pending_other_candidates_count":gate["pending_other_candidates_count"],
        "production_registry_modified":False,"production_ids_allocated":False,
        "proof_search_connected":False,
        "source_catalog_sha256":crosswalk["catalog_snapshot_sha256"],
        "records":result,
    }


def write_reports(report, output):
    output=Path(output)
    output.mkdir(parents=True,exist_ok=True)
    (output/"remaining_definitions.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    fields=["r48_index","chapter","source_file","source_line","editorial_key","candidate_role","catalog_containment","matched_locator","publication_position","defined_symbol_verified","review_status","registration_status"]
    with (output/"remaining_definitions.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore");w.writeheader();w.writerows(report["records"])
    lines=["# Phase 163 R4-R62：未処理 Definition 候補16件の根拠棚卸し","","R4-R52/R53/R61 の既存証拠に基づく読み取り専用監査。","","|章|行|候補（暫定 editorial key）|判定|","|---:|---:|---|---|"]
    for r in report["records"]:
        lines.append(f'|{r["chapter"]}|{r["source_line"]}|`{r["editorial_key"]}`|番号付き catalog unit と未接続|')
    lines.extend(["","16件とも原文抜粋は存在するが、文献掲載順・確定した定義対象・正式な Assertion は未確定。","R4-R55〜R61 の監査済み3件は対象から除外。未処理のその他候補237件も維持。","原本照合、数学的意味の認定、本番登録、ID 発行、証明探索への接続は行わない。全体 pytest は実施しない。"])
    (output/"report.md").write_text("\n".join(lines)+"\n",encoding="utf-8")


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--crosswalk",required=True)
    p.add_argument("--overlap",required=True)
    p.add_argument("--gate",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    result=audit_remaining(load_json(a.crosswalk),load_json(a.overlap),load_json(a.gate))
    write_reports(result,a.output)
    print(json.dumps({k:v for k,v in result.items() if k!="records"},ensure_ascii=False,indent=2))
    print("R4-R62 read-only evidence inventory complete. Full pytest not run.")


if __name__ == "__main__":
    main()
