$ErrorActionPreference = "Stop"
$env:PYTHONPATH = (Get-Location).Path
try {
  python ".\phase143_75ap_r17_completion_audit_r3\audit.py" |
    Tee-Object -FilePath ".\phase143_75ap_r17_completion_audit_r3\output.txt"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "R17 current-entrypoint completion audit passed."
  Write-Host "Do not run the full pytest suite until this result is reviewed."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
