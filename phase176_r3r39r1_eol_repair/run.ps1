param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $argsForPatch = @()
    if ($DryRun) { $argsForPatch += '--dry-run' }
    & python -B -m phase176_r3r39_public_equality_transport.apply @argsForPatch
    if ($LASTEXITCODE -ne 0) { throw 'R3R39R1 byte repair failed' }
    if ($DryRun) {
        Write-Host 'PHASE176_R3R39R1_GATE=PASS_R3R39R1_DRYRUN'
        return
    }
    & git diff --check
    if ($LASTEXITCODE -ne 0) { throw 'git diff check failed' }
    $stat = @(& git diff --numstat -- phase165_r52_r9_shared_math.py)
    if ($LASTEXITCODE -ne 0) { throw 'git diff numstat failed' }
    if ($stat.Count -ne 1 -or $stat[0] -notmatch '^9\t0\tphase165_r52_r9_shared_math\.py$') {
        throw ('Unexpected target diff: ' + ($stat -join '; '))
    }
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib .\phase176_r3r39r1_eol_repair\test_eol.py
    if ($LASTEXITCODE -ne 0) { throw 'EOL tests failed' }
    & powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_r3r39_public_equality_transport\run.ps1
    if ($LASTEXITCODE -ne 0) { throw 'R3R39 regression failed' }
    Write-Host 'PHASE176_R3R39R1_GATE=PASS_R3R39R1_MINIMAL_DIFF_FOCUSED_TESTS'
    Write-Host 'PHASE176_R3R39R1_FULL_PYTEST=NOT_RUN'
} finally {
    Pop-Location
}
