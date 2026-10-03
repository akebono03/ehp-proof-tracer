$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageRoot
$OutputDir = Join-Path $RepoRoot "phase156_r6_output"

Write-Host "=============================================================="
Write-Host "Phase156-R6 — focused/sharded regression"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host "Production changes: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""

Set-Location $RepoRoot

$OriginalPythonPath = $env:PYTHONPATH

if ([string]::IsNullOrWhiteSpace($OriginalPythonPath)) {
  $env:PYTHONPATH = $RepoRoot
}
else {
  $env:PYTHONPATH = $RepoRoot + [IO.Path]::PathSeparator + $OriginalPythonPath
}

try {
  if (Test-Path $OutputDir) {
    Remove-Item `
      -Path $OutputDir `
      -Recurse `
      -Force
  }

  New-Item `
    -ItemType Directory `
    -Path $OutputDir `
    -Force `
    | Out-Null

  Write-Host "Current git HEAD:"
  git rev-parse HEAD
  Write-Host ""

  Write-Host "1/8 R6 sharding contract tests"
  python -m pytest `
    ".\phase156_r6_focused_sharded_regression\test_phase156_r6_sharding.py" `
    -q `
    -p no:cacheprovider

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156-R6 sharding contract tests failed."
  }

  Write-Host ""
  Write-Host "2/8 Focused Reference selection / granularity / body regression"
  python -m pytest `
    ".\tests\test_phase153_r5_reference_selection.py" `
    ".\tests\test_phase153_r6_reference_granularity.py" `
    ".\tests\test_phase154_r2_fix3_reference_marker_completion.py" `
    -q `
    -p no:cacheprovider

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156-R6 focused Reference regression failed."
  }

  Write-Host ""
  Write-Host "3/8 Phase153 public Reference audit-only regression"
  python -m pytest `
    --noconftest `
    "tests/test_phase153_r3_10_public_reference_connection_repair.py::test_phase153_r3_10_all_group_reference_population_invariants" `
    -q `
    --tb=short `
    -p no:cacheprovider `
    -o addopts=

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156-R6 Phase153 audit-only regression failed."
  }

  Write-Host ""
  Write-Host "4/8 Shard 1/4"
  python `
    ".\phase156_r6_focused_sharded_regression\phase156_r6_sharded_reference_regression.py" `
    --shard-index 0 `
    --output-dir "$OutputDir"

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156-R6 shard 1 failed."
  }

  Write-Host ""
  Write-Host "5/8 Shard 2/4"
  python `
    ".\phase156_r6_focused_sharded_regression\phase156_r6_sharded_reference_regression.py" `
    --shard-index 1 `
    --output-dir "$OutputDir"

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156-R6 shard 2 failed."
  }

  Write-Host ""
  Write-Host "6/8 Shard 3/4"
  python `
    ".\phase156_r6_focused_sharded_regression\phase156_r6_sharded_reference_regression.py" `
    --shard-index 2 `
    --output-dir "$OutputDir"

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156-R6 shard 3 failed."
  }

  Write-Host ""
  Write-Host "7/8 Shard 4/4"
  python `
    ".\phase156_r6_focused_sharded_regression\phase156_r6_sharded_reference_regression.py" `
    --shard-index 3 `
    --output-dir "$OutputDir"

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156-R6 shard 4 failed."
  }

  Write-Host ""
  Write-Host "8/8 Aggregate four shards"
  python `
    ".\phase156_r6_focused_sharded_regression\aggregate_phase156_r6_shards.py" `
    --output-dir "$OutputDir"

  if ($LASTEXITCODE -ne 0) {
    throw "Phase156-R6 shard aggregate failed."
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase156-R6 completed"
  Write-Host "=============================================================="
  Write-Host "Production changes: none"
  Write-Host ""
  Write-Host "Output:"
  Write-Host "  $OutputDir\phase156_r6_shard_0_result.json"
  Write-Host "  $OutputDir\phase156_r6_shard_1_result.json"
  Write-Host "  $OutputDir\phase156_r6_shard_2_result.json"
  Write-Host "  $OutputDir\phase156_r6_shard_3_result.json"
  Write-Host "  $OutputDir\phase156_r6_aggregate_result.json"
  Write-Host ""
  Write-Host "Repository-wide pytest: NOT run"
  Write-Host "Next boundary:"
  Write-Host "  Phase156 closure — documentation + repository-wide pytest"
}
finally {
  $env:PYTHONPATH = $OriginalPythonPath
}
