"""Phase 163 R4-R91: five-chapter TeX-source registry, without proof eligibility."""
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
from phase163_r4_registry_bridge import build_registry_bridge

CHAPTER_FILES = (
    "Toda_01_corrected.tex",
    "Toda_02_2.tex",
    "Toda_03_2.tex",
    "Toda_04_2.tex",
    "Toda_05_2.tex",
)
ENV_KIND = {
    "theorem": ReferenceKind.THEOREM,
    "proposition": ReferenceKind.PROPOSITION,
    "lemma": ReferenceKind.LEMMA,
    "corollary": ReferenceKind.COROLLARY,
    "definition": ReferenceKind.DEFINITION,
    "remark": ReferenceKind.REMARK,
}
BEGIN = re.compile(r"\\begin\{(theorem|proposition|lemma|corollary|definition|remark|equation)\}(?:\[[^\n]*?\])?")
LABEL = re.compile(r"\\label\{([^{}]+)\}")
CHAPTER_LABEL = re.compile(r"(?<!\d)([1-5])(?:[.:\-])([1-9]\d*)(?!\d)")


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _clean_comments(text: str) -> str:
    """Mask LaTeX comments but preserve offsets and line numbers."""
    out = []
    for line in text.splitlines(keepends=True):
        match = re.search(r"(?<!\\)%", line)
        if match:
            idx = match.start()
            out.append(line[:idx] + re.sub(r"[^\n]", " ", line[idx:]))
        else:
            out.append(line)
    return "".join(out)


def extract_chapter(path: Path, chapter: int) -> list[dict]:
    raw = path.read_text(encoding="utf-8-sig")
    masked = _clean_comments(raw)
    stack: list[dict] = []
    candidates: list[dict] = []
    # A lexical environment stack is essential: equations inside propositions
    # are aliases of that proposition, not independently numbered statements.
    token = re.compile(r"\\(begin|end)\{([A-Za-z*]+)\}")
    for found in token.finditer(masked):
        action, env = found.groups()
        if action == "begin":
            if env in ENV_KIND or env == "equation":
                stack.append({"env": env, "start": found.start(), "children": [],
                              "parent": stack[-1] if stack else None})
            else:
                stack.append({"env": env, "start": found.start(), "children": [],
                              "parent": stack[-1] if stack else None})
            continue
        if not stack or stack[-1]["env"] != env:
            # Fail closed instead of extracting a spurious segment.
            if any(x["env"] == env for x in stack):
                raise ValueError(f"mismatched TeX environment near line {_line_number(raw, found.start())}")
            continue
        item = stack.pop()
        if env not in ENV_KIND and env != "equation":
            continue
        source = raw[item["start"]:found.end()]
        masked_source = masked[item["start"]:found.end()]
        labels = LABEL.findall(masked_source)
        direct_labels = LABEL.findall(masked_source[: min(len(masked_source), 220)])
        label = direct_labels[0] if direct_labels else (labels[0] if labels else None)
        parent = item["parent"]
        inside_statement = False
        while parent is not None:
            if parent["env"] in ENV_KIND:
                inside_statement = True
                break
            parent = parent["parent"]
        if env == "equation" and inside_statement:
            continue
        if env == "equation" and not label:
            continue
        if env in ENV_KIND and not label:
            # Preserve unlabelled source; never invent a printed theorem number.
            locator = f"UNLABELED CH{chapter} LINE {_line_number(raw, item['start'])}"
            review_needed = True
        else:
            match = CHAPTER_LABEL.search(label or "")
            if match and int(match.group(1)) == chapter:
                number = f"{chapter}.{int(match.group(2))}"
                locator = f"{env.capitalize() if env != 'equation' else 'Equation'} {number}" if env != "equation" else f"({number})"
                review_needed = False
            else:
                locator = f"LABEL {label}"
                review_needed = True
        candidates.append({
            "chapter": chapter,
            "source_file": path.name,
            "environment": env,
            "kind": ENV_KIND.get(env, ReferenceKind.EQUATION).value,
            "locator": locator,
            "label": label,
            "start_line": _line_number(raw, item["start"]),
            "end_line": _line_number(raw, found.end() - 1),
            "source_text": source,
            "source_sha256": _sha(source),
            "review_needed": review_needed,
            "status": "SOURCE_ONLY",
        })
    candidates.sort(key=lambda row: row["start_line"])
    for i, row in enumerate(candidates, 1):
        row["chapter_position"] = i
    return candidates


def extract_five_chapters(source_dir: Path) -> dict:
    rows: list[dict] = []
    for ch, filename in enumerate(CHAPTER_FILES, 1):
        path = source_dir / filename
        if not path.is_file():
            raise FileNotFoundError(path)
        rows.extend(extract_chapter(path, ch))
    if not rows:
        raise ValueError("no TeX statements extracted")
    for index, row in enumerate(rows, 1):
        row["publication_position"] = index
        row["source_id"] = f"toda:tex:ch{row['chapter']}:{row['chapter_position']:04d}"
    return {
        "phase": "163 R4-R91",
        "mode": "FIVE_CHAPTER_TEX_SOURCE_ONLY",
        "chapters": 5,
        "record_count": len(rows),
        "review_needed_count": sum(r["review_needed"] for r in rows),
        "original_edition_verified": False,
        "mathematical_semantics_verified_count": 0,
        "proof_eligible_count": 0,
        "production_registry_modified": False,
        "proof_search_connected": False,
        "full_suite_run": False,
        "records": rows,
    }


def integrate_source_catalog(catalog: dict, *, bridge=None):
    """Explicitly attach new source records to a fresh Bridge, never to production."""
    if catalog.get("phase") != "163 R4-R91" or catalog.get("mode") != "FIVE_CHAPTER_TEX_SOURCE_ONLY":
        raise ValueError("unrecognized catalog")
    rows = catalog["records"]
    if len(rows) != catalog["record_count"]:
        raise ValueError("record count changed")
    if bridge is None:
        bridge = build_registry_bridge()
    registry = bridge.registry
    reference_added = 0
    reference_reused = 0
    registered = 0
    id_set = set()
    # Use unique archival IDs per physical source position. The same printed
    # locator may occur in an existing fixed fact or TeX; no false promotion.
    for row in rows:
        if (row["status"] != "SOURCE_ONLY" or
                _sha(row["source_text"]) != row["source_sha256"] or
                row["source_id"] in id_set):
            raise ValueError("source integrity/identity violation")
        id_set.add(row["source_id"])
        kind = ReferenceKind(row["kind"])
        key = "toda:" + row["locator"]
        try:
            existing = registry.reference(key)
        except KeyError:
            registry.add_reference(LiteratureEntry(
                reference_id=key, kind=kind, locator=row["locator"],
                source_id="Toda translated TeX; original edition unverified",
                publication_position=row["publication_position"],
            ))
            reference_added += 1
        else:
            if existing.kind != kind or existing.locator != row["locator"]:
                # Never merge conflicting identities on the strength of a label.
                raise ValueError(f"reference identity conflict: {key}")
            reference_reused += 1
        registry.add_assertion(AssertionEntry(
            assertion_id=row["source_id"], reference_id=key,
            kind=AssertionKind.STATEMENT,
            origin=AssertionOrigin.SOURCE_ARCHIVE,
            component_position=row["chapter_position"],
            scope={"chapter": row["chapter"], "label": row["label"],
                   "review_needed": row["review_needed"]},
            content={"source_text": row["source_text"],
                     "source_sha256": row["source_sha256"],
                     "source_file": row["source_file"],
                     "source_lines": [row["start_line"], row["end_line"]],
                     "mathematics_verified": False,
                     "original_edition_verified": False,
                     "proof_eligible": False},
        ))
        registered += 1
    return registry, {
        "phase": "163 R4-R91", "reference_added_count": reference_added,
        "reference_reused_count": reference_reused,
        "source_assertion_added_count": registered,
        "review_needed_count": catalog["review_needed_count"],
        "production_registry_modified": False,
        "proof_search_connected": False,
        "full_suite_run": False,
    }


def write_outputs(catalog: dict, summary: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "source_catalog.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Phase 163 R4-R91：第1〜5章の原文一括登録", "",
             "原文を出典位置順に保存。数学的認定・証明利用は行わない。",
             "", f"抽出: {catalog['record_count']} 件、確認要: {catalog['review_needed_count']} 件。",
             f"統一台帳へ原文として追加: {summary['source_assertion_added_count']} 件。", "",
             "| 章 | 位置 | 環境 | ラベル | 要確認 |", "|---|---:|---|---|---|"]
    for row in catalog["records"]:
        lines.append(f"| {row['chapter']} | {row['start_line']} | {row['environment']} | `{row['label'] or ''}` | {'要' if row['review_needed'] else '—'} |")
    lines += ["", "注意：章内の無環境定義、ラベル欠落、数式の証明内・本文内区別は別途照合が必要。", "全体 pytest は Phase 163 終了時のみ実行する。"]
    (output / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    catalog = extract_five_chapters(args.source_dir)
    _, summary = integrate_source_catalog(catalog)
    write_outputs(catalog, summary, args.output)
    print(json.dumps({**summary, "extracted": catalog["record_count"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
