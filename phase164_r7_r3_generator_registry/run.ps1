$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$py = (Get-Command py -ErrorAction SilentlyContinue)
if ($py) {
    & py -3 "$PSScriptRoot\apply.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    & py -3 -m pytest -q tests/test_phase164_r7_r3_generator_registry.py tests/test_phase164_r7_statement_resolution.py tests/test_phase109_3_recursive_known_group_identity_lookup.py tests/test_phase109_10_existing_fact_known_group_identity_validation.py tests/test_phase120_2_web_generator_proof.py
} else {
    & python "$PSScriptRoot\apply.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    & python -m pytest -q tests/test_phase164_r7_r3_generator_registry.py tests/test_phase164_r7_statement_resolution.py tests/test_phase109_3_recursive_known_group_identity_lookup.py tests/test_phase109_10_existing_fact_known_group_identity_validation.py tests/test_phase120_2_web_generator_proof.py
}
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Phase 164 R7-R3 targeted tests PASS; full pytest NOT run."
