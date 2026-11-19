param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $here
Push-Location $root
try {
    python -B -m phase175_r4r14r11_closeout_preflight.audit $(if ($DryRun) { '--dry-run' })
    if ($LASTEXITCODE -ne 0) {
        throw 'R4R14R11 read-only audit failed'
    }
    if (-not $DryRun) {
        python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
            phase175_r4r14r11_closeout_preflight/tests `
            phase175_r4r14r10_complete_proof_audit/tests `
            phase175_r4r14r9_literature_zero_image/tests
        if ($LASTEXITCODE -ne 0) {
            throw 'R4R14R11 focused pytest failed'
        }
        git diff --check
        if ($LASTEXITCODE -ne 0) {
            throw 'R4R14R11 git diff --check failed'
        }
        Write-Output 'R4R14R11_HISTORICAL_GUARD=FOUR_KNOWN_FAILURES_NOT_RERUN'
        Write-Output 'R4R14R11_FULL_PYTEST=NOT_RUN'
        Write-Output '(END)'
    }
} finally {
    Pop-Location
}
