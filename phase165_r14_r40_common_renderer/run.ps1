$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
Copy-Item "$PSScriptRoot\phase165_r14_r40_replay.py" ".\phase165_r14_r40_replay.py" -Force
Copy-Item "$PSScriptRoot\phase165_r14_r39_toda51.tex" ".\phase165_r14_r39_toda51.tex" -Force
python "$PSScriptRoot\install.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$OldPath = $env:PYTHONPATH
try {
  $env:PYTHONPATH = if ($OldPath) { "$Root$([IO.Path]::PathSeparator)$OldPath" } else { $Root }
  python -m pytest -q "$PSScriptRoot\test_phase165_r14_r40_common_renderer.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally { $env:PYTHONPATH = $OldPath }
Write-Host "R40 common renderer connected; full pytest NOT run. Restart Web server."
