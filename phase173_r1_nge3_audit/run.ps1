param(
    [switch]$DryRun,
    [ValidateSet('priority', 'all')][string]$Scope = 'priority',
    [int]$TimeoutSeconds = 240,
    [switch]$SkipRemoteCheck
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
        Write-Output 'PHASE173_R1_GIT_STATUS_BEFORE'
        & git status -sb
        & python -B -m pytest -q --disable-warnings -p no:cacheprovider `
            '.\phase173_r1_nge3_audit\tests\test_audit.py'
        if ($LASTEXITCODE -ne 0) {
            throw "Phase 173 R1 focused pytest failed: $LASTEXITCODE"
        }
        Write-Output 'PHASE173_R1_FOCUSED_PYTEST=PASS'
        $PythonArgs = @(
            '-B', '-m', 'phase173_r1_nge3_audit.audit',
            '--root', $RepoRoot, '--scope', $Scope,
            '--timeout-seconds', [string]$TimeoutSeconds
        )
        if ($DryRun) { $PythonArgs += '--dry-run' }
        if ($SkipRemoteCheck) { $PythonArgs += '--skip-remote-check' }
        & python @PythonArgs
        $AuditExit = $LASTEXITCODE
        Write-Output 'PHASE173_R1_GIT_STATUS_AFTER'
        & git status -sb
        if ($AuditExit -ne 0) {
            throw "Phase 173 R1 audit requires investigation: $AuditExit"
        }
        Write-Output 'PHASE173_R1=PASS'
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
