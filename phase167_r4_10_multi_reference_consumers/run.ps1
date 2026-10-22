$ErrorActionPreference = "Stop"
$Root = (Get-Location).Path
$env:PYTHONPATH = $Root
python .\phase167_r4_10_multi_reference_consumers\patch.py
if ($LASTEXITCODE -ne 0) { throw "R4-10 patch failed" }
python -m pytest .\phase167_r4_10_multi_reference_consumers\test_phase167_r4_10.py .\phase167_r4_9_proofstep_reference_unification\test_phase167_r4_9.py .\phase167_r4_6_unified_reference_proof_newline_fix\test_phase167_r4_6_unified_reference_proof.py -q
if ($LASTEXITCODE -ne 0) { throw "R4-10 limited tests failed" }
Write-Host "Limited pytest PASS. Full pytest was not run."
