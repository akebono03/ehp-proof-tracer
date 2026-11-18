param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    python -m pytest -q -p no:cacheprovider phase175_r4r12r11_ehp_surjectivity_frontier/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R11 focused pytest failed' }
    $argsList = @('--root', $root)
    if ($DryRun) { $argsList += '--dry-run' }
    python -m phase175_r4r12r11_ehp_surjectivity_frontier.audit @argsList
    if ($LASTEXITCODE -ne 0) { throw 'R11 audit failed' }
} finally {
    Pop-Location
}
