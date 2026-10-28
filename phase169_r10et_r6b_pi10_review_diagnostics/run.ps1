$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$script = Join-Path $PSScriptRoot 'diagnose.py'
python -B $script --root $repo
$exitCode = $LASTEXITCODE
Write-Output "R10ET_R6B_SCRIPT_EXIT=$exitCode"
exit $exitCode
