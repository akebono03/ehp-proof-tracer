param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $folder
Push-Location $root
try {
    if ($DryRun) {
        python -B -m phase175_r4r14r13_final_gate_preflight.audit --dry-run
    } else {
        python -B -m phase175_r4r14r13_final_gate_preflight.audit
    }
    if ($LASTEXITCODE -ne 0) {
        throw 'R4R14R13 preflight audit failed'
    }
    if (-not $DryRun) {
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider `
            phase175_r4r14r13_final_gate_preflight/tests `
            phase175_r4r14r12_closeout_documents/tests
        if ($LASTEXITCODE -ne 0) {
            throw 'R4R14R13 focused pytest failed'
        }
        git diff --check
        if ($LASTEXITCODE -ne 0) {
            throw 'R4R14R13 git diff check failed'
        }
        Write-Output 'R4R14R13_FULL_PYTEST=NOT_RUN'
        Write-Output 'R4R14R13_HISTORICAL_SOURCE_GUARD=FOUR_KNOWN_FAILURES_NOT_RERUN'
        Write-Output '(END)'
    }
} finally {
    Pop-Location
}
