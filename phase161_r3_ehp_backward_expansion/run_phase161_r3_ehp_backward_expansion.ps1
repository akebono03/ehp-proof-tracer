$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Output "Repository root: $repo"
$required = @('proof.py', 'toda_rules.py', 'phase161_backward_goal_schema.py')
foreach ($file in $required) {
  if (-not (Test-Path (Join-Path $repo $file))) {
    throw "Required repository file not found: $file"
  }
}
Copy-Item (Join-Path $package 'phase161_r3_backward_goal_schema.py') (Join-Path $repo 'phase161_r3_backward_goal_schema.py') -Force
Copy-Item (Join-Path $package 'tests\test_phase161_r3_backward_goal_schema.py') (Join-Path $repo 'tests\test_phase161_r3_backward_goal_schema.py') -Force
python -B -m pytest -q tests/test_phase161_r2_backward_goal_schema.py tests/test_phase161_r3_backward_goal_schema.py
if ($LASTEXITCODE -ne 0) { throw 'Focused pytest failed' }
Write-Output 'Phase 161 R3 focused tests passed; entire suite not run.'
