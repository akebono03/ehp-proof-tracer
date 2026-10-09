$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$folder = Join-Path $repo 'phase162_r10_r6_origin_diagnosis'
$inputFile = Join-Path $repo 'phase162_r10_r5_prose_origin.json'
if (!(Test-Path $inputFile)) {
    throw "R10-R5 audit JSON not found: $inputFile. Run R10-R5 first."
}
$env:PYTHONDONTWRITEBYTECODE = '1'
python -B -m pytest -q (Join-Path $folder 'test_r10_r6.py')
if ($LASTEXITCODE -ne 0) { throw 'R10-R6 focused tests failed' }
python -B (Join-Path $folder 'audit.py') --input $inputFile --out $repo
if ($LASTEXITCODE -ne 0) { throw 'R10-R6 audit failed' }
Write-Host 'R10-R6 read-only audit complete. Whole suite not run.'
