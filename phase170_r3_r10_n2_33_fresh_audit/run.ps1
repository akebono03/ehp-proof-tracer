param(
    [switch]$DryRun,
    [int]$TimeoutSeconds = 240
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OriginalPythonPath = $env:PYTHONPATH
$OriginalPythonEncoding = $env:PYTHONIOENCODING
$OriginalUtf8 = $env:PYTHONUTF8
$OriginalNoBytecode = $env:PYTHONDONTWRITEBYTECODE

try {
    $env:PYTHONPATH = "$RepoRoot;$OriginalPythonPath"
    $env:PYTHONIOENCODING = 'utf-8'
    $env:PYTHONUTF8 = '1'
    $env:PYTHONDONTWRITEBYTECODE = '1'

    Push-Location $RepoRoot
    try {
        if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
            throw 'python is required'
        }
        if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
            throw 'git is required'
        }
        & python -B -m pytest -q -p no:cacheprovider `
            '.\phase170_r3_r10_n2_33_fresh_audit\tests\test_contract.py'
        if ($LASTEXITCODE -ne 0) {
            throw "R3-R10 focused contract tests failed: $LASTEXITCODE"
        }
        Write-Output 'PHASE170_R3R10_FOCUSED_PYTEST=PASS'
        if ($DryRun) {
            & python -B '.\phase170_r3_r10_n2_33_fresh_audit\audit.py' `
                --root $RepoRoot --dry-run --timeout-seconds $TimeoutSeconds
        }
        else {
            & python -B '.\phase170_r3_r10_n2_33_fresh_audit\audit.py' `
                --root $RepoRoot --timeout-seconds $TimeoutSeconds
        }
        $ExitCode = $LASTEXITCODE
        & git status -sb
        if ($ExitCode -ne 0) {
            throw "R3-R10 domain audit did not pass: exit $ExitCode"
        }
        Write-Output 'PHASE170_R3R10=PASS'
    }
    finally {
        Pop-Location
    }
}
finally {
    $env:PYTHONPATH = $OriginalPythonPath
    $env:PYTHONIOENCODING = $OriginalPythonEncoding
    $env:PYTHONUTF8 = $OriginalUtf8
    $env:PYTHONDONTWRITEBYTECODE = $OriginalNoBytecode
}
