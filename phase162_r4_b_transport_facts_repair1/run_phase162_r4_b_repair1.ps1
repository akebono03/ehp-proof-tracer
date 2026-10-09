$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
Copy-Item (Join-Path $package 'files\toda_group_proof_narrative_transport_facts.py') (Join-Path $root 'toda_group_proof_narrative_transport_facts.py') -Force
Copy-Item (Join-Path $package 'files\tests\test_phase162_r4_b_transport_facts.py') (Join-Path $root 'tests\test_phase162_r4_b_transport_facts.py') -Force
python -m pytest tests/test_phase162_r4_b_transport_facts.py -q
if ($LASTEXITCODE -ne 0) { throw 'Phase 162 R4-B repair1 focused tests failed' }
Write-Host 'R4-B repair1 focused tests complete; renderer unchanged; full suite not run.'
