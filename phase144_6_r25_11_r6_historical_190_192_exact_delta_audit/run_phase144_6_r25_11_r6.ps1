$ErrorActionPreference = "Stop"

$PhaseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PhaseDir
$HistoricalCommit = "af2e259b55fcfa7cf204fdcb50d5194bb2232bd0"
$Worktree = Join-Path $RepoRoot ".phase144_6_r25_11_r6_historical_worktree"
$HistoricalJson = Join-Path $PhaseDir "historical_inventory.json"
$CurrentJson = Join-Path $PhaseDir "current_inventory.json"

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-11-R6 Historical 190->192 Exact Delta Audit"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "Historical commit: $HistoricalCommit"
Write-Host "=============================================================="

Push-Location $RepoRoot
try {
  $env:PYTHONUTF8 = "1"

  Write-Host ""
  Write-Host "A. Syntax preflight..."
  python -m py_compile `
    ".\phase144_6_r25_11_r6_historical_190_192_exact_delta_audit\collect_r25_11_r6_inventory.py" `
    ".\phase144_6_r25_11_r6_historical_190_192_exact_delta_audit\compare_r25_11_r6.py" `
    ".\phase144_6_r25_11_r6_historical_190_192_exact_delta_audit\test_phase144_6_r25_11_r6.py"

  Write-Host ""
  Write-Host "B. Lightweight audit-contract tests..."
  $env:PYTHONPATH = (Get-Location).Path
  pytest -q `
    ".\phase144_6_r25_11_r6_historical_190_192_exact_delta_audit\test_phase144_6_r25_11_r6.py"
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue

  Write-Host ""
  Write-Host "C. Preparing detached historical worktree..."
  if (Test-Path $Worktree) {
    git worktree remove --force $Worktree
  }
  git worktree prune
  git worktree add --detach $Worktree $HistoricalCommit

  $HistoricalCollector = Join-Path $Worktree "_r25_11_r6_collector.py"
  Copy-Item `
    ".\phase144_6_r25_11_r6_historical_190_192_exact_delta_audit\collect_r25_11_r6_inventory.py" `
    $HistoricalCollector `
    -Force

  Write-Host ""
  Write-Host "D. Building historical inventory from the historical production code..."
  Push-Location $Worktree
  try {
    $env:PYTHONPATH = $Worktree
    python `
      ".\_r25_11_r6_collector.py" `
      --label historical `
      --output $HistoricalJson
  }
  finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Pop-Location
  }

  $HistoricalPayload = Get-Content `
    $HistoricalJson `
    -Raw `
    -Encoding UTF8 `
    | ConvertFrom-Json

  if ([int]$HistoricalPayload.selected_total -ne 190) {
    Write-Host ""
    Write-Host "STOP: historical commit did not reproduce selected=190."
    Write-Host "No exact-delta claim will be made."
    exit 2
  }

  Write-Host ""
  Write-Host "E. Building current inventory from the current checkout..."
  $env:PYTHONPATH = (Get-Location).Path
  python `
    ".\phase144_6_r25_11_r6_historical_190_192_exact_delta_audit\collect_r25_11_r6_inventory.py" `
    --label current `
    --output $CurrentJson
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue

  Write-Host ""
  Write-Host "F. Comparing historical 190 against current 192..."
  python `
    ".\phase144_6_r25_11_r6_historical_190_192_exact_delta_audit\compare_r25_11_r6.py" `
    $HistoricalJson `
    $CurrentJson

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "R25-11-R6 completed."
  Write-Host "Please paste the complete A-D comparison output from Section F."
  Write-Host "No production files were modified."
  Write-Host "No existing tests were modified."
  Write-Host "No full pytest was run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONUTF8 -ErrorAction SilentlyContinue

  if (Test-Path $Worktree) {
    git worktree remove --force $Worktree | Out-Null
  }
  git worktree prune | Out-Null

  Pop-Location
}
