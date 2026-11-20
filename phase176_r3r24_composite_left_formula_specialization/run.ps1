param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    if ($DryRun) {
        & python -B -m phase176_r3r24_composite_left_formula_specialization.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R3R24 DryRun failed' }
        exit 0
    }
    & python -B -m phase176_r3r24_composite_left_formula_specialization.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3R24 installer failed' }
    & python -B -m pytest -q -p no:cacheprovider `
        .\phase176_r3r24_composite_left_formula_specialization\tests `
        .\phase171_r2h_prop22_cited_hopf\tests\test_cited_formula.py `
        .\phase174_r3_r7_r9_composition_associativity\tests\test_rule.py `
        .\tests\test_hopf_rules.py
    if ($LASTEXITCODE -ne 0) { throw 'R3R24 focused pytest failed; inspect git diff and revert the one target file if necessary' }
    & git diff --check
    if ($LASTEXITCODE -ne 0) { throw 'R3R24 git diff check failed' }
    Write-Output 'PHASE176_R3R24_GATE=PASS_R3R24_FOCUSED_TESTS'
    Write-Output 'PHASE176_R3R24_FULL_PYTEST=NOT_RUN'
    Write-Output '(END)'
} finally { Pop-Location }
