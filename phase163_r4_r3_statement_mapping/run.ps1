$ErrorActionPreference = "Stop"
$ProjectRoot = (Get-Location).Path
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Copy-Item -LiteralPath (Join-Path $PackageRoot 'phase163_r4_r3_statement_mapping.py') -Destination (Join-Path $ProjectRoot 'phase163_r4_r3_statement_mapping.py') -Force
$Tests = Join-Path $ProjectRoot 'tests'
New-Item -Path $Tests -ItemType Directory -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $PackageRoot 'tests/test_phase163_r4_r3_statement_mapping.py') -Destination (Join-Path $Tests 'test_phase163_r4_r3_statement_mapping.py') -Force
python -m pytest -q tests/test_phase163_r4_r3_statement_mapping.py
if ($LASTEXITCODE -ne 0) { throw 'Focused pytest failed' }
python phase163_r4_r3_statement_mapping.py
if ($LASTEXITCODE -ne 0) { throw 'Audit failed' }
Write-Host 'Phase 163 R4-R3 read-only mapping audit complete. Full suite not run.'
