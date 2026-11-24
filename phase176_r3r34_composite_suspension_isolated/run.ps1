param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $auditArgs = @()
    if ($DryRun) { $auditArgs += '--dry-run' }
    & python -m phase176_r3r34_composite_suspension_isolated.audit @auditArgs
    if ($LASTEXITCODE -ne 0) { throw 'R3R34 audit failed' }
    if (-not $DryRun) {
        $focused = Join-Path (Join-Path $PSScriptRoot 'tests') 'test_source.py'
        & python -m pytest -q -p no:cacheprovider $focused
        if ($LASTEXITCODE -ne 0) { throw 'R3R34 isolated pytest failed' }
        & python -m pytest -q -p no:cacheprovider tests/test_hopf_rules.py -k 'hopf_composition_formula or hopf_invariant_reaches_hopf_composition_formula'
        if ($LASTEXITCODE -ne 0) { throw 'R3R34 existing Hopf pytest failed' }
    }
} finally {
    Pop-Location
}
