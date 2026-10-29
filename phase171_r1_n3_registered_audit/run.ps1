param(
    [switch]$DryRun,
    [int]$TimeoutSeconds = 240
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OriginalPythonPath = $env:PYTHONPATH
$OriginalEncoding = $env:PYTHONIOENCODING
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
            throw 'Python is required'
        }
        if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
            throw 'Git is required'
        }
        & python -B -m pytest -q -p no:cacheprovider `
            '.\phase171_r1_n3_registered_audit\tests\test_contract.py'
        if ($LASTEXITCODE -ne 0) {
            throw "Phase 171 R1 focused pytest failed: $LASTEXITCODE"
        }
        Write-Output 'PHASE171_R1_FOCUSED_PYTEST=PASS'
        if ($DryRun) {
            & python -B '.\phase171_r1_n3_registered_audit\audit.py' `
                --root $RepoRoot --dry-run --timeout-seconds $TimeoutSeconds
        }
        else {
            & python -B '.\phase171_r1_n3_registered_audit\audit.py' `
                --root $RepoRoot --timeout-seconds $TimeoutSeconds
        }
        $AuditExit = $LASTEXITCODE
        & git status -sb
        if ($AuditExit -ne 0) {
            throw "Phase 171 R1 audit refused or worker failed: $AuditExit"
        }
        Write-Output 'PHASE171_R1=PASS'
    }
    finally {
        Pop-Location
    }
}
finally {
    $env:PYTHONPATH = $OriginalPythonPath
    $env:PYTHONIOENCODING = $OriginalEncoding
    $env:PYTHONUTF8 = $OriginalUtf8
    $env:PYTHONDONTWRITEBYTECODE = $OriginalNoBytecode
}
