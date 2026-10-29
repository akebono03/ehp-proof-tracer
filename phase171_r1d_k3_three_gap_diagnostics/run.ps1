param(
    [Parameter(Mandatory = $true)][string]$ReportPath,
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
Push-Location $RepoRoot
try {
    & python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider '.\phase171_r1d_k3_three_gap_diagnostics\tests\test_triage.py'
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R1D_FOCUSED_PYTEST_FAILED' }
    Write-Host 'PHASE171_R1D_FOCUSED_PYTEST=PASS'
    $Arguments = @('-B', '.\phase171_r1d_k3_three_gap_diagnostics\triage.py', '--root', $RepoRoot, '--report', $ReportPath)
    if ($DryRun) { $Arguments += '--dry-run' }
    & python @Arguments
    if ($LASTEXITCODE -ne 0) { throw "PHASE171_R1D_TRIAGE_EXIT=$LASTEXITCODE" }
    Write-Host 'PHASE171_R1D=PASS'
}
finally {
    Pop-Location
}
