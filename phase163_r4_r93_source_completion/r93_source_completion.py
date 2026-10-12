"""Phase 163 R4-R93: source-only completion of the 14 R92 gap candidates.

This optional builder never certifies mathematics or modifies production lookup.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    LiteratureEntry,
    ReferenceKind,
)

EQUATION = re.compile(r"\\(begin|end)\{equation\}")
R93_MODE = "R92_GAP_COMPLETION_SOURCE_ONLY"


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def classify_gap(catalog: dict, audit: dict, source_dir: Path) -> dict:
    """Verify all earlier evidence anew, then classify the exact 14 gap sites."""
    from phase163_r4_r92_gap_completion.phase163_r4_r92_gap_completion import (
        audit_catalog, validate_r91, mask_comments, CHAPTER_FILES,
    )

    checked = audit_catalog(catalog, source_dir)
    if audit != checked:
        raise ValueError("R92 audit differs from verified source evidence")
    sources = validate_r91(catalog, source_dir)
    parents = catalog["records"]
    registered_positions = {(r["chapter"], r["start_line"]) for r in parents}
    result = []
    alias_links = []
    duplicate_mentions = []
    for gap in checked["gap_candidates"]:
        chapter, line, kind = gap["chapter"], gap["line"], gap["kind"]
        raw = sources[chapter]
        lines = raw.splitlines()
        if (chapter, line) in registered_positions or line > len(lines):
            raise ValueError("gap collides with R91 registration")
        if kind == "UNREGISTERED_EQUATION_OR_NESTED_ALIAS":
            masked = mask_comments(raw)
            starts = list(EQUATION.finditer(masked))
            open_stack = []
            pair = None
            for token in starts:
                position = raw.count("\n", 0, token.start()) + 1
                if token.group(1) == "begin":
                    open_stack.append((position, token.start()))
                elif open_stack:
                    begin_line, begin_offset = open_stack.pop()
                    if begin_line == line:
                        pair = (begin_offset, token.end())
                        break
            if pair is None:
                raise ValueError("unmatched equation gap")
            source_text = raw[pair[0]:pair[1]]
            parent = next((r for r in parents if r["chapter"] == chapter
                           and r["start_line"] < line <= r["end_line"]), None)
            if parent is not None:
                if parent["environment"] not in ("theorem", "proposition", "lemma", "corollary", "definition", "remark"):
                    raise ValueError("unexpected nested equation parent")
                alias_links.append({
                    "source_id": f"{parent['source_id']}:equation:{line}",
                    "parent_source_id": parent["source_id"],
                    "parent_locator": parent["locator"],
                    "chapter": chapter, "line": line,
                    "label": re.search(r"\\label\{([^{}]+)\}", source_text).group(1)
                    if re.search(r"\\label\{([^{}]+)\}", source_text) else None,
                    "source_text": source_text, "source_sha256": digest(source_text),
                    "status": "NESTED_EQUATION_ALIAS_NO_NEW_ASSERTION",
                })
                continue
            if re.search(r"\\label\{[^{}]+\}", mask_comments(source_text)):
                raise ValueError("labeled free equation should already be in R91")
            result.append({
                "source_id": f"toda:tex:ch{chapter}:unlabeled-equation:line{line}",
                "chapter": chapter, "line": line,
                "source_file": CHAPTER_FILES[chapter - 1],
                "kind": "equation", "locator": f"UNLABELED EQUATION CH{chapter} LINE {line}",
                "source_text": source_text, "source_sha256": digest(source_text),
                "status": "SOURCE_ONLY_UNLABELED", "review_needed": True,
            })
        elif kind == "INLINE_DEFINITION_CANDIDATE":
            if chapter == 1 and gap.get("term") == "secondary composition":
                start = line - 1
                # From the active \emph term through the paragraph defining it,
                # stopping before the commented-out end-definition marker.
                end = next((i for i in range(start, min(start + 20, len(lines)))
                            if lines[i].strip() == "%\\end{definition}"), None)
                if end is None or "集合として定める" not in "\n".join(lines[start:end]):
                    raise ValueError("inline definition boundaries changed")
                source_text = "\n".join(lines[start:end]).strip()
                result.append({
                    "source_id": "toda:tex:ch1:inline-definition:secondary-composition",
                    "chapter": chapter, "line": line, "source_file": "Toda_01_corrected.tex",
                    "kind": "definition", "locator": "UNNUMBERED DEFINITION CH1 secondary composition",
                    "source_text": source_text, "source_sha256": digest(source_text),
                    "status": "SOURCE_ONLY_INLINE_DEFINITION", "review_needed": True,
                })
            else:
                # The Chapter 2 mention restates an existing defined term;
                # preserve the source coordinate, but do not register a duplicate.
                duplicate_mentions.append({
                    "chapter": chapter, "line": line, "term": gap.get("term"),
                    "target_source_id": "toda:tex:ch1:inline-definition:secondary-composition",
                    "status": "CROSS_CHAPTER_MENTION_NO_NEW_ASSERTION",
                })
        else:
            raise ValueError(f"unexpected gap type: {kind}")
    if (len(checked["gap_candidates"]) != 14 or len(result) != 12
            or len(alias_links) != 1 or len(duplicate_mentions) != 1
            or len({x["source_id"] for x in result}) != 12):
        raise ValueError("R93 completeness/count mismatch")
    suggestions = []
    for entry in checked["label_reviews"]:
        hints = entry["number_hints"]
        suggestions.append({
            "source_id": entry["source_id"], "original_locator": entry["locator"],
            "number_hints": hints,
            "suggested_locator": f"({hints[0]})" if len(hints) == 1 and entry["label"].startswith("eq:") else None,
            "status": "UNVERIFIED_NUMBER_MAPPING_DO_NOT_RENAME",
        })
    return {
        "phase": "163 R4-R93", "mode": R93_MODE,
        "baseline_source_only_assertion_count": 105,
        "additional_source_only_assertion_count": len(result),
        "source_only_assertion_count": 105 + len(result),
        "gap_candidate_count": 14,
        "resolved_as_new_source_records": len(result),
        "nested_alias_count": len(alias_links),
        "duplicate_mention_count": len(duplicate_mentions),
        "label_review_count": len(suggestions),
        "additional_records": result, "nested_aliases": alias_links,
        "duplicate_mentions": duplicate_mentions, "number_reviews": suggestions,
        "mathematical_semantics_verified_count": 0,
        "proof_eligible_count": 0,
        "original_edition_verified": False,
        "production_registry_modified": False,
        "proof_search_connected": False,
        "full_suite_run": False,
    }


def register_completion(catalog: dict, audit_r92: dict, completion: dict):
    """Build a fresh R91/R92 registry and add only twelve archival assertions."""
    from phase163_r4_registry_bridge import build_registry_bridge
    from phase163_r4_r91_tex_bulk import integrate_source_catalog

    if completion.get("mode") != R93_MODE or len(completion["additional_records"]) != 12:
        raise ValueError("invalid R93 completion")
    bridge = build_registry_bridge()
    registry, baseline = integrate_source_catalog(catalog, bridge=bridge)
    if baseline["source_assertion_added_count"] != 96:
        raise ValueError("R91 baseline count changed")
    if len(audit_r92["source_subitems"]) != 9:
        raise ValueError("R92 baseline count changed")
    for item in audit_r92["source_subitems"]:
        parent = next(row for row in catalog["records"] if row["source_id"] == item["parent_source_id"])
        if (digest(item["source_text"]) != item["source_sha256"]
                or item["parent_source_sha256"] != parent["source_sha256"]
                or item["proof_eligible"] is not False):
            raise ValueError("R92 source item changed")
        registry.add_assertion(AssertionEntry(
            assertion_id=item["source_id"], reference_id="toda:" + parent["locator"],
            kind=AssertionKind.STATEMENT, origin=AssertionOrigin.SOURCE_ARCHIVE,
            component_position=item["component_position"],
            content={"source_text": item["source_text"], "source_sha256": item["source_sha256"],
                     "parent_source_id": parent["source_id"], "proof_eligible": False,
                     "mathematics_verified": False},
        ))
    for row in completion["additional_records"]:
        if (row["status"] not in ("SOURCE_ONLY_UNLABELED", "SOURCE_ONLY_INLINE_DEFINITION")
                or digest(row["source_text"]) != row["source_sha256"]):
            raise ValueError("R93 source tampering")
        reference_id = "toda:" + row["locator"]
        kind = ReferenceKind.DEFINITION if row["kind"] == "definition" else ReferenceKind.EQUATION
        try:
            existing = registry.reference(reference_id)
        except KeyError:
            registry.add_reference(LiteratureEntry(
                reference_id=reference_id, kind=kind, locator=row["locator"],
                source_id="Toda translated TeX; original edition unverified",
            ))
        else:
            if existing.kind is not kind or existing.locator != row["locator"]:
                raise ValueError("conflicting archive reference")
        registry.add_assertion(AssertionEntry(
            assertion_id=row["source_id"], reference_id=reference_id,
            kind=AssertionKind.STATEMENT, origin=AssertionOrigin.SOURCE_ARCHIVE,
            content={"source_text": row["source_text"], "source_sha256": row["source_sha256"],
                     "source_file": row["source_file"], "source_line": row["line"],
                     "mathematics_verified": False, "proof_eligible": False,
                     "original_edition_verified": False},
        ))
    if len(set(r["source_id"] for r in completion["additional_records"])) != 12:
        raise ValueError("duplicate R93 record")
    return registry, {
        "phase": "163 R4-R93", "source_only_assertion_count": 117,
        "additional_source_only_assertion_count": 12,
        "nested_alias_count": 1, "duplicate_mention_count": 1,
        "number_review_count": len(completion["number_reviews"]),
        "mathematical_semantics_verified_count": 0,
        "production_registry_modified": False, "proof_search_connected": False,
        "full_suite_run": False,
    }


def write_outputs(completion: dict, result: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    for name, data in (("completion.json", completion), ("registration.json", result)):
        (output / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Phase 163 R4-R93：未収録14候補の処理", "",
        "R91 96件 + R92 9件 + R93 12件 = **117件**（原文保存用 Assertion）。", "",
        "未収録候補14件：新規12件／親命題の内部式1件／第2章の再説明1件。", "",
        f"番号確認は {len(completion['number_reviews'])} 件。原文の番号を自動修正していない。", "",
        "| 章 | 行 | 種別 | ID |", "|---|---:|---|---|",
    ]
    for row in completion["additional_records"]:
        lines.append(f"| {row['chapter']} | {row['line']} | {row['kind']} | `{row['source_id']}` |")
    lines.extend(["", "## 親命題との関連付け", ""])
    for row in completion["nested_aliases"]:
        lines.append(f"- {row['parent_locator']} → 式 `{row['label']}`（第{row['chapter']}章 {row['line']}行）")
    lines.extend(["", "## 番号確認", "", "| Source ID | 推定番号 |", "|---|---|"])
    for row in completion["number_reviews"]:
        lines.append(f"| `{row['source_id']}` | {row['suggested_locator'] or '未確定'} |")
    lines.extend(["", "数学的認定・原著照合・証明探索接続・本番自動登録は実施していない。", ""])
    (output / "report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    audit = json.loads(args.audit.read_text(encoding="utf-8"))
    completion = classify_gap(catalog, audit, args.source_dir)
    _, result = register_completion(catalog, audit, completion)
    write_outputs(completion, result, args.output)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
