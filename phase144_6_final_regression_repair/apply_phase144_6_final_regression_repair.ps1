$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Get-Location).Path
$SourceTests = Join-Path $PackageRoot "tests"
$TargetTests = Join-Path $RepoRoot "tests"

if (-not (Test-Path $TargetTests -PathType Container)) {
  throw "tests directory not found: $TargetTests"
}

$Files = @(
  "test_phase133_7_group_proof_narrative_labels.py",
  "test_phase134_16_presentation_catalog.py",
  "test_phase134_3_pi6_3_numbered_narrative.py",
  "test_phase134_5_pi6_3_reference_fact_split.py",
  "test_phase134_6_pi6_3_mathbook_narrative.py",
  "test_phase134_7_pi6_3_final_narrative.py",
  "test_phase134_9_pi6_3_snapshot.py",
  "test_phase136_1_pi6_3_narrative_prose.py",
  "test_phase136_2_pi6_3_narrative_structure.py"
)

foreach ($File in $Files) {
  Copy-Item `
    -Path (Join-Path $SourceTests $File) `
    -Destination (Join-Path $TargetTests $File) `
    -Force
}

Write-Host "Phase 144-6 Final Regression Repair applied."
Write-Host "Production code changes: none."
Write-Host "Replaced regression tests: 9 files."
