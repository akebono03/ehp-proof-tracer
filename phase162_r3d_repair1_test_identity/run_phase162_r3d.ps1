$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$required = @(
  'audit_phase162_r3b_existing_renderer.py',
  'audit_phase162_r3a_presentation.py',
  'toda_group_structure_transport_reason.py',
  'toda_group_proof_narrative_renderer.py',
  'tests/test_phase162_r3c_root_reason.py'
)
foreach ($relative in $required) {
  if (-not (Test-Path (Join-Path $repo $relative))) { throw "Missing prerequisite: $relative" }
}
Copy-Item -LiteralPath (Join-Path $package 'audit_phase162_r3d_root_reason.py') -Destination (Join-Path $repo 'audit_phase162_r3d_root_reason.py') -Force
Copy-Item -LiteralPath (Join-Path $package 'tests/test_phase162_r3d_root_reason_audit.py') -Destination (Join-Path $repo 'tests/test_phase162_r3d_root_reason_audit.py') -Force
python -B -m pytest -q tests/test_phase162_r3d_root_reason_audit.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B audit_phase162_r3d_root_reason.py
exit $LASTEXITCODE
