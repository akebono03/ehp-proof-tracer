param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$python = if (Test-Path '.\.venv\Scripts\python.exe') { '.\.venv\Scripts\python.exe' } else { 'python' }
$patch = '.\phase175_r4r12r1r1_tracked_cache_guard_fix\patch.py'
& $python -m pytest -q .\phase175_r4r12r1r1_tracked_cache_guard_fix\tests\test_patch.py
if ($LASTEXITCODE -ne 0) { throw 'R4R12R1 focused patch tests failed' }
$argsList = @($patch, '--root', $root)
if ($DryRun) { $argsList += '--dry-run' }
& $python @argsList
if ($LASTEXITCODE -ne 0) { throw 'R4R12R1 correction failed' }
if (-not $DryRun) {
    powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase175_r4r12_public_two_summand_quotient\run.ps1' -DryRun
    if ($LASTEXITCODE -ne 0) { throw 'R4R12 DryRun failed after correction' }
    powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase175_r4r12_public_two_summand_quotient\run.ps1'
    if ($LASTEXITCODE -ne 0) { throw 'R4R12 execution failed after correction' }
    git diff --check
    if ($LASTEXITCODE -ne 0) { throw 'git diff --check failed' }
    git status -sb
}
