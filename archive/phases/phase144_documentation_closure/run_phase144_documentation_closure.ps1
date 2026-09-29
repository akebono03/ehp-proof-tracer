$ErrorActionPreference="Stop"
$P=Split-Path -Parent $MyInvocation.MyCommand.Path
$R=(Get-Location).Path

Write-Host "=============================================================="
Write-Host "Phase 144 Documentation Closure"
Write-Host "Production changes: none"
Write-Host "Test changes: none"
Write-Host "Whole-suite pytest: NOT run"
Write-Host "=============================================================="

Write-Host ""
Write-Host "A. Applying full-document closure update..."
python (Join-Path $P "apply_phase144_documentation_closure.py")
if($LASTEXITCODE-ne 0){throw "documentation closure apply failed"}

Write-Host ""
Write-Host "B. Verifying Phase 144 / Phase 145 / Phase 146+ markers..."
$checks=@(
  @("README.md","## Phase 144 closure"),
  @("docs/design.md","# 28. Phase 144 generic Narrative / ownership boundary"),
  @("docs/development_log.md","# Phase 144 — generic Narrative / ownership-boundary audit closure"),
  @("docs/roadmap.md","# Phase 144 完了後のロードマップ"),
  @("docs/proof_records.md","# Phase 144 generic Narrative / ownership provenance record")
)
foreach($c in $checks){
  $hit=Select-String -Path $c[0] -SimpleMatch $c[1]
  if(-not $hit){throw "missing marker: $($c[0]) :: $($c[1])"}
  Write-Host "PASS $($c[0])"
}

Write-Host ""
Write-Host "C. Confirming old roadmap tail is replaced..."
if(Select-String -Path "docs/roadmap.md" -SimpleMatch "# Phase 143 完了後のロードマップ"){
  throw "old Phase 143 roadmap tail remains"
}
Write-Host "PASS roadmap current-state replacement"

Write-Host ""
Write-Host "D. Git diff summary..."
git status --short
git diff --stat -- README.md docs/design.md docs/development_log.md docs/roadmap.md docs/proof_records.md

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 144 documentation closure: APPLIED"
Write-Host "Full updated documents are also copied under:"
Write-Host ".\phase144_documentation_closure\full_files\"
Write-Host "No pytest was run; documentation only."
Write-Host "=============================================================="
