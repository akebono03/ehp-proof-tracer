param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$env:PYTHONPATH = $root
$env:PYTHONDONTWRITEBYTECODE = '1'
$package = 'phase174_r3_r7_r71_common_narrative_regression'

python -m "$package.audit" --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R71 source guard failed' }

if ($DryRun) {
    Write-Output 'PHASE174_R71_GATE=PASS_R71_DRYRUN'
    Write-Output '(END)'
    exit 0
}

python -m pytest -q -p no:cacheprovider -o addopts= --import-mode=importlib `
    "$package/tests/test_audit.py" `
    'phase174_r3_r7_r70r1_assoc_chain_display_fix/tests/test_install.py' `
    'phase174_r3_r7_r70_verified_narrative_projection/tests/test_projection.py' `
    'phase171_r20r13_eta_sentence_layout/tests/test_projection.py' `
    'phase171_r20r13r2_multiple_blank_eta_merge/tests/test_correction.py' `
    'phase174_r3_r7_r69_general_narrative_gap_audit/tests/test_audit.py' `
    'phase174_r3_r7_r68_ehp_premise_semantics_audit/tests/test_audit.py' `
    'phase174_r3_r7_r67_zero_map_tex_arrow_fix/tests/test_install.py' `
    'phase174_r3_r5_finite_cyclic_extension/tests/test_rule.py'
if ($LASTEXITCODE -ne 0) { throw 'R71 focused pytest failed' }

python -m "$package.audit"
if ($LASTEXITCODE -ne 0) { throw 'R71 public cross-group regression failed' }

Write-Output 'PHASE174_R71_GATE=PASS_R71_FOCUSED_AND_CROSS_GROUP'
Write-Output '(END)'
