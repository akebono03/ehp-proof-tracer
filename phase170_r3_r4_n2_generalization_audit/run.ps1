param(
    [ValidateRange(3,20)] [int]$MaxK = 10,
    [ValidateRange(30,600)] [int]$CaseSeconds = 180
)
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$stamp = Get-Date -Format 'yyyyMMdd_HHmmss_fffffff'
$output = Join-Path $env:LOCALAPPDATA ("EHPProofTracerRecovery\phase170_r3_r4_n2_{0}" -f $stamp)
Push-Location $repo
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    Write-Host 'PHASE170_R3R4_MODE=AUDIT_ONLY'
    Write-Host "PHASE170_R3R4_REPO=$repo"
    Write-Host "PHASE170_R3R4_OUTPUT=$output"
    Write-Host 'PHASE170_R3R4_FOCUSED_TEST_START'
    python -B -m pytest -q -p no:cacheprovider `
        '.\phase170_r3_r4_n2_generalization_audit\tests\test_audit_contract.py' `
        '.\tests\test_phase167_r3_generic_resolver.py'
    $testCode = $LASTEXITCODE
    Write-Host "PHASE170_R3R4_FOCUSED_TEST_EXIT=$testCode"
    if ($testCode -ne 0) { exit $testCode }
    python -B '.\phase170_r3_r4_n2_generalization_audit\audit.py' `
        --root "$repo" `
        --output "$output" `
        --min-k 3 `
        --max-k $MaxK `
        --case-seconds $CaseSeconds
    $auditCode = $LASTEXITCODE
    Write-Host "PHASE170_R3R4_AUDIT_EXIT=$auditCode"
    exit $auditCode
}
finally {
    Pop-Location
}
