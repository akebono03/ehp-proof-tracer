param(
    [switch]$DryRun,
    [ValidateRange(1, 3600)][int]$TimeoutSeconds = 180
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
    & python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider '.\phase171_r1c_k3_registered_audit\tests\test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R1C_FOCUSED_PYTEST_FAILED' }
    Write-Host 'PHASE171_R1C_FOCUSED_PYTEST=PASS'
    $AuditArgs = @('-B', '.\phase171_r1c_k3_registered_audit\audit.py', '--root', $RepoRoot, '--timeout-seconds', [string]$TimeoutSeconds)
    if ($DryRun) { $AuditArgs += '--dry-run' }
    & python @AuditArgs
    if ($LASTEXITCODE -ne 0) { throw "PHASE171_R1C_AUDIT_EXIT=$LASTEXITCODE" }
    Write-Host 'PHASE171_R1C=PASS'
}
finally {
    Pop-Location
}
