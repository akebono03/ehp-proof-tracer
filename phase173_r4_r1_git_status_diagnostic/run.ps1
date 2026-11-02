param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
Push-Location -LiteralPath $Root
try {
    $Inside = @(git rev-parse --is-inside-work-tree)
    if ($LASTEXITCODE -ne 0 -or $Inside.Count -ne 1 -or $Inside[0] -ne 'true') {
        throw 'Not inside a Git worktree'
    }

    $Branch = @(git branch --show-current)
    if ($LASTEXITCODE -ne 0) { throw 'Cannot identify branch' }
    $Head = @(git rev-parse HEAD)
    if ($LASTEXITCODE -ne 0) { throw 'Cannot identify HEAD' }
    $Status = @(git status --porcelain=v1 --untracked-files=no)
    if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect tracked changes' }
    $Unstaged = @(git diff --name-status --)
    if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect unstaged changes' }
    $Staged = @(git diff --cached --name-status --)
    if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect staged changes' }
    $HeadDiff = @(git diff HEAD --name-status --)
    if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect changes since HEAD' }

    $Reviewed = @(
        'sources/toda/Toda_05_2.tex',
        'sources/toda/Toda_04_2.tex',
        'phase165_r52_r9_shared_math.py',
        'phase165_r52_r16_web_citation_gate.py',
        'phase165_r55_nk_only_goal.py',
        'phase165_r12_r11_prop42_unified.py',
        'phase165_r52_r27_r5_literature.py',
        'phase169_r3m_prior_result_catalog/prior_results.py',
        'phase169_r4b_prop44_injectivity/rule.py',
        'toda_rules.py',
        'homotopy_groups.py'
    )
    $ReviewedChanges = @(git diff HEAD --name-only -- $Reviewed)
    if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect reviewed source paths' }

    if ($Status.Count -eq 0) {
        $Classification = 'CLEAN_TRACKED_WORKTREE'
    }
    elseif ($ReviewedChanges.Count -gt 0) {
        $Classification = 'REVIEWED_SOURCE_MODIFIED_STOP'
    }
    else {
        $Classification = 'OTHER_TRACKED_FILES_MODIFIED_REVIEW_REQUIRED'
    }

    $Output = @(
        'PHASE173_R4_R1_STATUS_DIAGNOSTIC=AUDIT_ONLY',
        "BRANCH=$($Branch -join ' ')",
        "HEAD=$($Head -join ' ')",
        "CLASSIFICATION=$Classification",
        "TRACKED_CHANGE_COUNT=$($Status.Count)",
        "REVIEWED_SOURCE_CHANGE_COUNT=$($ReviewedChanges.Count)",
        '--- TRACKED_STATUS ---'
    )
    $Output += $Status
    $Output += '--- STAGED_NAME_STATUS ---'
    $Output += $Staged
    $Output += '--- UNSTAGED_NAME_STATUS ---'
    $Output += $Unstaged
    $Output += '--- DIFF_HEAD_NAME_STATUS ---'
    $Output += $HeadDiff
    $Output += '--- REVIEWED_SOURCE_CHANGES ---'
    $Output += $ReviewedChanges
    $Output += '--- END ---'

    $LocalBase = $env:LOCALAPPDATA
    if ([string]::IsNullOrWhiteSpace($LocalBase)) { $LocalBase = $HOME }
    $Directory = Join-Path $LocalBase 'EHPProofTracerRecovery\phase173_r4_r1_git_status_diagnostic'
    New-Item -ItemType Directory -Path $Directory -Force | Out-Null
    $Report = Join-Path $Directory 'status.txt'
    $Output | Set-Content -LiteralPath $Report -Encoding UTF8
    $Output | ForEach-Object { Write-Output $_ }
    Write-Output "PHASE173_R4_R1_DIAGNOSTIC_REPORT=$Report"
    Write-Output 'PHASE173_R4_R1_NO_GIT_MUTATION=True'
    Write-Output 'PHASE173_R4_R1_DIAGNOSTIC=PASS'
}
finally {
    Pop-Location
}
