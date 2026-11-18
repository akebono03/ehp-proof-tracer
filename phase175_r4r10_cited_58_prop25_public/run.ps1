param(
    [switch] $DryRun,
    [string] $R4R8Report = ""
)

$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path

Push-Location $root
try {
    $tests = @(
        'phase175_r4r10_cited_58_prop25_public/tests/test_installer.py',
        'phase175_r4r10_cited_58_prop25_public/tests/test_source.py',
        'phase175_r4r10_cited_58_prop25_public/tests/test_provider.py',
        'phase175_r4r10_cited_58_prop25_public/tests/test_audit.py',
        'phase175_r4r7_prop25_typed_composition/tests/test_rule.py',
        'phase175_r4r8_signed_delta_kernel_frontier/tests/test_audit.py'
    )
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib @tests
    if ($LASTEXITCODE -ne 0) { throw 'R4R10 focused pytest failed' }
    Write-Output 'PHASE175_R4R10_FOCUSED_PYTEST=PASS'

    $arguments = @(
        '-B', '-m', 'phase175_r4r10_cited_58_prop25_public.audit',
        '--root', $root
    )
    if ($DryRun) { $arguments += '--dry-run' }
    if ($R4R8Report -ne '') { $arguments += @('--r4r8-report', $R4R8Report) }
    & python @arguments
    if ($LASTEXITCODE -ne 0) { throw 'R4R10 source-first audit failed' }
    Write-Output 'PHASE175_R4R10_EXIT_CODE=0'
    exit 0
} catch {
    Write-Output ('PHASE175_R4R10_ERROR=' + $_.Exception.Message)
    Write-Output 'PHASE175_R4R10_EXIT_CODE=1'
    exit 1
} finally {
    Pop-Location
}
