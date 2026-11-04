param(
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$ExpectedRemoteHead = 'd57fa2e880c3fbdffea5d310252626d360f4fe25'
$OriginalBytecodePreference = $env:PYTHONDONTWRITEBYTECODE

function Invoke-GitRead {
    param([string[]]$Arguments)
    $output = & git --no-pager @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Git command failed: git $($Arguments -join ' ')"
    }
    return $output
}

function Get-ObjectBlob {
    param([string]$GitObject, [string]$RelativePath)
    $listing = @(Invoke-GitRead -Arguments @('ls-tree', $GitObject, '--', $RelativePath))
    foreach ($line in $listing) {
        if ($line -match '^\d+ blob ([a-f0-9]{40})\s') {
            return $Matches[1]
        }
    }
    return 'MISSING'
}

function Get-IndexBlob {
    param([string]$RelativePath)
    $listing = @(Invoke-GitRead -Arguments @('ls-files', '--stage', '--', $RelativePath))
    if ($listing.Count -eq 0) {
        return 'MISSING'
    }
    if ($listing.Count -ne 1) {
        return 'UNMERGED'
    }
    if ($listing[0] -match '^\d+ ([a-f0-9]{40}) 0\s') {
        return $Matches[1]
    }
    return 'UNMERGED'
}

Push-Location $RepoRoot
try {
    $ActualRoot = (Invoke-GitRead -Arguments @('rev-parse', '--show-toplevel') | Out-String).Trim()
    if ([System.IO.Path]::GetFullPath($ActualRoot).TrimEnd('\', '/') -ne
        [System.IO.Path]::GetFullPath($RepoRoot).TrimEnd('\', '/')) {
        throw 'The ZIP must be extracted into the repository root.'
    }

    $IndexBefore = (Invoke-GitRead -Arguments @('ls-files', '--stage') | Out-String)
    $Branch = (Invoke-GitRead -Arguments @('branch', '--show-current') | Out-String).Trim()
    $LocalHead = (Invoke-GitRead -Arguments @('rev-parse', 'HEAD') | Out-String).Trim()
    Write-Output "AUDIT_MODE=$(if ($DryRun) { 'DryRun' } else { 'Focused' })"
    Write-Output "AUDIT_BRANCH=$Branch"
    Write-Output "AUDIT_LOCAL_HEAD=$LocalHead"
    Write-Output "AUDIT_REVIEWED_REMOTE_HEAD=$ExpectedRemoteHead"
    Write-Output 'AUDIT_PRODUCTION_WRITES=NONE'
    Write-Output 'AUDIT_GIT_PAGER_DISABLED=True'
    Write-Output 'AUDIT_GIT_STAGE_RESET_CLEAN_COMMIT=NONE'
    Write-Output 'AUDIT_FULL_PYTEST=False'

    & git --no-pager fetch origin develop
    if ($LASTEXITCODE -ne 0) {
        throw 'git fetch origin develop failed. The working tree and index have not been changed.'
    }
    $RemoteHead = (Invoke-GitRead -Arguments @('rev-parse', 'origin/develop') | Out-String).Trim()
    Write-Output "AUDIT_CURRENT_REMOTE_HEAD=$RemoteHead"

    Write-Output '=== CURRENT STATUS ==='
    & git --no-pager status -sb
    if ($LASTEXITCODE -ne 0) { throw 'git status failed' }
    Write-Output '=== STAGED FILES ==='
    & git --no-pager diff --cached --name-status
    if ($LASTEXITCODE -ne 0) { throw 'git diff --cached failed' }
    Write-Output '=== UNSTAGED FILES ==='
    & git --no-pager diff --name-status
    if ($LASTEXITCODE -ne 0) { throw 'git diff failed' }
    Write-Output '=== COMMITTED CHANGES SINCE HANDOFF ==='
    & git --no-pager diff --name-status 92f967c079f4a66e19a598e0acc54b742f11df9c origin/develop
    if ($LASTEXITCODE -ne 0) { throw 'git diff handoff..origin/develop failed' }

    $ReviewedPaths = @(
        'phase165_r52_partial_proof.py',
        'phase165_r52_r3_web_adapter.py',
        'phase168_r3_3_proof_narrative_model.py',
        'phase168_r3_4_link_bridge.py',
        'phase168_r3_5_model_renderer.py',
        'phase168_r3_12_body_binding.py',
        'web_group_proof_common.py',
        'phase173_r4_r15r9_shared_abstract_renderer/projection.py',
        'phase173_r4_r15r13_unified_presentation/layout.py',
        'phase173_r4_r15r16r3_staged_guard_fix/tree_adapter.py',
        'phase173_r4_r15r16_verified_progress_punctuation/tests/test_integration.py',
        'phase173_r4_r15r16r3_staged_guard_fix/tests/test_integration.py',
        'phase173_r4_r15r16r3r1_windows_eol_test_fix/tests/test_contract.py'
    )
    Write-Output '=== PER-FILE HEAD / INDEX / WORKTREE / REMOTE BLOBS ==='
    foreach ($RelativePath in $ReviewedPaths) {
        $HeadBlob = Get-ObjectBlob -GitObject 'HEAD' -RelativePath $RelativePath
        $IndexBlob = Get-IndexBlob -RelativePath $RelativePath
        $RemoteBlob = Get-ObjectBlob -GitObject 'origin/develop' -RelativePath $RelativePath
        if (Test-Path -LiteralPath $RelativePath -PathType Leaf) {
            $WorktreeBlob = (Invoke-GitRead -Arguments @('hash-object', "--path=$RelativePath", '--', $RelativePath) | Out-String).Trim()
        } else {
            $WorktreeBlob = 'MISSING'
        }
        $Marker = if ($IndexBlob -eq $WorktreeBlob) { 'INDEX_EQ_WORKTREE' } else { 'INDEX_NE_WORKTREE' }
        Write-Output "AUDIT_FILE=$RelativePath HEAD=$HeadBlob INDEX=$IndexBlob WORKTREE_CLEAN=$WorktreeBlob REMOTE=$RemoteBlob $Marker"
    }

    if ($RemoteHead -ne $ExpectedRemoteHead) {
        throw "Remote HEAD changed since this package was reviewed: $RemoteHead. Re-audit before implementation."
    }
    if ($Branch -ne 'develop') {
        throw "Expected local develop branch, found $Branch. Do not alter Git state automatically."
    }

    if (-not $DryRun) {
        $env:PYTHONDONTWRITEBYTECODE = '1'
        Write-Output '=== R15R17 RUNTIME READ-ONLY PROBE ==='
        & python -m phase173_r4_r15r17_preflight_import_fix.runtime_probe
        if ($LASTEXITCODE -ne 0) { throw 'R15R17 runtime probe failed' }
        Write-Output '=== RELATED FOCUSED PYTEST ==='
        & python -m pytest -q -p no:cacheprovider `
            'phase173_r4_r15r16r3_staged_guard_fix/tests/test_adapter_unit.py' `
            'phase173_r4_r15r16r3_staged_guard_fix/tests/test_integration.py' `
            'phase173_r4_r15r16r3r1_windows_eol_test_fix/tests/test_contract.py'
        if ($LASTEXITCODE -ne 0) { throw 'R15R17 focused pytest failed' }
        Write-Output 'AUDIT_FOCUSED_PYTEST=PASS'
    } else {
        Write-Output 'AUDIT_DRY_RUN=PASS'
        Write-Output 'AUDIT_FOCUSED_PYTEST=SKIPPED'
    }
} finally {
    $env:PYTHONDONTWRITEBYTECODE = $OriginalBytecodePreference
    $IndexAfter = (Invoke-GitRead -Arguments @('ls-files', '--stage') | Out-String)
    if ($IndexAfter -ne $IndexBefore) {
        Pop-Location
        throw 'Git index changed during audit. Inspect before doing any other operation.'
    }
    Write-Output 'AUDIT_GIT_INDEX_PRESERVED=PASS'
    Pop-Location
}
