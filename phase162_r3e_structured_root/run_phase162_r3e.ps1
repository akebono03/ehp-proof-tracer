$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$required = @(
  'audit_phase162_r3b_existing_renderer.py',
  'audit_phase162_r3a_presentation.py',
  'toda_group_structure_transport_reason.py',
  'toda_group_proof_narrative_renderer.py'
)
foreach ($relative in $required) {
  if (-not (Test-Path (Join-Path $repo $relative))) { throw "Missing prerequisite: $relative" }
}
$files = @(
  'phase162_r3e_structured_root_renderer.py',
  'audit_phase162_r3e.py',
  'tests/test_phase162_r3e_structured_root.py'
)
foreach ($relative in $files) {
  $target = Join-Path $repo $relative
  $directory = Split-Path -Parent $target
  if (-not (Test-Path $directory)) { New-Item -ItemType Directory -Path $directory -Force | Out-Null }
  Copy-Item -LiteralPath (Join-Path $package $relative) -Destination $target -Force
  Write-Host "Updated: $relative"
}
python -B -m pytest -q tests/test_phase162_r3e_structured_root.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B audit_phase162_r3e.py
exit $LASTEXITCODE
