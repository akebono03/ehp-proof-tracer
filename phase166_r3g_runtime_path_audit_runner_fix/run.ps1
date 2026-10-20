$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
if (-not (Test-Path (Join-Path $repo 'phase165_r52_r9_shared_math.py'))) {
    throw 'Run from the repository root.'
}
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$originalPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = if ([string]::IsNullOrEmpty($originalPythonPath)) {
        $repo
    } else {
        "$repo$([IO.Path]::PathSeparator)$originalPythonPath"
    }
    python (Join-Path $folder 'audit.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-G runtime path audit failed.' }
} finally {
    $env:PYTHONPATH = $originalPythonPath
}
Write-Host 'Read-only runtime path audit completed; full pytest NOT run.'
