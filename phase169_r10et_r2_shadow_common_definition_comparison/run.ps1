param(
    [ValidateSet('core','all')][string]$Cases = 'all',
    [switch]$SkipTests
)
$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Stamp = Get-Date -Format 'yyyyMMdd_HHmmss_fff'
$Output = Join-Path $PSScriptRoot ('output\' + $Stamp)
Write-Host 'R10ET_R2_MODE=AUDIT_ONLY_SHADOW'
Write-Host "R10ET_R2_REPO=$Repo"
Write-Host "R10ET_R2_HEAD=$(git -C $Repo rev-parse HEAD)"
Write-Host "R10ET_R2_CASES=$Cases"
Push-Location $Repo
try {
    & python -m phase169_r10et_r2_shadow_common_definition_comparison.audit `
        --root $Repo --output $Output --cases $Cases
    $AuditExit = $LASTEXITCODE
    Write-Host "R10ET_R2_AUDIT_EXIT=$AuditExit"
    if ($AuditExit -ne 0) { exit $AuditExit }
    if (-not $SkipTests) {
        $Tests = @(
            'phase169_r10et_r2_shadow_common_definition_comparison/tests/test_shadow_provider.py',
            'phase169_r10et_r1_definition_reference_dependency_audit/tests/test_audit_helpers.py',
            'phase169_r10eq_r1_universal_stable_definition/tests/test_r10eq_stable_definition.py',
            'phase169_r10eq_r1_universal_stable_definition/tests/test_r10eq_live.py',
            'phase169_r10er_r1_mixed_definition_projection/tests/test_r10er_projection.py',
            'phase169_r10en_shared_citation_provenance/tests/test_r10en_core.py',
            'phase169_r10es_r1_typed_partial_power_display/tests/test_r10es_display.py'
        )
        Write-Host 'R10ET_R2_FOCUSED_PYTEST_START'
        & python -m pytest -q -p no:cacheprovider @Tests
        $TestExit = $LASTEXITCODE
        Write-Host "R10ET_R2_FOCUSED_PYTEST_EXIT=$TestExit"
        if ($TestExit -ne 0) { exit $TestExit }
    }
    Write-Host 'R10ET_R2_SHADOW_AUDIT_EXECUTED=PASS'
} finally {
    Pop-Location
}
