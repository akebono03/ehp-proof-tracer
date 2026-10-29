param(
    [Parameter(Mandatory = $true)]
    [string] $ReportPath,
    [switch] $DryRun
)
$ErrorActionPreference = 'Stop'
$packageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = (Resolve-Path (Join-Path $packageRoot '..')).Path
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
Push-Location $repoRoot
try {
    python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider phase171_r2b_prop56_source_dependency_audit/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw "PHASE171_R2B_FOCUSED_PYTEST_EXIT=$LASTEXITCODE" }
    Write-Host 'PHASE171_R2B_FOCUSED_PYTEST=PASS'
    $arguments = @('-B', '-m', 'phase171_r2b_prop56_source_dependency_audit.audit', '--root', $repoRoot, '--report', $ReportPath)
    if ($DryRun.IsPresent) { $arguments += '--dry-run' }
    & python @arguments
    if ($LASTEXITCODE -ne 0) { throw "PHASE171_R2B_AUDIT_EXIT=$LASTEXITCODE" }
    Write-Host 'PHASE171_R2B=PASS'
}
finally {
    Pop-Location
}
