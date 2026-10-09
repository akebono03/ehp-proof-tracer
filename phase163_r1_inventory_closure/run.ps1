$ErrorActionPreference = "Stop"
Set-Location (Resolve-Path (Join-Path $PSScriptRoot ".."))
$output = Join-Path (Get-Location) "phase163_r1_closure_output"
New-Item -ItemType Directory -Force -Path $output | Out-Null
Copy-Item -LiteralPath (Join-Path $PSScriptRoot "report.md") -Destination (Join-Path $output "report.md") -Force
Write-Host "Phase 163 R1 provisional inventory report saved: $output\report.md"
Write-Host "No project source changes; full pytest suite not run."
