param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$env:PYTHONPATH = $root
$package = 'phase174_r3_r7_r70r1_assoc_chain_display_fix'

python -m "$package.install" $(if ($DryRun) { '--dry-run' })
if ($LASTEXITCODE -ne 0) { throw 'R70R1 source guard or installer failed' }

if ($DryRun) {
    Write-Output 'PHASE174_R70R1_GATE=PASS_R70R1_DRYRUN'
    Write-Output '(END)'
    exit 0
}

python -m pytest -q -p no:cacheprovider -o addopts= --import-mode=importlib `
    "$package/tests/test_install.py" `
    'phase174_r3_r7_r70_verified_narrative_projection/tests/test_projection.py' `
    'phase171_r20r13_eta_sentence_layout/tests/test_projection.py' `
    'phase171_r20r13r2_multiple_blank_eta_merge/tests/test_correction.py' `
    'phase174_r3_r7_r69_general_narrative_gap_audit/tests/test_audit.py' `
    'phase174_r3_r7_r68_ehp_premise_semantics_audit/tests/test_audit.py'
if ($LASTEXITCODE -ne 0) { throw 'R70R1 focused pytest failed' }

python -m phase174_r3_r7_r70_verified_narrative_projection.audit
if ($LASTEXITCODE -ne 0) { throw 'R70R1 R70 public narrative regression failed' }

Write-Output 'PHASE174_R70R1_GATE=PASS_R70R1_FOCUSED_AND_PUBLIC_ASSOCIATIVITY'
Write-Output '(END)'
