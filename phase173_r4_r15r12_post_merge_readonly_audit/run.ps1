param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $RepoRoot
try {
    $actualRoot = (git rev-parse --show-toplevel).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Not a Git repository' }
    if ([System.IO.Path]::GetFullPath($actualRoot).TrimEnd('\', '/') -ne [System.IO.Path]::GetFullPath($RepoRoot).TrimEnd('\', '/')) {
        throw "Audit must run at repository root: $RepoRoot"
    }

    $branch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Unable to read branch' }
    $head = (git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Unable to read HEAD' }

    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'git fetch origin develop failed' }
    $remote = (git rev-parse origin/develop).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Unable to read origin/develop' }

    Write-Output "AUDIT_BRANCH=$branch"
    Write-Output "AUDIT_LOCAL_HEAD=$head"
    Write-Output "AUDIT_REMOTE_HEAD=$remote"
    Write-Output 'AUDIT_EXPECTED_REMOTE_HEAD_AT_PREPARATION=715dff58df263c419cdcb45c51a1fa169a87de45'
    Write-Output 'AUDIT_WORKTREE_MUTATION=NONE'
    Write-Output 'AUDIT_COMMIT_ATTEMPTED=False'
    Write-Output 'AUDIT_FULL_PYTEST_RUN=False'

    Write-Output '=== git status -sb ==='
    git status -sb
    if ($LASTEXITCODE -ne 0) { throw 'git status failed' }
    Write-Output '=== local tracked modifications ==='
    git diff --name-status
    if ($LASTEXITCODE -ne 0) { throw 'git diff failed' }
    Write-Output '=== local staged changes ==='
    git diff --cached --name-status
    if ($LASTEXITCODE -ne 0) { throw 'git diff --cached failed' }
    Write-Output '=== remote changes since handoff HEAD ==='
    git diff --name-status e2996ec2ff496203f94daa9bc22550c5e69a6b11 origin/develop
    if ($LASTEXITCODE -ne 0) { throw 'git diff handoff..origin/develop failed' }

    $paths = New-Object 'System.Collections.Generic.List[string]'
    $fixedFiles = @(
        'phase168_r3_37c_reference_projection.py',
        'phase168_r3_3_proof_narrative_model.py',
        'phase169_r4e_citation_binding/tests/test_r4e_citation_binding.py',
        'phase169_r4g_hopf_reference/tests/test_r4g_hopf_reference.py',
        'web_group_proof_common.py'
    )
    foreach ($path in $fixedFiles) { $paths.Add($path) }
    $packageFiles = @(git ls-tree -r --name-only origin/develop -- 'phase173_r4_r15r12_reference_correction/')
    if ($LASTEXITCODE -ne 0) { throw 'git ls-tree failed' }
    foreach ($file in $packageFiles) {
        if (-not [string]::IsNullOrWhiteSpace($file)) { $paths.Add($file.Trim()) }
    }
    $bad = 0
    $good = 0
    foreach ($path in $paths) {
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
            Write-Output "CONTENT_MISSING=$path"
            $bad++
            continue
        }
        $remoteBlob = (git rev-parse "origin/develop:$path").Trim()
        if ($LASTEXITCODE -ne 0) { throw "Cannot obtain remote blob: $path" }
        $localBlob = (git hash-object --path="$path" -- "$path").Trim()
        if ($LASTEXITCODE -ne 0) { throw "Cannot hash local file: $path" }
        if ($remoteBlob -eq $localBlob) {
            $good++
            Write-Output "CONTENT_MATCH=$path"
        } else {
            $bad++
            Write-Output "CONTENT_DIFFER=$path"
            Write-Output "REMOTE_BLOB=$remoteBlob"
            Write-Output "LOCAL_BLOB=$localBlob"
        }
    }
    Write-Output "AUDIT_CONTENT_MATCH_COUNT=$good"
    Write-Output "AUDIT_CONTENT_MISMATCH_COUNT=$bad"
    if ($branch -ne 'develop') {
        Write-Output 'AUDIT_BRANCH_GUARD=REVIEW_REQUIRED'
    } else {
        Write-Output 'AUDIT_BRANCH_GUARD=PASS'
    }
    if ($bad -eq 0) {
        Write-Output 'AUDIT_R15R12_REMOTE_CONTENT=PASS'
    } else {
        Write-Output 'AUDIT_R15R12_REMOTE_CONTENT=REVIEW_REQUIRED'
        exit 2
    }
} finally {
    Pop-Location
}
