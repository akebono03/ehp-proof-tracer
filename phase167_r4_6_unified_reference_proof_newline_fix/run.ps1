$ErrorActionPreference = "Stop"
python .\phase167_r4_6_unified_reference_proof_newline_fix\patch.py
if ($LASTEXITCODE -ne 0) { throw "R4-6 patch failed" }
python -m pytest .\phase167_r4_6_unified_reference_proof_newline_fix\test_phase167_r4_6_unified_reference_proof.py -q
if ($LASTEXITCODE -ne 0) { throw "R4-6 tests failed" }
Write-Host "Limited pytest PASS. Full pytest not run."
