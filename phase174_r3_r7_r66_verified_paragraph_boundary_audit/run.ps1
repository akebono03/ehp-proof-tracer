[CmdletBinding()]
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    $Module = 'phase174_r3_r7_r66_verified_paragraph_boundary_audit.audit'
    if ($DryRun) {
        python -B -m $Module --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R66 DryRun Source Guard failed' }
    } else {
        python -B -m $Module
        if ($LASTEXITCODE -ne 0) { throw 'R66 public proof boundary audit failed' }
        python -B -m pytest -q -o addopts= -p no:cacheprovider --import-mode=importlib `
            'phase174_r3_r7_r66_verified_paragraph_boundary_audit/tests/test_audit.py' `
            'phase174_r3_r7_r65_paragraph_provenance_candidate_audit/tests/test_audit.py' `
            'phase174_r3_r7_r63_sentence_witness_audit/tests/test_audit.py'
        if ($LASTEXITCODE -ne 0) { throw 'R66 focused pytest failed' }
        Write-Output 'PHASE174_R66_GATE=PASS_R66_FOCUSED_AND_PARAGRAPH_BOUNDARIES'
        Write-Output '(END)'
    }
}
finally {
    Pop-Location
}
