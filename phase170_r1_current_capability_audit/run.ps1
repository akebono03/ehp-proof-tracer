param(
    [ValidateSet('core','sample')]
    [string]$Scope = 'sample',
    [switch]$SkipFocusedTests
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONUTF8 = '1'
$stamp = Get-Date -Format 'yyyyMMdd_HHmmss_fffffff'
$recovery = Join-Path $env:LOCALAPPDATA 'EHPProofTracerRecovery'
if (-not (Test-Path $recovery)) {
    New-Item -ItemType Directory -Path $recovery -Force | Out-Null
}
$out = Join-Path $recovery ("phase170_r1_" + $stamp)
Write-Host "PHASE170_R1_MODE=AUDIT_ONLY"
Write-Host "PHASE170_R1_ROOT=$repo"
Write-Host "PHASE170_R1_OUTPUT=$out"
Push-Location $repo
try {
    if (-not $SkipFocusedTests) {
        Write-Host 'PHASE170_R1_FOCUSED_TEST_START'
        python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider `
            phase170_r1_current_capability_audit/tests/test_audit_contract.py `
            phase169_r10et_r1_definition_reference_dependency_audit/tests/test_audit_helpers.py `
            phase169_r10et_r6c_root_reachable_citations/tests/test_r6c_root_citations.py
        if ($LASTEXITCODE -ne 0) {
            throw "Focused tests failed (exit=$LASTEXITCODE); live audit not started"
        }
        Write-Host 'PHASE170_R1_FOCUSED_TEST_PASS=True'
    }
    python -B -m phase170_r1_current_capability_audit.audit `
        --root $repo --output $out --scope $Scope
    if ($LASTEXITCODE -ne 0) {
        throw "Audit requires review (exit=$LASTEXITCODE); report if created: $out"
    }
    Write-Host 'PHASE170_R1_AUDIT_EXECUTION=PASS'
} finally {
    Pop-Location
}
