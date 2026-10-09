$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$folder = Join-Path $repo 'phase162_r10_r8_branch_evidence'
$source = Join-Path $repo 'phase162_r10_r5_prose_origin.json'
if (-not (Test-Path -LiteralPath $source -PathType Leaf)) {
    throw "Required R10-R5 audit JSON not found: $source"
}
$testPath = Join-Path $folder 'test_r10_r8.py'
$auditPath = Join-Path $folder 'audit.py'
if (-not (Test-Path -LiteralPath $testPath -PathType Leaf)) {
    throw "R10-R8 test file not found: $testPath"
}
if (-not (Test-Path -LiteralPath $auditPath -PathType Leaf)) {
    throw "R10-R8 audit script not found: $auditPath"
}
python -B -m pytest -q $testPath
if ($LASTEXITCODE -ne 0) {
    throw 'R10-R8 focused tests failed'
}
python -B $auditPath --repo $repo
if ($LASTEXITCODE -ne 0) {
    throw 'R10-R8 audit failed'
}
Write-Host 'Read-only R10-R8 audit finished. Full suite not run.'
