param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
Push-Location (Split-Path -Parent $PSScriptRoot)
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONUTF8 = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    $arguments = @('-B', '-m', 'phase179_r4_zero_group_source_first_audit.audit')
    if ($DryRun) { $arguments += '--dry-run' }
    & python @arguments
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
