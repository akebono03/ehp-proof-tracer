param(
    [switch]$DryRun,
    [switch]$KeepR20
)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    $InstallerArgs = @('.\phase171_r20r2_first_successful_search\install.py')
    if ($DryRun) { $InstallerArgs += '--dry-run' }
    if ($KeepR20) { $InstallerArgs += '--keep-r20' }
    & python @InstallerArgs
    if ($LASTEXITCODE -ne 0) { throw 'R20R2 installer failed; tests were not started.' }
    if ($DryRun) {
        Write-Host 'PHASE171_R20R2_TESTS=SKIPPED_DRY_RUN'
        return
    }
    Write-Host 'PHASE171_R20R2_FOCUSED_PYTEST_START'
    & python -m pytest -q `
        .\phase171_r20r2_first_successful_search\tests\test_first_successful_search.py `
        .\tests\test_phase165_r3_recursive_search.py `
        .\phase165_r52_r15_ordered_citation\test_phase165_r52_r15_ordered_citation.py `
        .\phase165_r12_r33_proof_tree_dedup\test_phase165_r12_r33_proof_tree_dedup.py
    if ($LASTEXITCODE -ne 0) { throw 'R20R2 focused pytest failed.' }
    Write-Host 'PHASE171_R20R2_FOCUSED_PYTEST=PASS'
    & git status -sb
    & git diff --stat
}
finally {
    Pop-Location
}
