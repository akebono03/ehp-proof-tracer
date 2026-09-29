$ErrorActionPreference = "Stop"

$repo = Get-Location
$env:PYTHONPATH = $repo.Path

try {
  $audit = Get-ChildItem `
    -Path $repo `
    -Recurse `
    -File `
    -Filter "audit_phase143_75u_remaining_fallbacks.py" |
    Select-Object -First 1

  if ($null -eq $audit) {
    throw (
      "Could not find audit_phase143_75u_remaining_fallbacks.py " +
      "under the repository. Keep the previously extracted Phase 143 " +
      "audit directory in the repository and rerun this script."
    )
  }

  Write-Host "Using audit:"
  Write-Host $audit.FullName
  Write-Host ""

  python $audit.FullName
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 143-75AP completion audit finished."
  Write-Host "=============================================================="
  Write-Host "Expected completion condition:"
  Write-Host "  rule-name fallback occurrences: 0"
  Write-Host "  statement types: 0"
  Write-Host "  distinct fallback rule names: 0"
  Write-Host "  render errors: 0"
  Write-Host ""
  Write-Host "Do not run the full pytest suite yet."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
