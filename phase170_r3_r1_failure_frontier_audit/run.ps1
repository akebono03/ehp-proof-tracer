param(
    [string]$R2Report = ''
)
$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Recovery = Join-Path $env:LOCALAPPDATA 'EHPProofTracerRecovery'
if (-not (Test-Path -LiteralPath $Recovery -PathType Container)) {
    throw 'Recovery reports directory not found'
}
if ([string]::IsNullOrWhiteSpace($R2Report)) {
    $Found = Get-ChildItem -LiteralPath $Recovery -Directory -Filter 'phase170_r2_head_sync_r1_*' |
        Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName 'audit.json') -PathType Leaf } |
        Sort-Object Name -Descending |
        Select-Object -First 1
    if ($null -eq $Found) { throw 'No reviewed R2 audit.json found' }
    $R2Report = Join-Path $Found.FullName 'audit.json'
}
if (-not (Test-Path -LiteralPath $R2Report -PathType Leaf)) { throw "Missing R2 report: $R2Report" }
$Stamp = Get-Date -Format 'yyyyMMdd_HHmmss_fffffff'
$Output = Join-Path $Recovery ('phase170_r3_r1_' + $Stamp)
Write-Host 'PHASE170_R3_MODE=AUDIT_ONLY'
Write-Host "PHASE170_R3_REPO=$Repo"
Write-Host "PHASE170_R3_R2_REPORT=$R2Report"
Write-Host "PHASE170_R3_OUTPUT=$Output"
Push-Location $Repo
try {
    Write-Host 'PHASE170_R3_FOCUSED_TEST_START'
    & python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider (Join-Path $PSScriptRoot 'tests')
    $TestExit = $LASTEXITCODE
    Write-Host "PHASE170_R3_FOCUSED_TEST_EXIT=$TestExit"
    if ($TestExit -ne 0) { exit $TestExit }
    & python -B (Join-Path $PSScriptRoot 'audit.py') --root $Repo --r2-report $R2Report --output $Output
    $AuditExit = $LASTEXITCODE
    Write-Host "PHASE170_R3_AUDIT_EXIT=$AuditExit"
    exit $AuditExit
} finally {
    Pop-Location
}
