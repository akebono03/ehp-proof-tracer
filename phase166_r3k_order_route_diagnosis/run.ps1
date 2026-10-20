$ErrorActionPreference = 'Stop'
if (-not (Test-Path '.\phase165_r52_r9_shared_math.py')) { throw 'Run from repository root.' }
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$previous = $env:PYTHONPATH
try {
    $env:PYTHONPATH = (Get-Location).Path + [IO.Path]::PathSeparator + $previous
    python (Join-Path $folder 'audit.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-K audit failed.' }
}
finally { $env:PYTHONPATH = $previous }
Write-Host 'R3-K read-only audit finished; no production changes and no pytest.'
