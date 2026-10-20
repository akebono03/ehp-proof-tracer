$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
if (-not (Test-Path '.\phase165_r52_r13_reference_registration.py')) { throw 'Run from repository root.' }
$env:PYTHONPATH = if ($env:PYTHONPATH) { "$root;$env:PYTHONPATH" } else { $root }
python '.\phase166_r3j_proof_use_order_correction\apply.py'
if ($LASTEXITCODE -ne 0) { throw 'R3-J guarded patch failed.' }
python -m pytest -q '.\phase166_r3j_proof_use_order_correction\test_phase166_r3j_proof_use_order.py' '.\phase166_r3h_uniform_assertion_source\test_phase166_r3h_uniform_assertion_source.py' '.\test_phase165_r52_r9_shared_math.py'
if ($LASTEXITCODE -ne 0) { throw 'R3-J focused tests failed.' }
Write-Host 'R3-J focused tests PASS; full pytest NOT run.'
