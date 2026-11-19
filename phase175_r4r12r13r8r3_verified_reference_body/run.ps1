param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$package = Join-Path $repo 'phase175_r4r12r13r8r3_verified_reference_body'
if ($DryRun) {
    & python -B (Join-Path $package 'installer.py') --root $repo --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R13R8R3 guarded DryRun failed' }
    Write-Output 'PHASE175_R13R8R3_GATE=DRYRUN_PASS'
    exit 0
}
& python -B (Join-Path $package 'installer.py') --root $repo
if ($LASTEXITCODE -ne 0) { throw 'R13R8R3 patch failed' }
& python -B -m pytest -q -p no:cacheprovider (Join-Path (Join-Path $package 'tests') 'test_verified_reference.py')
if ($LASTEXITCODE -ne 0) { throw 'R13R8R3 focused tests failed' }
& git diff --check
if ($LASTEXITCODE -ne 0) { throw 'Git diff whitespace check failed' }
Write-Output 'PHASE175_R13R8R3_GATE=REFERENCE_BODIES_TESTED_PREFIX_NOT_YET_AUDITED'
