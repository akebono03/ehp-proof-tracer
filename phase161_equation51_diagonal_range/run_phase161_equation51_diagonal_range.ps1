$ErrorActionPreference = "Stop"
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repo
python -B (Join-Path $PSScriptRoot "apply_phase161_equation51_diagonal_range.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B -m pytest -q (Join-Path $PSScriptRoot "tests\test_phase161_equation51_diagonal_range.py")
exit $LASTEXITCODE
