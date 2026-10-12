# R95 complete added code

## Added files

- `phase163_r4_r95_phase_closure/r95_phase_closure.py`
- `phase163_r4_r95_phase_closure/tests/test_r95_phase_closure.py`
- `phase163_r4_r95_phase_closure/run.ps1`
- `phase163_r4_r95_phase_closure/README.md`

Existing source files, imports, classes, methods, and the five root project documentation files are unchanged.

## New Python module (full)

```python
"""Phase 163 R4-R95: targeted-only, read-only archival closure audit.

Full pytest is explicitly forbidden here. This module never changes production
source, enables proof search, or promotes source-only mathematical statements.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def verify_manifest(manifest: dict) -> dict:
    """Validate archival identity, provenance, order and proof-ineligible gates."""
    if (manifest.get("phase") != "163 R4-R94"
            or manifest.get("mode") != "ORDERED_SOURCE_ONLY_MANIFEST"
            or manifest.get("reference_count") != 108
            or manifest.get("assertion_count") != 117
            or manifest.get("r91_count") != 96
            or manifest.get("r92_subitem_count") != 9
            or manifest.get("r93_added_count") != 12
            or manifest.get("number_review_count") != 8
            or manifest.get("publication_order_scope") != "SOURCE_TEX_ORDER_NOT_ORIGINAL_EDITION"
            or manifest.get("original_edition_verified") is not False
            or manifest.get("mathematical_semantics_verified_count") != 0
            or manifest.get("proof_eligible_count") != 0
            or manifest.get("production_registry_modified") is not False
            or manifest.get("proof_search_connected") is not False
            or manifest.get("full_suite_run") is not False):
        raise ValueError("R94 archive identity or safety gate mismatch")
    rows = manifest.get("assertions")
    if not isinstance(rows, list) or len(rows) != 117:
        raise ValueError("R94 assertion count mismatch")
    identifiers = set()
    reference_positions: dict[str, int] = {}
    parents: dict[str, dict] = {}
    subitems = []
    previous_key = (0, 0, 0, "")
    origin_counts = {"R91": 0, "R92": 0, "R93": 0}
    for row in rows:
        identifier = row["statement_id"]
        if identifier in identifiers:
            raise ValueError("duplicate Statement ID")
        identifiers.add(identifier)
        if sha256(row["source_text"]) != row["source_sha256"]:
            raise ValueError("source SHA-256 mismatch")
        if row["source_origin"] not in origin_counts:
            raise ValueError("unknown source origin")
        origin_counts[row["source_origin"]] += 1
        if row["chapter"] not in (1, 2, 3, 4, 5) or row["start_line"] < 1:
            raise ValueError("invalid source coordinates")
        component = row["component_position"]
        if component is not None and (not isinstance(component, int) or component < 1):
            raise ValueError("invalid component position")
        key = (row["chapter"], row["start_line"], component or 0, identifier)
        if key < previous_key:
            raise ValueError("out-of-order source entries")
        previous_key = key
        if row["source_origin"] == "R92":
            subitems.append(row)
            if component is None:
                raise ValueError("R92 subitem has no component position")
        else:
            if component is not None:
                raise ValueError("unexpected parent component position")
            if row["reference_id"] in reference_positions:
                raise ValueError("duplicate Reference ID")
            reference_positions[row["reference_id"]] = row["publication_position"]
            parents[identifier] = row
    if origin_counts != {"R91": 96, "R92": 9, "R93": 12}:
        raise ValueError("source origin counts differ")
    if len(reference_positions) != 108 or sorted(reference_positions.values()) != list(range(1, 109)):
        raise ValueError("Reference position sequence mismatch")
    children_by_parent: dict[str, list[int]] = {}
    for row in subitems:
        parent = parents.get(row["parent_statement_id"])
        if (parent is None or row["reference_id"] != parent["reference_id"]
                or row["publication_position"] != parent["publication_position"]
                or row["chapter"] != parent["chapter"]):
            raise ValueError("broken R92 parent-child crosswalk")
        children_by_parent.setdefault(row["parent_statement_id"], []).append(row["component_position"])
    for positions in children_by_parent.values():
        if sorted(positions) != list(range(1, len(positions) + 1)):
            raise ValueError("nonconsecutive component positions")
    if len(manifest.get("nested_aliases", [])) != 1 or len(manifest.get("duplicate_mentions", [])) != 1:
        raise ValueError("alias or mention count mismatch")
    alias = manifest["nested_aliases"][0]
    if (alias.get("status") != "NESTED_EQUATION_ALIAS_NO_NEW_ASSERTION"
            or alias.get("label") != "4.4"
            or alias.get("parent_source_id") not in parents
            or sha256(alias["source_text"]) != alias["source_sha256"]):
        raise ValueError("nested Equation (4.4) identity mismatch")
    mention = manifest["duplicate_mentions"][0]
    if (mention.get("status") != "CROSS_CHAPTER_MENTION_NO_NEW_ASSERTION"
            or mention.get("target_source_id") not in parents):
        raise ValueError("cross-chapter mention mismatch")
    reviews = manifest.get("number_reviews", [])
    if (len(reviews) != 8 or len({item["source_id"] for item in reviews}) != 8
            or any(item["source_id"] not in parents
                   or item["status"] != "UNVERIFIED_NUMBER_MAPPING_DO_NOT_RENAME"
                   for item in reviews)):
        raise ValueError("number review state changed")
    return {"reference_count": 108, "assertion_count": 117, "source_origin_counts": origin_counts,
            "number_review_count": 8, "nested_alias_count": 1, "duplicate_mention_count": 1}


def audit_closure(manifest: dict, catalog: dict, audit: dict, source_dir: Path) -> dict:
    """Independently regenerate R94 from the source inputs; reject any drift."""
    from phase163_r4_r93_source_completion.r93_source_completion import classify_gap
    from phase163_r4_r94_registry_finalization.r94_registry_finalization import (
        build_ordered_registry, finalize_manifest, reconcile_bridge,
    )
    measured = verify_manifest(manifest)
    rebuilt = finalize_manifest(catalog, audit, classify_gap(catalog, audit, source_dir))
    if manifest != rebuilt:
        raise ValueError("R94 manifest differs from reproducible source transcript")
    registry = build_ordered_registry(manifest)
    from unified_statement_registry import AssertionOrigin
    for row in manifest["assertions"]:
        entry = registry.assertion(row["statement_id"])
        if (entry.origin is not AssertionOrigin.SOURCE_ARCHIVE
                or entry.content["proof_eligible"] is not False
                or entry.content["mathematics_verified"] is not False
                or entry.available_after_position is not None):
            raise ValueError("source-only Assertion promoted")
    bridge = reconcile_bridge(manifest)
    if (bridge["bridge_reference_reused_count"] + bridge["bridge_reference_new_count"] != 108
            or bridge["source_only_proof_link_count"] != 0):
        raise ValueError("Bridge reconciliation failed")
    return {"phase": "163 R4-R95", "status": "PHASE163_CLOSED_SOURCE_ARCHIVE_ONLY",
            **measured, **bridge,
            "reproducible_manifest": True,
            "original_edition_verified": False,
            "mathematical_semantics_verified_count": 0,
            "proof_eligible_count": 0,
            "production_registry_modified": False,
            "proof_search_connected": False,
            "full_suite_run": False,
            "test_scope": "TARGETED_ONLY_NO_FULL_PYTEST",
            "deferred": ["8 uncertain number mappings", "Toda original-edition comparison",
                         "claim-by-claim mathematical certification",
                         "production proof-search connection", "full pytest not requested"],
            "next_phase": "164: pi_5^3 goal-driven ProofStep narrative"}


def write_outputs(report: dict, folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "closure.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Phase 163 終了記録（R95）", "",
             "第1〜5章の原文保存台帳を終了状態として固定する。数学的認定は行っていない。", "",
             f"- Reference: {report['reference_count']}件",
             f"- Assertion: {report['assertion_count']}件（R91 96件、R92 9件、R93 12件）",
             f"- 番号未確認: {report['number_review_count']}件",
             f"- Bridge 再利用: {report['bridge_reference_reused_count']}件",
             "- 原文照合: 現行日本語訳 TeX と再生成結果が一致（原著との一致は未認定）",
             "- 数学的認定: 0件、証明探索への新規接続: 0件",
             "- 本番ソース変更: なし", "- **全体 pytest: 実施しない（ユーザー指定）**", "",
             "## 未完了として引き継ぐ事項", "",
             "原著照合、番号未確認8件、個別の数学的認定、証明探索への接続は後続課題。", "",
             "## 次 Phase", "",
             "Phase 164 では $\\pi_5^3$ の goal-driven proof（目標逆向き証明）と ProofStep からの一般文章生成を再開する。", ""]
    (folder / "closure_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    audit = json.loads(args.audit.read_text(encoding="utf-8"))
    report = audit_closure(manifest, catalog, audit, args.source_dir)
    write_outputs(report, args.output)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

```

## New tests (full)

```python
"""R95 targeted-only closure tests. Never collect the full test suite."""
import copy
import json
from pathlib import Path

import pytest

from phase163_r4_r95_phase_closure.r95_phase_closure import (
    audit_closure, verify_manifest, write_outputs,
)

ROOT = Path(__file__).resolve().parents[2]
R94 = ROOT / "phase163_r4_r94_output" / "manifest.json"
CATALOG = ROOT / "phase163_r4_r91_output" / "source_catalog.json"
AUDIT = ROOT / "phase163_r4_r92_output" / "audit.json"
SOURCE = ROOT / "sources" / "toda"


@pytest.fixture(scope="module")
def manifest():
    return json.loads(R94.read_text(encoding="utf-8"))


def test_counts_and_origin_contract(manifest):
    out = verify_manifest(manifest)
    assert out["reference_count"] == 108
    assert out["assertion_count"] == 117
    assert out["source_origin_counts"] == {"R91": 96, "R92": 9, "R93": 12}


def test_all_statement_ids_unique(manifest):
    assert len({x["statement_id"] for x in manifest["assertions"]}) == 117


def test_subitem_order_and_parent_link(manifest):
    rows = {x["statement_id"]: x for x in manifest["assertions"]}
    assert len([x for x in rows.values() if x["source_origin"] == "R92"]) == 9
    for row in rows.values():
        if row["source_origin"] == "R92":
            assert row["reference_id"] == rows[row["parent_statement_id"]]["reference_id"]


def test_number_revisions_not_silently_promoted(manifest):
    assert verify_manifest(manifest)["number_review_count"] == 8
    assert manifest["original_edition_verified"] is False


def test_digest_tampering_rejected(manifest):
    wrong = copy.deepcopy(manifest)
    wrong["assertions"][0]["source_text"] += "changed"
    with pytest.raises(ValueError, match="SHA-256"):
        verify_manifest(wrong)


def test_duplicate_statement_id_rejected(manifest):
    wrong = copy.deepcopy(manifest)
    wrong["assertions"][1]["statement_id"] = wrong["assertions"][0]["statement_id"]
    with pytest.raises(ValueError, match="duplicate Statement ID"):
        verify_manifest(wrong)


def test_proof_promotion_rejected(manifest):
    wrong = copy.deepcopy(manifest)
    wrong["proof_eligible_count"] = 1
    with pytest.raises(ValueError, match="safety gate"):
        verify_manifest(wrong)


def test_rebuild_and_archival_only(manifest):
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    result = audit_closure(manifest, catalog, audit, SOURCE)
    assert result["reproducible_manifest"] is True
    assert result["proof_search_connected"] is False
    assert result["mathematical_semantics_verified_count"] == 0
    assert result["full_suite_run"] is False


def test_final_report_explicitly_excludes_full_pytest(manifest, tmp_path):
    out = {"reference_count": 108, "assertion_count": 117,
           "number_review_count": 8, "bridge_reference_reused_count": 23}
    write_outputs(out, tmp_path)
    assert json.loads((tmp_path / "closure.json").read_text(encoding="utf-8")) == out
    assert "全体 pytest: 実施しない" in (tmp_path / "closure_report.md").read_text(encoding="utf-8")

```

## Runner (full)

```powershell
$ErrorActionPreference = "Stop"
$Project = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $Project
$env:PYTHONPATH = $Project

# Explicitly selected tests only. NEVER run pytest without test paths.
python -m pytest -q `
  ".\phase163_r4_r95_phase_closure\tests\test_r95_phase_closure.py" `
  ".\phase163_r4_r94_registry_finalization\tests\test_r94_registry_finalization.py" `
  ".\tests\test_phase163_r2_unified_registry.py" `
  ".\tests\test_phase163_r4_registry_bridge.py"
if ($LASTEXITCODE -ne 0) { throw "R95 targeted tests failed" }

python -m phase163_r4_r95_phase_closure.r95_phase_closure `
  --manifest ".\phase163_r4_r94_output\manifest.json" `
  --catalog ".\phase163_r4_r91_output\source_catalog.json" `
  --audit ".\phase163_r4_r92_output\audit.json" `
  --source-dir ".\sources\toda" `
  --output ".\phase163_r4_r95_output"
if ($LASTEXITCODE -ne 0) { throw "R95 closure audit failed" }
Write-Output "R95 targeted-only closure completed; full pytest was NOT run."

```
