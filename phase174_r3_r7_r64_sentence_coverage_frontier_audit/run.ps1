[CmdletBinding()]
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    $module = 'phase174_r3_r7_r64_sentence_coverage_frontier_audit.audit'
    if ($DryRun) {
        python -B -m $module --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R64 DryRun Source Guard failed' }
    } else {
        python -B -m $module
        if ($LASTEXITCODE -ne 0) { throw 'R64 public sentence inventory failed' }
        python -B -m pytest -q -o addopts= -p no:cacheprovider --import-mode=importlib `
            'phase174_r3_r7_r64_sentence_coverage_frontier_audit/tests/test_audit.py' `
            'phase174_r3_r7_r63_sentence_witness_audit/tests/test_audit.py'
        if ($LASTEXITCODE -ne 0) { throw 'R64 focused pytest failed' }
        Write-Output 'PHASE174_R64_GATE=PASS_R64_FOCUSED_AND_COVERAGE_FRONTIER'
        Write-Output '(END)'
    }
}
finally {
    Pop-Location
}
