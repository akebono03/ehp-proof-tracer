param([string]$R3Report = '')
$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Recovery = Join-Path $env:LOCALAPPDATA 'EHPProofTracerRecovery'
if (-not (Test-Path -LiteralPath $Recovery -PathType Container)) {
    throw 'Recovery reports directory not found'
}
if ([string]::IsNullOrWhiteSpace($R3Report)) {
    $Found = Get-ChildItem -LiteralPath $Recovery -Directory -Filter 'phase170_r3_r1_*' |
        Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName 'audit.json') -PathType Leaf } |
        Sort-Object Name -Descending |
        Select-Object -First 1
    if ($null -eq $Found) { throw 'No reviewed R3-R1 audit.json found' }
    $R3Report = Join-Path $Found.FullName 'audit.json'
}
if (-not (Test-Path -LiteralPath $R3Report -PathType Leaf)) { throw "Missing R3 report: $R3Report" }
$Stamp = Get-Date -Format 'yyyyMMdd_HHmmss_fffffff'
$Output = Join-Path $Recovery ('phase170_r3_r2_' + $Stamp)
Write-Host 'PHASE170_R3R2_MODE=AUDIT_ONLY'
Write-Host "PHASE170_R3R2_REPO=$Repo"
Write-Host "PHASE170_R3R2_R3_REPORT=$R3Report"
Write-Host "PHASE170_R3R2_OUTPUT=$Output"
Push-Location $Repo
try {
    Write-Host 'PHASE170_R3R2_FOCUSED_TEST_START'
    & python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider (Join-Path $PSScriptRoot 'tests')
    $TestExit = $LASTEXITCODE
    Write-Host "PHASE170_R3R2_FOCUSED_TEST_EXIT=$TestExit"
    if ($TestExit -ne 0) { exit $TestExit }
    & python -B (Join-Path $PSScriptRoot 'audit.py') --root $Repo --r3-report $R3Report --output $Output
    $AuditExit = $LASTEXITCODE
    Write-Host "PHASE170_R3R2_AUDIT_EXIT=$AuditExit"
    exit $AuditExit
} finally {
    Pop-Location
}
