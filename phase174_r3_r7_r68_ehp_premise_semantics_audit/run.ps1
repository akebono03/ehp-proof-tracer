[CmdletBinding()]
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    $module = 'phase174_r3_r7_r68_ehp_premise_semantics_audit.audit'
    if ($DryRun) {
        python -B -m $module --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R68 source guard preflight failed' }
        Write-Output 'PHASE174_R68_GATE=PASS_R68_DRYRUN'
        Write-Output '(END)'
    } else {
        python -B -m $module
        if ($LASTEXITCODE -ne 0) { throw 'R68 verified EHP premise audit failed' }
        python -B -m pytest -q -o addopts= -p no:cacheprovider --import-mode=importlib `
            'phase174_r3_r7_r68_ehp_premise_semantics_audit/tests/test_audit.py' `
            'phase174_r3_r7_r3_ehp_zero_rule/tests/test_rule.py' `
            'phase174_r3_r7_r5_zero_image_hopf_injective/tests/test_rule.py' `
            'phase174_r3_r7_r67_zero_map_tex_arrow_fix/tests/test_install.py'
        if ($LASTEXITCODE -ne 0) { throw 'R68 focused pytest failed' }
        Write-Output 'PHASE174_R68_GATE=PASS_R68_FOCUSED_AND_EHP_PREMISES'
        Write-Output '(END)'
    }
}
finally { Pop-Location }
