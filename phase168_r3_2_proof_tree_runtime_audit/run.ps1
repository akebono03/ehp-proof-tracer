$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = Split-Path -Parent $folder
Push-Location $repo
try {
    python "$folder\audit.py"
    if ($LASTEXITCODE -ne 0) { throw 'R3-2 runtime audit failed' }
} finally {
    Pop-Location
}
