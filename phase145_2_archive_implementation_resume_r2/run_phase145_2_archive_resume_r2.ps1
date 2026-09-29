$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 145-2 Archive Implementation Resume R2"
Write-Host "Rename-aware resume after partial git mv"
Write-Host "=============================================================="

$env:PYTHONIOENCODING = "utf-8"

try {
    Write-Host ""
    Write-Host "A. Resuming audited archive move..."
    python ".\phase145_2_archive_implementation_resume_r2\apply_phase145_2_archive_resume_r2.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 145-2 resumable archive move failed."
    }

    Write-Host ""
    Write-Host "B. Canonical Python syntax preflight..."
    $canonicalPy = @(
        git ls-files "*.py" |
        Where-Object {
            $_ -notlike "archive/phases/*" -and
            $_ -notlike "phase145_2_*/*"
        }
    )
    if ($canonicalPy.Count -eq 0) {
        throw "No canonical Python files found."
    }
    python -m py_compile @canonicalPy
    if ($LASTEXITCODE -ne 0) {
        throw "Canonical Python syntax preflight failed."
    }

    Write-Host ""
    Write-Host "C. Repository-wide pytest - Phase 145-2 final regression gate..."
    python -m pytest tests -q
    if ($LASTEXITCODE -ne 0) {
        throw "Repository-wide pytest failed."
    }

    Write-Host ""
    Write-Host "D. Final Git status..."
    git status --short

    Write-Host ""
    Write-Host "=============================================================="
    Write-Host "Phase 145-2 Archive Implementation Resume R2: PASS"
    Write-Host "Repository-wide pytest: PASS"
    Write-Host "Production semantics changed: no"
    Write-Host "Historical runner executability from archive: not guaranteed"
    Write-Host "=============================================================="
}
finally {
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
