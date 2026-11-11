[CmdletBinding()]
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    $Module = 'phase174_r3_r7_r67_zero_map_tex_arrow_fix.install'
    if ($DryRun) {
        python -B -m $Module --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R67 DryRun Source Guard failed' }
    } else {
        python -B -m $Module
        if ($LASTEXITCODE -ne 0) { throw 'R67 arrow patch failed' }
        python -B -m pytest -q -o addopts= -p no:cacheprovider --import-mode=importlib `
            'phase174_r3_r7_r67_zero_map_tex_arrow_fix/tests/test_install.py' `
            'phase174_r3_r7_r55r3r2_narrative_removal/tests/test_typed.py'
        if ($LASTEXITCODE -ne 0) { throw 'R67 focused pytest failed' }
        python -B -m $Module --audit-only
        if ($LASTEXITCODE -ne 0) { throw 'R67 public R57 proof and arrow audit failed' }
        Write-Output 'PHASE174_R67_GATE=PASS_R67_FOCUSED_AND_PUBLIC_ARROW'
        Write-Output '(END)'
    }
}
finally {
    Pop-Location
}
