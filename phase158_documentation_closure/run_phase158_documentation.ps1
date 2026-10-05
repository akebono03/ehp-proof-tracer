$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 158 documentation closure"
Write-Host "=============================================================="
Write-Host "Repository root: $((Get-Location).Path)"
Write-Host "Production code changes: none"
Write-Host "Test code changes: none"
Write-Host "pytest: NOT RUN"
Write-Host ""

Write-Host "[1/3] Apply Phase 158 documentation update"
python ".\phase158_documentation_closure\apply_phase158_documentation.py"
if ($LASTEXITCODE -ne 0) {
  throw "Phase 158 documentation update failed."
}
Write-Host ""

Write-Host "[2/3] Check documentation diff hygiene"
git diff --check -- `
  README.md `
  docs/design.md `
  docs/development_log.md `
  docs/roadmap.md `
  docs/proof_records.md
if ($LASTEXITCODE -ne 0) {
  throw "git diff --check failed."
}
Write-Host ""

Write-Host "[3/3] Show changed documentation files"
git status --short -- `
  README.md `
  docs/design.md `
  docs/development_log.md `
  docs/roadmap.md `
  docs/proof_records.md
Write-Host ""

Write-Host "=============================================================="
Write-Host "Phase 158 documentation closure completed."
Write-Host "No pytest was executed."
Write-Host ""
Write-Host "Next:"
Write-Host "  Phase 159-R1 - k=1, n=2 starting-point audit"
Write-Host "=============================================================="
