$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$original = Join-Path $root 'phase165_r6_2_unified_registry_r4_r4	est_r4_r4_integration.py'
$replacement = Join-Path $PSScriptRoot 'test_r4_r4_integration.py'
if (-not (Test-Path $original)) { throw 'Original integration test is missing' }
$old = Get-Content $original -Raw -Encoding UTF8
if ($old -notmatch 'premise = ProofStep\(') { throw 'Unexpected integration test file' }
if ($old -notmatch 'premises=\(\), rule=ProofRule.GIVEN') {
  if ($old -notmatch 'premise = ProofStep\(conclusion=IsomorphismStatement\(map="f"\), rule=ProofRule.GIVEN\)') {
    throw 'Test differs from expected R4-4 version; refusing overwrite'
  }
  Copy-Item $original ($original + '.before_test_fix.bak') -Force
  Copy-Item $replacement $original -Force
}
Push-Location $root
try {
  python -m pytest -q (Join-Path $PSScriptRoot 'test_test_fix.py')
  if ($LASTEXITCODE -ne 0) { throw 'Fix unit tests failed' }
  python -m pytest -q (Join-Path $root 'phase165_r6_2_unified_registry_r4_r4	est_r4_r4_integration.py') tests/test_phase165_r8_rule_provider.py
  if ($LASTEXITCODE -ne 0) { throw 'Targeted regression failed' }
  Write-Output 'R4-4 integration test corrected; production math unchanged; full pytest NOT run.'
} finally { Pop-Location }
