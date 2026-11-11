[CmdletBinding()]
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    $module = 'phase174_r3_r7_r59_toda510_signed_semantics_audit.audit'
    if ($DryRun) {
        python -m $module --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R59 DryRun Source Guard failed' }
        exit 0
    }

    python -m $module
    if ($LASTEXITCODE -ne 0) { throw 'R59 cited semantic/public audit failed' }

    python -m pytest -q -o addopts= --import-mode=importlib `
        'phase174_r3_r7_r59_toda510_signed_semantics_audit/tests/test_audit.py' `
        'phase174_r3_r7_r34_prior_lower_delta_source_wiring/tests/test_source.py' `
        'phase174_r3_r7_r35_isolated_cyclic_delta_kernel/tests/test_rule.py'
    if ($LASTEXITCODE -ne 0) { throw 'R59 focused pytest failed' }

    Write-Output 'PHASE174_R59_GATE=PASS_R59_FOCUSED_AND_PUBLIC'
    Write-Output '(END)'
}
finally {
    Pop-Location
}
