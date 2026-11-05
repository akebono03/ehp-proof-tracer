param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$PackagePath = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $PackagePath '..')).Path
$ExpectedAudit = Join-Path $RepoRoot 'phase174_r3_r7_source_first_audit\audit.py'
if (-not (Test-Path -LiteralPath $ExpectedAudit)) {
    throw 'Phase 174 R3-R7 audit.py is missing.'
}

Push-Location $RepoRoot
$PreviousPythonPath = $env:PYTHONPATH
$PreviousNoBytecode = $env:PYTHONDONTWRITEBYTECODE
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    $FocusedTests = @(
        '.\phase174_r3_r7_source_first_audit\tests\test_audit.py',
        '.\phase174_r3_r6_source_extension\tests\test_source.py',
        '.\phase174_r3_r6_r3_common_narrative\tests\test_projection.py',
        '.\phase174_r3_r6_r4r1_cited_reference_link_fix\tests\test_r4r1_live_binding.py'
    )
    foreach ($TestFile in $FocusedTests) {
        if (-not (Test-Path -LiteralPath $TestFile)) {
            throw "Focused test file missing: $TestFile"
        }
    }

    Write-Output 'PHASE174_R3R7_FOCUSED_PYTEST_START'
    & python -B -m pytest -q --import-mode=importlib -p no:cacheprovider @FocusedTests
    if ($LASTEXITCODE -ne 0) {
        throw "R3-R7 focused pytest failed: $LASTEXITCODE"
    }
    Write-Output 'PHASE174_R3R7_FOCUSED_PYTEST=PASS'

    if ($DryRun) {
        & python -B '.\phase174_r3_r7_source_first_audit\audit.py' --dry-run
    }
    else {
        & python -B '.\phase174_r3_r7_source_first_audit\audit.py'
    }
    if ($LASTEXITCODE -ne 0) {
        throw "R3-R7 source-first audit failed: $LASTEXITCODE"
    }
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $PreviousNoBytecode
    Pop-Location
}
