param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$python = if (Test-Path '.\.venv\Scripts\python.exe') { '.\.venv\Scripts\python.exe' } else { 'python' }
$patch = '.\phase175_r4r12r1r2_prior_fixture_fix\patch.py'
& $python -m pytest -q .\phase175_r4r12r1r2_prior_fixture_fix\tests\test_patch.py
if ($LASTEXITCODE -ne 0) { throw 'R4R12R1R2 patch regression tests failed' }
$argsList = @($patch, '--root', $root)
if ($DryRun) { $argsList += '--dry-run' }
& $python @argsList
if ($LASTEXITCODE -ne 0) { throw 'R4R12R1R2 test fixture patch failed' }
if (-not $DryRun) {
    powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase175_r4r12_public_two_summand_quotient\run.ps1' -DryRun
    if ($LASTEXITCODE -ne 0) { throw 'R4R12 DryRun failed after test correction' }
    powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase175_r4r12_public_two_summand_quotient\run.ps1'
    if ($LASTEXITCODE -ne 0) { throw 'R4R12 execution failed after test correction' }
    git diff --check
    if ($LASTEXITCODE -ne 0) { throw 'git diff --check failed' }
    git status -sb
}
