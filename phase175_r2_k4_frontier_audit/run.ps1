param(
    [switch]$DryRun,
    [string]$R1Report = '',
    [ValidateRange(1, 7200)][int]$TimeoutSeconds = 240
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
        if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw 'Python is required' }
        if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'Git is required' }
        Write-Output 'PHASE175_R2_GIT_STATUS_BEFORE'
        & git status -sb
        if ($LASTEXITCODE -ne 0) { throw 'R2 Git status before failed' }

        & python -B -m pytest -q --disable-warnings -p no:cacheprovider -o addopts= `
            --import-mode=importlib '.\phase175_r2_k4_frontier_audit\tests\test_audit.py' `
            '.\phase175_r1_k4_audit\tests\test_audit.py' `
            '.\phase174_r3_r7_r34_prior_lower_delta_source_wiring\tests\test_source.py'
        if ($LASTEXITCODE -ne 0) { throw 'R2 focused pytest failed' }
        Write-Output 'PHASE175_R2_FOCUSED_PYTEST=PASS'

        $Arguments = @(
            '-B', '-m', 'phase175_r2_k4_frontier_audit.audit',
            '--root', $RepoRoot, '--timeout-seconds', [string]$TimeoutSeconds
        )
        if ($DryRun) { $Arguments += '--dry-run' }
        if ($R1Report.Trim()) { $Arguments += @('--r1-report', $R1Report) }
        & python @Arguments
        $AuditExitCode = $LASTEXITCODE

        Write-Output 'PHASE175_R2_GIT_STATUS_AFTER'
        & git status -sb
        if ($LASTEXITCODE -ne 0) { throw 'R2 Git status after failed' }
        if ($AuditExitCode -ne 0) { throw "R2 audit failed or requires investigation: $AuditExitCode" }
        Write-Output 'PHASE175_R2=PASS'
        Write-Output '(END)'
    }
    finally { Pop-Location }
}
finally {
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONIOENCODING = $OldPythonEncoding
    $env:PYTHONUTF8 = $OldPythonUtf8
    $env:PYTHONDONTWRITEBYTECODE = $OldNoBytecode
}
