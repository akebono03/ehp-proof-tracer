param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$ExpectedHead = '7e9e00f42e8b125480cd2928b0ee7ec2c5269d3a'
Push-Location $RepoRoot
try {
    if ((git branch --show-current).Trim() -ne 'develop') {
        throw 'R15R11 requires the develop branch'
    }
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R15R11 git fetch failed' }
    $RemoteHead = (git rev-parse origin/develop).Trim()
    if ($RemoteHead -ne $ExpectedHead) {
        throw "GitHub develop HEAD changed: $RemoteHead (expected $ExpectedHead). Review again."
    }
    $LocalHead = (git rev-parse HEAD).Trim()
    if ($LocalHead -ne $ExpectedHead) {
        throw "Local HEAD $LocalHead differs from reviewed GitHub HEAD $ExpectedHead. Inspect git status and use git pull --ff-only only when safe."
    }
    Write-Output 'PHASE173_R4_R15R11R1_HEAD_LINEAGE=PASS'

    if ($DryRun) {
        python -m phase173_r4_r15r11_model_abstract_integration.install --root "$RepoRoot" --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R15R11 source guard failed' }
        python -m pytest -q -p no:cacheprovider `
            phase173_r4_r15r11_model_abstract_integration/tests/test_static.py
        if ($LASTEXITCODE -ne 0) { throw 'R15R11 dry-run source tests failed' }
        Write-Output 'PHASE173_R4_R15R11_DRY_RUN_TESTS=PASS'
        Write-Output 'PHASE173_R4_R15R11_PRODUCTION_EDIT=NONE'
    } else {
        python -m phase173_r4_r15r11_model_abstract_integration.install --root "$RepoRoot" --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R15R11 source guard failed' }
        python -m phase173_r4_r15r11_model_abstract_integration.install --root "$RepoRoot" --apply
        if ($LASTEXITCODE -ne 0) { throw 'R15R11 installation failed' }
        try {
            python -m pytest -q -p no:cacheprovider `
                phase173_r4_r15r11_model_abstract_integration/tests/test_integration.py `
                phase173_r4_r15r9_shared_abstract_renderer/tests/test_projection.py `
                phase173_r4_r15r9_shared_abstract_renderer/tests/test_projection_isolated.py `
                phase173_r4_r15r8_public_abstract_sidecar/tests/test_integration.py `
                phase173_r4_r11_zero_public_connection/tests/test_route.py `
                phase173_r4_r15r10_common_route_audit/tests/test_contract.py
            if ($LASTEXITCODE -ne 0) { throw 'R15R11 focused pytest failed' }
            Write-Output 'PHASE173_R4_R15R11_FOCUSED_PYTEST=PASS'
            python -m phase173_r4_r15r11_model_abstract_integration.audit `
                --output (Join-Path $PSScriptRoot 'model_abstract_report.json')
            if ($LASTEXITCODE -ne 0) { throw 'R15R11 Web/Model audit failed' }
            Write-Output 'PHASE173_R4_R15R11_PRODUCTION_EDIT=4_FILES'
        } catch {
            python -m phase173_r4_r15r11_model_abstract_integration.install --root "$RepoRoot" --restore
            throw
        }
    }
} finally {
    Pop-Location
}
