param(
    [ValidateSet('on', 'off')][string]$Probes = 'on',
    [switch]$SkipTests
)
$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Stamp = Get-Date -Format 'yyyyMMdd_HHmmss_fff'
$Output = Join-Path $PSScriptRoot ('output\' + $Stamp)
Push-Location $Repo
try {
    & python -m phase169_r10et_r6_residual_definition_dependency_audit.audit `
        --root $Repo --output $Output --probes $Probes
    $AuditCode = $LASTEXITCODE
    Write-Host "R10ET_R6_AUDIT_EXIT=$AuditCode"
    if ($AuditCode -ne 0) { exit $AuditCode }
    if (-not $SkipTests) {
        Write-Host 'R10ET_R6_FOCUSED_PYTEST_START'
        & python -m pytest -q -p no:cacheprovider `
            'phase169_r10et_r6_residual_definition_dependency_audit/tests/test_r6_helpers.py' `
            'phase169_r10et_r5d_staged_audit_guard/tests/test_r5_live.py' `
            'phase169_r10eq_r1_universal_stable_definition/tests/test_r10eq_stable_definition.py' `
            'phase169_r10et_r4_cyclic_definition_projection/tests/test_r10et_r4_live.py'
        $TestsCode = $LASTEXITCODE
        Write-Host "R10ET_R6_FOCUSED_PYTEST_EXIT=$TestsCode"
        if ($TestsCode -ne 0) { exit $TestsCode }
    }
    Write-Host 'R10ET_R6_AUDIT_ONLY_COMPLETE=PASS'
    Write-Host 'R10ET_R6_EXIT=0'
} finally {
    Pop-Location
}
