param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    if ($DryRun) {
        & python -B -m phase176_r3r22_composite_hopf_frontier.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R3R22 DryRun failed' }
    } else {
        & python -B -m phase176_r3r22_composite_hopf_frontier.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3R22 audit failed' }
        & python -B -m pytest -q -p no:cacheprovider `
            .\phase176_r3r22_composite_hopf_frontier\tests `
            .\tests\test_hopf_rules.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R22 focused pytest failed' }
    }
} finally {
    Pop-Location
}
