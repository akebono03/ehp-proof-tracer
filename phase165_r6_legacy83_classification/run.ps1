param()
$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not (Test-Path (Join-Path $project "phase165_r52_r9_shared_math.py"))) {
  throw "Execute from EHP Proof Tracer project root"
}
python (Join-Path $folder "audit.py")
if ($LASTEXITCODE -ne 0) { throw "Classification failed" }
python -m pytest -q (Join-Path $folder "test_contract.py")
if ($LASTEXITCODE -ne 0) { throw "Focused contract tests failed" }
Write-Host "83 historical tests classified. No files archived. Full pytest NOT run."
