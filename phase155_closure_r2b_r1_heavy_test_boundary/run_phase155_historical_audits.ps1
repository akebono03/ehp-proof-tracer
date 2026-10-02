param(
  [string]$RepoRoot = (Get-Location).Path
)

$ErrorActionPreference = "Stop"

Set-Location $RepoRoot

$Manifest = Join-Path `
  $RepoRoot `
  "tests\phase155_audit_only_nodeids.txt"

if (-not (Test-Path $Manifest)) {
  throw "Phase155 audit-only manifest not found: $Manifest"
}

$NodeIds = Get-Content `
  $Manifest |
  Where-Object {
    $_.Trim().Length -gt 0
  }

Write-Host "Phase155 historical audit-only suite"
Write-Host "Nodeids: $($NodeIds.Count)"
Write-Host ""
Write-Host "WARNING: this suite is intentionally excluded from routine pytest."
Write-Host "Some tests are heavy and/or historical."
Write-Host ""

python -m pytest `
  @NodeIds `
  --include-phase155-audits `
  -q `
  --tb=line `
  --durations=20

exit $LASTEXITCODE
