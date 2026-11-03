param(
    [switch]$DryRun,
    [switch]$SkipBroadScan
)
$ErrorActionPreference = 'Stop'
$Package = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = (Resolve-Path (Join-Path $Package '..')).Path
$ExpectedHead = '188f707e1fcd8fde7b22af02a6b4005986fb3c1e'

function Assert-LastExit([string]$Step) {
    if ($LASTEXITCODE -ne 0) {
        throw "$Step failed with exit code $LASTEXITCODE"
    }
}

Push-Location $Root
try {
    $Branch = (git branch --show-current).Trim()
    Assert-LastExit 'git branch'
    if ($Branch -ne 'develop') {
        throw "Expected develop; current branch: $Branch"
    }
    git fetch origin develop
    Assert-LastExit 'git fetch origin develop'
    $RemoteHead = (git rev-parse origin/develop).Trim()
    Assert-LastExit 'git remote HEAD'
    $LocalHead = (git rev-parse HEAD).Trim()
    Assert-LastExit 'git local HEAD'
    Write-Output "PHASE173_R4_R12R3_REMOTE_HEAD=$RemoteHead"
    Write-Output "PHASE173_R4_R12R3_LOCAL_HEAD=$LocalHead"
    if ($RemoteHead -ne $ExpectedHead) {
        throw "GitHub develop advanced after review. Re-audit before running. Expected $ExpectedHead, got $RemoteHead"
    }
    if ($LocalHead -ne $ExpectedHead) {
        throw "Local HEAD differs from reviewed GitHub HEAD. No automatic checkout/merge is performed."
    }
    $Staged = @(git diff --cached --name-only)
    Assert-LastExit 'git staged diff'
    if ($Staged.Count -gt 0) {
        throw 'Staged changes detected; review before using the baseline.'
    }
    $TrackedChanges = @(git diff --name-only)
    Assert-LastExit 'git worktree diff'
    if ($TrackedChanges.Count -gt 0) {
        throw 'Tracked worktree modifications detected; review before using the baseline.'
    }
    Write-Output 'PHASE173_R4_R12R3_PREFLIGHT=PASS'
    if ($DryRun) {
        Write-Output 'PHASE173_R4_R12R3_DRY_RUN=PASS'
        Write-Output 'PHASE173_R4_R12R3_PRODUCTION_EDIT=NONE'
        exit 0
    }
    $ArgsList = @(
        (Join-Path $Package 'audit.py'), '--root', $Root,
        '--output', (Join-Path $Package 'audit_result.json')
    )
    if ($SkipBroadScan) {
        $ArgsList += '--fast'
    }
    python @ArgsList
    Assert-LastExit 'read-only structural audit'
    python -m pytest -q `
        phase173_r4_r12r3_architecture_audit/tests/test_audit.py `
        phase173_r4_r12_common_narrative/tests/test_projection.py `
        phase173_r4_r12_common_narrative/tests/test_install.py `
        phase173_r4_r13_narrative_audit/tests/test_audit.py
    Assert-LastExit 'focused pytest'
    Write-Output 'PHASE173_R4_R12R3_FOCUSED_PYTEST=PASS'
    Write-Output 'PHASE173_R4_R12R3_ONLY_AUDIT=PASS'
    Write-Output 'PHASE173_R4_R12R3_PRODUCTION_EDIT=NONE'
}
finally {
    Pop-Location
}
