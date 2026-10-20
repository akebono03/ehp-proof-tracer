$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
  python -m phase166_r3q_unset_reference_positions.apply
  if ($LASTEXITCODE -ne 0) { throw 'Source alias patch failed' }
  python -m pytest -q phase166_r3q_unset_reference_positions/tests/test_phase166_r3q_unset_reference_positions.py phase166_r3d_pi32_regression/tests/test_phase166_r3d_pi32_regression.py
  if ($LASTEXITCODE -ne 0) {
    python -m phase166_r3q_unset_reference_positions.restore
    throw 'Targeted regression FAILED; restoration attempted'
  }
  Write-Host 'R3-Q registered source order PASS; full pytest NOT run.'
} finally {
  Pop-Location
}
