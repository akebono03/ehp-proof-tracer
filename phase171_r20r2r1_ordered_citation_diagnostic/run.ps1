param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldBytecode = $env:PYTHONDONTWRITEBYTECODE
Push-Location $Root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    Write-Host 'PHASE171_R20R2R1_DIAGNOSTIC_START'
    & python '.\phase171_r20r2r1_ordered_citation_diagnostic\audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R20R2R1 audit failed before pytest.' }
    if ($DryRun) {
        Write-Host 'PHASE171_R20R2R1_PYTEST=SKIPPED_DRY_RUN'
        return
    }
    Write-Host 'PHASE171_R20R2R1_FOCUSED_PYTEST_START'
    & python -m pytest -p no:cacheprovider -q `
        '.\phase165_r52_r15_ordered_citation\test_phase165_r52_r15_ordered_citation.py::test_ordered_reference_requires_only_prior_order' `
        '.\phase165_r52_r15_ordered_citation\test_phase165_r52_r15_ordered_citation.py::test_ordered_reference_integrates_with_backward_search'
    $TestExit = $LASTEXITCODE
    Write-Host "PHASE171_R20R2R1_FOCUSED_PYTEST_EXIT=$TestExit"
    & git status -sb
    & git diff --stat
    if ($TestExit -ne 0) { throw 'R20R2R1 focused pytest still fails; see diagnostic.json.' }
    Write-Host 'PHASE171_R20R2R1_FOCUSED_PYTEST=PASS'
}
finally {
    if ($null -eq $OldBytecode) {
        Remove-Item Env:PYTHONDONTWRITEBYTECODE -ErrorAction SilentlyContinue
    } else {
        $env:PYTHONDONTWRITEBYTECODE = $OldBytecode
    }
    Pop-Location
}
