param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$ExpectedHead = '8bfa13946251c5618530641c572e8c756bb49af4'
Push-Location $RepoRoot
try {
    if ((git branch --show-current).Trim() -ne 'develop') {
        throw 'R15R10 requires develop branch'
    }
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R15R10 git fetch failed' }
    $RemoteHead = (git rev-parse origin/develop).Trim()
    if ($RemoteHead -ne $ExpectedHead) {
        throw "GitHub develop HEAD changed: $RemoteHead (expected $ExpectedHead). Reaudit required."
    }
    python -m phase173_r4_r15r10_common_route_audit.audit --root "$RepoRoot" --preflight
    if ($LASTEXITCODE -ne 0) { throw 'R15R10 reviewed-source preflight failed' }
    python -m pytest -q -p no:cacheprovider `
        phase173_r4_r15r10_common_route_audit/tests/test_contract.py `
        phase173_r4_r15r9_shared_abstract_renderer/tests/test_projection_isolated.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R10 small focused tests failed' }
    if ($DryRun) {
        Write-Output 'PHASE173_R4_R15R10_DRY_RUN=PASS'
        Write-Output 'PHASE173_R4_R15R10_PRODUCTION_EDIT=NONE'
    } else {
        python -m pytest -q -p no:cacheprovider `
            phase173_r4_r15r9_shared_abstract_renderer/tests/test_projection.py `
            phase173_r4_r15r8_public_abstract_sidecar/tests/test_integration.py `
            phase173_r4_r15r7_source_first_abstract_certificate/tests/test_integration.py `
            phase173_r4_r11_zero_public_connection/tests/test_route.py
        if ($LASTEXITCODE -ne 0) { throw 'R15R10 repository regression tests failed' }
        Write-Output 'PHASE173_R4_R15R10_FOCUSED_PYTEST=PASS'
        python -m phase173_r4_r15r10_common_route_audit.audit `
            --root "$RepoRoot" `
            --output (Join-Path $PSScriptRoot 'regression_report.json')
        if ($LASTEXITCODE -ne 0) { throw 'R15R10 public Web audit failed' }
        Write-Output 'PHASE173_R4_R15R10_PHASE_COMPLETED=False'
        Write-Output 'PHASE173_R4_R15R10_PRODUCTION_EDIT=NONE'
    }
} finally {
    Pop-Location
}
