$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$bundle = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host "Repository root: $root"
if (!(Test-Path (Join-Path $root 'proof.py')) -or !(Test-Path (Join-Path $root 'toda_rules.py'))) {
  throw 'Run this script from the EHP Proof Tracer repository root.'
}
Copy-Item -LiteralPath (Join-Path $bundle 'phase161_backward_goal_schema.py') -Destination (Join-Path $root 'phase161_backward_goal_schema.py') -Force
Copy-Item -LiteralPath (Join-Path $bundle 'tests\test_phase161_r2_backward_goal_schema.py') -Destination (Join-Path $root 'tests\test_phase161_r2_backward_goal_schema.py') -Force
python -B -m pytest -q tests/test_phase161_r2_backward_goal_schema.py
if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed ($LASTEXITCODE)" }
Write-Host 'Phase 161 R2 focused tests passed; entire suite not run.'
