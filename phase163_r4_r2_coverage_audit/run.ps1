$ErrorActionPreference = 'Stop'
$Root = (Get-Location).Path
$Package = Split-Path -Parent $MyInvocation.MyCommand.Path
foreach ($required in @('proof.py', 'unified_statement_registry.py', 'phase163_r4_registry_bridge.py')) {
  if (-not (Test-Path (Join-Path $Root $required))) { throw "Missing prerequisite: $required. Run at repository root." }
}
$destination = Join-Path $Root 'phase163_r4_r2_coverage_audit.py'
$testDir = Join-Path $Root 'tests'
if (-not (Test-Path $testDir)) { throw 'tests directory not found' }
Copy-Item (Join-Path $Package 'phase163_r4_r2_coverage_audit.py') $destination -Force
Copy-Item (Join-Path $Package 'tests\test_phase163_r4_r2_coverage_audit.py') (Join-Path $testDir 'test_phase163_r4_r2_coverage_audit.py') -Force
python -m pytest -q tests/test_phase163_r4_r2_coverage_audit.py tests/test_phase163_r4_registry_bridge.py
if ($LASTEXITCODE -ne 0) { throw 'Focused tests failed' }
python phase163_r4_r2_coverage_audit.py
if ($LASTEXITCODE -ne 0) { throw 'Audit failed' }
Write-Host 'Phase 163 R4-R2 read-only coverage audit complete. Full suite not run.'
