$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$required = @(
  'proof.py',
  'phase162_r2_existing_proof_connection.py',
  'phase162_group_structure_backward.py',
  'audit_phase162_r3a_presentation.py',
  'toda_group_proof_narrative_renderer.py',
  'toda_group_proof_generic_narrative_renderer.py',
  'toda_group_proof_presentation.py',
  'tests/test_phase59_n3_ehp_chain.py',
  'tests/test_phase59_toda52_pi4_2_transport.py'
)
foreach ($relative in $required) {
  if (-not (Test-Path (Join-Path $repo $relative))) {
    throw "Missing prerequisite: $relative"
  }
}
Copy-Item -LiteralPath (Join-Path $package 'audit_phase162_r3b_existing_renderer.py') -Destination (Join-Path $repo 'audit_phase162_r3b_existing_renderer.py') -Force
Copy-Item -LiteralPath (Join-Path $package 'tests/test_phase162_r3b_existing_renderer.py') -Destination (Join-Path $repo 'tests/test_phase162_r3b_existing_renderer.py') -Force
python -B -m pytest -q tests/test_phase162_r3b_existing_renderer.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B audit_phase162_r3b_existing_renderer.py
exit $LASTEXITCODE
