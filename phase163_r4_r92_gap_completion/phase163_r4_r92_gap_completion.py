"""Phase 163 R4-R92: source-only subitem registration and coverage inventory.

No mathematical certification or production-registry mutation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

CHAPTER_FILES = (
    "Toda_01_corrected.tex",
    "Toda_02_2.tex",
    "Toda_03_2.tex",
    "Toda_04_2.tex",
    "Toda_05_2.tex",
)
STATEMENTS = ("theorem", "proposition", "lemma", "corollary", "definition", "remark")
BEGIN_STATEMENT = re.compile(r"\\begin\{(" + "|".join(STATEMENTS) + r")\}")
BEGIN_EQUATION = re.compile(r"\\begin\{equation\*?\}")
ITEM = re.compile(r"\\item(?:\[[^\n]*?\])?")
LABEL = re.compile(r"\\label\{([^{}]+)\}")
NUMBER_HINT = re.compile(r"(?m)^\s*%\s*\(([1-5]\.\d+)\)")
DEFINITION_HINT = re.compile(r"\\emph\{([^{}]+)\}[^\n]{0,240}")


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def mask_comments(text: str) -> str:
    """Mask comments while keeping offsets and line numbers intact."""
    chunks = []
    for line in text.splitlines(keepends=True):
        m = re.search(r"(?<!\\)%", line)
        if m is None:
            chunks.append(line)
        else:
            chunks.append(line[:m.start()] + re.sub(r"[^\n]", " ", line[m.start():]))
    return "".join(chunks)


def original_excerpt(raw: str, row: dict) -> str:
    lines = raw.splitlines()
    first, last = row["start_line"], row["end_line"]
    if not (isinstance(first, int) and isinstance(last, int) and 1 <= first <= last <= len(lines)):
        raise ValueError("invalid source line span")
    return "\n".join(lines[first - 1:last])


def validate_r91(catalog: dict, source_dir: Path) -> dict[int, str]:
    if (catalog.get("phase") != "163 R4-R91" or
            catalog.get("mode") != "FIVE_CHAPTER_TEX_SOURCE_ONLY" or
            catalog.get("chapters") != 5 or catalog.get("record_count") != 96):
        raise ValueError("unexpected R91 catalog")
    rows = catalog.get("records")
    if not isinstance(rows, list) or len(rows) != 96:
        raise ValueError("R91 record count mismatch")
    sources = {
        chapter: (source_dir / filename).read_text(encoding="utf-8-sig")
        for chapter, filename in enumerate(CHAPTER_FILES, 1)
    }
    seen = set()
    prior = (0, 0)
    for index, row in enumerate(rows, 1):
        chapter = row["chapter"]
        if chapter not in sources or row["source_file"] != CHAPTER_FILES[chapter - 1]:
            raise ValueError("source origin mismatch")
        position = (chapter, row["start_line"])
        if position <= prior or row["publication_position"] != index:
            raise ValueError("publication order mismatch")
        prior = position
        if (row["source_id"] in seen or row["status"] != "SOURCE_ONLY" or
                sha256(row["source_text"]) != row["source_sha256"]):
            raise ValueError("R91 source identity or checksum mismatch")
        seen.add(row["source_id"])
        # The original excerpt must agree byte-for-byte with source text, apart
        # from newline encodings already normalized by Python's text reader.
        if original_excerpt(sources[chapter], row) != row["source_text"]:
            raise ValueError("R91 and current TeX disagree")
    return sources


def item_components(row: dict) -> list[dict]:
    """Record explicit TeX list items as archival subitems; never infer semantics."""
    if row["environment"] not in STATEMENTS:
        return []
    text = row["source_text"]
    masked = mask_comments(text)
    # Only explicit enumerate environments. Keep each item and preserve its
    # containing full proposition as the source of inherited constraints.
    begins = list(re.finditer(r"\\begin\{enumerate\}", masked))
    ends = list(re.finditer(r"\\end\{enumerate\}", masked))
    if len(begins) != 1 or len(ends) != 1 or begins[0].end() >= ends[0].start():
        return []
    start, stop = begins[0].end(), ends[0].start()
    matches = list(ITEM.finditer(masked, start, stop))
    if len(matches) < 2:
        return []
    rows = []
    for index, found in enumerate(matches, 1):
        end = matches[index].start() if index < len(matches) else stop
        source = text[found.start():end].strip()
        if not source:
            raise ValueError("empty TeX list item")
        rows.append({
            "source_id": f"{row['source_id']}:item:{index:02d}",
            "parent_source_id": row["source_id"],
            "parent_locator": row["locator"],
            "chapter": row["chapter"],
            "component_position": index,
            "source_text": source,
            "source_sha256": sha256(source),
            "source_file": row["source_file"],
            "parent_source_sha256": row["source_sha256"],
            "inherited_context": "Parent TeX block retained; conditions may precede list items",
            "mathematical_semantics_verified": False,
            "proof_eligible": False,
            "status": "SOURCE_ONLY_SUBITEM",
        })
    return rows


def coverage_gaps(catalog: dict, sources: dict[int, str]) -> list[dict]:
    """Make review candidates, never turn guesses into fixed statements."""
    result = []
    for chapter, raw in sources.items():
        masked = mask_comments(raw)
        registered = [r for r in catalog["records"] if r["chapter"] == chapter]
        for found in BEGIN_STATEMENT.finditer(masked):
            line = raw.count("\n", 0, found.start()) + 1
            if not any(row["start_line"] == line for row in registered):
                result.append({"chapter": chapter, "line": line,
                               "kind": "UNREGISTERED_STATEMENT_ENVIRONMENT", "status": "REVIEW_ONLY"})
        for found in BEGIN_EQUATION.finditer(masked):
            line = raw.count("\n", 0, found.start()) + 1
            if not any(row["start_line"] == line for row in registered):
                result.append({"chapter": chapter, "line": line,
                               "kind": "UNREGISTERED_EQUATION_OR_NESTED_ALIAS", "status": "REVIEW_ONLY"})
        # A concrete Chapter 1 informal definition is present outside a TeX
        # definition environment. This is only a candidate, not a theorem.
        for found in DEFINITION_HINT.finditer(masked):
            term = found.group(1)
            if "secondary composition" not in term.lower():
                continue
            line = raw.count("\n", 0, found.start()) + 1
            if not any(row["start_line"] <= line <= row["end_line"] for row in registered):
                result.append({"chapter": chapter, "line": line,
                               "kind": "INLINE_DEFINITION_CANDIDATE", "term": term,
                               "status": "REVIEW_ONLY"})
    return result


def audit_catalog(catalog: dict, source_dir: Path) -> dict:
    sources = validate_r91(catalog, source_dir)
    items = []
    labels_to_rows = {}
    for row in catalog["records"]:
        items.extend(item_components(row))
        if row["label"]:
            labels_to_rows.setdefault((row["chapter"], row["label"]), []).append(row["source_id"])
    if len(set(x["source_id"] for x in items)) != len(items):
        raise ValueError("duplicate subitem source ID")
    aliases = []
    for row in catalog["records"]:
        if not row["review_needed"]:
            continue
        hints = NUMBER_HINT.findall(row["source_text"])
        aliases.append({"source_id": row["source_id"], "locator": row["locator"],
                        "label": row["label"], "number_hints": hints,
                        "status": "REVIEW_ONLY"})
    duplicates = [
        {"chapter": ch, "label": label, "source_ids": ids}
        for (ch, label), ids in labels_to_rows.items() if len(ids) > 1
    ]
    gaps = coverage_gaps(catalog, sources)
    return {
        "phase": "163 R4-R92", "mode": "R91_COVERAGE_AND_SOURCE_ONLY_SUBITEMS",
        "r91_parent_record_count": len(catalog["records"]),
        "source_subitem_count": len(items),
        "r91_review_count": len(aliases),
        "label_collision_count": len(duplicates),
        "gap_candidate_count": len(gaps),
        "production_registry_modified": False,
        "mathematical_semantics_verified_count": 0,
        "proof_search_connected": False, "full_suite_run": False,
        "source_subitems": items, "label_reviews": aliases,
        "label_collisions": duplicates, "gap_candidates": gaps,
    }


def register_subitems(catalog: dict, audit: dict, *, bridge=None) -> dict:
    """Opt-in addition to the R91 unified registry; no proof link is built."""
    from unified_statement_registry import AssertionEntry, AssertionKind, AssertionOrigin
    if audit["mode"] != "R91_COVERAGE_AND_SOURCE_ONLY_SUBITEMS":
        raise ValueError("not an R92 audit")
    if bridge is None:
        from phase163_r4_registry_bridge import build_registry_bridge
        bridge = build_registry_bridge()
    from phase163_r4_r91_tex_bulk import integrate_source_catalog
    registry, baseline = integrate_source_catalog(catalog, bridge=bridge)
    parents = {x["source_id"]: x for x in catalog["records"]}
    for item in audit["source_subitems"]:
        parent = parents[item["parent_source_id"]]
        if (item["parent_source_sha256"] != parent["source_sha256"] or
                sha256(item["source_text"]) != item["source_sha256"] or
                item["status"] != "SOURCE_ONLY_SUBITEM" or
                item["proof_eligible"] is not False or
                item["mathematical_semantics_verified"] is not False):
            raise ValueError("subitem provenance or eligibility mismatch")
        registry.add_assertion(AssertionEntry(
            assertion_id=item["source_id"], reference_id="toda:" + parent["locator"],
            kind=AssertionKind.STATEMENT, origin=AssertionOrigin.SOURCE_ARCHIVE,
            component_position=item["component_position"],
            scope={"parent_source_id": item["parent_source_id"], "shared_context_required": True},
            content={"source_text": item["source_text"],
                     "source_sha256": item["source_sha256"],
                     "parent_source_sha256": item["parent_source_sha256"],
                     "mathematics_verified": False, "proof_eligible": False},
        ))
    return {
        "phase": "163 R4-R92", "r91_assertion_count": baseline["source_assertion_added_count"],
        "subitem_assertion_added_count": len(audit["source_subitems"]),
        "source_only_assertion_count": baseline["source_assertion_added_count"] + len(audit["source_subitems"]),
        "production_registry_modified": False,
        "mathematical_semantics_verified_count": 0, "proof_search_connected": False,
        "full_suite_run": False,
    }


def write_outputs(audit: dict, registration: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    for filename, contents in (("audit.json", audit), ("registration.json", registration)):
        (output / filename).write_text(json.dumps(contents, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Phase 163 R4-R92：第1〜5章の追加候補と命題内主張",
        "", f"R91 原文ブロック: {audit['r91_parent_record_count']}件",
        f"命題内の明示的 item: {audit['source_subitem_count']}件（原文のみ）",
        f"ラベル要確認: {audit['r91_review_count']}件",
        f"未収録・入れ子候補: {audit['gap_candidate_count']}件",
        f"ラベル重複: {audit['label_collision_count']}件",
        "", "数学的認定・原著照合・本番台帳変更・証明探索接続は実施していない。",
        "", "## 明示的 item", "",
        "| Parent | 順序 | Source ID |", "|---|---:|---|",
    ]
    for r in audit["source_subitems"]:
        lines.append(f"| {r['parent_locator']} | {r['component_position']} | `{r['source_id']}` |")
    lines.extend(["", "## 残る候補（数学的主張と未認定）", "",
                  "| 章 | 行 | 種別 |", "|---|---:|---|"])
    for g in audit["gap_candidates"]:
        lines.append(f"| {g['chapter']} | {g['line']} | {g['kind']} |")
    (output / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    audit = audit_catalog(catalog, args.source_dir)
    registration = register_subitems(catalog, audit)
    write_outputs(audit, registration, args.output)
    print(json.dumps({**registration,
                      "gap_candidate_count": audit["gap_candidate_count"],
                      "r91_review_count": audit["r91_review_count"]},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
