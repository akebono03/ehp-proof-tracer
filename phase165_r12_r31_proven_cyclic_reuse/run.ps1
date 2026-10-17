$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $folder
Push-Location $project
$prior = $env:PYTHONPATH
try {
    $env:PYTHONPATH = $project + [IO.Path]::PathSeparator + $prior
    python "$folder\install.py"
    if ($LASTEXITCODE -ne 0) { throw 'R12-R31 installation failed' }
    python -m pytest -q "$folder\test_phase165_r12_r31_proven_cyclic_reuse.py" "tests\test_phase165_r12_r2_quotient_rules.py"
    if ($LASTEXITCODE -ne 0) { throw 'R12-R31 targeted pytest failed' }
    python "$folder\audit.py"
    if ($LASTEXITCODE -ne 0) { throw 'R12-R31 audit failed' }
} finally {
    $env:PYTHONPATH = $prior
    Pop-Location
}
