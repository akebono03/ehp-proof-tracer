$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
if (-not (Test-Path (Join-Path $root 'phase165_r52_r4_flask_bridge.py'))) {
    throw 'Run this script from the ehp_proof repository root.'
}
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = "$root;$env:PYTHONPATH"
$env:PYTHONIOENCODING = 'utf-8'
& python (Join-Path $scriptDir 'runner.py') --root $root
$code = $LASTEXITCODE
if ($code -ne 0) { throw "R6 audit incomplete or failed (exit code $code). Check phase165_r6_audit_results." }
Write-Host 'R6 automated tests PASS. Manual Web verification remains required.'
