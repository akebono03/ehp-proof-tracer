$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$TestsDir = Join-Path $RepoRoot "tests"
$TestsInit = Join-Path $TestsDir "__init__.py"
$CreatedTestsInit = $false

Write-Host "=============================================================="
Write-Host "Phase 144-6 Final Full Suite R2"
Write-Host "Canonical tests/ collection only"
Write-Host "Production changes: none"
Write-Host "Persistent test changes: none"
Write-Host "=============================================================="

if (-not (Test-Path $TestsDir)) {
  throw "tests directory was not found: $TestsDir"
}

if (-not (Test-Path $TestsInit)) {
  New-Item -ItemType File -Path $TestsInit -Force | Out-Null
  $CreatedTestsInit = $true
  Write-Host "Temporary package marker created: tests/__init__.py"
} else {
  Write-Host "Existing tests/__init__.py preserved."
}

$env:PYTHONPATH = $RepoRoot

try {
  Write-Host ""
  Write-Host "Running canonical full suite: pytest -q tests"
  Write-Host ""

  pytest -q tests
  $Code = $LASTEXITCODE
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue

  if ($CreatedTestsInit -and (Test-Path $TestsInit)) {
    Remove-Item $TestsInit -Force
    Write-Host ""
    Write-Host "Temporary package marker removed: tests/__init__.py"
  }
}

if ($Code -ne 0) {
  Write-Host ""
  Write-Host "Phase 144-6 canonical final full suite: FAIL"
  exit $Code
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 144-6 canonical final full suite: PASS"
Write-Host "=============================================================="
Write-Host "Production changes in this package: none."
Write-Host "Persistent test changes in this package: none."
Write-Host "Phase-package duplicate tests were intentionally excluded."
