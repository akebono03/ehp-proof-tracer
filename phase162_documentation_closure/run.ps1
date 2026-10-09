$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
if (-not (Test-Path (Join-Path $repo 'proof.py'))) { throw 'Run from the repository root.' }
$script = Join-Path $PSScriptRoot 'update_documents.py'
python -B $script
if ($LASTEXITCODE -ne 0) { throw "Documentation update failed ($LASTEXITCODE)" }
Write-Host 'Documentation update complete. No tests were run.'
