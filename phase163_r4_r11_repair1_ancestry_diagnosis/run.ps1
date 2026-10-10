$ErrorActionPreference = 'Stop'
$ProjectRoot = (Get-Location).Path
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Required = @('proof.py', 'phase163_r4_registry_bridge.py', 'phase163_r4_r11_prop56_remaining.py', 'phase163_r4_r7_representative_bindings.py')
foreach ($Filename in $Required) {
  if (-not (Test-Path (Join-Path $ProjectRoot $Filename))) { throw "Missing required project file: $Filename" }
}
Copy-Item -LiteralPath (Join-Path $PackageRoot 'phase163_r4_r11_ancestry_diagnosis.py') -Destination (Join-Path $ProjectRoot 'phase163_r4_r11_ancestry_diagnosis.py') -Force
Copy-Item -LiteralPath (Join-Path $PackageRoot 'tests\test_phase163_r4_r11_ancestry_diagnosis.py') -Destination (Join-Path $ProjectRoot 'tests\test_phase163_r4_r11_ancestry_diagnosis.py') -Force
Copy-Item -LiteralPath (Join-Path $PackageRoot 'audit.py') -Destination (Join-Path $ProjectRoot 'phase163_r4_r11_prop56_remaining\audit.py') -Force
& python -B -m pytest -q tests/test_phase163_r4_r11_prop56_remaining.py tests/test_phase163_r4_r11_ancestry_diagnosis.py
if ($LASTEXITCODE -ne 0) { throw 'R4-R11 focused tests failed.' }
$env:PYTHONPATH = "$ProjectRoot$([System.IO.Path]::PathSeparator)$env:PYTHONPATH"
& python -B (Join-Path $ProjectRoot 'phase163_r4_r11_prop56_remaining\audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-R11 diagnostic execution failed.' }
Write-Host 'R4-R11 provenance diagnosis executed. R4-R11 is not complete if audit reports BLOCKED_BY_PROVENANCE. Full suite not run.'
