$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    python ".\phase165_final_targeted\run.py"
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
