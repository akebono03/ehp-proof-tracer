$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Repo = Split-Path -Parent $Root
Set-Location $Repo

Write-Host "=============================================================="
Write-Host "Phase 150 Finalization Repair R3"
Write-Host "UTF-8 normalization + remaining focused contract repair"
Write-Host "Production changes: none"
Write-Host "=============================================================="

Write-Host ""
Write-Host "A. Applying R3 test updates..."
python "$Root\apply_phase150_finalization_repair_r3.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "B. UTF-8 and syntax preflight..."
$Files = @(
  "tests\test_phase132_6_group_proof_narrative_renderer.py",
  "tests\test_phase132_7_group_proof_cli_modes.py",
  "tests\test_phase132_8_group_proof_narrative_dedup.py",
  "tests\test_phase132_9_web_group_proof_modes.py",
  "tests\test_phase133_10_sigma_label_wording.py",
  "tests\test_phase133_6_group_proof_narrative_labels.py",
  "tests\test_phase133_9_group_proof_narrative_labels.py",
  "tests\test_phase144_6_r3_production_references.py",
  "tests\test_phase144_6_r3_structured_references.py",
  "tests\test_phase144_6_r4_supporting_fact_filtering.py"
)
python -c "from pathlib import Path; import sys; [Path(p).read_text(encoding='utf-8') for p in sys.argv[1:]]" @Files
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m py_compile @Files
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "C. Focused pytest only..."
python -m pytest @Files -q 2>&1 | Tee-Object -FilePath "$Root\focused_pytest_r3.txt"
$PytestExit = $LASTEXITCODE

Write-Host ""
Write-Host "Focused pytest exit code: $PytestExit"
Write-Host "Result: $Root\focused_pytest_r3.txt"
Write-Host "Full regression: NOT run"

if ($PytestExit -eq 0) {
  Write-Host ""
  Write-Host "R3 focused tests PASS."
  Write-Host "Next: one final Phase 150 full regression."
} else {
  Write-Host ""
  Write-Host "R3 still has focused failures. Do NOT run full regression yet."
}
exit $PytestExit
