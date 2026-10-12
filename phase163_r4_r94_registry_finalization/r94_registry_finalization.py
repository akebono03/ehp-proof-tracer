"""Phase 163 R4-R94: immutable source-only crosswalk and ordered archival registry.

This module does not change the production registry or authorize proof search.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    LiteratureEntry,
    ReferenceKind,
    UnifiedStatementRegistry,
)


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def finalize_manifest(catalog: dict, audit: dict, completion: dict) -> dict:
    """Build publication order without renumbering previously issued source IDs."""
    if (catalog.get("phase") != "163 R4-R91"
            or catalog.get("record_count") != 96
            or len(catalog.get("records", [])) != 96
            or audit.get("phase") != "163 R4-R92"
            or len(audit.get("source_subitems", [])) != 9
            or completion.get("phase") != "163 R4-R93"
            or len(completion.get("additional_records", [])) != 12
            or len(completion.get("nested_aliases", [])) != 1
            or len(completion.get("duplicate_mentions", [])) != 1
            or len(completion.get("number_reviews", [])) != 8):
        raise ValueError("R91-R93 input contract mismatch")
    if (audit.get("label_collision_count") != 0
            or len(audit.get("gap_candidates", [])) != 14
            or any(document.get("proof_search_connected") is not False for document in (catalog, audit, completion))
            or any(document.get("production_registry_modified") is not False for document in (catalog, audit, completion))):
        raise ValueError("unresolved label collision or changed safety gate")
    parent_rows = []
    seen_ids = set()
    for row in catalog["records"]:
        if (row["source_id"] in seen_ids or row["status"] != "SOURCE_ONLY"
                or _sha(row["source_text"]) != row["source_sha256"]):
            raise ValueError("R91 source identity or SHA mismatch")
        seen_ids.add(row["source_id"])
        parent_rows.append({
            "statement_id": row["source_id"], "reference_id": "toda:" + row["locator"],
            "locator": row["locator"], "kind": row["kind"],
            "chapter": row["chapter"], "start_line": row["start_line"],
            "source_file": row["source_file"], "source_text": row["source_text"],
            "source_sha256": row["source_sha256"], "source_origin": "R91",
            "review_needed": bool(row["review_needed"]),
        })
    for row in completion["additional_records"]:
        if (row["source_id"] in seen_ids or
                row["status"] not in ("SOURCE_ONLY_UNLABELED", "SOURCE_ONLY_INLINE_DEFINITION")
                or _sha(row["source_text"]) != row["source_sha256"]):
            raise ValueError("R93 source identity or SHA mismatch")
        seen_ids.add(row["source_id"])
        parent_rows.append({
            "statement_id": row["source_id"], "reference_id": "toda:" + row["locator"],
            "locator": row["locator"], "kind": row["kind"],
            "chapter": row["chapter"], "start_line": row["line"],
            "source_file": row["source_file"], "source_text": row["source_text"],
            "source_sha256": row["source_sha256"], "source_origin": "R93",
            "review_needed": bool(row["review_needed"]),
        })
    parent_rows.sort(key=lambda row: (row["chapter"], row["start_line"], row["statement_id"]))
    if len({row["reference_id"] for row in parent_rows}) != 108:
        raise ValueError("duplicated top-level reference; manual mapping required")
    parent_by_id = {}
    source_order = []
    for index, row in enumerate(parent_rows, 1):
        row["publication_position"] = index
        row["component_position"] = None
        parent_by_id[row["statement_id"]] = row
        source_order.append((row["chapter"], row["start_line"], 0, row["statement_id"], row))
    subitems_by_parent = {}
    for item in audit["source_subitems"]:
        key = item["parent_source_id"]
        if key not in parent_by_id or item["source_id"] in seen_ids:
            raise ValueError("R92 parent missing or duplicate subitem ID")
        parent = parent_by_id[key]
        if (parent["source_sha256"] != item["parent_source_sha256"]
                or parent["source_origin"] != "R91"
                or _sha(item["source_text"]) != item["source_sha256"]
                or item["proof_eligible"] is not False
                or item["mathematical_semantics_verified"] is not False
                or item["parent_locator"] != parent["locator"]):
            raise ValueError("R92 subitem provenance changed")
        seen_ids.add(item["source_id"])
        subitems_by_parent.setdefault(key, []).append(item)
    for key, items in subitems_by_parent.items():
        items.sort(key=lambda r: r["component_position"])
        if [item["component_position"] for item in items] != list(range(1, len(items) + 1)):
            raise ValueError("R92 component order changed")
        parent = parent_by_id[key]
        for item in items:
            row = {
                "statement_id": item["source_id"], "reference_id": parent["reference_id"],
                "locator": parent["locator"], "kind": parent["kind"],
                "chapter": parent["chapter"], "start_line": parent["start_line"],
                "source_file": parent["source_file"], "source_text": item["source_text"],
                "source_sha256": item["source_sha256"], "source_origin": "R92",
                "parent_statement_id": key,
                "publication_position": parent["publication_position"],
                "component_position": item["component_position"],
                "review_needed": False,
            }
            source_order.append((row["chapter"], row["start_line"], item["component_position"], row["statement_id"], row))
    for alias in completion["nested_aliases"]:
        parent = parent_by_id.get(alias["parent_source_id"])
        if (parent is None or alias["parent_locator"] != parent["locator"]
                or _sha(alias["source_text"]) != alias["source_sha256"]
                or alias["status"] != "NESTED_EQUATION_ALIAS_NO_NEW_ASSERTION"):
            raise ValueError("nested equation alias mismatch")
    for mention in completion["duplicate_mentions"]:
        if (mention["target_source_id"] not in parent_by_id
                or mention["status"] != "CROSS_CHAPTER_MENTION_NO_NEW_ASSERTION"):
            raise ValueError("duplicate mention link mismatch")
    for item in completion["number_reviews"]:
        if (item["source_id"] not in parent_by_id
                or item["status"] != "UNVERIFIED_NUMBER_MAPPING_DO_NOT_RENAME"):
            raise ValueError("number review identity mismatch")
    source_order.sort(key=lambda row: row[:4])
    assertions = [row[-1] for row in source_order]
    if len(assertions) != 117 or len(seen_ids) != 117:
        raise ValueError("final manifest count mismatch")
    return {
        "phase": "163 R4-R94", "mode": "ORDERED_SOURCE_ONLY_MANIFEST",
        "reference_count": len(parent_rows), "assertion_count": len(assertions),
        "r91_count": 96, "r92_subitem_count": 9, "r93_added_count": 12,
        "nested_alias_count": 1, "duplicate_mention_count": 1,
        "number_review_count": 8,
        "publication_order_scope": "SOURCE_TEX_ORDER_NOT_ORIGINAL_EDITION",
        "original_edition_verified": False,
        "mathematical_semantics_verified_count": 0,
        "proof_eligible_count": 0,
        "production_registry_modified": False, "proof_search_connected": False,
        "full_suite_run": False,
        "assertions": assertions,
        "nested_aliases": completion["nested_aliases"],
        "duplicate_mentions": completion["duplicate_mentions"],
        "number_reviews": completion["number_reviews"],
    }


def build_ordered_registry(manifest: dict) -> UnifiedStatementRegistry:
    """Recreate a detached archival registry from validated R94 manifest."""
    if (manifest.get("mode") != "ORDERED_SOURCE_ONLY_MANIFEST"
            or manifest.get("assertion_count") != 117
            or manifest.get("reference_count") != 108
            or manifest.get("proof_eligible_count") != 0):
        raise ValueError("unrecognized R94 manifest")
    registry = UnifiedStatementRegistry()
    parent_ref_ids = set()
    for row in manifest["assertions"]:
        if _sha(row["source_text"]) != row["source_sha256"]:
            raise ValueError("manifest source digest mismatch")
        if row["source_origin"] != "R92":
            if row["reference_id"] in parent_ref_ids:
                raise ValueError("duplicate parent reference")
            parent_ref_ids.add(row["reference_id"])
            registry.add_reference(LiteratureEntry(
                reference_id=row["reference_id"], kind=ReferenceKind(row["kind"]),
                locator=row["locator"], source_id="Toda translated TeX; original edition unverified",
                publication_position=row["publication_position"],
            ))
    if len(parent_ref_ids) != 108:
        raise ValueError("archive reference count mismatch")
    for row in manifest["assertions"]:
        registry.add_assertion(AssertionEntry(
            assertion_id=row["statement_id"], reference_id=row["reference_id"],
            kind=AssertionKind.STATEMENT, origin=AssertionOrigin.SOURCE_ARCHIVE,
            content={"source_text": row["source_text"], "source_sha256": row["source_sha256"],
                     "source_file": row["source_file"], "mathematics_verified": False,
                     "original_edition_verified": False, "proof_eligible": False},
            component_position=row["component_position"],
            available_after_position=None,
        ))
    return registry


def reconcile_bridge(manifest: dict) -> dict:
    """Read-only identity reconciliation against the existing production Bridge."""
    from phase163_r4_registry_bridge import build_registry_bridge
    bridge = build_registry_bridge()
    exact = []
    missing = []
    for row in manifest["assertions"]:
        if row["source_origin"] == "R92":
            continue
        try:
            existing = bridge.registry.reference(row["reference_id"])
        except KeyError:
            missing.append(row["reference_id"])
        else:
            if existing.locator != row["locator"] or existing.kind.value != row["kind"]:
                raise ValueError("existing Bridge has conflicting reference identity")
            exact.append(row["reference_id"])
    archive_ids = {r["statement_id"] for r in manifest["assertions"]}
    if any(link.assertion_id in archive_ids for link in bridge.proof_links):
        raise ValueError("source-only assertion connected to a ProofStep")
    return {
        "bridge_reference_reused_count": len(exact),
        "bridge_reference_new_count": len(missing),
        "bridge_proof_link_count_unchanged": len(bridge.proof_links),
        "source_only_proof_link_count": 0,
    }


def write_outputs(manifest: dict, reconcile: dict, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = {
        "phase": manifest["phase"], "reference_count": manifest["reference_count"],
        "assertion_count": manifest["assertion_count"],
        "number_review_count": manifest["number_review_count"],
        "mathematical_semantics_verified_count": 0,
        "production_registry_modified": False, "proof_search_connected": False,
        "full_suite_run": False, **reconcile,
    }
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = ["# Phase 163 R4-R94：原文登録台帳の掲載順確定", "",
              "第1〜5章 TeX の原文保存用台帳：Reference 108件、Assertion 117件。", "",
              "原著の掲載順や数学的内容を認定したものではない。", "",
              "既存IDは不変。第1〜5章の現在の TeX 内の位置から掲載順を確定。", "",
              f"既存BridgeとReferenceが一致するもの：{reconcile['bridge_reference_reused_count']}件。", "",
              "番号未確認8件は変更しない。", "",
              "| 文献順 | 種別 | Source ID | Reference | 命題内順 |",
              "|---:|---|---|---|---:|"]
    for row in manifest["assertions"]:
        cp = row["component_position"]
        report.append(f"| {row['publication_position']} | {row['kind']} | `{row['statement_id']}` | {row['locator']} | {cp if cp is not None else '—'} |")
    report.extend(["", "原文台帳以外の実装は変更していない。証明探索への接続なし。", ""])
    (out / "report.md").write_text("\n".join(report), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    audit = json.loads(args.audit.read_text(encoding="utf-8"))
    from phase163_r4_r93_source_completion.r93_source_completion import classify_gap
    completion = classify_gap(catalog, audit, args.source_dir)
    manifest = finalize_manifest(catalog, audit, completion)
    registry = build_ordered_registry(manifest)
    if len(registry.assertions_for("toda:Proposition 1.2")) != 6:
        raise ValueError("Proposition 1.2 component count mismatch")
    reconcile = reconcile_bridge(manifest)
    write_outputs(manifest, reconcile, args.output)
    print(json.dumps({"phase": "163 R4-R94", "reference_count": 108,
                      "assertion_count": 117, "number_review_count": 8,
                      "mathematical_semantics_verified_count": 0,
                      "production_registry_modified": False, "proof_search_connected": False,
                      "full_suite_run": False, **reconcile}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
