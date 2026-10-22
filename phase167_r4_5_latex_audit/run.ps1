$ErrorActionPreference = "Stop"
$RepoRoot = (Get-Location).Path
$Folder = Join-Path $RepoRoot "phase167_r4_5_latex_audit"
Write-Host "=== R4-5: LaTeX audit ==="
python -m phase167_r4_5_latex_audit.audit
if ($LASTEXITCODE -ne 0) { throw "LaTeX audit failed" }
Write-Host "=== R4-5: limited pytest ==="
python -m pytest (Join-Path $Folder "test_audit.py") -q
if ($LASTEXITCODE -ne 0) { throw "Limited pytest failed" }
Write-Host "Production code not modified. Full pytest not run."
