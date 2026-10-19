$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$triage = Join-Path $root 'phase165_r6_audit_results\collection_error_triage.json'
$output = Join-Path $root 'phase165_r6_audit_results\dependency_chain_audit.json'
if (-not (Test-Path $triage)) { throw "Missing triage report: $triage" }
$python = 'python'
& $python (Join-Path $PSScriptRoot 'audit.py') --root $root --triage $triage --out $output
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
