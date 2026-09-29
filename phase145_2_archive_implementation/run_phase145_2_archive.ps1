$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 145-2 Archive Implementation"
Write-Host "553 audited historical artifacts -> archive/phases/"
Write-Host "=============================================================="

$env:PYTHONIOENCODING = "utf-8"

try {
    Write-Host ""
    Write-Host "A. Applying audited archive move..."
    python ".\phase145_2_archive_implementation\apply_phase145_2_archive.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 145-2 archive move failed."
    }

    Write-Host ""
    Write-Host "B. Python syntax preflight for current canonical Python files..."
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
    Write-Host "D. Final archive verification..."
    $remainingTrackedRootPhase = @(
        git ls-files |
        Where-Object {
            $_ -notmatch "/" -and
            (
                $_ -match "^(?i:phase\d)" -or
                $_ -match "^(?i:apply_phase\d)" -or
                $_ -match "^(?i:audit_phase\d)"
            )
        }
    )

    Write-Host ("Tracked root Phase-like files remaining: " + $remainingTrackedRootPhase.Count)
    if ($remainingTrackedRootPhase.Count -gt 0) {
        Write-Host "Note: these are shown for final human review; the audited Stage 1 population has already been verified exactly."
        $remainingTrackedRootPhase | ForEach-Object { Write-Host ("  " + $_) }
    }

    Write-Host ""
    git status --short

    Write-Host ""
    Write-Host "=============================================================="
    Write-Host "Phase 145-2 Archive Implementation: PASS"
    Write-Host "Repository-wide pytest: PASS"
    Write-Host "Production semantics changed: no"
    Write-Host "Historical runner executability from archive: not guaranteed"
    Write-Host "=============================================================="
}
finally {
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
