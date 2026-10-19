$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $triage = Join-Path $root 'phase165_r6_audit_results\collection_close\triage_130.json'
    $audit = Join-Path $root 'phase165_r6_dependency_audit\audit.py'
    $out = Join-Path $root 'phase165_r6_audit_results\collection_close\r6_8_dependency_chains.json'
    if (-not (Test-Path -LiteralPath $triage -PathType Leaf)) { throw "Missing triage: $triage" }
    if (-not (Test-Path -LiteralPath $audit -PathType Leaf)) { throw "Missing existing audit: $audit" }
    python $audit --root $root --triage $triage --out $out
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python (Join-Path $PSScriptRoot 'summarize.py') $out
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    Write-Host 'R6-8 dependency chain audit completed. No source files changed; no pytest run.'
} finally {
    Pop-Location
}
