param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    python -m pytest -q phase175_r4r12r10r1r3_orientation_type_diagnostic/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R10R1R3 focused pytest failed' }
    $argsList = @('-m', 'phase175_r4r12r10r1r3_orientation_type_diagnostic.audit')
    if ($DryRun) { $argsList += '--dry-run' }
    python @argsList
    if ($LASTEXITCODE -ne 0) { throw 'R10R1R3 diagnostic failed' }
}
finally {
    Pop-Location
}
