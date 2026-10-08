$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$env:PYTHONPATH = $root
$script = Join-Path $PSScriptRoot 'audit_phase161_real_proof_execution.py'
python -B $script
if ($LASTEXITCODE -ne 0) {
    throw "Audit failed with exit code $LASTEXITCODE; inspect phase161_real_proof_execution.json"
}
