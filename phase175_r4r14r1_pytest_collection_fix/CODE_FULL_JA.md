# R4R14R1 実行スクリプト全文

`run.ps1` の全文です。

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$audit = Join-Path $repo 'phase175_r4r14_pi106_frontier_audit\audit.py'
$tests = Join-Path $repo 'phase175_r4r14_pi106_frontier_audit\tests\test_audit.py'
if (-not (Test-Path $audit) -or -not (Test-Path $tests)) {
    throw 'R4R14 original audit package is required. Run from ehp_proof repository root.'
}
if ($DryRun) {
    & python -B -m phase175_r4r14_pi106_frontier_audit.audit --root $repo --dry-run
} else {
    & python -B -m phase175_r4r14_pi106_frontier_audit.audit --root $repo
}
if ($LASTEXITCODE -ne 0) { throw 'R4R14R1 source/live audit failed' }
if ($DryRun) {
    Write-Output 'PHASE175_R4R14R1_GATE=PASS_DRYRUN_SOURCE_GUARD'
    exit 0
}
& python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
    $tests `
    'phase174_r3_r7_r12_toda59_annihilator_source/tests/test_rule.py' `
    'phase174_r3_r7_r3_ehp_zero_rule/tests/test_rule.py' `
    'phase174_r3_r7_r14_public_annihilator_connection/tests/test_public.py'
if ($LASTEXITCODE -ne 0) { throw 'R4R14R1 focused pytest failed' }
& git diff --check
if ($LASTEXITCODE -ne 0) { throw 'R4R14R1 diff check failed' }
Write-Output 'PHASE175_R4R14R1_GATE=PASS_SOURCE_AND_FOCUSED_TESTS'
Write-Output 'PHASE175_R4R14R1_PRODUCTION_UNCHANGED=PASS'
```
