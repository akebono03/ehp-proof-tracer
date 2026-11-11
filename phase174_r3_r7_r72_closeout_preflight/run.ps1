param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$env:PYTHONPATH = $root
$env:PYTHONDONTWRITEBYTECODE = '1'
$package = 'phase174_r3_r7_r72_closeout_preflight'

python -m "$package.audit" --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R72 source/head/document preflight failed' }

if ($DryRun) {
    Write-Output 'PHASE174_R72_GATE=PASS_R72_DRYRUN'
    Write-Output '(END)'
    exit 0
}

python -m pytest -q -p no:cacheprovider -o addopts= --import-mode=importlib `
    "$package/tests/test_audit.py" `
    'phase174_r3_r7_r71_common_narrative_regression/tests/test_audit.py' `
    'phase174_r3_r7_r70r1_assoc_chain_display_fix/tests/test_install.py' `
    'phase174_r3_r7_r70_verified_narrative_projection/tests/test_projection.py'
if ($LASTEXITCODE -ne 0) { throw 'R72 focused pytest failed' }

python -m "$package.audit"
if ($LASTEXITCODE -ne 0) { throw 'R72 prior-evidence or partial public preflight failed' }

Write-Output 'PHASE174_R72_GATE=PASS_R72_FOCUSED_AND_PREFLIGHT'
Write-Output '(END)'
