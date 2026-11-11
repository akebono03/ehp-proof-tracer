[CmdletBinding()]
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    $module = 'phase174_r3_r7_r62_attribution_policy_boundary_audit.audit'
    if ($DryRun) {
        python -B -m $module --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R62 DryRun source and policy guard failed' }
    } else {
        python -B -m $module
        if ($LASTEXITCODE -ne 0) { throw 'R62 public policy audit failed' }
        python -B -m pytest -q -o addopts= -p no:cacheprovider --import-mode=importlib `
            'phase174_r3_r7_r62_attribution_policy_boundary_audit/tests/test_audit.py' `
            'phase174_r3_r7_r61_reference_attribution_route_audit/tests/test_audit.py' `
            'phase174_r3_r7_r60_reference_ownership_audit/tests/test_audit.py'
        if ($LASTEXITCODE -ne 0) { throw 'R62 focused pytest failed' }
        Write-Output 'PHASE174_R62_GATE=PASS_R62_FOCUSED_AND_PUBLIC_POLICY_AUDIT'
        Write-Output '(END)'
    }
}
finally {
    Pop-Location
}
