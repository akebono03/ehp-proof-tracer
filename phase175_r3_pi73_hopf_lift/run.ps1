param(
    [switch]$DryRun,
    [string]$R2Report = '',
    [ValidateRange(1, 7200)][int]$TimeoutSeconds = 240
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$PreviousPythonPath = $env:PYTHONPATH
$PreviousEncoding = $env:PYTHONIOENCODING
$PreviousUtf8 = $env:PYTHONUTF8
$PreviousNoBytecode = $env:PYTHONDONTWRITEBYTECODE

try {
    $env:PYTHONPATH = "$RepoRoot;$PreviousPythonPath"
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
        Write-Output 'PHASE175_R3_GIT_STATUS_BEFORE'
        & git status -sb
        if ($LASTEXITCODE -ne 0) { throw 'R3 git status before failed' }

        & python -B -m pytest -q --disable-warnings -p no:cacheprovider -o addopts= `
            --import-mode=importlib `
            '.\phase175_r3_pi73_hopf_lift\tests\test_audit.py' `
            '.\phase175_r3_pi73_hopf_lift\tests\test_rule.py' `
            '.\phase175_r3_pi73_hopf_lift\tests\test_frontier.py' `
            '.\phase175_r2_k4_frontier_audit\tests\test_audit.py' `
            '.\phase174_r3_r7_r5_zero_image_hopf_injective\tests\test_rule.py' `
            '.\phase174_r3_r7_r34_prior_lower_delta_source_wiring\tests\test_source.py'
        if ($LASTEXITCODE -ne 0) { throw 'R3 focused pytest failed' }
        Write-Output 'PHASE175_R3_FOCUSED_PYTEST=PASS'

        $Arguments = @(
            '-B', '-m', 'phase175_r3_pi73_hopf_lift.audit',
            '--root', $RepoRoot, '--timeout-seconds', [string]$TimeoutSeconds
        )
        if ($DryRun) { $Arguments += '--dry-run' }
        if ($R2Report.Trim()) { $Arguments += @('--r2-report', $R2Report) }
        & python @Arguments
        $AuditExitCode = $LASTEXITCODE

        Write-Output 'PHASE175_R3_GIT_STATUS_AFTER'
        & git status -sb
        if ($LASTEXITCODE -ne 0) { throw 'R3 git status after failed' }
        if ($AuditExitCode -ne 0) {
            throw "R3 audit failed or needs investigation: $AuditExitCode"
        }
        Write-Output 'PHASE175_R3=PASS'
        Write-Output '(END)'
    }
    finally { Pop-Location }
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
    $env:PYTHONIOENCODING = $PreviousEncoding
    $env:PYTHONUTF8 = $PreviousUtf8
    $env:PYTHONDONTWRITEBYTECODE = $PreviousNoBytecode
}
