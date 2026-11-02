param(
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
Push-Location -LiteralPath $root
$oldPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = $root
    Write-Output 'PHASE173_R4_R1_CACHE_GUARD_FOCUSED_PYTEST_START'
    & python -m pytest -q -p no:cacheprovider '.\phase173_r4_r1_cache_guard_fix\tests\test_install.py'
    if ($LASTEXITCODE -ne 0) { throw 'Correction installer focused pytest failed' }
    Write-Output 'PHASE173_R4_R1_CACHE_GUARD_FOCUSED_PYTEST=PASS'

    $argsForInstall = @('.\phase173_r4_r1_cache_guard_fix\install.py', '--root', $root)
    if ($DryRun) { $argsForInstall += '--dry-run' }
    & python @argsForInstall
    if ($LASTEXITCODE -ne 0) { throw 'Correction installer rejected local files' }

    if ($DryRun) {
        Write-Output 'PHASE173_R4_R1_CACHE_GUARD_DRY_RUN=PASS_NO_INSTALL'
    }
    else {
        & powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_r4_r1_audit_only\run.ps1' -DryRun
        if ($LASTEXITCODE -ne 0) { throw 'Corrected source guard dry-run failed' }
        & powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_r4_r1_audit_only\run.ps1'
        if ($LASTEXITCODE -ne 0) { throw 'Corrected R4-R1 audit failed' }
        Write-Output 'PHASE173_R4_R1_CACHE_GUARD_CORRECTION=PASS'
    }
}
finally {
    $env:PYTHONPATH = $oldPythonPath
    Pop-Location
}
