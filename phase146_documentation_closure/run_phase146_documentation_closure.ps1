$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 146 Documentation Closure"
Write-Host "design / development_log / roadmap / proof_records"
Write-Host "README.md unchanged"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = $RepoRoot
$env:PYTHONIOENCODING = "utf-8"

try {
    Write-Host ""
    Write-Host "A. Applying full-document update..."
    python "$ScriptDir\apply_phase146_documentation_closure.py"
    if ($LASTEXITCODE -ne 0) { throw "Documentation update failed." }

    Write-Host ""
    Write-Host "B. Verifying Phase 146 markers..."
    python -c "from pathlib import Path; checks=[('docs/design.md','# 30. Phase 146 historical Narrative difference audit / root-cause boundary'),('docs/development_log.md','# Phase 146 — historical Narrative difference audit / root-cause classification'),('docs/roadmap.md','## Phase 146 — 完了: historical Narrative difference audit'),('docs/proof_records.md','# Phase 146 historical Narrative comparison / provenance record')]; missing=[p for p,m in checks if m not in Path(p).read_text(encoding='utf-8')]; assert not missing, missing; print('Phase 146 documentation markers: PASS')"
    if ($LASTEXITCODE -ne 0) { throw "Marker verification failed." }

    Write-Host ""
    Write-Host "C. Verifying Phase 147-152 roadmap..."
    python -c "from pathlib import Path; t=Path('docs/roadmap.md').read_text(encoding='utf-8'); markers=['## Phase 147 — RC1','## Phase 148 — RC2','## Phase 149 — RC3','## Phase 150 — RC4','## Phase 151 — RC5','## Phase 152 — RC6']; missing=[m for m in markers if m not in t]; assert not missing, missing; print('Phase 147-152 roadmap: PASS')"
    if ($LASTEXITCODE -ne 0) { throw "Roadmap verification failed." }

    Write-Host ""
    Write-Host "D. UTF-8 strict decode..."
    python -c "from pathlib import Path; paths=['docs/design.md','docs/development_log.md','docs/roadmap.md','docs/proof_records.md']; [Path(p).read_text(encoding='utf-8',errors='strict') for p in paths]; print('UTF-8 strict decode: PASS')"
    if ($LASTEXITCODE -ne 0) { throw "UTF-8 verification failed." }

    Write-Host ""
    Write-Host "E. Full updated documents emitted..."
    Get-ChildItem "$ScriptDir\updated_full_documents" | Select-Object Name, Length

    Write-Host ""
    Write-Host "F. Git diff summary..."
    git diff --stat -- docs/design.md docs/development_log.md docs/roadmap.md docs/proof_records.md
    git status --short -- docs/design.md docs/development_log.md docs/roadmap.md docs/proof_records.md

    Write-Host ""
    Write-Host "No pytest is run by this documentation package."
    Write-Host "Phase-final repository-wide pytest remains:"
    Write-Host "  python -m pytest tests -q"
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 146 documentation closure: PASS"
Write-Host "Production code changes: none"
Write-Host "Test code changes: none"
Write-Host "=============================================================="
