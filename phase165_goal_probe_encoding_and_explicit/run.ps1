$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $root
try {
    $env:PYTHONPATH = $root
    $env:PYTHONIOENCODING = "utf-8"
    python -X utf8 (Join-Path $PSScriptRoot "probe.py")
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally {
    Pop-Location
}
