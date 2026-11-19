param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$package = Join-Path $repo 'phase175_r4r14r3_binary_composition_audit'
if (-not (Test-Path (Join-Path $package 'audit.py'))) { throw 'Run from ehp_proof repository root.' }
& python -B -m phase175_r4r14r3_binary_composition_audit.audit --root $repo $(if ($DryRun) {'--dry-run'})
if ($LASTEXITCODE -ne 0) { throw 'R4R14R3 audit failed' }
if ($DryRun) { exit 0 }
& python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
    (Join-Path $package 'tests/test_audit.py') `
    'phase169_r10e5_composite_generator_image/tests/test_r10e5_composite_generator_image.py' `
    'phase174_r3_r7_r12_toda59_annihilator_source/tests/test_rule.py'
if ($LASTEXITCODE -ne 0) { throw 'R4R14R3 focused pytest failed' }
Write-Output 'PHASE175_R4R14R3_FOCUSED_TESTS=PASS'
& git diff --check
if ($LASTEXITCODE -ne 0) { throw 'R4R14R3 git diff check failed' }
Write-Output 'PHASE175_R4R14R3_PRODUCTION_UNCHANGED=PASS'
