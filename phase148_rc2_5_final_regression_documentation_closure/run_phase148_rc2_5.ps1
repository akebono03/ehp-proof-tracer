$ErrorActionPreference = "Stop"

function Invoke-NativeChecked {
  param(
    [Parameter(Mandatory=$true)]
    [scriptblock]$Command,
    [Parameter(Mandatory=$true)]
    [string]$FailureMessage
  )
  & $Command
  if ($LASTEXITCODE -ne 0) {
    throw "$FailureMessage (exit code $LASTEXITCODE)"
  }
}

Write-Host "=============================================================="
Write-Host "Phase 148 RC2-5"
Write-Host "Final Regression & Documentation Closure"
Write-Host "Production changes: none"
Write-Host "=============================================================="

$Root = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = "$Root;$Root\tests"
$env:PYTHONIOENCODING = "utf-8"

$FullOutput = Join-Path $PackageDir "phase148_rc2_5_full_pytest_output.txt"
$SummaryFile = Join-Path $PackageDir "phase148_rc2_5_regression_summary.txt"

try {
  Write-Host ""
  Write-Host "A. Syntax / document preflight..."
  Invoke-NativeChecked -Command {
    python -m py_compile `
      "$PackageDir\apply_phase148_rc2_5_documentation.py" `
      "$PackageDir\verify_phase148_rc2_5_documentation.py"
  } -FailureMessage "RC2-5 helper syntax preflight failed"

  python -c "from pathlib import Path; paths=['README.md','docs/design.md','docs/development_log.md','docs/roadmap.md','docs/proof_records.md']; missing=[p for p in paths if not Path(p).exists()]; assert not missing, missing; [Path(p).read_text(encoding='utf-8',errors='strict') for p in paths]; print('Required documents / UTF-8: PASS')"
  if ($LASTEXITCODE -ne 0) {
    throw "RC2-5 document preflight failed."
  }

  Write-Host ""
  Write-Host "B. Phase 148 focused final preflight..."
  $Focused = @(
    ".\tests\test_phase148_rc2_4_post_repair_six_group.py",
    ".\tests\test_phase148_rc2_4_repair_r5.py",
    ".\tests\test_phase148_rc2_4_repair_r5_r2.py",
    ".\tests\test_phase148_rc2_4_repair_r4_2_calculation_premise_semantic_closure.py",
    ".\tests\test_phase148_rc2_4_repair_r4_web_narrative_depth_parity.py",
    ".\tests\test_phase148_rc2_4_repair_r2.py",
    ".\tests\test_phase148_rc2_3_exactness_exposure.py",
    ".\tests\test_phase148_rc2_3_repair_r1.py"
  )
  $ExistingFocused = @(
    $Focused | Where-Object { Test-Path $_ }
  )
  if ($ExistingFocused.Count -eq 0) {
    throw "No Phase 148 focused tests were found."
  }
  & pytest -q @ExistingFocused
  if ($LASTEXITCODE -ne 0) {
    throw "Phase 148 focused final preflight failed."
  }

  Write-Host ""
  Write-Host "C. Repository-wide final regression..."
  Write-Host "   This is the single whole-suite run for the end of Phase 148."
  & python -m pytest tests -q 2>&1 |
    Tee-Object -FilePath $FullOutput
  if ($LASTEXITCODE -ne 0) {
    Write-Host "Repository-wide regression FAILED."
    Write-Host "Documentation has NOT been changed."
    throw "Phase 148 repository-wide final regression failed."
  }

  Write-Host ""
  Write-Host "D. Extracting measured pytest summary..."
  python -c "from pathlib import Path; import re,sys; src=Path(sys.argv[1]).read_text(encoding='utf-8',errors='replace'); lines=[line.strip() for line in src.splitlines() if re.search(r'\bpassed\b',line)]; assert lines, 'pytest summary not found'; summary=lines[-1]; Path(sys.argv[2]).write_text(summary+'\n',encoding='utf-8'); print(summary)" "$FullOutput" "$SummaryFile"
  if ($LASTEXITCODE -ne 0) {
    throw "Could not extract final pytest summary."
  }

  Write-Host ""
  Write-Host "E. Applying five full-document closure updates..."
  Invoke-NativeChecked -Command {
    python `
      "$PackageDir\apply_phase148_rc2_5_documentation.py" `
      "$SummaryFile"
  } -FailureMessage "Phase 148 documentation closure failed"

  Write-Host ""
  Write-Host "F. Verifying documentation markers / measured result..."
  Invoke-NativeChecked -Command {
    python `
      "$PackageDir\verify_phase148_rc2_5_documentation.py" `
      "$SummaryFile"
  } -FailureMessage "Phase 148 documentation verification failed"

  Write-Host ""
  Write-Host "G. Git diff summary..."
  git diff --stat -- `
    README.md `
    docs/design.md `
    docs/development_log.md `
    docs/roadmap.md `
    docs/proof_records.md

  Write-Host ""
  Write-Host "H. Git status..."
  git status --short

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 148 RC2-5: PASS"
  Write-Host "Phase 148 / RC2: COMPLETE"
  Write-Host "Production changes in RC2-5: none."
  Write-Host "Repository-wide pytest: PASS."
  Write-Host "Full updated documents:"
  Write-Host "  .\phase148_rc2_5_final_regression_documentation_closure\updated_full_documents\"
  Write-Host "Next: Phase 149 / RC3 Contribution ownership / insertion ordering."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
