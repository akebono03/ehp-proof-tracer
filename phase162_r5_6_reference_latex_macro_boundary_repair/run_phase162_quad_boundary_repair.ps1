$ErrorActionPreference = "Stop"
$repo = (Get-Location).Path
$source = Join-Path $PSScriptRoot "files"
$files = @(
    "toda_general_reference_schema.py",
    "tests\test_phase162_r5_6_final_reference_format.py"
)
foreach ($relative in $files) {
    $from = Join-Path $source $relative
    $to = Join-Path $repo $relative
    if (Test-Path $to) {
        Copy-Item -LiteralPath $to -Destination ($to + ".phase162_quad_boundary.bak") -Force
    }
    $directory = Split-Path -Parent $to
    if (-not (Test-Path $directory)) { New-Item -ItemType Directory -Path $directory -Force | Out-Null }
    Copy-Item -LiteralPath $from -Destination $to -Force
    Write-Host "Updated: $relative"
}
python -m pytest -q tests/test_phase162_r5_6_final_reference_format.py
if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed (exit code $LASTEXITCODE)" }
Write-Host "Macro-boundary focused tests complete. Full suite not run."
