$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Project
$env:PYTHONPATH = $Project

$Source = Join-Path $PSScriptRoot 'phase164_r2_citation_eligibility.py'
$Target = Join-Path $Project 'phase164_r2_citation_eligibility.py'
$TestSource = Join-Path $PSScriptRoot 'tests\test_phase164_r2_citation_eligibility.py'
$TestTarget = Join-Path $Project 'tests\test_phase164_r2_citation_eligibility.py'

foreach ($required in @('unified_statement_registry.py', 'phase163_r3_registry_validation.py', 'phase163_r4_registry_bridge.py', 'tests\test_phase163_r3_registry_validation.py')) {
    if (-not (Test-Path (Join-Path $Project $required))) {
        throw "Missing prerequisite: $required"
    }
}
if ((Test-Path $Target) -or (Test-Path $TestTarget)) {
    throw 'R2 target already exists. Review existing files rather than overwriting them.'
}
python -B -c "import ast,sys; [ast.parse(open(p,encoding='utf-8').read(),filename=p) for p in sys.argv[1:]]" $Source $TestSource
if ($LASTEXITCODE -ne 0) { throw 'R2 source syntax validation failed' }
Copy-Item $Source $Target
Copy-Item $TestSource $TestTarget
python -B -m pytest -q `
    tests/test_phase164_r2_citation_eligibility.py `
    tests/test_phase163_r2_unified_registry.py `
    tests/test_phase163_r3_registry_validation.py `
    tests/test_phase163_r4_registry_bridge.py
if ($LASTEXITCODE -ne 0) { throw 'R2 focused tests failed' }
Write-Host 'Phase 164 R2 targeted tests passed. Full pytest NOT run.'
