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
    python -B -m phase177_r10_composition_associativity_isolated.audit
    if ($LASTEXITCODE -ne 0) { throw 'Phase177 R10 preflight failed' }
    if ($DryRun) {
        Write-Output 'PHASE177_R10_GATE=PASS_R10_READ_ONLY_DRYRUN'
    } else {
        python -B -m pytest -q -s --import-mode=importlib -p no:cacheprovider phase177_r10_composition_associativity_isolated/tests phase174_r3_r7_r9_composition_associativity/tests/test_rule.py phase177_r8_unsigned_delta_public/tests/test_public.py
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R10 focused tests failed' }
        python -B -m phase177_r10_composition_associativity_isolated.audit
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R10 postflight failed' }
        git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R10 git diff check failed' }
        Write-Output 'PHASE177_R10_NEW_MATH_RULES=1'
        Write-Output 'PHASE177_R10_NEW_GIVEN=0'
        Write-Output 'PHASE177_R10_PUBLIC_CONNECTION=NOT_ADDED'
        Write-Output 'PHASE177_R10_FULL_PYTEST=NOT_RUN'
        Write-Output 'PHASE177_R10_GATE=PASS_R10_GENERAL_COMPOSITION_ASSOCIATIVITY_ISOLATED'
    }
} finally {
    $env:PYTHONDONTWRITEBYTECODE = $previousBytecode
    $env:PYTHONUTF8 = $previousUtf8
    Pop-Location
}
