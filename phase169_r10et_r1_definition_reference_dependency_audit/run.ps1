param(
    [ValidateSet('core','all')][string]$Cases = 'all',
    [switch]$SkipTests,
    [switch]$AllowHeadChange
)
$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Stamp = Get-Date -Format 'yyyyMMdd_HHmmss_fff'
$Out = Join-Path $PSScriptRoot ('output\' + $Stamp)
$Audit = Join-Path $PSScriptRoot 'audit.py'
Write-Host 'R10ET_MODE=AUDIT_ONLY'
Write-Host "R10ET_REPO=$Repo"
Write-Host "R10ET_BRANCH=$(git -C $Repo branch --show-current)"
Write-Host "R10ET_HEAD=$(git -C $Repo rev-parse HEAD)"
Write-Host "R10ET_CASES=$Cases"
$PythonArgs = @($Audit, '--root', $Repo, '--output', $Out, '--cases', $Cases)
if ($AllowHeadChange) { $PythonArgs += '--allow-head-change' }
& python @PythonArgs
$AuditExit = $LASTEXITCODE
Write-Host "R10ET_AUDIT_EXIT=$AuditExit"
if (-not $SkipTests) {
    $TestList = @(
        'phase169_r10eq_r1_universal_stable_definition/tests/test_r10eq_stable_definition.py',
        'phase169_r10eq_r1_universal_stable_definition/tests/test_r10eq_live.py',
        'phase169_r10er_r1_mixed_definition_projection/tests/test_r10er_projection.py',
        'phase169_r10en_shared_citation_provenance/tests/test_r10en_core.py',
        'phase169_r10es_r1_typed_partial_power_display/tests/test_r10es_display.py'
    )
    Write-Host 'R10ET_FOCUSED_PYTEST_START'
    Push-Location $Repo
    try {
        & python -m pytest -q -p no:cacheprovider @TestList
        $TestExit = $LASTEXITCODE
    } finally {
        Pop-Location
    }
    Write-Host "R10ET_FOCUSED_PYTEST_EXIT=$TestExit"
    if ($TestExit -ne 0) { exit $TestExit }
}
if ($AuditExit -ne 0) { exit $AuditExit }
Write-Host 'R10ET_AUDIT_ONLY_COMPLETE=PASS'
