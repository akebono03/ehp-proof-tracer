# Phase 173 R3 停止点表示 — コード全文

## 対象ファイル・関数

- 新規 `phase173_r3_frontier_readout/readout.py`: `default_report_path`, `load_report`, `format_report`, `main`
- 新規 `phase173_r3_frontier_readout/tests/test_readout.py`: テスト全体
- 新規 `phase173_r3_frontier_readout/run.ps1`: 実行スクリプト全体

既存ファイル、既存クラス・関数・import は変更しない。

## __init__.py

```python
"""Read-only post-processing of the already completed Phase 173 R3 audit."""
```

## readout.py

```python
"""Summarize the existing Phase 173 R3 audit report; never run proof search."""
from __future__ import annotations

import json
import os
from pathlib import Path

EXPECTED_HEAD = "10f77860a5631d363d606e76b8c1f12ee6c500d5"
TARGETS = ((4, 3), (5, 3))


def default_report_path() -> Path:
    local_appdata = os.environ.get("LOCALAPPDATA")
    if not local_appdata:
        raise RuntimeError("LOCALAPPDATA is not available")
    return (
        Path(local_appdata)
        / "EHPProofTracerRecovery"
        / "phase173_r3_manual"
        / "audit.json"
    )


def load_report(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"R3 audit.json not found: {path}")
    report = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(report, dict):
        raise ValueError("R3 report must be an object")
    if report.get("head") != EXPECTED_HEAD:
        raise ValueError("R3 report was created from a different source HEAD")
    if report.get("mode") != "AUDIT_ONLY":
        raise ValueError("R3 report is not marked AUDIT_ONLY")
    rows = report.get("rows")
    if not isinstance(rows, list) or len(rows) != len(TARGETS):
        raise ValueError("Expected exactly two R3 report rows")
    if tuple((row.get("n"), row.get("k")) for row in rows) != TARGETS:
        raise ValueError("Unexpected R3 target coordinates")
    for row in rows:
        roots = row.get("roots")
        if not isinstance(roots, list):
            raise ValueError("Root list is missing")
        if row.get("root_candidate_count") != len(roots):
            raise ValueError("Root candidates are incomplete or truncated")
        if row.get("target_direct_given_count") != 0:
            raise ValueError("Target is incorrectly available as a direct GIVEN")
        if not isinstance(row.get("prior_sources"), list):
            raise ValueError("Prior source listing is missing")
        for root in roots:
            if not isinstance(root.get("rule"), str) or not isinstance(root.get("children"), list):
                raise ValueError("Malformed root/children record")
    return report


def format_report(report: dict) -> str:
    output = ["PHASE173_R3_FRONTIER_READOUT=AUDIT_ONLY"]
    for row in report["rows"]:
        output.append(
            f"TARGET pi_{row['n'] + row['k']}^{row['n']} "
            f"locator={row.get('source_locator')} "
            f"given={row.get('screened_given_count')} "
            f"roots={len(row['roots'])}"
        )
        for position, root in enumerate(row["roots"], start=1):
            output.append(f"  ROOT {position}: {root['rule']}")
            for child_index, child in enumerate(root["children"], start=1):
                count = child.get("child_proposal_count", "NOT_PROBED_DUPLICATE")
                direct = child.get("exact_screened_given", "NOT_PROBED_DUPLICATE")
                output.append(
                    f"    SUBGOAL {child_index}: {child.get('type')} "
                    f"proposals={count} exact_given={direct}"
                )
                for rule in child.get("child_proposal_rules", []):
                    output.append(f"      RULE: {rule}")
                if "child_probe_error" in child:
                    output.append(f"      PROBE_ERROR: {child['child_probe_error']}")
                output.append(f"      TARGET_REPR: {child.get('repr', '')}")
        for source in row["prior_sources"]:
            output.append(
                f"  PRIOR n={source.get('n')} k={source.get('k')} "
                f"eligible={source.get('eligible')} "
                f"stable_source={source.get('stable_source')} "
                f"reason={source.get('reason')}"
            )
    output.append("PHASE173_R3_FRONTIER_READOUT=PASS")
    output.append("OBSERVATION_IS_NOT_A_PROOF=True")
    return "\n".join(output)


def main() -> int:
    print(format_report(load_report(default_report_path())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## tests/test_readout.py

```python
"""Focused offline tests for the R3 report readout; no production imports."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from phase173_r3_frontier_readout.readout import (
    EXPECTED_HEAD,
    format_report,
    load_report,
)


def sample_report() -> dict:
    return {
        "head": EXPECTED_HEAD,
        "mode": "AUDIT_ONLY",
        "rows": [
            {
                "n": n,
                "k": 3,
                "source_locator": "Proposition 5.6",
                "screened_given_count": 26 if n == 4 else 27,
                "target_direct_given_count": 0,
                "root_candidate_count": 1 if n == 4 else 3,
                "roots": [
                    {
                        "rule": "mock inference candidate",
                        "children": [
                            {
                                "type": "Relation",
                                "repr": "Relation(mock)",
                                "child_proposal_count": 0,
                                "child_proposal_rules": [],
                                "exact_screened_given": False,
                            }
                        ],
                    }
                    for _ in range(1 if n == 4 else 3)
                ],
                "prior_sources": [
                    {
                        "n": 3,
                        "k": 3,
                        "eligible": True,
                        "reason": "prior_fixed_source",
                        "stable_source": False,
                    }
                ],
            }
            for n in (4, 5)
        ],
    }


def write_report(path: Path, data: dict) -> Path:
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_valid_report_formats_all_roots(tmp_path: Path) -> None:
    report = load_report(write_report(tmp_path / "audit.json", sample_report()))
    text = format_report(report)
    assert text.count("  ROOT ") == 4
    assert "pi_7^4" in text
    assert "pi_8^5" in text
    assert "proposals=0 exact_given=False" in text
    assert "OBSERVATION_IS_NOT_A_PROOF=True" in text


def test_missing_report_fails(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="not found"):
        load_report(tmp_path / "missing.json")


@pytest.mark.parametrize("field,value", [
    ("head", "unknown"),
    ("mode", "PROOF_COMPLETE"),
    ("rows", []),
])
def test_invalid_top_level_rejected(tmp_path: Path, field: str, value: object) -> None:
    data = sample_report()
    data[field] = value
    with pytest.raises(ValueError):
        load_report(write_report(tmp_path / "audit.json", data))


def test_direct_target_given_rejected(tmp_path: Path) -> None:
    data = sample_report()
    data["rows"][0]["target_direct_given_count"] = 1
    with pytest.raises(ValueError, match="direct GIVEN"):
        load_report(write_report(tmp_path / "audit.json", data))


def test_truncated_root_list_rejected(tmp_path: Path) -> None:
    data = sample_report()
    data["rows"][1]["roots"].pop()
    with pytest.raises(ValueError, match="truncated"):
        load_report(write_report(tmp_path / "audit.json", data))


def test_target_order_rejected(tmp_path: Path) -> None:
    data = sample_report()
    data["rows"].reverse()
    with pytest.raises(ValueError, match="coordinates"):
        load_report(write_report(tmp_path / "audit.json", data))


def test_malformed_root_rejected(tmp_path: Path) -> None:
    data = sample_report()
    data["rows"][0]["roots"][0]["children"] = None
    with pytest.raises(ValueError, match="Malformed"):
        load_report(write_report(tmp_path / "audit.json", data))


def test_duplicate_child_reports_unprobed(tmp_path: Path) -> None:
    data = sample_report()
    data["rows"][0]["roots"][0]["children"][0] = {
        "type": "Relation", "repr": "Relation(duplicate)"
    }
    text = format_report(load_report(write_report(tmp_path / "audit.json", data)))
    assert "NOT_PROBED_DUPLICATE" in text


def test_probe_error_reported(tmp_path: Path) -> None:
    data = sample_report()
    data["rows"][0]["roots"][0]["children"][0]["child_probe_error"] = "ValueError: x"
    text = format_report(load_report(write_report(tmp_path / "audit.json", data)))
    assert "PROBE_ERROR: ValueError: x" in text
```

## run.ps1

```powershell
param()
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Root
$env:PYTHONUTF8 = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
Write-Output 'PHASE173_R3_FRONTIER_FOCUSED_PYTEST_START'
python -B -m pytest -q -p no:cacheprovider '.\phase173_r3_frontier_readout\tests\test_readout.py'
if ($LASTEXITCODE -ne 0) { throw 'R3 frontier focused pytest failed' }
Write-Output 'PHASE173_R3_FRONTIER_FOCUSED_PYTEST=PASS'
python -B -m phase173_r3_frontier_readout.readout
if ($LASTEXITCODE -ne 0) { throw 'R3 frontier readout failed' }
git status -sb
```
