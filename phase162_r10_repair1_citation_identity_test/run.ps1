$ErrorActionPreference = "Stop"
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$installed = Join-Path $root "phase162_r10_reference_boundary"
$target = Join-Path $installed "test_r10.py"
$source = Join-Path $package "test_r10.py"
$boundary = Join-Path $root "phase162_reference_boundary.py"
if (!(Test-Path (Join-Path $root "proof.py"))) { throw "Run from repository root" }
if (!(Test-Path $boundary)) { throw "R10 reference boundary is not installed" }
if (!(Test-Path $target)) { throw "Original R10 focused test not found" }
$previous = Get-Content -LiteralPath $target -Raw -Encoding UTF8
if ($previous.Contains('assert len(citations) == 1')) {
    $backup = "$target.phase162_r10_repair1.bak"
    if (!(Test-Path $backup)) { Copy-Item -LiteralPath $target -Destination $backup }
    Copy-Item -LiteralPath $source -Destination $target -Force
    Write-Host "Updated: $target"
    Write-Host "Backup: $backup"
} elseif ((Get-FileHash $target -Algorithm SHA256).Hash -eq (Get-FileHash $source -Algorithm SHA256).Hash) {
    Write-Host "R10 focused test already updated; running verification."
} else {
    throw "Guard: R10 test differs from expected version; no overwrite"
}
python -m pytest $target -q
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "R10 Repair 1 focused tests complete. Full suite not run."
