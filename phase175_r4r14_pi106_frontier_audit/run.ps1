param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$package = Join-Path $repo 'phase175_r4r14_pi106_frontier_audit'
if (-not (Test-Path (Join-Path $package 'audit.py'))) { throw 'Run from ehp_proof repository root.' }
if ($DryRun) {
    & python -B -m phase175_r4r14_pi106_frontier_audit.audit --root $repo --dry-run
} else {
    & python -B -m phase175_r4r14_pi106_frontier_audit.audit --root $repo
}
if ($LASTEXITCODE -ne 0) { throw 'R4R14 source/live audit failed' }
if ($DryRun) { exit 0 }
& python -B -m pytest -q -p no:cacheprovider `
  (Join-Path $package 'tests/test_audit.py') `
  'phase174_r3_r7_r12_toda59_annihilator_source/tests/test_rule.py' `
  'phase174_r3_r7_r3_ehp_zero_rule/tests/test_rule.py' `
  'phase174_r3_r7_r14_public_annihilator_connection/tests/test_public.py'
if ($LASTEXITCODE -ne 0) { throw 'R4R14 focused pytest failed' }
& git diff --check
if ($LASTEXITCODE -ne 0) { throw 'R4R14 diff check failed' }
Write-Output 'PHASE175_R4R14_PRODUCTION_UNCHANGED=PASS'
