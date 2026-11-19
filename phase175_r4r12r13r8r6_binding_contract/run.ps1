param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$package = Join-Path $repo 'phase175_r4r12r13r8r6_binding_contract'
$test = Join-Path (Join-Path $package 'tests') 'test_contract.py'
if (-not (Test-Path (Join-Path $package 'audit.py'))) {
    throw 'Run from ehp_proof repository root.'
}
if ($DryRun) {
    & python -B -m phase175_r4r12r13r8r6_binding_contract.audit --root $repo --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R13R8R6 DryRun failed' }
    exit 0
}
& python -B -m pytest -q -p no:cacheprovider $test
if ($LASTEXITCODE -ne 0) { throw 'R13R8R6 focused pytest failed' }
& python -B -m phase175_r4r12r13r8r6_binding_contract.audit --root $repo
if ($LASTEXITCODE -ne 0) { throw 'R13R8R6 contract audit failed; inspect report' }
& git diff --check
if ($LASTEXITCODE -ne 0) { throw 'R13R8R6 diff check failed' }
Write-Output 'PHASE175_R13R8R6_PRODUCTION_UNCHANGED=PASS'
