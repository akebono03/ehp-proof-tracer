$ErrorActionPreference="Stop"
$PackageRoot=Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot=(Get-Location).Path
$TestsDir=Join-Path $RepoRoot "tests"
$Marker=Join-Path $TestsDir "__init__.py"
$CreatedMarker=$false
$OldPythonPath=$env:PYTHONPATH
$OldEncoding=$env:PYTHONIOENCODING
$Output=Join-Path $PackageRoot "phase144_6_finalization_focused_gate_output.txt"

function Run-Pytest {
  param([string]$Label,[string[]]$Targets)
  Write-Host ""
  Write-Host "--------------------------------------------------------------"
  Write-Host $Label
  Write-Host "--------------------------------------------------------------"
  foreach($Target in $Targets){
    $FilePart=$Target.Split("::")[0]
    if(-not(Test-Path (Join-Path $RepoRoot $FilePart))){
      throw "Required test file was not found: $FilePart"
    }
  }
  python -m pytest -q @Targets
  if($LASTEXITCODE -ne 0){throw "$Label failed."}
}

Write-Host "=============================================================="
Write-Host "Phase 144-6 Finalization Focused Gate"
Write-Host "Production changes: none"
Write-Host "Test changes: none"
Write-Host "Documentation changes: none"
Write-Host "Repository-wide pytest: NOT run by this runner"
Write-Host "=============================================================="
Start-Transcript -Path $Output -Force|Out-Null
try{
  Write-Host ""
  Write-Host "A. Repository / environment preflight"
  git rev-parse --show-toplevel
  if($LASTEXITCODE -ne 0){throw "Not inside a Git repository."}
  git branch --show-current
  git rev-parse HEAD
  python --version
  python -m pytest --version
  git status --short

  if(-not(Test-Path $Marker)){
    New-Item -ItemType File -Path $Marker -Force|Out-Null
    $CreatedMarker=$true
  }
  $env:PYTHONPATH="$RepoRoot;$TestsDir"
  $env:PYTHONIOENCODING="utf-8"

  Write-Host ""
  Write-Host "B. Syntax / whitespace preflight"
  python -m py_compile `
    ".\toda_group_proof_narrative_semantics.py" `
    ".\toda_group_proof_narrative_renderer.py" `
    ".\toda_group_proof_narrative_argument_multi_renderer.py" `
    ".\toda_group_proof_narrative_argument_body_renderer.py"
  if($LASTEXITCODE -ne 0){throw "Production syntax preflight failed."}
  git diff --check
  if($LASTEXITCODE -ne 0){throw "git diff --check failed."}

  Run-Pytest -Label "C. Canonical Phase 144-6 production-route / completion regressions" -Targets @(
    "tests/test_phase144_6_pi6_generic_production_route.py",
    "tests/test_phase144_6_public_route_cutover.py",
    "tests/test_phase144_6_r4_supporting_fact_filtering.py",
    "tests/test_phase144_6_r5_43_11d_final_completion_audit.py",
    "tests/test_phase144_6_r5_43_r2_recursive_repr_repair.py",
    "tests/test_phase144_6_r5_43_r3_current_markdown_plumbing_repair.py",
    "tests/test_phase144_6_r25_9a_pi5_suppression.py",
    "tests/test_phase144_6_r25_9a_r1_relocation_hidden.py",
    "tests/test_phase144_6_r25_9b_nu_prime_definition_depth2.py"
  )

  Run-Pytest -Label "D. Cross-phase Narrative boundary controls" -Targets @(
    "tests/test_phase143_61b_direct_premise_narrative.py",
    "tests/test_phase143_61b_r_semantic_suppression_priority.py",
    "tests/test_phase144_5_generic_definition_order_equations.py"
  )

  Write-Host ""
  Write-Host "E. Local R25-30-R3 evidence discovery"
  $Candidates=@(
    Get-ChildItem -Path $RepoRoot -Recurse -File -Filter "test*.py" -ErrorAction SilentlyContinue |
      Where-Object {
        ($_.FullName -match "r25[_-]30" -or $_.FullName -match "argument[_-]boundary[_-]entry[_-]classification") -and
        $_.FullName -notmatch "\\.git\\" -and $_.FullName -notmatch "\\__pycache__\\"
      } | Select-Object -ExpandProperty FullName -Unique
  )
  if($Candidates.Count -eq 0){
    Write-Host "No separately packaged R25-30-R3 pytest file was discovered."
  } else {
    Write-Host ("Discovered R25-30-related pytest files: {0}" -f $Candidates.Count)
    $Candidates|ForEach-Object{Write-Host ("  "+$_)}
    python -m pytest -q @Candidates
    if($LASTEXITCODE -ne 0){throw "Local R25-30-related regression failed."}
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 144-6 Finalization focused gate: PASS"
  Write-Host "=============================================================="
  Write-Host "Historical R5-37 through R5-41 fixed-count snapshots were not used."
  Write-Host "Next after PASS: one repository-wide pytest Phase-end run."
}
finally{
  if($null -eq $OldPythonPath){Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue}else{$env:PYTHONPATH=$OldPythonPath}
  if($null -eq $OldEncoding){Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue}else{$env:PYTHONIOENCODING=$OldEncoding}
  if($CreatedMarker -and (Test-Path $Marker)){Remove-Item $Marker -Force}
  Stop-Transcript|Out-Null
}
Write-Host "Output: $Output"
