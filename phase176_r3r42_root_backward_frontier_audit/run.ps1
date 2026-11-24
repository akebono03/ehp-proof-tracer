param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    $env:PYTHONUTF8 = '1'
    $module = 'phase176_r3r42_root_backward_frontier_audit.audit'
    if ($DryRun) {
        python -B -m $module --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R3R42 DryRun audit failed' }
        exit 0
    }
    python -B -m $module
    if ($LASTEXITCODE -ne 0) { throw 'R3R42 audit failed' }
    python -B -m pytest -q --import-mode=importlib -p no:cacheprovider `
        phase176_r3r42_root_backward_frontier_audit/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R3R42 focused pytest failed' }
    git diff --check
    if ($LASTEXITCODE -ne 0) { throw 'R3R42 git diff check failed' }
    Write-Output 'PHASE176_R3R42_GATE=PASS_R3R42_FRONTIER_AUDIT_FOCUSED_TESTS'
    Write-Output 'PHASE176_R3R42_FULL_PYTEST=NOT_RUN'
    Write-Output '(END)'
} finally {
    Pop-Location
}
