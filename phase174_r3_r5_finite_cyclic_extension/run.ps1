param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
$OldBytecode = $env:PYTHONDONTWRITEBYTECODE
$OldEncoding = $env:PYTHONIOENCODING
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONIOENCODING = 'utf-8'

    $IndexBefore = @(git ls-files --stage) -join "`n"
    if ($LASTEXITCODE -ne 0) { throw 'Could not inspect the Git index' }
    $StatusBefore = @(git status --porcelain=v1 --untracked-files=all) -join "`n"
    if ($LASTEXITCODE -ne 0) { throw 'Could not inspect the working tree' }

    if ($DryRun) {
        & python -B -m phase174_r3_r5_finite_cyclic_extension.patch --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R3-R5 patch DryRun failed' }
        $IndexAfter = @(git ls-files --stage) -join "`n"
        $StatusAfter = @(git status --porcelain=v1 --untracked-files=all) -join "`n"
        if ($IndexAfter -cne $IndexBefore -or $StatusAfter -cne $StatusBefore) {
            throw 'DryRun unexpectedly changed the index or working tree'
        }
        Write-Output 'PHASE174_R3R5_IMPL_DRY_RUN_GATE=PASS'
    } else {
        & python -B -m phase174_r3_r5_finite_cyclic_extension.patch
        if ($LASTEXITCODE -ne 0) { throw 'R3-R5 patch failed' }
        & python -B -m phase174_r3_r5_finite_cyclic_extension.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3-R5 public backward-expansion audit failed' }
        & python -B -m pytest -q -p no:cacheprovider `
            phase174_r3_r5_finite_cyclic_extension/tests/test_rule.py `
            phase174_r3_r5_finite_cyclic_extension/tests/test_head_lineage.py `
            phase174_r3_r4_public_delta_connection/tests/test_connection.py `
            phase174_r3_r5_preflight/tests/test_audit.py `
            phase174_r3_r3_injective_delta_zero/tests/test_rule.py
        if ($LASTEXITCODE -ne 0) { throw 'R3-R5 focused tests failed' }
        Write-Output 'PHASE174_R3R5_IMPL_FOCUSED_PYTEST=PASS'

        $IndexAfter = @(git ls-files --stage) -join "`n"
        if ($IndexAfter -cne $IndexBefore) { throw 'Git index was changed' }
        $ChangedTracked = @(git diff --name-only)
        $ExpectedTracked = @(
            'phase165_r52_r9_shared_math.py',
            'phase174_r3_r4_public_delta_connection/tests/test_connection.py',
            'phase174_r3_r5_preflight/audit.py'
        )
        foreach ($Entry in $ChangedTracked) {
            if ($ExpectedTracked -notcontains $Entry) {
                throw ('Unreviewed tracked change: ' + $Entry)
            }
        }
        Write-Output 'PHASE174_R3R5_IMPL_PREFLIGHT_COMPATIBILITY=PASS'
        Write-Output 'PHASE174_R3R5_IMPL_GIT_GUARD=PASS'
        Write-Output 'PHASE174_R3R5_IMPL_GATE=PASS'
    }
}
finally {
    $env:PYTHONDONTWRITEBYTECODE = $OldBytecode
    $env:PYTHONIOENCODING = $OldEncoding
    Pop-Location
}
