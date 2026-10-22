$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
if (-not (Test-Path '.\web_group_proof.py')) { throw 'Run from the repository root.' }
New-Item -ItemType Directory -Path '.\phase167_r4_readonly_results' -Force | Out-Null
git status -sb | Out-File -Encoding utf8 '.\phase167_r4_readonly_results\git_status.txt'
git rev-parse HEAD | Out-File -Encoding utf8 '.\phase167_r4_readonly_results\head.txt'
$previousPythonPath = $env:PYTHONPATH
try {
  $env:PYTHONPATH = if ($previousPythonPath) { "$root;$previousPythonPath" } else { $root }
  python '.\phase167_r4_readonly_audit\audit.py'
  if ($LASTEXITCODE -ne 0) { throw 'Read-only audit failed' }
} finally {
  $env:PYTHONPATH = $previousPythonPath
}
Write-Host 'READ-ONLY audit finished. No production changes and no pytest.'
