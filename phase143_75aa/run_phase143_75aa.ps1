$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$BundleDir = Split-Path -Parent $MyInvocation.MyCommand.Path

python (Join-Path $BundleDir "apply_phase143_75aa.py")

$env:PYTHONPATH = $RepoRoot
try {
  pytest -q `
    ".\tests\test_phase63_nu4_prop44_specialization.py" `
    ".\tests\test_phase143_75aa_toda56_nu4_prop44_specialization_rendering.py"
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
