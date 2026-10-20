$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$env:PYTHONPATH = $root + [IO.Path]::PathSeparator + $env:PYTHONPATH
python -m phase166_r3g_toda45_bidirectional_audit.audit
if ($LASTEXITCODE -ne 0) { throw 'Toda 4.5 audit failed' }
Write-Host 'Production-path read-only audit finished; full pytest NOT run.'
