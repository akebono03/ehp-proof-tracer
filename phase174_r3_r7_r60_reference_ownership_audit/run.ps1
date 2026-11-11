[CmdletBinding()]
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    $module = 'phase174_r3_r7_r60_reference_ownership_audit.audit'
    if ($DryRun) {
        python -B -m $module --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R60 DryRun Source Guard failed' }
        exit 0
    }

    python -B -m $module
    if ($LASTEXITCODE -ne 0) { throw 'R60 citation ownership audit failed' }

    # Disable pytest's cache provider: the repository tracks cache/nodeids.
    python -B -m pytest -q -o addopts= -p no:cacheprovider --import-mode=importlib `
        'phase174_r3_r7_r60_reference_ownership_audit/tests/test_audit.py' `
        'phase174_r3_r7_r59_toda510_signed_semantics_audit/tests/test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R60 focused pytest failed' }

    Write-Output 'PHASE174_R60_GATE=PASS_R60_FOCUSED_AND_REFERENCE_AUDIT'
    Write-Output '(END)'
}
finally {
    Pop-Location
}
