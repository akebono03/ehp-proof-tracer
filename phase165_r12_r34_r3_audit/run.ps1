$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $folder
Push-Location $root
try {
    $env:PYTHONPATH = "$folder;$root"
    python "$folder\audit.py"
    if ($LASTEXITCODE -ne 0) { throw 'R3 audit failed' }
    python -m pytest -q "$folder\test_audit.py" "$root\phase165_r14_r17_foundational_proofstep\test_phase165_r14_r17_foundational_proofstep.py"
    if ($LASTEXITCODE -ne 0) { throw 'R3 focused pytest failed' }
} finally {
    Pop-Location
}
