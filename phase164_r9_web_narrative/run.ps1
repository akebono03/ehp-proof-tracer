$ErrorActionPreference = 'Stop'
$Root = (Get-Location).Path
$Pack = $PSScriptRoot
$Python = 'python'
try { & python --version | Out-Null; if ($LASTEXITCODE -ne 0) { throw 'python not usable' } } catch { $Python = 'py' }
Write-Host 'Phase 164 R9 guarded shared narrative normalization'
& $Python "$Pack\apply.py" --root "$Root" --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R9 preflight failed' }
& $Python "$Pack\apply.py" --root "$Root"
if ($LASTEXITCODE -ne 0) { throw 'R9 apply or tests failed' }
Write-Host 'R9 focused checks passed. Full pytest NOT run.'
Write-Host 'Open Phase 164 R9 report: phase164_r9_output\audit.json'
