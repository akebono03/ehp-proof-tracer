param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONUTF8 = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    $arguments = @('-B','-m','phase178_r10_equal_cardinality_reason_display.audit')
    if ($DryRun) { $arguments += '--dry-run' }
    & python @arguments
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
