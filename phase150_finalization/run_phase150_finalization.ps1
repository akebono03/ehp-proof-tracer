$ErrorActionPreference = "Stop"

$repo = (Get-Location).Path
$pkg = Join-Path $repo "phase150_finalization"
$log = Join-Path $pkg "phase150_full_pytest.txt"
$summary = Join-Path $pkg "phase150_full_pytest_summary.txt"

Write-Host "=============================================================="
Write-Host "Phase 150 Finalization"
Write-Host "No production/test changes; final full regression + docs closure"
Write-Host "=============================================================="

$required = @(
  "README.md",
  "docs/design.md",
  "docs/development_log.md",
  "docs/roadmap.md",
  "docs/proof_records.md",
  "tests"
)

Write-Host ""
Write-Host "A. Preflight..."
foreach ($item in $required) {
  if (-not (Test-Path (Join-Path $repo $item))) {
    throw "Missing required repository path: $item"
  }
}
Write-Host "Preflight: PASS"

Write-Host ""
Write-Host "B. Running Phase-final repository-wide regression..."
$env:PYTHONPATH = $repo
$env:PYTHONIOENCODING = "utf-8"
try {
  python -m pytest tests -q 2>&1 | Tee-Object -FilePath $log
  $pytestExit = $LASTEXITCODE
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}

if ($pytestExit -ne 0) {
  Write-Host ""
  Write-Host "Repository-wide regression: FAIL"
  Write-Host "Documentation was NOT changed."
  Write-Host "Log: $log"
  exit $pytestExit
}

$lines = Get-Content $log
$summaryLine = $lines |
  Where-Object { $_ -match '\bpassed\b' -and $_ -match '\bin\b' } |
  Select-Object -Last 1

if (-not $summaryLine) {
  throw "Could not locate pytest final summary in $log"
}
Set-Content -Path $summary -Value $summaryLine -Encoding UTF8

Write-Host ""
Write-Host "Repository-wide regression: PASS"
Write-Host $summaryLine

Write-Host ""
Write-Host "C. Applying documentation-only Phase 150 closure..."
python (Join-Path $pkg "apply_phase150_finalization.py") $summary
if ($LASTEXITCODE -ne 0) {
  throw "Documentation closure failed."
}

Write-Host ""
Write-Host "D. Verifying closure markers..."
python -c "from pathlib import Path; checks=[('README.md','<!-- PHASE150_CLOSURE -->'),('docs/design.md','# Phase 150 終了時の Narrative 一般化戦略境界'),('docs/development_log.md','# Phase 150 — Generic provenance / reason prose 終了と開発戦略の切替'),('docs/roadmap.md','## Phase 151 — All-group generic baseline / cross-group audit'),('docs/proof_records.md','# Phase 150 closure / provenance strategy boundary')]; missing=[p for p,m in checks if m not in Path(p).read_text(encoding='utf-8-sig')]; assert not missing, missing; print('Phase 150 closure markers: PASS')"
if ($LASTEXITCODE -ne 0) {
  throw "Closure marker verification failed."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 150 Finalization completed successfully."
Write-Host "Phase 150 is closed."
Write-Host "Next boundary: Phase 151 All-group generic baseline / cross-group audit."
Write-Host "Full updated documents are under:"
Write-Host "  .\phase150_finalization\updated_full_documents\"
Write-Host "=============================================================="
