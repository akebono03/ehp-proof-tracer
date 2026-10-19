$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $root
try {
    $source = Join-Path $root "phase165_r6_audit_results\collection_close\collection.log"
    $parser = Join-Path $root "phase165_r6_error_triage\triage.py"
    $output = Join-Path $root "phase165_r6_audit_results\collection_close\triage_130.json"
    if (-not (Test-Path -LiteralPath $source -PathType Leaf)) {
        throw "Collection log not found: $source"
    }
    if (-not (Test-Path -LiteralPath $parser -PathType Leaf)) {
        throw "Existing triage script not found: $parser"
    }
    python $parser --log $source --output $output
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    Write-Host "No pytest executed. No source files changed."
} finally {
    Pop-Location
}
