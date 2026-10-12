$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$py = Get-Command py -ErrorAction SilentlyContinue
if ($py) { $exe = "py"; $prefix = @("-3") } else { $exe = "python"; $prefix = @() }
& $exe @prefix "$PSScriptRoot\apply.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $exe @prefix -m pytest -q `
  tests/test_phase164_r7_r5_group_registry.py `
  tests/test_phase164_r7_r4_operation_registry.py `
  tests/test_phase164_r7_r3_generator_registry.py `
  tests/test_phase164_r7_statement_resolution.py `
  tests/test_phase131_5_web_group_proof.py `
  tests/test_phase145_group_proof_defaults.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Phase 164 R7-R5 focused tests PASS; full pytest NOT run."
