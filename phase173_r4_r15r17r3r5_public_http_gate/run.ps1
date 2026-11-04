param(
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$env:GIT_PAGER = 'cat'
$env:PAGER = 'cat'
$env:PYTHONDONTWRITEBYTECODE = '1'

$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Reviewed = 'a3baa7f2d5fa94983bbe1b795bd1883d57680b5b'
$SourceFiles = @(
    'phase168_r3_5_model_renderer.py',
    'phase168_r3_3_proof_narrative_model.py',
    'phase165_r52_r3_web_adapter.py',
    'web_group_proof_common.py',
    'web_group_proof.py',
    'web_app.py',
    'templates/index.html'
)

Push-Location $Root
try {
    $RepositoryRoot = (& git --no-pager rev-parse --show-toplevel).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Git repository root was not found' }
    $Expected = [System.IO.Path]::GetFullPath($Root)
    $Actual = [System.IO.Path]::GetFullPath($RepositoryRoot)
    if (-not [string]::Equals($Expected, $Actual, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw 'Extract R15R17-R3R5 ZIP at the repository root'
    }
    $Branch = (& git --no-pager branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $Branch -ne 'develop') {
        throw 'R15R17-R3R5 requires local develop branch'
    }
    $LocalHead = (& git --no-pager rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Unable to read local HEAD' }
    $BeforeIndex = (& git --no-pager write-tree).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Unable to verify the current Git index' }
    Write-Output "R15R17R3R5_LOCAL_HEAD=$LocalHead"
    Write-Output "R15R17R3R5_REVIEWED_BASE=$Reviewed"
    Write-Output 'R15R17R3R5_PRODUCTION_WRITES=NONE'
    Write-Output 'R15R17R3R5_GIT_STAGE_RESET_CLEAN_COMMIT=NONE'
    Write-Output 'R15R17R3R5_FULL_PYTEST=False'
    Write-Output 'R15R17R3R5_BROWSER_VISUAL_VERIFIED=False'

    & git --no-pager fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'GitHub develop fetch failed' }
    $RemoteHead = (& git --no-pager rev-parse origin/develop).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Unable to read origin/develop HEAD' }
    & git --no-pager merge-base --is-ancestor $Reviewed $LocalHead
    if ($LASTEXITCODE -ne 0) { throw "Local HEAD is not descended from reviewed R3R3: $LocalHead" }
    & git --no-pager merge-base --is-ancestor $Reviewed $RemoteHead
    if ($LASTEXITCODE -ne 0) { throw "Remote HEAD is not descended from reviewed R3R3: $RemoteHead" }
    Write-Output "R15R17R3R5_REMOTE_HEAD=$RemoteHead"

    $RemoteProductionChanges = @(& git --no-pager diff --name-only $Reviewed $RemoteHead -- $SourceFiles)
    if ($LASTEXITCODE -ne 0) { throw 'Remote production-source audit failed' }
    $StagedProductionChanges = @(& git --no-pager diff --cached --name-only -- $SourceFiles)
    if ($LASTEXITCODE -ne 0) { throw 'Staged production-source audit failed' }
    $WorktreeProductionChanges = @(& git --no-pager diff --name-only -- $SourceFiles)
    if ($LASTEXITCODE -ne 0) { throw 'Worktree production-source audit failed' }
    if ($RemoteProductionChanges.Count -gt 0 -or $StagedProductionChanges.Count -gt 0 -or $WorktreeProductionChanges.Count -gt 0) {
        Write-Output 'R15R17R3R5_SOURCE_GUARD=FAIL'
        $RemoteProductionChanges | ForEach-Object { Write-Output "REMOTE_CHANGED=$_" }
        $StagedProductionChanges | ForEach-Object { Write-Output "STAGED_CHANGED=$_" }
        $WorktreeProductionChanges | ForEach-Object { Write-Output "WORKTREE_CHANGED=$_" }
        throw 'Reviewed public Web sources have changed; R3R5 requires a new source review'
    }
    Write-Output 'R15R17R3R5_SOURCE_GUARD=PASS'

    Write-Output '=== R15R17-R3R5 HTML PARSER CONTRACT ==='
    & python -m pytest -q -p no:cacheprovider `
        phase173_r4_r15r17r3r5_public_http_gate/tests/test_html_probe.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R17-R3R5 HTML parser contract failed' }

    if ($DryRun) {
        Write-Output 'R15R17R3R5_DRY_RUN=PASS'
    }
    else {
        Write-Output '=== R15R17-R3R5 REAL FLASK HTTP GATE ==='
        & python -m pytest -q -s -p no:cacheprovider `
            phase173_r4_r15r17r3r5_public_http_gate/tests/test_flask_public_output.py
        if ($LASTEXITCODE -ne 0) { throw 'R15R17-R3R5 real Flask HTTP gate failed' }
        Write-Output 'R15R17R3R5_HTTP_GATE=PASS'
    }

    $AfterIndex = (& git --no-pager write-tree).Trim()
    if ($LASTEXITCODE -ne 0 -or $AfterIndex -ne $BeforeIndex) {
        throw 'R15R17-R3R5 changed the Git index'
    }
    Write-Output 'R15R17R3R5_GIT_INDEX_PRESERVED=PASS'
    if (-not $DryRun) {
        Write-Output 'R15R17R3R5_AUDIT_COMPLETE=PASS'
    }
    & git --no-pager status -sb
    if ($LASTEXITCODE -ne 0) { throw 'Git status failed' }
}
finally {
    Pop-Location
}
