param([switch]$DryRun)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$env:GIT_PAGER = 'cat'
$env:PAGER = 'cat'
$env:PYTHONDONTWRITEBYTECODE = '1'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$ExpectedHead = 'aa25a9930d36b61e7588d1ef8e5916a766b569e6'

function Invoke-CheckedGit {
    param([string[]]$Arguments)
    $result = & git --no-pager @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw ('Git command failed: git ' + ($Arguments -join ' '))
    }
    return $result
}

Push-Location $Root
try {
    $GitRoot = (Invoke-CheckedGit -Arguments @('rev-parse', '--show-toplevel')).Trim()
    $CanonicalGitRoot = [System.IO.Path]::GetFullPath($GitRoot)
    $CanonicalScriptRoot = [System.IO.Path]::GetFullPath($Root)
    if (-not [string]::Equals(
        $CanonicalGitRoot,
        $CanonicalScriptRoot,
        [System.StringComparison]::OrdinalIgnoreCase
    )) {
        throw 'Extract the R15R17-R3 audit ZIP at the Git repository root'
    }
    $Branch = (Invoke-CheckedGit -Arguments @('branch', '--show-current')).Trim()
    $Head = (Invoke-CheckedGit -Arguments @('rev-parse', 'HEAD')).Trim()
    if ($Branch -ne 'develop' -or $Head -ne $ExpectedHead) {
        throw ('R15R17-R3 requires develop at reviewed HEAD ' + $ExpectedHead + '; current branch=' + $Branch + '; current HEAD=' + $Head)
    }
    Write-Output ('R15R17R3_LOCAL_HEAD=' + $Head)
    Write-Output ('R15R17R3_REVIEWED_HEAD=' + $ExpectedHead)
    Write-Output 'R15R17R3_SCOPE=READ_ONLY_GOAL_AND_CONTRACT_AUDIT'
    Write-Output 'R15R17R3_PRODUCTION_WRITES=NONE'
    Write-Output 'R15R17R3_GIT_STAGE_RESET_CLEAN_COMMIT=NONE'
    Write-Output 'R15R17R3_FULL_PYTEST=False'

    $IndexBefore = (Invoke-CheckedGit -Arguments @('write-tree')).Trim()
    Invoke-CheckedGit -Arguments @('fetch', 'origin', 'develop') | Out-Null
    $Remote = (Invoke-CheckedGit -Arguments @('rev-parse', 'origin/develop')).Trim()
    Write-Output ('R15R17R3_REMOTE_HEAD=' + $Remote)
    if ($Remote -ne $ExpectedHead) {
        throw 'GitHub develop advanced; inspect changes before continuing'
    }

    Write-Output '=== R15R17-R3 FOCUSED CONTRACT TESTS ==='
    & python -B -m pytest -q -p no:cacheprovider `
      phase173_r4_r15r17r3_goal_contract_audit/tests/test_audit_helpers.py `
      phase173_r4_r15r17r3_goal_contract_audit/tests/test_head_guard.py `
      phase173_r4_r15r17r3_goal_contract_audit/tests/test_reference_heading_contract.py
    if ($LASTEXITCODE -ne 0) {
        throw 'R15R17-R3 focused contract tests failed'
    }
    Write-Output 'R15R17R3_FOCUSED_PYTEST=PASS'

    if ($DryRun) {
        & python -B -m phase173_r4_r15r17r3_goal_contract_audit.audit --dry-run
    }
    else {
        & python -B -m phase173_r4_r15r17r3_goal_contract_audit.audit
    }
    if ($LASTEXITCODE -ne 0) {
        throw 'R15R17-R3 audit program failed'
    }
    $IndexAfter = (Invoke-CheckedGit -Arguments @('write-tree')).Trim()
    if ($IndexBefore -ne $IndexAfter) {
        throw 'Git index was changed during R15R17-R3 audit'
    }
    Write-Output 'R15R17R3_GIT_INDEX_PRESERVED=PASS'
    if ($DryRun) {
        Write-Output 'R15R17R3_DRY_RUN=PASS'
    }
    else {
        Write-Output 'R15R17R3_AUDIT_COMPLETE=PASS'
    }
    Invoke-CheckedGit -Arguments @('status', '-sb')
}
finally {
    Pop-Location
}
