$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$required = @(
  'proof.py',
  'toda_group_proof_narrative_renderer.py',
  'phase162_r2_existing_proof_connection.py',
  'phase162_group_structure_backward.py',
  'audit_phase162_r3a_presentation.py',
  'audit_phase162_r3b_existing_renderer.py'
)
foreach ($relative in $required) {
  if (-not (Test-Path (Join-Path $repo $relative))) { throw "Missing prerequisite: $relative" }
}
Copy-Item -LiteralPath (Join-Path $package 'toda_group_structure_transport_reason.py') -Destination (Join-Path $repo 'toda_group_structure_transport_reason.py') -Force
Copy-Item -LiteralPath (Join-Path $package 'tests/test_phase162_r3c_root_reason.py') -Destination (Join-Path $repo 'tests/test_phase162_r3c_root_reason.py') -Force
python -B (Join-Path $package 'patch_renderer.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B -m pytest -q tests/test_phase162_r3c_root_reason.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B audit_phase162_r3b_existing_renderer.py
exit $LASTEXITCODE
