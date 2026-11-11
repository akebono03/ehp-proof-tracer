param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$env:PYTHONPATH = $root
$package = 'phase174_r3_r7_r70_verified_narrative_projection'

if ($DryRun) {
    python -m "$package.install" --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R70 install DryRun failed' }
    python -m "$package.audit" --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R70 public audit DryRun failed' }
    Write-Output 'PHASE174_R70_GATE=PASS_R70_DRYRUN'
    Write-Output '(END)'
    exit 0
}

python -m "$package.install"
if ($LASTEXITCODE -ne 0) { throw 'R70 reviewed formatter patch failed' }
python -m pytest -q -o addopts= --import-mode=importlib `
    "$package/tests/test_projection.py" `
    'phase171_r20r13_eta_sentence_layout/tests/test_projection.py' `
    'phase171_r20r13r2_multiple_blank_eta_merge/tests/test_correction.py' `
    'phase174_r3_r7_r69_general_narrative_gap_audit/tests/test_audit.py' `
    'phase174_r3_r7_r68_ehp_premise_semantics_audit/tests/test_audit.py'
if ($LASTEXITCODE -ne 0) { throw 'R70 focused pytest failed' }
python -m "$package.audit"
if ($LASTEXITCODE -ne 0) { throw 'R70 public proof display audit failed' }
Write-Output 'PHASE174_R70_GATE=PASS_R70_FOCUSED_AND_PUBLIC_GENERAL_NARRATIVE'
Write-Output '(END)'
