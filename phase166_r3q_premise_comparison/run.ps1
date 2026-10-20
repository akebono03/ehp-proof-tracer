$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $root
try {
    python -m phase166_r3q_premise_comparison.audit
    if ($LASTEXITCODE -ne 0) { throw "R3-Q premise comparison audit failed." }
} finally {
    Pop-Location
}
