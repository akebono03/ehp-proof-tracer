$ErrorActionPreference="Stop"

$PackageRoot=Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot=(Get-Location).Path
$TestsDir=Join-Path $RepoRoot "tests"
$Output=Join-Path $PackageRoot "phase144_6_finalization_r25_30_boundary_gate_r1_output.txt"

$OldPythonPath=$env:PYTHONPATH
$OldEncoding=$env:PYTHONIOENCODING

$env:PYTHONPATH="$RepoRoot;$TestsDir"
$env:PYTHONIOENCODING="utf-8"

Write-Host "=============================================================="
Write-Host "Phase 144-6 Finalization R25-30 Boundary Gate R1"
Write-Host "Runner repair: include repo root AND tests in PYTHONPATH"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "Documentation changes: none"
Write-Host "=============================================================="

Start-Transcript -Path $Output -Force | Out-Null

try {
  Write-Host ""
  Write-Host "A. Import preflight"
  Write-Host "--------------------------------------------------------------"
  Write-Host ("PYTHONPATH=" + $env:PYTHONPATH)

  python -c "import audit_phase144_6_r5_43_11d; import test_phase144_6_r5_18_production_generic_proof_chain_foundation; print('R5-43 dual-path import preflight: PASS')"
  if ($LASTEXITCODE -ne 0) {
    throw "R5-43 dual-path import preflight failed."
  }

  Write-Host ""
  Write-Host "B. Current R5-43-11D inventory"
  Write-Host "--------------------------------------------------------------"

  python -c "from audit_phase144_6_r5_43_11d import build_completion_inventory; rows=build_completion_inventory(); [print(f'pi_{r.n+r.k}^{r.n}: selected={r.selected} participating={r.participating_selected}/{r.participating_insertable} detached={r.detached_selected}/{r.detached_insertable} transport={r.transport_connectors} missing={r.missing_inserted_lines}') for r in rows]; print('TOTAL selected=',sum(r.selected for r in rows)); print('TOTAL participating=',sum(r.participating_selected for r in rows)); print('TOTAL detached=',sum(r.detached_selected for r in rows)); print('TOTAL detached_insertable=',sum(r.detached_insertable for r in rows)); print('TOTAL missing=',sum(r.missing_inserted_lines for r in rows))"
  if ($LASTEXITCODE -ne 0) {
    throw "R5-43 inventory failed."
  }

  Write-Host ""
  Write-Host "C. Locate the latest local R25-30-R3 boundary-classification test"
  Write-Host "--------------------------------------------------------------"

  $Candidates=@(
    Get-ChildItem -Path $RepoRoot -Recurse -File -Filter "test*.py" -ErrorAction SilentlyContinue |
      Where-Object {
        (
          $_.FullName -match "r25[_-]30" -or
          $_.FullName -match "argument[_-]boundary[_-]entry[_-]classification"
        ) -and
        $_.FullName -notmatch "\\.git\\" -and
        $_.FullName -notmatch "\\__pycache__\\"
      } |
      Sort-Object LastWriteTime -Descending
  )

  if ($Candidates.Count -eq 0) {
    throw "No local R25-30 / argument-boundary-entry-classification pytest file was found. Do not infer PASS."
  }

  $Candidate=$Candidates[0]
  Write-Host ("Selected: " + $Candidate.FullName)
  Write-Host ("Modified: " + $Candidate.LastWriteTime.ToString("s"))

  Write-Host ""
  Write-Host "D. Run only the latest R25-30-R3 boundary-classification test"
  Write-Host "--------------------------------------------------------------"

  python -m pytest -q $Candidate.FullName
  if ($LASTEXITCODE -ne 0) {
    throw "R25-30-R3 boundary-classification regression failed."
  }

  Write-Host ""
  Write-Host "E. Small production-route controls"
  Write-Host "--------------------------------------------------------------"

  python -m pytest -q `
    "tests/test_phase144_6_pi6_generic_production_route.py" `
    "tests/test_phase144_6_public_route_cutover.py" `
    "tests/test_phase144_6_r25_9b_nu_prime_definition_depth2.py"

  if ($LASTEXITCODE -ne 0) {
    throw "Production-route controls failed."
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 144-6 R25-30 boundary gate R1: PASS"
  Write-Host "=============================================================="
  Write-Host "Interpretation:"
  Write-Host "  R5-43 fixed-count completion snapshot is stale."
  Write-Host "  Current R25-30-R3 ownership/boundary classification passes."
  Write-Host "  Do not repair production merely to restore 190/33/157 counts."
  Write-Host "  Result-reuse subtree expansion remains Phase 145."
}
finally {
  if ($null -eq $OldPythonPath) {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  } else {
    $env:PYTHONPATH=$OldPythonPath
  }

  if ($null -eq $OldEncoding) {
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
  } else {
    $env:PYTHONIOENCODING=$OldEncoding
  }

  Stop-Transcript | Out-Null
}

Write-Host ""
Write-Host ("Output: " + $Output)
