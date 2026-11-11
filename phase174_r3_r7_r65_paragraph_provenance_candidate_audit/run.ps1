[CmdletBinding()]
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    $Module = 'phase174_r3_r7_r65_paragraph_provenance_candidate_audit.audit'
    if ($DryRun) {
        python -B -m $Module --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R65 DryRun Source Guard failed' }
    } else {
        python -B -m $Module
        if ($LASTEXITCODE -ne 0) { throw 'R65 public paragraph audit failed' }
        python -B -m pytest -q -o addopts= -p no:cacheprovider --import-mode=importlib `
            'phase174_r3_r7_r65_paragraph_provenance_candidate_audit/tests/test_audit.py' `
            'phase174_r3_r7_r64_sentence_coverage_frontier_audit/tests/test_audit.py' `
            'phase174_r3_r7_r63_sentence_witness_audit/tests/test_audit.py'
        if ($LASTEXITCODE -ne 0) { throw 'R65 focused pytest failed' }
        Write-Output 'PHASE174_R65_GATE=PASS_R65_FOCUSED_AND_PARAGRAPH_PROVENANCE_CANDIDATES'
        Write-Output '(END)'
    }
}
finally {
    Pop-Location
}
