param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $audit = Join-Path $PSScriptRoot 'audit.py'
    $parameters = @($audit, '--root', $root)
    if ($DryRun) { $parameters += '--dry-run' }
    & python @parameters
    if ($LASTEXITCODE -ne 0) { throw 'R3R33R1 audit failed' }
    if (-not $DryRun) {
        $testFile = Join-Path (Join-Path $PSScriptRoot 'tests') 'test_audit.py'
        & python -m pytest -q -p no:cacheprovider $testFile
        if ($LASTEXITCODE -ne 0) { throw 'R3R33R1 tests failed' }
        & python -m pytest -q -p no:cacheprovider tests/test_hopf_rules.py -k 'hopf_composition_formula or hopf_invariant_reaches_hopf_composition_formula'
        if ($LASTEXITCODE -ne 0) { throw 'Hopf regression tests failed' }
    }
} finally {
    Pop-Location
}
