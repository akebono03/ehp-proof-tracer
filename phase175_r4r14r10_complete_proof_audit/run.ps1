param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $here
Push-Location $root
try {
    python -m phase175_r4r14r10_complete_proof_audit.audit $(if ($DryRun) { '--dry-run' })
    if ($LASTEXITCODE -ne 0) { throw 'R4R14R10 audit failed' }
    if (-not $DryRun) {
        python -m pytest -q --import-mode=importlib `
            phase175_r4r14r10_complete_proof_audit/tests `
            phase175_r4r14r9_literature_zero_image/tests `
            phase175_r4r14r6_surjective_zero_codomain/tests
        if ($LASTEXITCODE -ne 0) { throw 'R4R14R10 focused pytest failed' }
        git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'git diff --check failed' }
        Write-Output 'R4R14R10_FULL_PYTEST=NOT_RUN'
        Write-Output 'R4R14R10_HISTORICAL_SOURCE_GUARD=FOUR_KNOWN_FAILURES_NOT_RERUN'
        Write-Output '(END)'
    }
} finally {
    Pop-Location
}
