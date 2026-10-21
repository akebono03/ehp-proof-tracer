$ErrorActionPreference = 'Stop'
$Package = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $Package
Set-Location $Root
$env:PYTHONPATH = if ($env:PYTHONPATH) { "$Root$([IO.Path]::PathSeparator)$env:PYTHONPATH" } else { $Root }
python ".\phase166_close_full_suite\close.py" --repo "$Root"
if ($LASTEXITCODE -ne 0) {
  Write-Host "Phase 166 closure BLOCKED. Inspect phase166_close_full_suite\results\<timestamp>\pytest_full.log"
  exit $LASTEXITCODE
}
Write-Host 'Phase 166 full pytest PASS candidate. Review results before official closure.'
