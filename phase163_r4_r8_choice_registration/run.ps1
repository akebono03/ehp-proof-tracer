$ErrorActionPreference = 'Stop'
$ProjectRoot = (Get-Location).Path
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = 'python'

$TargetSource = Join-Path $ProjectRoot 'phase163_r4_r8_choice_registration.py'
$TargetTest = Join-Path $ProjectRoot 'tests\test_phase163_r4_r8_choice_registration.py'
$ExpectedFiles = @(
    'unified_statement_registry.py',
    'phase163_r4_registry_bridge.py',
    'phase163_r4_r6_structured_binding.py',
    'phase163_r4_r7_representative_bindings.py',
    'phase162_reference_boundary.py',
    'toda_literature_statement_boundary.py',
    'proof.py',
    'toda_rules.py'
)
foreach ($Filename in $ExpectedFiles) {
    if (-not (Test-Path (Join-Path $ProjectRoot $Filename))) {
        throw "Required current project file missing: $Filename"
    }
}
if (-not (Test-Path (Join-Path $ProjectRoot 'tests'))) {
    throw 'Expected project tests directory missing.'
}
Copy-Item -LiteralPath (Join-Path $PackageRoot 'phase163_r4_r8_choice_registration.py') -Destination $TargetSource -Force
Copy-Item -LiteralPath (Join-Path $PackageRoot 'tests\test_phase163_r4_r8_choice_registration.py') -Destination $TargetTest -Force

& $Python -B -m pytest -q tests/test_phase163_r4_r8_choice_registration.py
if ($LASTEXITCODE -ne 0) { throw 'Phase 163 R4-R8 focused pytest failed; audit not run.' }
& $Python -B phase163_r4_r8_choice_registration.py
if ($LASTEXITCODE -ne 0) { throw 'Phase 163 R4-R8 audit failed.' }
Write-Host 'Phase 163 R4-R8 focused test and choice declaration audit complete. Full suite not run.'
