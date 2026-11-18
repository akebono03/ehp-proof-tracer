param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    python -m pytest -q phase175_r4r12r10r1r7_public_visibility_diagnostic/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R7 focused pytest failed' }
    $flags = @()
    if ($DryRun) { $flags += '--dry-run' }
    python -m phase175_r4r12r10r1r7_public_visibility_diagnostic.audit @flags
    if ($LASTEXITCODE -ne 0) { throw 'R7 read-only audit failed' }
} finally { Pop-Location }
