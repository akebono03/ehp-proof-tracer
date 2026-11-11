param(
    [switch]$DryRun,
    [ValidateRange(1, 7200)][int]$TimeoutSeconds = 300
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldPythonPath = $env:PYTHONPATH
$OldPythonEncoding = $env:PYTHONIOENCODING
$OldPythonUtf8 = $env:PYTHONUTF8
$OldNoBytecode = $env:PYTHONDONTWRITEBYTECODE

try {
    $env:PYTHONPATH = "$RepoRoot;$OldPythonPath"
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
        Write-Output 'PHASE175_R1_GIT_STATUS_BEFORE'
        & git status -sb
        if ($LASTEXITCODE -ne 0) { throw 'R1 git status before failed' }

        & python -B -m pytest -q --disable-warnings -p no:cacheprovider -o addopts= `
            --import-mode=importlib '.\phase175_r1_k4_audit\tests\test_audit.py'
        if ($LASTEXITCODE -ne 0) { throw 'R1 focused pytest failed' }
        Write-Output 'PHASE175_R1_FOCUSED_PYTEST=PASS'

        $PythonArgs = @(
            '-B', '-m', 'phase175_r1_k4_audit.audit', '--root', $RepoRoot,
            '--timeout-seconds', [string]$TimeoutSeconds
        )
        if ($DryRun) { $PythonArgs += '--dry-run' }
        & python @PythonArgs
        $AuditExitCode = $LASTEXITCODE

        Write-Output 'PHASE175_R1_GIT_STATUS_AFTER'
        & git status -sb
        if ($LASTEXITCODE -ne 0) { throw 'R1 git status after failed' }
        if ($AuditExitCode -ne 0) { throw "R1 audit failed or requires investigation: $AuditExitCode" }
        Write-Output 'PHASE175_R1=PASS'
        Write-Output '(END)'
    }
    finally {
        Pop-Location
    }
}
finally {
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONIOENCODING = $OldPythonEncoding
    $env:PYTHONUTF8 = $OldPythonUtf8
    $env:PYTHONDONTWRITEBYTECODE = $OldNoBytecode
}
