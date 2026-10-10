# Phase 163 R4-R4 — 数学的役割候補の分類監査

## 変更対象（既存ファイルの変更なし）

- 新規 `phase163_r4_r4_role_classification.py`：`classify_site`, `classify_unlinked`, `build_classification`, `_write_csv`, `write_audit`, `main`。
- 新規 `tests/test_phase163_r4_r4_role_classification.py`：軽量テスト7件。
- `run.ps1`：ソースとテストのみをプロジェクトにコピーして実行。

## 方針

R4-R3 の現行ソースを再解析して、生成箇所を文献対応候補、Toda 未分類、非 Toda の一般規則候補、動的規則名の未確認に分ける。分類結果は数学的同一性を証明しない。文献との明示対応のない component は独立 CSV で扱う。Definition 全件、動的登録、証明完了位置の特定は対象外。

## 実行

`run.ps1` をプロジェクト直下から実行する。Python と pytest が既に利用可能であること、および R4-R3 の Python モジュール・テストがプロジェクト直下に存在することが必要。

## 完了条件

新規7件と R4-R3 既存6件の focused pytest が PASS し、`phase163_r4_r4_output` に `report.md`, `summary.json`, `role_candidates.csv`, `toda_unmapped.csv`, `unlinked_review.csv` が生成されること。全体 pytest は Phase 163 の終わりまで実施しない。

## 次 Phase との境界

候補の手動検証、Definition の出典照合、実際の構造化 Statement への対応、統一台帳への登録は R4 の後続作業。Backward Search は Phase 164。

## コード全文

以下のファイルがそのまま置換・追加できる全文です（抜粋ではありません）。

### `phase163_r4_r4_role_classification.py`

```python
"""Phase 163 R4-R4: conservative, read-only classification of rule sites.

All categories are evidence classes, not claims of mathematical equivalence.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path



FIELDS = ("file", "line", "rule_name", "mapping_status", "role_candidate",
          "evidence", "manual_review_required")


def classify_site(site: dict[str, object]) -> dict[str, object]:
    filename = str(site["file"])
    name = site.get("name")
    status = str(site["status"])
    if status == "listed_in_boundary_mapping":
        role = "literature_mapping_candidate"
        evidence = "rule name explicitly listed in boundary mapping"
    elif name is None or not str(name).strip():
        role = "dynamic_rule_name_unverified"
        evidence = "literal inference-rule name unavailable"
    elif filename == "toda_rules.py":
        role = "toda_rule_unclassified"
        evidence = "Toda rule name absent from boundary mapping"
    else:
        role = "general_inference_candidate"
        evidence = "non-Toda rule name absent from boundary mapping"
    return {"file": filename, "line": int(site["line"]),
            "rule_name": "" if name is None else str(name),
            "mapping_status": status, "role_candidate": role,
            "evidence": evidence, "manual_review_required": "yes"}


def classify_unlinked(component: dict[str, object]) -> dict[str, object]:
    return {"locator": str(component["locator"]),
            "component_key": str(component["key"]),
            "statement_role": str(component["role"]),
            "status": "unlinked_by_literal_name",
            "next_check": "inspect rule builders, structural statements and aliases",
            "mathematical_equivalence_confirmed": "no"}


def build_classification(mapping: dict[str, object]) -> dict[str, object]:
    sites = [classify_site(site) for site in mapping["rule_sites"]]
    unlinked = [classify_unlinked(item) for item in mapping["unlinked_components"]]
    names = {s["rule_name"] for s in sites if s["rule_name"]}
    todo = [s for s in sites if s["file"] == "toda_rules.py"
            and s["mapping_status"] == "not_listed_in_boundary_mapping"]
    return {"sites": sites, "unlinked": unlinked, "toda_unmapped": todo,
            "counts": {"total_sites": len(sites),
                       "role_candidates": dict(sorted(Counter(s["role_candidate"] for s in sites).items())),
                       "toda_unmapped_literal_sites": len(todo),
                       "unlinked_components": len(unlinked),
                       "distinct_literal_rule_names": len(names)}}


def _write_csv(path: Path, fields: tuple[str, ...], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_audit(root: Path, output: Path) -> dict[str, object]:
    """Use the checked-in R4-R3 scanner, not a copied heuristic."""
    boundary_path = root / "toda_literature_statement_boundary.py"
    rule_names = ("toda_rules.py", "hopf_rules.py", "stable_rules.py",
                  "ehp_rules.py", "scalar_rules.py", "relation_rules.py", "set_rules.py")
    missing = [name for name in ("toda_literature_statement_boundary.py", *rule_names)
               if not (root / name).is_file()]
    if missing:
        raise FileNotFoundError("required source files absent: " + ", ".join(missing))
    import phase163_r4_r3_statement_mapping as prior
    sources = {name: (root / name).read_text(encoding="utf-8-sig") for name in rule_names}
    mapping = prior.analyze(boundary_path.read_text(encoding="utf-8-sig"), sources)
    result = build_classification(mapping)
    output.mkdir(parents=True, exist_ok=True)
    _write_csv(output / "role_candidates.csv", FIELDS, result["sites"])
    _write_csv(output / "toda_unmapped.csv", FIELDS, result["toda_unmapped"])
    _write_csv(output / "unlinked_review.csv",
               ("locator", "component_key", "statement_role", "status", "next_check",
                "mathematical_equivalence_confirmed"), result["unlinked"])
    summary = {"audit": "Phase 163 R4-R4 conservative role classification",
               "counts": result["counts"], "source_files": list(rule_names),
               "missing_sources": missing,
               "limitations": [
                   "Role labels are candidates only, not verified theorem identities.",
                   "A constructor site is not an instantiated rule or a unique statement.",
                   "A non-Toda rule is not necessarily generic mathematics.",
                   "Unlisted Toda rules can be fixed statements, specializations, or helper rules.",
                   "No automatic conversion into Unified Statement Registry is performed.",
                   "Definitions and runtime registrations are not exhaustively audited.",
                   "Publication and proof-completion order remain unknown.",
                   "No proof search, renderer, or existing API is modified.",
               ]}
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Phase 163 R4-R4 — 数学的役割候補の分類監査", "",
             "## 候補数（命題数ではない）", "",
             f"- InferenceRule 生成箇所: {result['counts']['total_sites']}",
             f"- toda_rules.py の未掲載候補: {result['counts']['toda_unmapped_literal_sites']}",
             f"- 明示規則名への対応がない文献 component: {result['counts']['unlinked_components']}", "",
             "## 分類", ""]
    lines.extend(f"- {k}: {v}" for k, v in result["counts"]["role_candidates"].items())
    lines.extend(["", "## 制約", ""])
    lines.extend(f"- {s}" for s in summary["limitations"])
    lines.extend(["", "**全命題の統合・数学的同一性検証は未完了。**", "全体 pytest は未実施。", ""])
    (output / "report.md").write_text("\n".join(lines), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path.cwd() / "phase163_r4_r4_output")
    args = parser.parse_args()
    summary = write_audit(args.root, args.output)
    print("Phase 163 R4-R4 read-only role classification:", summary["counts"])
    print("Saved:", args.output / "report.md")
    print("No existing source changes; full pytest suite not run.")


if __name__ == "__main__":
    main()

```

### `tests/test_phase163_r4_r4_role_classification.py`

```python
import csv
from pathlib import Path

import pytest

from phase163_r4_r4_role_classification import (
    build_classification,
    classify_site,
    classify_unlinked,
    write_audit,
)


def test_mapped_rule_is_only_a_candidate():
    row = classify_site({"file": "toda_rules.py", "line": 5,
                         "name": "Toda example", "status": "listed_in_boundary_mapping"})
    assert row["role_candidate"] == "literature_mapping_candidate"
    assert row["manual_review_required"] == "yes"


def test_unmapped_toda_rule_is_not_automatically_generic():
    row = classify_site({"file": "toda_rules.py", "line": 8,
                         "name": "Toda unknown", "status": "not_listed_in_boundary_mapping"})
    assert row["role_candidate"] == "toda_rule_unclassified"


def test_non_toda_rule_is_candidate_only():
    row = classify_site({"file": "relation_rules.py", "line": 4,
                         "name": "composition", "status": "not_listed_in_boundary_mapping"})
    assert row["role_candidate"] == "general_inference_candidate"
    assert row["manual_review_required"] == "yes"


def test_dynamic_name_not_assigned_a_mathematical_role():
    row = classify_site({"file": "toda_rules.py", "line": 2,
                         "name": None, "status": "dynamic_name_unverified"})
    assert row["role_candidate"] == "dynamic_rule_name_unverified"


def test_unlinked_is_not_equivalent_to_missing_mathematical_statement():
    row = classify_unlinked({"locator": "(5.1)", "key": "k", "role": "OTHER"})
    assert row["mathematical_equivalence_confirmed"] == "no"
    assert row["status"] == "unlinked_by_literal_name"


def test_counts_preserve_constructor_site_unit():
    result = build_classification({"rule_sites": [
        {"file": "toda_rules.py", "line": 1, "name": "x", "status": "not_listed_in_boundary_mapping"},
        {"file": "toda_rules.py", "line": 2, "name": "x", "status": "not_listed_in_boundary_mapping"},
    ], "unlinked_components": []})
    assert result["counts"]["toda_unmapped_literal_sites"] == 2
    assert result["counts"]["distinct_literal_rule_names"] == 1


def test_requires_live_sources_without_fabrication(tmp_path):
    with pytest.raises(FileNotFoundError):
        write_audit(tmp_path, tmp_path / "out")

```

### `run.ps1`

```powershell
$ErrorActionPreference = "Stop"
$ProjectRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Copy-Item -Path (Join-Path $PackageDir "phase163_r4_r4_role_classification.py") -Destination (Join-Path $ProjectRoot "phase163_r4_r4_role_classification.py") -Force
$TestDir = Join-Path $ProjectRoot "tests"
if (-not (Test-Path $TestDir)) { New-Item -ItemType Directory -Path $TestDir | Out-Null }
Copy-Item -Path (Join-Path $PackageDir "tests\test_phase163_r4_r4_role_classification.py") -Destination (Join-Path $TestDir "test_phase163_r4_r4_role_classification.py") -Force
python -m pytest -q tests/test_phase163_r4_r3_statement_mapping.py tests/test_phase163_r4_r4_role_classification.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python phase163_r4_r4_role_classification.py --root "$ProjectRoot" --output (Join-Path $ProjectRoot "phase163_r4_r4_output")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Phase 163 R4-R4 focused tests complete. Full suite not run."

```
