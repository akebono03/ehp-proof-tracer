$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$review = Join-Path $root 'phase163_r4_r45_output\review.json'
$tex = Join-Path $root 'phase163_r4_r42_tex_extract\inputs\Toda_05_2(6).tex'
$output = Join-Path $root 'phase163_r4_r46_output'
foreach ($path in @($review, $tex)) {
    if (-not (Test-Path -LiteralPath $path)) { throw "Required input not found: $path" }
}
$env:PYTHONPATH = "$package;$root"
python -m pytest -q "$package\tests\test_phase163_r4_r46_semantic_audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python "$package\phase163_r4_r46_semantic_audit.py" --review "$review" --tex "$tex" --output "$output"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
