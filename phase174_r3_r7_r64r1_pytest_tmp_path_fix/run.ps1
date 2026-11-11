[CmdletBinding()]
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    $module = 'phase174_r3_r7_r64r1_pytest_tmp_path_fix.install'
    if ($DryRun) {
        python -B -m $module --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R64R1 source guard failed' }
        python -B -m phase174_r3_r7_r64_sentence_coverage_frontier_audit.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R64 preflight after R64R1 failed' }
        Write-Output 'PHASE174_R64R1_GATE=PASS_R64R1_DRYRUN'
        Write-Output '(END)'
    } else {
        python -B -m $module
        if ($LASTEXITCODE -ne 0) { throw 'R64R1 installer failed' }
        python -B -m phase174_r3_r7_r64_sentence_coverage_frontier_audit.audit
        if ($LASTEXITCODE -ne 0) { throw 'R64 public coverage audit failed' }
        python -B -m pytest -q -o addopts= -p no:cacheprovider --import-mode=importlib `
            'phase174_r3_r7_r64r1_pytest_tmp_path_fix/tests/test_install.py' `
            'phase174_r3_r7_r64_sentence_coverage_frontier_audit/tests/test_audit.py' `
            'phase174_r3_r7_r63_sentence_witness_audit/tests/test_audit.py'
        if ($LASTEXITCODE -ne 0) { throw 'R64R1 focused pytest failed' }
        Write-Output 'PHASE174_R64R1_GATE=PASS_R64R1_FOCUSED_AND_R64_COVERAGE_FRONTIER'
        Write-Output '(END)'
    }
}
finally {
    Pop-Location
}
