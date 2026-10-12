$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Project

$Required = @(
  'web_group_proof.py',
  'phase164_r5_r2_common_replay.py',
  'phase164_r5_r2_unified_web_display\sweep_112.py'
)
foreach ($RelativePath in $Required) {
  if (-not (Test-Path (Join-Path $Project $RelativePath))) {
    throw "Required file missing: $RelativePath"
  }
}

# -m includes the project root on sys.path, unlike running a nested script by path.
python -B -m phase164_r5_r2_unified_web_display.sweep_112
if ($LASTEXITCODE -ne 0) {
  throw 'R5-R2 112-target sweep failed; inspect phase164_r5_r2_output\report.json'
}
Write-Host 'Phase 164 R5-R2 112-target sweep completed. Full pytest NOT run.'
