[CmdletBinding()]
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    $installer = 'phase174_r3_r7_r60r1_reviewed_head_lineage_fix.install'
    $r60 = '.\phase174_r3_r7_r60_reference_ownership_audit\run.ps1'
    if ($DryRun) {
        python -B -m $installer --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R60R1 DryRun preflight failed' }
        Write-Output 'PHASE174_R60R1_GATE=PASS_R60R1_DRYRUN'
        Write-Output '(END)'
        exit 0
    }

    python -B -m $installer
    if ($LASTEXITCODE -ne 0) { throw 'R60R1 exact source patch failed' }

    powershell -NoProfile -ExecutionPolicy Bypass -File $r60 -DryRun
    if ($LASTEXITCODE -ne 0) { throw 'R60 reviewed-head corrected DryRun failed' }

    python -B -m pytest -q -o addopts= -p no:cacheprovider --import-mode=importlib `
        'phase174_r3_r7_r60r1_reviewed_head_lineage_fix/tests/test_install.py'
    if ($LASTEXITCODE -ne 0) { throw 'R60R1 focused installer tests failed' }

    powershell -NoProfile -ExecutionPolicy Bypass -File $r60
    if ($LASTEXITCODE -ne 0) { throw 'R60 source/reference/public audit failed' }

    Write-Output 'PHASE174_R60R1_GATE=PASS_R60R1_FOCUSED_AND_R60_REFERENCE_AUDIT'
    Write-Output '(END)'
}
finally {
    Pop-Location
}
