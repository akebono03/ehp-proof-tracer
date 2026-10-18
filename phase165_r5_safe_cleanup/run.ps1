$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$script = Join-Path $PSScriptRoot 'audit.py'
$output = Join-Path $root 'phase165_r5_audit_results\audit_result.json'
python $script --root $root --output $output
if ($LASTEXITCODE -ne 0) { throw 'R5 read-only audit failed; no production files modified.' }
Write-Host 'R5 audit finished; deletion deferred unless reachability can be proven. Full pytest NOT run.'
