$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$originalFolder = Join-Path $root 'phase165_r6_2_unified_registry_r4_r4'
$original = Join-Path $originalFolder 'test_r4_r4_integration.py'
$replacement = Join-Path $PSScriptRoot 'test_r4_r4_integration.py'
if ($original -match '[\x00-\x1F]') { throw 'Invalid control character in test path' }
if (-not (Test-Path -LiteralPath $original -PathType Leaf)) { throw "Original integration test missing: $original" }
if (-not (Test-Path -LiteralPath $replacement -PathType Leaf)) { throw 'Replacement test missing' }
$old = Get-Content -LiteralPath $original -Raw -Encoding UTF8
if ($old -notmatch 'def test_forward_builder_kept\(') { throw 'Unexpected original test file' }
$fixed = $old -match 'premise\s*=\s*ProofStep\(conclusion=IsomorphismStatement\(map="f"\),\s*premises=\(\),\s*rule=ProofRule.GIVEN\)'
if (-not $fixed) {
  if ($old -notmatch 'premise\s*=\s*ProofStep\(conclusion=IsomorphismStatement\(map="f"\),\s*rule=ProofRule.GIVEN\)') {
    throw 'Test differs from expected R4-4 version; refusing overwrite'
  }
  $backup = $original + '.before_test_fix.bak'
  if (-not (Test-Path -LiteralPath $backup)) { Copy-Item -LiteralPath $original -Destination $backup }
  Copy-Item -LiteralPath $replacement -Destination $original -Force
}
Push-Location $root
try {
  python -m pytest -q (Join-Path $PSScriptRoot 'test_test_fix.py')
  if ($LASTEXITCODE -ne 0) { throw 'Fix unit tests failed' }
  python -m pytest -q $original 'tests/test_phase165_r8_rule_provider.py'
  if ($LASTEXITCODE -ne 0) { throw 'Targeted regression failed' }
  Write-Output 'R4-4 test path corrected; production math unchanged; full pytest NOT run.'
} finally { Pop-Location }
