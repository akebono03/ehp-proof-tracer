$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Write-Host "Repository root: $repoRoot"
python -B (Join-Path $PSScriptRoot 'apply_phase161_docs.py') --repository $repoRoot
if ($LASTEXITCODE -ne 0) { throw "Documentation update failed: exit $LASTEXITCODE" }
Write-Host 'No pytest was run. Full documents have been written.'
