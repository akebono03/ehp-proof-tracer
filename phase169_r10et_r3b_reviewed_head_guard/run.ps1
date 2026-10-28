param(
    [ValidateSet('focus','all')][string]$Cases = 'all',
    [switch]$SkipTests
)
$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Stamp = Get-Date -Format 'yyyyMMdd_HHmmss_fff'
$Output = Join-Path $PSScriptRoot ('output\' + $Stamp)
Write-Host 'R10ET_R3B_MODE=AUDIT_ONLY_IN_MEMORY_PROJECTION'
Write-Host "R10ET_R3B_REPO=$Repo"
Write-Host "R10ET_R3B_HEAD=$(git -C $Repo rev-parse HEAD)"
Write-Host "R10ET_R3B_CASES=$Cases"
Push-Location $Repo
try {
    & python -m phase169_r10et_r3b_reviewed_head_guard.audit `
        --root $Repo --output $Output --cases $Cases
    $AuditExit = $LASTEXITCODE
    Write-Host "R10ET_R3B_AUDIT_EXIT=$AuditExit"
    if ($AuditExit -ne 0) { exit $AuditExit }
    if (-not $SkipTests) {
        $Tests = @(
            'phase169_r10et_r3b_reviewed_head_guard/tests/test_reviewed_head.py',
            'phase169_r10et_r3_cyclic_definition_projection_audit/tests/test_shadow_policy.py',
            'phase169_r10et_r2_shadow_common_definition_comparison/tests/test_shadow_provider.py',
            'phase169_r10eq_r1_universal_stable_definition/tests/test_r10eq_stable_definition.py',
            'phase169_r10eq_r1_universal_stable_definition/tests/test_r10eq_live.py',
            'phase169_r10er_r1_mixed_definition_projection/tests/test_r10er_projection.py',
            'phase169_r10a_verified_stable_chain_projection/tests/test_r10a_verified_stable_chain.py',
            'phase169_r10en_shared_citation_provenance/tests/test_r10en_core.py',
            'phase169_r10es_r1_typed_partial_power_display/tests/test_r10es_display.py'
        )
        Write-Host 'R10ET_R3B_FOCUSED_PYTEST_START'
        & python -m pytest -q -p no:cacheprovider @Tests
        $TestExit = $LASTEXITCODE
        Write-Host "R10ET_R3B_FOCUSED_PYTEST_EXIT=$TestExit"
        if ($TestExit -ne 0) { exit $TestExit }
    }
    Write-Host 'R10ET_R3B_SHADOW_AUDIT_EXECUTED=PASS'
} finally {
    Pop-Location
}
