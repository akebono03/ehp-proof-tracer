param(
    [switch] $DryRun,
    [string] $R4R11Report = ""
)

$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path

Push-Location $root
try {
    $tests = @(
        'phase175_r4r12_public_two_summand_quotient/tests/test_provider.py',
        'phase175_r4r12_public_two_summand_quotient/tests/test_installer.py',
        'phase175_r4r12_public_two_summand_quotient/tests/test_audit.py',
        'phase175_r4r3_two_summand_quotient/tests/test_rule.py',
        'phase175_r4r11_signed_eta_torsion_public/tests/test_rule.py',
        'phase175_r4r11_signed_eta_torsion_public/tests/test_provider.py',
        'phase175_r4r11_signed_eta_torsion_public/tests/test_installer.py',
        'phase175_r4r11_signed_eta_torsion_public/tests/test_audit.py',
        'phase175_r4r10_cited_58_prop25_public/tests/test_provider.py',
        'phase175_r4r5r3_public_order_zero/tests/test_real_integration.py'
    )
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib @tests
    if ($LASTEXITCODE -ne 0) { throw 'R4R12 focused pytest failed' }
    Write-Output 'PHASE175_R4R12_FOCUSED_PYTEST=PASS'

    $arguments = @(
        '-B', '-m', 'phase175_r4r12_public_two_summand_quotient.audit',
        '--root', $root
    )
    if ($DryRun) { $arguments += '--dry-run' }
    if ($R4R11Report -ne '') { $arguments += @('--r4r11-report', $R4R11Report) }
    & python @arguments
    if ($LASTEXITCODE -ne 0) { throw 'R4R12 public quotient audit failed' }
    Write-Output 'PHASE175_R4R12_EXIT_CODE=0'
    exit 0
} catch {
    Write-Output ('PHASE175_R4R12_ERROR=' + $_.Exception.Message)
    Write-Output 'PHASE175_R4R12_EXIT_CODE=1'
    exit 1
} finally {
    Pop-Location
}
