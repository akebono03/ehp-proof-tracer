$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
Copy-Item -LiteralPath (Join-Path $package 'files\toda_stable_proof_path_selection.py') -Destination (Join-Path $project 'toda_stable_proof_path_selection.py') -Force
Copy-Item -LiteralPath (Join-Path $package 'files\tests\test_phase162_r4_b1_stable_path_selection.py') -Destination (Join-Path $project 'tests\test_phase162_r4_b1_stable_path_selection.py') -Force
Write-Host 'Updated: toda_stable_proof_path_selection.py'
Write-Host 'Updated: tests\test_phase162_r4_b1_stable_path_selection.py'
python -B -m pytest -q tests/test_phase162_r4_b1_stable_path_selection.py tests/test_phase160_stable_target_semantics.py tests/test_phase160_canonical_toda45_specialization.py
if ($LASTEXITCODE -ne 0) { throw 'R4-B1 focused tests failed' }
Write-Host 'R4-B1 selection-focused tests complete; no proof-tree rewriting or renderer changes; full suite not run.'
