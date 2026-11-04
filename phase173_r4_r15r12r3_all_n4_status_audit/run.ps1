param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$ExpectedHead = '715dff58df263c419cdcb45c51a1fa169a87de45'
$SourceBlobGuards = [ordered]@{
    'data/sphere.csv' = 'b7e98a4469e0dcf2c5ea16691a7225951fd36395'
    'phase173_r4_r10_general_toda56_core/core.py' = 'd35600804ecbbc5f8566d52e45a2f6ecf8816347'
    'phase165_r55_nk_only_goal.py' = '9aa232c8f98a7a75f27266044224eddfa98c5e04'
    'phase169_r10e4_ordered_db_prior/db_prior.py' = 'ed8c6a1f0f6f130005d42a2edba4ab40991e879b'
    'phase168_r3_5_model_renderer.py' = '6dd75099bb2c71fb9873477cb36c11bdb7dad410'
    'phase165_r52_r3_web_adapter.py' = '211fdb73342019cee4503c01e549c118e286125a'
    'phase168_r3_3_proof_narrative_model.py' = '5bc85174ec5b04924603e7160a3fb262041e00fd'
    'web_group_proof.py' = '2c66da9c8e80a13812a63b6adda34c9414d8413c'
    'web_group_proof_common.py' = '943e25ff4607bad2f6a7a8284304f4160131765c'
    'phase173_r4_r15r8_public_abstract_sidecar/attach.py' = '0a35ebc183ca0ad2e23edf4d4601333d4b755247'
    'phase173_r4_r15r7_source_first_abstract_certificate/search.py' = '2cf9f4c998f4876a44c7d057ca1caaf7ca7bdb80'
    'phase173_r4_r15r12_reference_correction/tests/test_integration.py' = 'ead4223ec8166323618d496a31f82298b91a73f9'
}
Push-Location $RepoRoot
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'GitHub develop fetch failed' }
    $Branch = (git branch --show-current).Trim()
    $LocalHead = (git rev-parse HEAD).Trim()
    $RemoteHead = (git rev-parse origin/develop).Trim()
    Write-Output "AUDIT_BRANCH=$Branch"
    Write-Output "AUDIT_LOCAL_HEAD=$LocalHead"
    Write-Output "AUDIT_REMOTE_HEAD=$RemoteHead"
    if ($Branch -ne 'develop' -or $LocalHead -ne $RemoteHead -or $LocalHead -ne $ExpectedHead) {
        throw 'HEAD/branch guard failed; re-review new GitHub contents before executing'
    }
    $Tracked = @(git diff --name-only)
    $Staged = @(git diff --cached --name-only)
    if ($LASTEXITCODE -ne 0) { throw 'git diff guard failed' }
    if ($Tracked.Count -gt 0 -or $Staged.Count -gt 0) {
        Write-Output 'AUDIT_TRACKED_CHANGES_PRESENT=True'
        git status -sb
        throw 'Tracked/staged worktree changes need review; no changes were made'
    }
    foreach ($File in $SourceBlobGuards.Keys) {
        $ActualBlob = (git rev-parse "HEAD:$File").Trim()
        if ($LASTEXITCODE -ne 0 -or $ActualBlob -ne $SourceBlobGuards[$File]) {
            throw "Source Guard mismatch: $File"
        }
    }
    Write-Output "AUDIT_SOURCE_GUARD=PASS"
    Write-Output "AUDIT_SOURCE_GUARD_FILES=$($SourceBlobGuards.Count)"
    Write-Output 'AUDIT_PRODUCTION_CODE_EDITS=NONE'
    Write-Output 'AUDIT_FULL_PYTEST_RUN=False'
    Write-Output 'AUDIT_COMMIT_ATTEMPTED=False'
    if ($DryRun) {
        python -m pytest -q -p no:cacheprovider phase173_r4_r15r12r3_all_n4_status_audit/tests/test_contract.py
        if ($LASTEXITCODE -ne 0) { throw 'Focused audit contract pytest failed' }
        Write-Output 'AUDIT_DRY_RUN=PASS'
        Write-Output 'AUDIT_SCAN_EXECUTED=False'
    } else {
        python -m phase173_r4_r15r12r3_all_n4_status_audit.audit `
            --head "$LocalHead" `
            --output (Join-Path $PSScriptRoot 'all_n4_status_report.json') `
            --csv-output (Join-Path $PSScriptRoot 'all_n4_status_report.csv') `
            --markdown-output (Join-Path $PSScriptRoot 'all_n4_status_report.md')
        $ScanExit = $LASTEXITCODE
        if ($ScanExit -ne 0) {
            Write-Output 'AUDIT_SCAN_REVIEW_REQUIRED=True'
            throw 'Audit scan observed public Web errors or inconsistencies; inspect generated report'
        }
        Write-Output 'AUDIT_N4_READ_ONLY_SCAN=PASS'
    }
    git status -sb
    if ($LASTEXITCODE -ne 0) { throw 'git status failed' }
} finally {
    Pop-Location
}
