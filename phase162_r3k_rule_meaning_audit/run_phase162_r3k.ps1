$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$required = @(
  'audit_phase162_r3b_existing_renderer.py',
  'phase162_r3f_recursive_renderer.py',
  'phase162_r3g_existing_reason_bridge.py',
  'phase162_r3h_reason_inventory.py',
  'phase162_r3i_semantic_sidecar_audit.py',
  'phase162_r3j_inference_rule_audit.py'
)
foreach ($relative in $required) {
  if (-not (Test-Path (Join-Path $repo $relative))) { throw "Missing prerequisite: $relative" }
}
$files = @(
  'phase162_r3k_rule_meaning_audit.py',
  'audit_phase162_r3k.py',
  'tests/test_phase162_r3k_rule_meaning_audit.py'
)
foreach ($relative in $files) {
  $target = Join-Path $repo $relative
  $folder = Split-Path -Parent $target
  if (-not (Test-Path $folder)) { New-Item -ItemType Directory -Path $folder -Force | Out-Null }
  Copy-Item -LiteralPath (Join-Path $package $relative) -Destination $target -Force
  Write-Host "Updated: $relative"
}
python -B -m pytest -q tests/test_phase162_r3k_rule_meaning_audit.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B audit_phase162_r3k.py
exit $LASTEXITCODE
