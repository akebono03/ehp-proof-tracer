param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$package = Join-Path $repo 'phase175_r4r12r13r8r5_reference_binding_audit'
$audit = Join-Path $package 'audit.py'
$test = Join-Path (Join-Path $package 'tests') 'test_audit.py'
if (-not (Test-Path $audit) -or -not (Test-Path $test)) {
    throw 'Run this script from the ehp_proof repository root.'
}
if ($DryRun) {
    & python -B -m phase175_r4r12r13r8r5_reference_binding_audit.audit --root $repo --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R13R8R5 DryRun source guard failed' }
    Write-Output 'PHASE175_R13R8R5_DRYRUN=PASS'
    exit 0
}
& python -B -m pytest -q -p no:cacheprovider $test
if ($LASTEXITCODE -ne 0) { throw 'R13R8R5 focused tests failed' }
& python -B -m phase175_r4r12r13r8r5_reference_binding_audit.audit --root $repo --targets '5:4,6:5,7:5'
if ($LASTEXITCODE -ne 0) { throw 'R13R8R5 live binding audit failed' }
& git diff --check
if ($LASTEXITCODE -ne 0) { throw 'R13R8R5 diff check failed' }
Write-Output 'PHASE175_R13R8R5_SOURCE_UNCHANGED=PASS'
