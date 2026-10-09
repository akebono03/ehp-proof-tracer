$ErrorActionPreference = 'Stop'
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $PackageRoot
Set-Location $ProjectRoot
Copy-Item -Path "$PackageRoot\files\toda_group_proof_narrative_transport_facts.py" -Destination ".\toda_group_proof_narrative_transport_facts.py" -Force
Copy-Item -Path "$PackageRoot\files\toda_group_proof_narrative_transport_link.py" -Destination ".\toda_group_proof_narrative_transport_link.py" -Force
Copy-Item -Path "$PackageRoot\files\tests\test_phase162_r4_b_common_renderer_link.py" -Destination ".\tests\test_phase162_r4_b_common_renderer_link.py" -Force
python -B "$PackageRoot\patch_renderer.py"
if ($LASTEXITCODE -ne 0) { throw 'Renderer patch failed' }
python -m pytest ".\tests\test_phase162_r4_b_transport_facts.py" ".\tests\test_phase162_r4_b_common_renderer_link.py" -q
if ($LASTEXITCODE -ne 0) { throw 'R4-B focused tests failed' }
Write-Host 'R4-B common renderer focused checks completed; public stable renderer unchanged; full suite not run.'
