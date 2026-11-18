param(
    [switch] $DryRun,
    [string] $R4R10Report = ""
)

$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path

Push-Location $root
try {
    $tests = @(
        'phase175_r4r11_signed_eta_torsion_public/tests/test_rule.py',
        'phase175_r4r11_signed_eta_torsion_public/tests/test_provider.py',
        'phase175_r4r11_signed_eta_torsion_public/tests/test_installer.py',
        'phase175_r4r11_signed_eta_torsion_public/tests/test_audit.py',
        'phase175_r4r10_cited_58_prop25_public/tests/test_provider.py',
        'phase175_r4r10_cited_58_prop25_public/tests/test_source.py',
        'phase175_r4r10_cited_58_prop25_public/tests/test_installer.py',
        'phase175_r4r10_cited_58_prop25_public/tests/test_audit.py',
        'phase175_r4r7_prop25_typed_composition/tests/test_rule.py',
        'phase175_r4r5r3_public_order_zero/tests/test_real_integration.py'
    )
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib @tests
    if ($LASTEXITCODE -ne 0) { throw 'R4R11 focused pytest failed' }
    Write-Output 'PHASE175_R4R11_FOCUSED_PYTEST=PASS'

    $arguments = @(
        '-B', '-m', 'phase175_r4r11_signed_eta_torsion_public.audit',
        '--root', $root
    )
    if ($DryRun) { $arguments += '--dry-run' }
    if ($R4R10Report -ne '') { $arguments += @('--r4r10-report', $R4R10Report) }
    & python @arguments
    if ($LASTEXITCODE -ne 0) { throw 'R4R11 signed torsion audit failed' }
    Write-Output 'PHASE175_R4R11_EXIT_CODE=0'
    exit 0
} catch {
    Write-Output ('PHASE175_R4R11_ERROR=' + $_.Exception.Message)
    Write-Output 'PHASE175_R4R11_EXIT_CODE=1'
    exit 1
} finally {
    Pop-Location
}
