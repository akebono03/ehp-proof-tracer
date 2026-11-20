param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    if ($DryRun) {
        & python -B -m phase176_r3r23_hopf_composition_type_audit.audit --dry-run
    } else {
        & python -B -m phase176_r3r23_hopf_composition_type_audit.audit
    }
    if ($LASTEXITCODE -ne 0) { throw 'R3R23 audit failed' }
    if (-not $DryRun) {
        & python -B -m pytest -q -p no:cacheprovider `
          .\phase176_r3r23_hopf_composition_type_audit\tests `
          .\phase174_r3_r7_r9_composition_associativity\tests\test_rule.py `
          .\tests\test_hopf_rules.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R23 focused pytest failed' }
    }
} finally {
    Pop-Location
}
