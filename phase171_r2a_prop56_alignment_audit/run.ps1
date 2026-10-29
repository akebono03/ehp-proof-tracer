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
    & python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider '.\phase171_r2a_prop56_alignment_audit\tests\test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2A_FOCUSED_PYTEST_FAILED' }
    Write-Host 'PHASE171_R2A_FOCUSED_PYTEST=PASS'
    $Arguments = @('-B', '-m', 'phase171_r2a_prop56_alignment_audit.audit', '--root', $RepoRoot, '--report', $ReportPath)
    if ($DryRun) { $Arguments += '--dry-run' }
    & python @Arguments
    if ($LASTEXITCODE -ne 0) { throw "PHASE171_R2A_AUDIT_EXIT=$LASTEXITCODE" }
    Write-Host 'PHASE171_R2A=PASS'
}
finally {
    Pop-Location
}
