# Phase 163 R4-R9 — audit import path repair

## 変更対象

- `phase163_r4_r9_declaration_catalog/audit.py`：import に `sys` を追加し、実行開始時に `Path.cwd().resolve()` を `sys.path` へ追加。監査本体は変更なし。
- `phase163_r4_r9_declaration_catalog/run.ps1`：修正版 `audit.py` の実行、既存 R8・R9 の軽量テスト16件、必要ファイル事前確認。既存プロジェクト内のコードは変更しない。

## 配置

既存の `phase163_r4_r9_declaration_catalog` フォルダを上書きする。同フォルダ内の R9 本体およびテストは削除しない。

## 差し替え対象の import 全文

```python
from __future__ import annotations

import json
from pathlib import Path
import sys

# The audit is executed from this package directory, whereas project modules
# are installed in the current project root by run.ps1.
PROJECT_ROOT = Path.cwd().resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from phase163_r4_registry_bridge import build_registry_bridge
from phase163_r4_r8_choice_registration import build_nu_prime_choice
from phase163_r4_r9_declaration_catalog import adapt_r8_snapshot
from probes.probe_phase58_capabilities import build_phase58_representative_result
```

## 修正範囲と完了条件

- `ModuleNotFoundError` を解消し、監査が `phase163_r4_r9_output/report.md` と `summary.json` を保存すること。
- `python -B -m pytest -q tests/test_phase163_r4_r8_choice_registration.py tests/test_phase163_r4_r9_declaration_catalog.py` が PASS すること。
- 全体 pytest は実行しない。次の Phase に属する実登録は追加しない。

## audit.py 完全版

```python
"""Read-only Phase 163 R4-R9 catalog demonstration using actual R8 choice."""
from __future__ import annotations

import json
from pathlib import Path
import sys

# The audit is executed from this package directory, whereas project modules
# are installed in the current project root by run.ps1.
PROJECT_ROOT = Path.cwd().resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from phase163_r4_registry_bridge import build_registry_bridge
from phase163_r4_r8_choice_registration import build_nu_prime_choice
from phase163_r4_r9_declaration_catalog import adapt_r8_snapshot
from probes.probe_phase58_capabilities import build_phase58_representative_result


def main() -> None:
    base = build_registry_bridge()
    selection = build_phase58_representative_result()["bracket_membership_step"]
    catalog = adapt_r8_snapshot(build_nu_prime_choice(base, selection))
    choice = catalog.declarations[0]
    record = next(x for x in base.records if x.assertion_id == choice.assertion_id)
    summary = {
        "phase": "163 R4-R9",
        "declarations": len(catalog.declarations),
        "kind": choice.kind.value,
        "reference_id": choice.reference_id,
        "assertion_id": choice.assertion_id,
        "defined_symbol": choice.defined_symbol,
        "index": choice.content.bracket.index,
        "coefficient": choice.content.bracket.second.coefficient,
        "source_verification": choice.provenance.value,
        "original_bridge_status": record.status.value,
        "definition_fixture_only": True,
        "citation_eligibility_granted": False,
        "full_pytest": "not_run",
    }
    destination = Path("phase163_r4_r9_output")
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report = "\n".join((
        "# Phase 163 R4-R9 — Definition / Choice 共通登録モデル", "",
        r"- Choice: $\nu'\in\{\eta_3,2\iota_4,\eta_4\}_1$", 
        "- (5.3) の Choice を既存の R8 から型付きで移送: 1件",
        "- 登録状態: source_unverified（引用許可なし）",
        "- 元の Bridge: metadata_only（変更なし）",
        "- Definition の独立した登録 API: 軽量テストの架空出典だけで確認",
        "- 他の文献 Definition の実登録: 未実施",
        "- 数学的同一性、原典の検証、Proof Search / Renderer 接続: 未実施",
        "- 全体 pytest: 未実施", "",
    ))
    (destination / "report.md").write_text(report, encoding="utf-8")
    print("Phase 163 R4-R9:", summary["declarations"], "choice declaration; bridge:", record.status.value)
    print("Saved phase163_r4_r9_output/report.md; full pytest not run.")


if __name__ == "__main__":
    main()

```

## run.ps1 完全版

```powershell
$ErrorActionPreference = 'Stop'
$ProjectRoot = (Get-Location).Path
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Required = @(
  'unified_statement_registry.py',
  'phase163_r4_registry_bridge.py',
  'phase163_r4_r8_choice_registration.py',
  'phase163_r4_r9_declaration_catalog.py',
  'proof.py',
  'expression.py',
  'toda_rules.py',
  'phase162_reference_boundary.py'
)
foreach ($Filename in $Required) {
  if (-not (Test-Path (Join-Path $ProjectRoot $Filename))) {
    throw "Required file is missing from project root: $Filename"
  }
}
if (-not (Test-Path (Join-Path $ProjectRoot 'tests'))) {
  throw 'Project tests folder is missing.'
}
& python -B -m pytest -q tests/test_phase163_r4_r8_choice_registration.py tests/test_phase163_r4_r9_declaration_catalog.py
if ($LASTEXITCODE -ne 0) { throw 'R4-R8/R9 focused pytest failed; audit skipped.' }
& python -B (Join-Path $PackageRoot 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-R9 audit failed.' }
Write-Host 'Phase 163 R4-R9 audit import path fixed. Full suite not run.'

```
