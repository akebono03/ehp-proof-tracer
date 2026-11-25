param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $folder
Push-Location $root
$previousBytecode = $env:PYTHONDONTWRITEBYTECODE
$previousUtf8 = $env:PYTHONUTF8
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONUTF8 = '1'
    $before = @(git status --porcelain --untracked-files=all) -join "`n"
    if ($LASTEXITCODE -ne 0) { throw 'git status failed' }
    if ($DryRun) {
        python -B -m phase177_r3_unsigned_delta_composition_isolated.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R3 DryRun failed' }
    } else {
        python -B -m phase177_r3_unsigned_delta_composition_isolated.audit
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R3 preflight failed' }
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase177_r3_unsigned_delta_composition_isolated/tests phase175_r4r7_prop25_typed_composition/tests/test_rule.py
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R3 focused tests failed' }
        python -B -m phase177_r3_unsigned_delta_composition_isolated.audit
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R3 postflight failed' }
        $after = @(git status --porcelain --untracked-files=all) -join "`n"
        if ($LASTEXITCODE -ne 0 -or $before -cne $after) { throw 'Phase177 R3 repository status changed' }
        Write-Output 'PHASE177_R3_GATE=PASS_R3_UNSIGNED_DELTA_COMPOSITION_ISOLATED'
    }
} finally {
    $env:PYTHONDONTWRITEBYTECODE = $previousBytecode
    $env:PYTHONUTF8 = $previousUtf8
    Pop-Location
}
