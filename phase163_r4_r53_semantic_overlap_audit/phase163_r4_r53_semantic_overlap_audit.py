"""Phase 163 R4-R53: evidence-limited, read-only overlap/containment audit."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

SOURCE_NAMES = {
    1: "Toda_01_corrected.tex",
    2: "Toda_02_2(2).tex",
    3: "Toda_03_2(2).tex",
    4: "Toda_04_2(2).tex",
    5: "Toda_05_2(6).tex",
}


def catalog_digest(catalog: dict) -> str:
    return hashlib.sha256(json.dumps(catalog, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def _unit_span(item: dict, source_lines: list[str]) -> tuple[int, int]:
    start = item["source_line"]
    match = re.match(r"\\begin\{([^}]+)\}", source_lines[start - 1].strip())
    if not match:
        raise ValueError(f"Catalog start not found: {item['source_unit_id']}")
    closing = "\\end{" + match.group(1) + "}"
    for index in range(start, len(source_lines) + 1):
        if closing in source_lines[index - 1]:
            return start, index
    raise ValueError(f"Catalog end not found: {item['source_unit_id']}")


def _same_text_unit(candidate: dict, item: dict, source_lines: list[str]) -> bool:
    """Confirm that an anchor belongs to a catalog unit, including introductory prose.

    A preceding sentence is associated only if directly adjacent to the unit and
    its end introduces it (e.g. '次で定義する'). This is not mathematical equivalence.
    """
    if candidate["chapter"] != item["chapter"]:
        return False
    line = candidate["source_line"]
    start, end = _unit_span(item, source_lines)
    if start <= line <= end:
        return True
    if not (0 < start - line <= 2):
        return False
    between = source_lines[line - 1:start - 1]
    if not between or not any(token in "".join(between) for token in ("次で定義", "次のように定義", "以下で定義")):
        return False
    if any(value.strip() for value in source_lines[line:start - 1]):
        return False
    return True


def audit(crosswalk: dict, catalog: dict, inputs: Path) -> dict:
    if crosswalk.get("phase") != "163 R4-R52" or crosswalk.get("mode") != "READ_ONLY_DEFINITION_CROSSWALK":
        raise ValueError("R4-R52 crosswalk required")
    if catalog.get("phase") != "163 R4-R47" or len(catalog.get("items", [])) != 108:
        raise ValueError("R4-R47 catalog required")
    if crosswalk.get("catalog_snapshot_sha256") != catalog_digest(catalog):
        raise ValueError("Catalog snapshot mismatch")
    if crosswalk.get("source_sha256") != catalog.get("source_sha256"):
        raise ValueError("Source snapshot mismatch")
    if crosswalk.get("registry_snapshot_only") is not True or crosswalk.get("live_registry_verified") is not False:
        raise ValueError("Cannot claim live Registry review")
    if crosswalk.get("registration_applied") is not False or crosswalk.get("ids_allocated") is not False:
        raise ValueError("Prior review must be read-only")
    candidates = crosswalk.get("candidates", [])
    if len(candidates) != 19 or len({r["r48_index"] for r in candidates}) != 19:
        raise ValueError("Exactly 19 unique definition candidates required")
    reference_ids = set(catalog.get("existing_reference_ids", []))
    assertion_ids = set(catalog.get("existing_assertion_ids", []))
    if len(reference_ids) != 23 or len(assertion_ids) != 67:
        raise ValueError("R4-R47 snapshot unexpectedly changed")
    source_lines = {}
    for chapter, name in SOURCE_NAMES.items():
        raw = (inputs / name).read_bytes()
        if hashlib.sha256(raw).hexdigest() != catalog["source_sha256"][str(chapter)]:
            raise ValueError(f"TeX source changed: {name}")
        source_lines[chapter] = raw.decode("utf-8-sig").splitlines()
    by_chapter = {}
    for unit in catalog["items"]:
        by_chapter.setdefault(unit["chapter"], []).append(unit)
        start, end = _unit_span(unit, source_lines[unit["chapter"]])
        if end < start:
            raise ValueError(f"Catalog unit span invalid: {unit['source_unit_id']}")
    results = []
    for candidate in candidates:
        if candidate["role_decision"] != "DEFINITION_CANDIDATE":
            raise ValueError("Unexpected candidate classification")
        if candidate["new_registration_status"] != "NOT_DECIDED" or candidate["original_edition_verified"] is not False:
            raise ValueError("Cannot use previously registered/verified candidate")
        chapter, line = candidate["chapter"], candidate["source_line"]
        lines = source_lines[chapter]
        if not (1 <= line <= len(lines)) or candidate["source_file"] != SOURCE_NAMES[chapter]:
            raise ValueError("Candidate anchor mismatch")
        if candidate["excerpt"].startswith("\\[") and not lines[line - 1].strip().startswith("\\["):
            raise ValueError("Display anchor mismatch")
        if not candidate["excerpt"].startswith("\\[") and lines[line - 1].strip() != candidate["excerpt"].strip():
            raise ValueError("Prose anchor mismatch")
        matched = [u for u in by_chapter.get(chapter, []) if _same_text_unit(candidate, u, lines)]
        if len(matched) > 1:
            raise ValueError("Ambiguous TeX unit containment")
        match = matched[0] if matched else None
        if match is None:
            status = "NO_DIRECT_CATALOG_UNIT"
        elif match.get("reference_id") in reference_ids:
            status = "EXISTING_REFERENCE_SAME_TEX_UNIT"
        else:
            status = "CATALOG_UNIT_WITHOUT_EXISTING_REFERENCE"
        row = {
            "r48_index": candidate["r48_index"],
            "chapter": chapter,
            "source_line": line,
            "editorial_key": candidate["editorial_key"],
            "source_file": candidate["source_file"],
            "tex_catalog_containment_status": status,
            "matched_source_unit_id": match["source_unit_id"] if match else None,
            "matched_locator": match["locator"] if match else None,
            "existing_reference_id": match["reference_id"] if match else None,
            "existing_assertion_ids_inferred": [],
            "content_overlap_status": "NOT_DETERMINABLE_FROM_R47_METADATA",
            "registration_action": "NONE",
            "new_statement_confirmed": False,
            "original_edition_verified": False,
            "evidence": "catalog tex_body and source_line containment; no typed assertion contents compared",
            "excerpt": candidate["excerpt"],
            "context": candidate["context"],
        }
        results.append(row)
    counts = dict(sorted(Counter(row["tex_catalog_containment_status"] for row in results).items()))
    return {
        "phase": "163 R4-R53",
        "mode": "READ_ONLY_SEMANTIC_OVERLAP_BOUNDARY_AUDIT",
        "catalog_snapshot_sha256": catalog_digest(catalog),
        "source_sha256": catalog["source_sha256"],
        "definition_candidate_count": len(results),
        "status_counts": counts,
        "mathematical_content_equivalence_verified": False,
        "typed_assertion_content_available_in_snapshot": False,
        "semantic_overlap_unresolved_count": 19,
        "new_statement_confirmed_count": 0,
        "pending_other_candidates_count": crosswalk["pending_mathematical_review_count"],
        "registry_snapshot_only": True,
        "live_registry_verified": False,
        "registration_applied": False,
        "registry_modified": False,
        "ids_allocated": False,
        "proof_search_connected": False,
        "original_edition_verified": False,
        "candidates": results,
    }


def write_results(result: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "overlap_audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fields = ["r48_index", "chapter", "source_line", "editorial_key", "tex_catalog_containment_status",
              "matched_source_unit_id", "matched_locator", "existing_reference_id", "content_overlap_status",
              "new_statement_confirmed", "excerpt", "context"]
    with (output / "overlap_audit.csv").open("w", encoding="utf-8-sig", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(result["candidates"])
    lines = ["# Phase 163 R4-R53 数学的重複・包含の境界監査", "",
             "R4-R47 のスナップショットは Reference/Assertion の ID を含むが、各 Assertion の型付き数学的内容を含まない。", "従って、数学的同値・包含・重複の判定はできず、同じ TeX 掲載単位への所属のみを検査する。", "",
             "## 集計", "",
             f"- 定義候補: {result['definition_candidate_count']} 件"]
    lines += [f"- {k}: {v} 件" for k,v in result["status_counts"].items()]
    lines += ["- 数学的内容の重複未判定: 19 件", "- 新規 Statement 確定: 0 件", "", "## 同一 TeX 掲載単位の候補", ""]
    for r in result["candidates"]:
        if r["matched_source_unit_id"]:
            lines.append(f"- 第{r['chapter']}章 L{r['source_line']} {r['editorial_key']} → {r['matched_locator']} ({r['matched_source_unit_id']}) / {r['tex_catalog_containment_status']}")
    lines += ["", "## 判断境界", "", "TeX 掲載単位の一致は Assertion の内容的同値を示さない。",
              "対応 Assertion ID を推測しない。既存 ID の改変・本番台帳への登録・証明探索接続を行わない。",
              "237件の未判定候補、原本未照合状態を維持する。全体 pytest は行わない。", ""]
    (output / "report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--crosswalk", required=True, type=Path)
    p.add_argument("--catalog", required=True, type=Path)
    p.add_argument("--inputs", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    args = p.parse_args()
    result = audit(json.loads(args.crosswalk.read_text(encoding="utf-8")),
                   json.loads(args.catalog.read_text(encoding="utf-8")), args.inputs)
    write_results(result, args.output)
    print(json.dumps({k: v for k, v in result.items() if k != "candidates"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
