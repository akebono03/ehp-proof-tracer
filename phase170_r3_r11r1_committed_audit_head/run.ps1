param(
    [switch]$DryRun,
    [string]$AuditReport = ''
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
        $PythonArgs = @('-B', '.\phase170_r3_r11r1_committed_audit_head\closeout.py', '--root', $RepoRoot)
        if ($DryRun) { $PythonArgs += '--dry-run' }
        if ($AuditReport -ne '') { $PythonArgs += @('--audit-report', $AuditReport) }
        & python @PythonArgs
        $ExitCode = $LASTEXITCODE
        & git status -sb
        if ($ExitCode -ne 0) {
            throw "Phase 170 active suite closeout did not pass: exit $ExitCode"
        }
        Write-Output 'PHASE170_R3R11=PASS'
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
