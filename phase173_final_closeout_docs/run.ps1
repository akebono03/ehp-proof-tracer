param(
    [switch]$DryRun,
    [string]$ReportPath = ''
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$Package = $PSScriptRoot
$Root = (Resolve-Path (Join-Path $Package '..')).Path
if ([string]::IsNullOrWhiteSpace($ReportPath)) {
    $ReportPath = Join-Path $env:LOCALAPPDATA 'EHPProofTracerRecovery\phase173_final_gate_r2\phase173_full_test_report_r2.json'
}
Write-Output 'PHASE173_CLOSEOUT_SCOPE=FIVE_FULL_DOCUMENTS_ONLY'
Write-Output 'PHASE173_CLOSEOUT_GIT_STAGE_RESET_CLEAN_COMMIT=NONE'
Write-Output 'PHASE173_CLOSEOUT_FULL_PYTEST=False'
& git -C $Root fetch origin develop
if ($LASTEXITCODE -ne 0) { throw 'git fetch failed' }
Push-Location $Root
try {
    Write-Output '=== PHASE 173 FINAL DOCUMENT CONTRACT TESTS ==='
    & python -B -m pytest -q -p no:cacheprovider `
        phase173_final_closeout_docs/tests/test_docs_closeout.py
    if ($LASTEXITCODE -ne 0) { throw 'Phase 173 document contract tests failed' }
    $Arguments = @(
        '-B', '-m', 'phase173_final_closeout_docs.docs_closeout',
        '--repo', $Root, '--package', $Package, '--report', $ReportPath
    )
    if (-not $DryRun) { $Arguments += '--apply' }
    & python @Arguments
    if ($LASTEXITCODE -ne 0) { throw 'Phase 173 full-document closeout failed' }
} finally {
    Pop-Location
}
