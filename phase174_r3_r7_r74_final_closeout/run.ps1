param([switch]$DryRun)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$env:PYTHONPATH = $root
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:GIT_PAGER = 'cat'
$package = 'phase174_r3_r7_r74_final_closeout'

python -B -m "$package.audit" --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R74 reviewed-source or documents preflight failed' }

if ($DryRun) {
    Write-Output 'PHASE174_R74_GATE=PASS_R74_DRYRUN'
    Write-Output '(END)'
    exit 0
}

python -B -m pytest -q -p no:cacheprovider -o addopts= --import-mode=importlib `
    "$package/tests/test_audit.py" `
    'phase174_r3_r7_r73_closeout_documents/tests/test_audit.py'
if ($LASTEXITCODE -ne 0) { throw 'R74 focused test contracts failed before full suite' }

python -B -m "$package.audit"
if ($LASTEXITCODE -ne 0) { throw 'R74 full active-suite or document gate failed' }

Write-Output 'PHASE174_R74_GATE=PASS_R74_FOCUSED_FULL_SUITE_AND_FIVE_DOCUMENTS'
Write-Output '(END)'
