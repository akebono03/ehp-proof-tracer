param(
    [switch]$DryRun,
    [int]$TimeoutSeconds = 300
)

$ErrorActionPreference = 'Stop'
# Enforce UTF-8 default text decoding in Windows Python (not only console I/O).
# This also protects pre-existing R3R5 tests using Path.read_text() without encoding.
# run.ps1 is invoked in a child PowerShell process; caller environment is unchanged.
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    if (-not (Test-Path '.git')) { throw 'Git checkout required' }
    Write-Output 'PHASE175_R3R6_GIT_STATUS_BEFORE'
    & git status -sb
    if ($LASTEXITCODE -ne 0) { throw 'git status failed' }

    & python -B -m pytest -q -p no:cacheprovider `
        .\phase175_r3r6_lemma57_general\tests `
        .\phase175_r3r5_pi73_lemma57_frontier\tests `
        .\phase174_r3_r7_r5_zero_image_hopf_injective\tests\test_rule.py
    if ($LASTEXITCODE -ne 0) { throw 'R3R6 focused pytest failed' }
    Write-Output 'PHASE175_R3R6_FOCUSED_PYTEST=PASS'

    $argsPy = @('-B', '-m', 'phase175_r3r6_lemma57_general.audit', '--root', $root, '--timeout-seconds', $TimeoutSeconds)
    if ($DryRun) { $argsPy += '--dry-run' }
    & python @argsPy
    $code = $LASTEXITCODE
    Write-Output 'PHASE175_R3R6_GIT_STATUS_AFTER'
    & git status -sb
    if ($LASTEXITCODE -ne 0) { throw 'git status failed' }
    if ($code -ne 0) { throw "R3R6 audit failed or needs investigation: $code" }
    Write-Output 'PHASE175_R3R6=PASS'
    Write-Output '(END)'
}
finally {
    Pop-Location
}
