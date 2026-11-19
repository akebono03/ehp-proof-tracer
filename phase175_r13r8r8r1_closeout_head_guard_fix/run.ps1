param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
if (-not (Test-Path (Join-Path $repo 'phase175_r4r12r13r8r6_binding_contract\audit.py'))) {
    throw 'Run from the ehp_proof repository root.'
}
$env:PYTHONDONTWRITEBYTECODE = '1'
& python -B -m phase175_r13r8r8r1_closeout_head_guard_fix.audit --root $repo $(if ($DryRun) { '--dry-run' })
if ($LASTEXITCODE -ne 0) { throw 'R13R8R8R1 audit failed' }
if ($DryRun) { exit 0 }
& python -B -m pytest -q -p no:cacheprovider `
    'phase175_r4r12r13r8r3_verified_reference_body/tests/test_verified_reference.py' `
    'phase175_r4r12r13r8r4_body_citation/tests/test_citation_prefix.py' `
    'phase175_r4r12r13r8r6_binding_contract/tests/test_contract.py'
if ($LASTEXITCODE -ne 0) { throw 'R13R8R8R1 focused pytest failed' }
& git diff --check
if ($LASTEXITCODE -ne 0) { throw 'R13R8R8R1 git diff check failed' }
Write-Output 'PHASE175_R13R8R8R1_FOCUSED_TESTS=PASS'
Write-Output 'PHASE175_R13R8R8R1_PRODUCTION_UNCHANGED=PASS'
