$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host "Repository root: $repo"
foreach ($required in @('proof.py', 'toda_rules.py', 'phase161_backward_goal_schema.py', 'phase161_r3_backward_goal_schema.py', 'phase161_r4_literature_premise_matching.py')) {
    if (-not (Test-Path (Join-Path $repo $required))) { throw "Missing prerequisite: $required" }
}
Copy-Item -LiteralPath (Join-Path $package 'phase161_r5_backward_proof_reconstruction.py') -Destination (Join-Path $repo 'phase161_r5_backward_proof_reconstruction.py') -Force
Copy-Item -LiteralPath (Join-Path $package 'tests\test_phase161_r5_backward_proof_reconstruction.py') -Destination (Join-Path $repo 'tests\test_phase161_r5_backward_proof_reconstruction.py') -Force
python -B -m pytest -q tests/test_phase161_r2_backward_goal_schema.py tests/test_phase161_r3_backward_goal_schema.py tests/test_phase161_r4_literature_premise_matching.py tests/test_phase161_r5_backward_proof_reconstruction.py
if ($LASTEXITCODE -ne 0) { throw "Phase 161 R5 focused pytest failed: $LASTEXITCODE" }
Write-Host 'Phase 161 R5 focused tests passed; entire suite not run.'
