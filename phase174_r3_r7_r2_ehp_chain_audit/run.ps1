param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$PreviousPythonPath = $env:PYTHONPATH
$PreviousNoBytecode = $env:PYTHONDONTWRITEBYTECODE

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    $FocusedTests = @(
        'phase174_r3_r7_r2_ehp_chain_audit/tests/test_contract.py',
        'phase174_r3_r7_r2_ehp_chain_audit/tests/test_repo.py',
        'phase174_r3_r7_r2_ehp_chain_audit/tests/test_runner_import_mode.py',
        'phase174_r3_r7_r1_zero_root_audit/tests/test_audit.py',
        'phase165_r12_r11_prop42_unified/tests/test_phase165_r12_r11_prop42_unified.py',
        'phase165_r12_r12_ehp_consequences/tests/test_phase165_r12_r12_ehp_consequences.py',
        'phase165_r14_r6_generic_iso/test_phase165_r14_r6_generic_iso.py',
        'phase173_r4_r11_zero_public_connection/tests/test_route.py'
    )
    foreach ($TestFile in $FocusedTests) {
        if (-not (Test-Path -LiteralPath $TestFile)) {
            throw "Missing focused test: $TestFile"
        }
    }

    # importlib would insert namespace packages for sibling directories named
    # like phase165_r12_r11_prop42_unified.py, shadowing actual source modules.
    # prepend imports those test files as modules without the namespace collision.
    Write-Output 'PHASE174_R3R7R2_FOCUSED_PYTEST_START'
    & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider @FocusedTests
    if ($LASTEXITCODE -ne 0) {
        throw 'Phase 174 R3-R7-R2 focused pytest failed'
    }
    Write-Output 'PHASE174_R3R7R2_FOCUSED_PYTEST=PASS'

    if ($DryRun) {
        & python -B -m phase174_r3_r7_r2_ehp_chain_audit.audit --dry-run
    } else {
        & python -B -m phase174_r3_r7_r2_ehp_chain_audit.audit
    }
    if ($LASTEXITCODE -ne 0) {
        throw 'Phase 174 R3-R7-R2 audit failed'
    }
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $PreviousNoBytecode
    Pop-Location
}
