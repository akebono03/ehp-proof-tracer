param(
    [switch]$DryRun,
    [ValidateSet('frontier', 'n3-all')][string]$Scope = 'frontier',
    [int]$TimeoutSeconds = 240,
    [switch]$SkipRemoteCheck
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldPythonPath = $env:PYTHONPATH
$OldEncoding = $env:PYTHONIOENCODING
$OldUtf8 = $env:PYTHONUTF8
$OldNoBytecode = $env:PYTHONDONTWRITEBYTECODE

try {
    $env:PYTHONPATH = "$RepoRoot;$OldPythonPath"
    $env:PYTHONIOENCODING = 'utf-8'
    $env:PYTHONUTF8 = '1'
    $env:PYTHONDONTWRITEBYTECODE = '1'
    Push-Location $RepoRoot
    try {
        Write-Output 'PHASE173_R4_R2_FOCUSED_PYTEST_START'
        & python -B -m pytest -q -p no:cacheprovider `
          'phase173_r4_r2_generalization_audit/tests/test_audit.py' `
          'phase170_r3_r7_toda52_ordered_db_transport/tests/test_ordered_db_toda52.py' `
          'phase173_r4_r1_source_bound_56/tests/test_rule.py'
        if ($LASTEXITCODE -ne 0) { throw 'Phase 173 R4-R2 focused pytest failed' }
        Write-Output 'PHASE173_R4_R2_FOCUSED_PYTEST=PASS'
        $ArgsList = @(
            '-B', '-m', 'phase173_r4_r2_generalization_audit.audit',
            '--root', $RepoRoot, '--scope', $Scope,
            '--timeout-seconds', [string]$TimeoutSeconds
        )
        if ($DryRun) { $ArgsList += '--dry-run' }
        if ($SkipRemoteCheck) { $ArgsList += '--skip-remote-check' }
        & python @ArgsList
        if ($LASTEXITCODE -ne 0) { throw 'Phase 173 R4-R2 audit requires investigation' }
        & git status -sb
        Write-Output 'PHASE173_R4_R2_AUDIT=PASS'
    }
    finally { Pop-Location }
}
finally {
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONIOENCODING = $OldEncoding
    $env:PYTHONUTF8 = $OldUtf8
    $env:PYTHONDONTWRITEBYTECODE = $OldNoBytecode
}
