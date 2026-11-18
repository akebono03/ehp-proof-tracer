param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    python -m pytest -q -p no:cacheprovider phase175_r4r12r12_odd_hopf_and_e_image_frontier/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R12 focused pytest failed' }
    $arguments = @('--root', $root)
    if ($DryRun) { $arguments += '--dry-run' }
    python -m phase175_r4r12r12_odd_hopf_and_e_image_frontier.audit @arguments
    if ($LASTEXITCODE -ne 0) { throw 'R12 audit failed' }
} finally {
    Pop-Location
}
