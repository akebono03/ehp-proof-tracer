param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $parameters = @()
    if ($DryRun) { $parameters += '--dry-run' }
    & python -B -m phase176_r3r45_direct_premise_audit.apply @parameters
    if ($LASTEXITCODE -ne 0) { throw 'R3R45 patch guard failed' }
    if ($DryRun) {
        Write-Host 'PHASE176_R3R45_GATE=PASS_R3R45_DRYRUN'
    } else {
        & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
            .\phase176_r3r45_direct_premise_audit\tests\test_audit.py `
            .\phase174_r3_r7_r55r3r2_narrative_removal\tests\test_typed.py `
            .\phase176_r3r42_root_backward_frontier_audit\tests\test_audit.py `
            .\phase176_r3r44_public_subgroup_lift\tests\test_public_subgroup_lift.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R45 focused pytest failed' }
        & python -B -m phase176_r3r45_direct_premise_audit.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3R45 Web audit failed' }
        & git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'R3R45 diff check failed' }
        Write-Host 'PHASE176_R3R45_GATE=PASS_R3R45_FOCUSED_TESTS'
    }
    Write-Host '(END)'
} finally { Pop-Location }
