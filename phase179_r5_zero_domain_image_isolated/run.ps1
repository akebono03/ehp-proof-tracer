param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
Push-Location (Split-Path -Parent $PSScriptRoot)
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONUTF8 = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    $arguments = @('-B', '-m', 'phase179_r5_zero_domain_image_isolated.audit')
    if ($DryRun) { $arguments += '--dry-run' }
    & python @arguments
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
