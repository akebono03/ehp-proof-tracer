param(
    [string]$R1Report = ''
)
$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Recovery = Join-Path $env:LOCALAPPDATA 'EHPProofTracerRecovery'
if (-not (Test-Path $Recovery)) { throw 'Missing R1 recovery directory' }
if ([string]::IsNullOrWhiteSpace($R1Report)) {
    $Found = Get-ChildItem -LiteralPath $Recovery -Directory -Filter 'phase170_r1_*' |
        Where-Object { Test-Path (Join-Path $_.FullName 'audit.json') } |
        Sort-Object Name -Descending |
        Select-Object -First 1
    if ($null -eq $Found) { throw 'No Phase 170 R1 audit.json found' }
    $R1Report = Join-Path $Found.FullName 'audit.json'
}
if (-not (Test-Path -LiteralPath $R1Report -PathType Leaf)) { throw "Missing R1 report: $R1Report" }
$Stamp = Get-Date -Format 'yyyyMMdd_HHmmss_fffffff'
$Output = Join-Path $Recovery ('phase170_r2_head_sync_r1_' + $Stamp)
Write-Host 'PHASE170_R2_MODE=AUDIT_ONLY'
Write-Host "PHASE170_R2_REPO=$Repo"
Write-Host "PHASE170_R2_R1_REPORT=$R1Report"
Write-Host "PHASE170_R2_OUTPUT=$Output"
Push-Location $Repo
try {
    Write-Host 'PHASE170_R2_FOCUSED_TEST_START'
    & python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider (Join-Path $PSScriptRoot 'tests')
    $TestExit = $LASTEXITCODE
    if ($TestExit -ne 0) {
        Write-Host "PHASE170_R2_FOCUSED_TEST_EXIT=$TestExit"
        exit $TestExit
    }
    Write-Host 'PHASE170_R2_FOCUSED_TEST_PASS=True'
    & python -B (Join-Path $PSScriptRoot 'audit.py') --root $Repo --r1-report $R1Report --output $Output
    $AuditExit = $LASTEXITCODE
    Write-Host "PHASE170_R2_AUDIT_EXIT=$AuditExit"
    exit $AuditExit
} finally {
    Pop-Location
}
