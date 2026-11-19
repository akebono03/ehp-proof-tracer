param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $argsList = @('-m', 'phase175_r4r14r5_public_zero_transport.installer', '--root', $root)
    if ($DryRun) { $argsList += '--dry-run' }
    python @argsList
    if ($LASTEXITCODE -ne 0) { throw 'R4R14R5 source guard / installer failed' }
    if ($DryRun) { exit 0 }

    python -m pytest -q --import-mode=importlib -p no:cacheprovider `
        phase175_r4r14r5_public_zero_transport/tests/test_provider.py `
        phase175_r4r14r5_public_zero_transport/tests/test_installer.py `
        phase175_r4r14r4_general_zero_transport/tests/test_rule.py `
        phase169_r10e5_composite_generator_image/tests/test_r10e5_composite_generator_image.py `
        phase174_r3_r7_r12_toda59_annihilator_source/tests/test_rule.py
    if ($LASTEXITCODE -ne 0) { throw 'R4R14R5 focused pytest failed' }
    Write-Output 'PHASE175_R4R14R5_FOCUSED_TESTS=PASS'
    python -m phase175_r4r14r5_public_zero_transport.audit
    if ($LASTEXITCODE -ne 0) { throw 'R4R14R5 public search failed' }
    Write-Output 'PHASE175_R4R14R5_NEW_GIVEN=0'
    Write-Output 'PHASE175_R4R14R5_PUBLIC_ROOT_COMPLETE=NOT_ASSERTED'
    Write-Output 'PHASE175_R4R14R5_GATE=PASS_SHARED_ZERO_TRANSPORT_CONNECTED'
} finally {
    Pop-Location
}
