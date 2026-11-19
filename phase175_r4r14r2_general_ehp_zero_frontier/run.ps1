param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$package = Join-Path $repo 'phase175_r4r14r2_general_ehp_zero_frontier'
if (-not (Test-Path (Join-Path $package 'audit.py'))) {
    throw 'Run from ehp_proof repository root.'
}
& python -B -m phase175_r4r14r2_general_ehp_zero_frontier.audit --root $repo $(if ($DryRun) { '--dry-run' })
if ($LASTEXITCODE -ne 0) { throw 'R4R14R2 source audit failed' }
if ($DryRun) { exit 0 }
& python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
  (Join-Path $package 'tests/test_audit.py') `
  (Join-Path $repo 'phase174_r3_r7_r12_toda59_annihilator_source/tests/test_rule.py') `
  (Join-Path $repo 'phase174_r3_r7_r3_ehp_zero_rule/tests/test_rule.py')
if ($LASTEXITCODE -ne 0) { throw 'R4R14R2 focused pytest failed' }
& git diff --check
if ($LASTEXITCODE -ne 0) { throw 'R4R14R2 git diff check failed' }
Write-Output 'PHASE175_R4R14R2_FOCUSED_TESTS=PASS'
Write-Output 'PHASE175_R4R14R2_PRODUCTION_UNCHANGED=PASS'
