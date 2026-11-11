[CmdletBinding()]
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    $module = 'phase174_r3_r7_r69_general_narrative_gap_audit.audit'
    if ($DryRun) {
        python -B -m $module --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R69 Source Guard DryRun failed' }
        Write-Output 'PHASE174_R69_GATE=PASS_R69_DRYRUN'
        Write-Output '(END)'
    } else {
        python -B -m $module
        if ($LASTEXITCODE -ne 0) { throw 'R69 audited proof-step boundary failed' }
        python -B -m pytest -q -o addopts= -p no:cacheprovider --import-mode=importlib `
            'phase174_r3_r7_r69_general_narrative_gap_audit/tests/test_audit.py' `
            'phase174_r3_r7_r68_ehp_premise_semantics_audit/tests/test_audit.py'
        if ($LASTEXITCODE -ne 0) { throw 'R69 focused pytest failed' }
        Write-Output 'PHASE174_R69_GATE=PASS_R69_FOCUSED_AND_NARRATIVE_BOUNDARY'
        Write-Output '(END)'
    }
}
finally { Pop-Location }
