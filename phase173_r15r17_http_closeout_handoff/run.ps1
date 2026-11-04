param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$root = (git rev-parse --show-toplevel).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Not in a Git repository' }
$here = (Get-Location).Path
$normalizedRoot = [System.IO.Path]::GetFullPath($root.Replace('/', [System.IO.Path]::DirectorySeparatorChar)).TrimEnd('\','/')
$normalizedHere = [System.IO.Path]::GetFullPath($here).TrimEnd('\','/')
if (-not [string]::Equals($normalizedRoot, $normalizedHere, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw 'Run this from the repository root'
}
$branch = (git branch --show-current).Trim()
if ($branch -ne 'develop') { throw "Unexpected branch: $branch" }
$head = (git rev-parse HEAD).Trim()
Write-Output "PHASE173_R15R17_HANDOFF_MODE=$(if ($DryRun) { 'DryRun' } else { 'ReportOnly' })"
Write-Output "PHASE173_R15R17_BRANCH=$branch"
Write-Output "PHASE173_R15R17_LOCAL_HEAD=$head"
git --no-pager status -sb
if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect Git status' }
Write-Output 'PHASE173_R15R17_HTTP_GATE=PASS_REPORTED_BY_USER_2026-11-04'
Write-Output 'PHASE173_R15R17_BROWSER_VISUAL_VERIFIED=UNCONFIRMED'
Write-Output 'PHASE173_R15R17_PHASE_END_FULL_PYTEST=NOT_RUN_BY_THIS_SCRIPT'
Write-Output 'PHASE173_R15R17_PRODUCTION_WRITES=NONE'
Write-Output 'PHASE173_R15R17_GIT_STAGE_RESET_CLEAN_COMMIT=NONE'
Write-Output 'PHASE173_R15R17_NEXT=VISUAL_CHECK_DOCUMENTS_PHASE_END_TEST'
