param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    if ($DryRun) {
        & python -B -m phase176_r3r21_hopf_right_composition_audit.audit --dry-run
    } else {
        & python -B -m phase176_r3r21_hopf_right_composition_audit.audit
    }
    if ($LASTEXITCODE -ne 0) { throw 'R3R21 source audit failed' }
    if (-not $DryRun) {
        & python -B -m pytest -q -p no:cacheprovider .\tests\test_hopf_rules.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R21 focused pytest failed' }
    }
} finally {
    Pop-Location
}
