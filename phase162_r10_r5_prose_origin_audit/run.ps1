$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$folder = Join-Path $root 'phase162_r10_r5_prose_origin_audit'
if (-not (Test-Path (Join-Path $folder 'audit.py'))) {
  throw "Run from project root: $folder"
}
$env:PYTHONPATH = "$folder;$root"
python -B -m pytest -q (Join-Path $folder 'test_r10_r5.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B (Join-Path $folder 'audit.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R10-R5 audit complete; repository source files unchanged. Whole suite not run.'
