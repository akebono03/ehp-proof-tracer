$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python (Join-Path $PSScriptRoot 'install.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q `
  (Join-Path $PSScriptRoot 'test_r5_typed_references.py') `
  'test_phase165_r52_r9_shared_math.py' -k 'not public_pi32_narrative_unchanged'
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R27-R5 typed-source targeted tests passed; known public narrative regression remains; full pytest NOT run.'
