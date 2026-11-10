param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    if ($DryRun) {
        python -m phase174_r3_r7_r55r2_reference_tree_audit.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R55R2 Source Guard failed' }
        Write-Output 'PHASE174_R55R2_DRYRUN=PASS'
        Write-Output '(END)'
        exit 0
    }

    python -m phase174_r3_r7_r55r2_reference_tree_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R55R2 Source Guard failed' }

    python -m pytest -q --import-mode=importlib `
        .\phase174_r3_r7_r55r2_reference_tree_audit\tests\test_audit.py `
        .\phase174_r3_r7_r55_common_exactness_intro\tests\test_http.py `
        .\phase174_r3_r7_r37_upper_delta_surjectivity_isolated\tests\test_rule.py
    if ($LASTEXITCODE -ne 0) { throw 'R55R2 Focused pytest failed' }

    python -m phase174_r3_r7_r55r2_reference_tree_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R55R2 evidence audit failed' }
    Write-Output 'PHASE174_R55R2_FOCUSED_TESTS=PASS'
    Write-Output '(END)'
}
finally {
    Pop-Location
}
