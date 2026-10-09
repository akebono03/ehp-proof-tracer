$ErrorActionPreference = 'Stop'
$RepoRoot = (Get-Location).Path
$Package = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not (Test-Path (Join-Path $RepoRoot 'phase162_validated_proof_presentation.py'))) {
  throw 'Run from the repository root after applying the Phase 162 R2 repair.'
}
$env:PYTHONPATH = "$RepoRoot;$env:PYTHONPATH"
python -B (Join-Path $Package 'audit_phase162_r3.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'Phase 162 R3 reference-boundary audit complete. No files changed. Full suite not run.'
