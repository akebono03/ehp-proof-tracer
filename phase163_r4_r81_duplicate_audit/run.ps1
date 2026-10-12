$ErrorActionPreference = 'Stop'
$Root = (Get-Location).Path
$Package = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not (Test-Path (Join-Path $Root 'phase163_r4_r80_output\registration_preflight.json'))) { throw 'R80 output not found.' }
foreach ($file in @('unified_statement_registry.py','phase163_r4_registry_bridge.py','toda_literature_statement_boundary.py','theorem_facts.py')) {
  if (-not (Test-Path (Join-Path $Root $file))) { throw "Missing project file: $file" }
}
$env:PYTHONPATH = "$Package;$Root"
python -m pytest -q (Join-Path $Package 'tests\test_phase163_r4_r81_duplicate_audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R81 focused pytest failed.' }
python (Join-Path $Package 'phase163_r4_r81_duplicate_audit.py') --root $Root --output (Join-Path $Root 'phase163_r4_r81_output')
if ($LASTEXITCODE -ne 0) { throw 'R81 audit failed.' }
Write-Host 'R81 complete. No production changes. Full pytest not run.'
