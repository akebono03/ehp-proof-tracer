"""R4-R54 read-only live registry content/provenance audit.

No new registry assertion is constructed, no ID assigned, and no inference of
mathematical equivalence from metadata or Python repr is permitted.
"""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def observe_bridge(result):
    from phase163_r4_registry_bridge import MigrationStatus
    from unified_statement_registry import AssertionKind, AssertionOrigin

    records = tuple(result.records)
    findings = []
    seen = set()
    for record in records:
        if record.assertion_id is None:
            findings.append({"source": record.source, "source_key": record.source_key,
                             "assertion_id": None, "reference_id": None,
                             "status": record.status.value, "origin": None,
                             "kind": None, "content_type": None,
                             "typed_fixed_content_comparable": False})
            continue
        if record.assertion_id in seen:
            raise ValueError("duplicate bridge assertion ID")
        seen.add(record.assertion_id)
        assertion = result.registry.assertion(record.assertion_id)
        ref = result.registry.reference(assertion.reference_id)
        if not ref.locator:
            raise ValueError("empty literature locator")
        typed_fixed = (record.status is MigrationStatus.STRUCTURED
                       and assertion.origin is AssertionOrigin.FIXED_STATEMENT
                       and assertion.kind is AssertionKind.DEFINITION)
        findings.append({"source": record.source, "source_key": record.source_key,
                         "assertion_id": assertion.assertion_id,
                         "reference_id": assertion.reference_id,
                         "locator": ref.locator, "status": record.status.value,
                         "origin": assertion.origin.value, "kind": assertion.kind.value,
                         "content_type": type(assertion.content).__module__ + "." + type(assertion.content).__qualname__,
                         "typed_fixed_content_comparable": typed_fixed})
    return findings


def audit(overlap, bridge_result, *, overlap_digest=None):
    if overlap.get("phase") != "163 R4-R53" or overlap.get("definition_candidate_count") != 19:
        raise ValueError("expected R4-R53 19-candidate input")
    if overlap.get("new_statement_confirmed_count") != 0 or overlap.get("registry_modified"):
        raise ValueError("input is not the read-only R4-R53 result")
    candidates = overlap["candidates"]
    if len(candidates) != 19 or len({x["r48_index"] for x in candidates}) != 19:
        raise ValueError("candidate integrity violation")
    findings = observe_bridge(bridge_result)
    counters = Counter(x["status"] for x in findings)
    comparable = [x for x in findings if x["typed_fixed_content_comparable"]]
    # An existing definition may be expressible in other Assertion types.
    # Do not conclude DISTINCT_CANDIDATE merely because no DEFINITION exists.
    rows = []
    for candidate in candidates:
        if candidate["new_statement_confirmed"] or candidate["registration_action"] != "NONE":
            raise ValueError("mutating candidate input")
        rows.append({"r48_index": candidate["r48_index"],
                     "chapter": candidate["chapter"], "source_line": candidate["source_line"],
                     "editorial_key": candidate["editorial_key"],
                     "matched_locator": candidate["matched_locator"],
                     "live_comparison_status": "UNRESOLVED_NO_COMPARABLE_FIXED_DEFINITION" if not comparable else "UNRESOLVED_TYPED_COMPARISON_REQUIRED",
                     "matched_live_assertion_id": None,
                     "mathematical_equivalence_verified": False,
                     "new_registration_confirmed": False})
    return {"phase": "163 R4-R54", "mode": "READ_ONLY_LIVE_BRIDGE_CONTENT_AUDIT",
            "r53_input_sha256": overlap_digest,
            "definition_candidate_count": len(rows),
            "live_bridge_record_count": len(findings),
            "live_bridge_status_counts": dict(sorted(counters.items())),
            "live_bridge_typed_fixed_definition_count": len(comparable),
            "live_bridge_unresolved_source_count": counters.get("unresolved_source", 0),
            "mathematical_equivalence_verified_count": 0,
            "semantic_overlap_unresolved_count": len(rows),
            "new_statement_confirmed_count": 0,
            "pending_other_candidates_count": overlap["pending_other_candidates_count"],
            "live_registry_bridge_constructed": True,
            "proof_repository_included": False,
            "metadata_only_not_treated_as_math": True,
            "registration_applied": False, "registry_modified": False,
            "ids_allocated": False, "proof_search_connected": False,
            "original_edition_verified": False,
            "bridge_assertions": findings, "candidates": rows}


def write_results(result, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "live_audit.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with (out / "comparison_queue.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(result["candidates"][0]))
        writer.writeheader()
        writer.writerows(result["candidates"])
    lines = ["# Phase 163 R4-R54 現行 Registry bridge 内容監査", "",
             f"- 定義候補：{result['definition_candidate_count']} 件",
             f"- 実行時 bridge 記録：{result['live_bridge_record_count']} 件",
             f"- MigrationStatus 内訳：{result['live_bridge_status_counts']}",
             f"- 比較可能な文献固定 Definition：{result['live_bridge_typed_fixed_definition_count']} 件",
             f"- 同値性未判定：{result['semantic_overlap_unresolved_count']} 件", "",
             "実際に bridge を構築したが、metadata_only は型付きの数学的内容ではない。",
             "locator 不明の theorem_fact は未解決のまま保持する。",
             "証明内部の結論を文献固定命題に流用しないため proof_repository は指定しない。",
             "数学的な重複なし／新規登録が必要と結論していない。", "",
             "本番 Registry・TeX・ID・証明探索は未変更。原本照合および全体 pytest は未実施。"]
    (out / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--overlap", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    from phase163_r4_registry_bridge import build_registry_bridge
    overlap = json.loads(Path(args.overlap).read_text(encoding="utf-8"))
    bridge = build_registry_bridge()  # existing fixed component + theorem facts only
    result = audit(overlap, bridge, overlap_digest=sha256(args.overlap))
    write_results(result, args.output)
    print(json.dumps({k: v for k, v in result.items() if k not in ("bridge_assertions", "candidates")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
