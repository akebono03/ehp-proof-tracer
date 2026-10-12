$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$py = Get-Command py -ErrorAction SilentlyContinue
if ($py) { $exe = "py"; $prefix = @("-3") } else { $exe = "python"; $prefix = @() }
& $exe @prefix "$PSScriptRoot\apply.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $exe @prefix -m pytest -q `
  tests/test_phase164_r7_r4_operation_registry.py `
  tests/test_phase164_r7_r3_generator_registry.py `
  tests/test_phase164_r7_statement_resolution.py `
  tests/test_phase110_5_minimal_operation_query_core.py `
  tests/test_phase110_10_operation_query_proof_replay.py `
  tests/test_phase114_3_nu5_operation_query_handoff.py `
  tests/test_phase118_web_operation_query_proof.py `
  tests/test_phase120_2_web_generator_proof.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Phase 164 R7-R4 focused tests PASS; full pytest NOT run."
