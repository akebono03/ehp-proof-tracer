param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$env:PYTHONPATH = $root
$env:PYTHONDONTWRITEBYTECODE = '1'
$package = 'phase174_r3_r7_r73_closeout_documents'

python -B -m "$package.audit" --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R73 reviewed-source and prior-report preflight failed' }

if ($DryRun) {
    Write-Output 'PHASE174_R73_GATE=PASS_R73_DRYRUN'
    Write-Output '(END)'
    exit 0
}

python -B -m pytest -q -p no:cacheprovider -o addopts= --import-mode=importlib `
    "$package/tests/test_audit.py" `
    'phase174_r3_r7_r72_closeout_preflight/tests/test_audit.py'
if ($LASTEXITCODE -ne 0) { throw 'R73 focused pytest failed before document write' }

python -B -m "$package.audit"
if ($LASTEXITCODE -ne 0) { throw 'R73 five full-document installation failed' }

Write-Output 'PHASE174_R73_GATE=PASS_R73_FOCUSED_AND_FIVE_FULL_DOCUMENTS'
Write-Output '(END)'
