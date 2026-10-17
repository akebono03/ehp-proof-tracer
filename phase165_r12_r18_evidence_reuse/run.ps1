$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$source = Join-Path $package 'phase165_r12_r18_evidence_reuse.py'
$target = Join-Path $root 'phase165_r12_r18_evidence_reuse.py'
if ((Test-Path $target) -and ((Get-FileHash $target).Hash -ne (Get-FileHash $source).Hash)) {
    throw 'Existing R12-R18 implementation differs; no overwrite performed'
}
Copy-Item -LiteralPath $source -Destination $target -Force
$env:PYTHONPATH = $root
python -m pytest -q (Join-Path $package 'tests/test_phase165_r12_r18_evidence_reuse.py')
if ($LASTEXITCODE -ne 0) { throw 'R12-R18 targeted pytest failed' }
python (Join-Path $package 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R12-R18 audit failed' }
Write-Host 'R12-R18 focused evidence reuse audit finished; full pytest NOT run.'
