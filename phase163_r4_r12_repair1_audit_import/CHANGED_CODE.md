# Phase 163 R4-R12 repair1 — complete changed files

## audit.py

```python
"""Read-only literature statement registration audit for Proposition 5.1/5.3."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) in sys.path:
    sys.path.remove(str(ROOT))
sys.path.insert(0, str(ROOT))

from phase163_r4_registry_bridge import build_registry_bridge
from phase163_r4_r12_literature_registration import (
    COMPONENTS, existing_prop51_prop53_candidates,
    register_prop51_prop53_literature_statements,
)


def run_audit(directory: Path) -> dict[str, object]:
    base = build_registry_bridge()
    result = register_prop51_prop53_literature_statements(
        base, existing_prop51_prop53_candidates()
    )
    targets = {e.assertion_id for e in result.evidence}
    unchanged_original = all(
        r.status.value == "metadata_only" for r in base.records if r.assertion_id in targets
    )
    output = {
        "phase": "163 R4-R12",
        "status": "TYPED_SOURCE_UNVERIFIED",
        "registered_count": len(result.evidence),
        "counts_by_reference": {
            locator: len(keys) for locator, keys in COMPONENTS.items()
        },
        "proof_status": "PROOF_ANCESTRY_NOT_CHECKED",
        "proof_links_unchanged": result.snapshot.proof_links == base.proof_links,
        "base_metadata_unchanged": unchanged_original,
        "evidence": [
            {
                "assertion_id": e.assertion_id,
                "source_description": e.source_description,
                "verification_status": e.verification_status,
                "proof_status": e.proof_status,
            }
            for e in result.evidence
        ],
    }
    if len(result.evidence) != 8 or not output["proof_links_unchanged"] or not unchanged_original:
        raise RuntimeError("Proposition 5.1/5.3 registration audit failed")
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "summary.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Phase 163 R4-R12 — Proposition 5.1 / 5.3 の型付き登録",
        "", "状態: TYPED_SOURCE_UNVERIFIED（原典照合は未実施）", "",
        "| 文献 | 成分 | 登録 | 出典検証 | 証明木検証 |",
        "|---|---|---|---|---|",
    ]
    for entry in result.evidence:
        locator, component = entry.assertion_id.removeprefix("boundary:").rsplit(":", 1)
        lines.append(
            f"| {locator} | `{component}` | STRUCTURED | {entry.verification_status} | {entry.proof_status} |"
        )
    lines.extend([
        "", "生成元・型付き範囲は R4-R12 の検証で確認。",
        "Proposition 5.1 の高次部分は境界 metadata の n >= 3 を型付き宣言として保持。",
        "Proposition 5.3 の高次部分は n >= 5 を型付き宣言として保持。",
        "出典の数学的正しさや証明成立を示すものではありません。",
        "全体 pytest は実施していません。", "",
    ])
    (directory / "report.md").write_text("\n".join(lines), encoding="utf-8")
    return output


if __name__ == "__main__":
    output = run_audit(Path("phase163_r4_r12_output"))
    print(f"Phase 163 R4-R12: {output['status']} {output['registered_count']}")
    print("Saved phase163_r4_r12_output/report.md")
    print("Full pytest not run.")
```

## tests/test_phase163_r4_r12_audit_import.py

```python
"""Regression test: packaged audit must import the installed project module."""
import os
from pathlib import Path
import subprocess
import sys


def test_packaged_audit_imports_project_root_registration_module():
    project_root = Path(__file__).resolve().parents[1]
    audit_path = project_root / "phase163_r4_r12_prop51_prop53" / "audit.py"
    assert audit_path.is_file()
    command = (
        "import runpy, sys; "
        "from pathlib import Path; "
        f"runpy.run_path({str(audit_path)!r}, run_name='audit_import_probe'); "
        "module = sys.modules['phase163_r4_r12_literature_registration']; "
        f"assert Path(module.__file__).resolve() == Path({str(project_root / 'phase163_r4_r12_literature_registration.py')!r}) "
        "and Path(module.__file__).is_file()"
    )
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(project_root)
    result = subprocess.run(
        [sys.executable, "-B", "-c", command],
        cwd=project_root,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
```

## run.ps1

```powershell
$ErrorActionPreference = 'Stop'
$ProjectRoot = (Get-Location).Path
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$OriginalPackage = Join-Path $ProjectRoot 'phase163_r4_r12_prop51_prop53'
$Required = @(
  'phase163_r4_r12_literature_registration.py',
  'phase163_r4_registry_bridge.py',
  'tests\test_phase59_prop53_integration.py',
  'tests\test_phase163_r4_r12_literature_registration.py',
  'phase163_r4_r12_prop51_prop53\audit.py'
)
foreach ($Filename in $Required) {
  if (-not (Test-Path (Join-Path $ProjectRoot $Filename))) {
    throw "Missing required project file: $Filename"
  }
}
Copy-Item -LiteralPath (Join-Path $PackageRoot 'audit.py') -Destination (Join-Path $OriginalPackage 'audit.py') -Force
Copy-Item -LiteralPath (Join-Path $PackageRoot 'tests\test_phase163_r4_r12_audit_import.py') -Destination (Join-Path $ProjectRoot 'tests\test_phase163_r4_r12_audit_import.py') -Force
& python -B -m pytest -q tests/test_phase163_r4_r12_literature_registration.py tests/test_phase163_r4_r12_audit_import.py
if ($LASTEXITCODE -ne 0) { throw 'R4-R12 focused tests failed; audit skipped.' }
$env:PYTHONPATH = "$ProjectRoot$([System.IO.Path]::PathSeparator)$env:PYTHONPATH"
& python -B (Join-Path $OriginalPackage 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-R12 typed literature registration audit failed.' }
Write-Host 'R4-R12 repair1 audit import resolved. Full suite not run.'
```
