$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $root
try {
 python (Join-Path $PSScriptRoot "check.py")
 if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally {
 Pop-Location
}
