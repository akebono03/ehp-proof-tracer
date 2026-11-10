[CmdletBinding()]
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    $module = 'phase174_r3_r7_r61_reference_attribution_route_audit.audit'
    if ($DryRun) {
        python -B -m $module --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R61 DryRun Source Guard failed' }
    } else {
        python -B -m $module
        if ($LASTEXITCODE -ne 0) { throw 'R61 public attribution audit failed' }
        python -B -m pytest -q -o addopts= -p no:cacheprovider --import-mode=importlib `
            'phase174_r3_r7_r61_reference_attribution_route_audit/tests/test_audit.py' `
            'phase174_r3_r7_r60_reference_ownership_audit/tests/test_audit.py'
        if ($LASTEXITCODE -ne 0) { throw 'R61 focused pytest failed' }
        Write-Output 'PHASE174_R61_GATE=PASS_R61_FOCUSED_AND_PUBLIC_REFERENCE_AUDIT'
        Write-Output '(END)'
    }
}
finally {
    Pop-Location
}
