$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    python ".\phase165_goal_probe_path_fix\run.py"
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
