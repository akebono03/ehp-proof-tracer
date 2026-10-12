$ErrorActionPreference = 'Stop'
$Root = (Get-Location).Path
$Package = $PSScriptRoot
$R86 = Join-Path $Root 'phase163_r4_r86_output\claim_review_catalog.json'
$R87 = Join-Path $Root 'phase163_r4_r87_output\semantic_registration_gate.json'
if (-not (Test-Path $R86)) { throw "R86 output missing: $R86" }
if (-not (Test-Path $R87)) { throw "R87 output missing: $R87" }
python (Join-Path $Package 'phase163_r4_r88_verify_snapshots.py') `
  --r86 $R86 `
  --r87 $R87 `
  --snapshot-r86 (Join-Path $Package 'r86_claim_review_snapshot.json') `
  --snapshot-r87 (Join-Path $Package 'r87_semantic_gate_snapshot.json')
if ($LASTEXITCODE -ne 0) { throw 'R88 reviewed JSON data verification failed' }
$env:PYTHONPATH = "$Package;$Root;$env:PYTHONPATH"
python -m pytest -q `
  (Join-Path $Package 'tests\test_phase163_r4_r88_claim_conditions.py') `
  (Join-Path $Package 'tests\test_phase163_r4_r88_verify_snapshots.py')
if ($LASTEXITCODE -ne 0) { throw 'R88 focused pytest failed' }
python (Join-Path $Package 'phase163_r4_r88_claim_conditions.py') `
  --r86 $R86 `
  --r87 $R87 `
  --output (Join-Path $Root 'phase163_r4_r88_output')
if ($LASTEXITCODE -ne 0) { throw 'R88 validation failed' }
Write-Host 'R88 corrected JSON integrity check complete. No production changes; full pytest not run.'
