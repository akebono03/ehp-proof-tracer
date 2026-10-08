$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$source = Join-Path $PSScriptRoot 'files'
$targets = @(
    'phase162_web_narrative_integration.py',
    'tests\test_phase162_r5_6_narrative_final_format.py'
)
foreach ($relative in $targets) {
    $from = Join-Path $source $relative
    $to = Join-Path $root $relative
    if (Test-Path $to) {
        Copy-Item $to ($to + '.phase162_r5_6_format.bak') -Force
    }
    $dir = Split-Path -Parent $to
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    Copy-Item $from $to -Force
    Write-Host "Updated: $relative"
}
python -B -m py_compile '.\phase162_web_narrative_integration.py' '.\tests\test_phase162_r5_6_narrative_final_format.py'
if ($LASTEXITCODE -ne 0) { throw 'Syntax check failed' }
python -B -m pytest -q `
    '.\tests\test_phase162_r5_6_narrative_final_format.py' `
    '.\tests\test_phase162_r5_web_integration.py' `
    '.\tests\test_phase162_r5_6_repair5_reference_component_boundary.py' `
    '.\tests\test_phase161_r7_premise_provenance_validation.py'
if ($LASTEXITCODE -ne 0) { throw 'Focused pytest failed' }
Write-Host 'Phase 162 narrative final format focused tests complete. Full suite not run.'
