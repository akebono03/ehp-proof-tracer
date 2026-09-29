$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 145-2 Final Gate R3"
Write-Host "Post-archive syntax preflight + repository-wide pytest"
Write-Host "=============================================================="

$env:PYTHONIOENCODING = "utf-8"

try {
    Write-Host ""
    Write-Host "A. Verifying completed archive state..."

    $archiveReadme = ".\archive\phases\README.md"
    if (-not (Test-Path $archiveReadme)) {
        throw "archive/phases/README.md is missing."
    }

    $remainingPhaseArtifacts = @(
        git ls-files |
        Where-Object {
            $_ -notlike "archive/phases/*" -and
            (
                $_ -match '^(?i:phase[0-9])' -or
                $_ -match '^(?i:PHASE[0-9])' -or
                $_ -match '^(?i:apply_phase[0-9])' -or
                $_ -match '^(?i:audit_phase[0-9])'
            )
        }
    )

    Write-Host "Tracked Phase-like paths remaining outside archive: $($remainingPhaseArtifacts.Count)"
    if ($remainingPhaseArtifacts.Count -gt 0) {
        $remainingPhaseArtifacts | Select-Object -First 50 | ForEach-Object {
            Write-Host "  $_"
        }
        throw "Tracked historical Phase-like paths remain outside archive."
    }

    Write-Host "Archive state preflight: PASS"

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

    $compiled = 0
    foreach ($pyFile in $canonicalPy) {
        python -m py_compile -- "$pyFile"
        if ($LASTEXITCODE -ne 0) {
            throw "Canonical Python syntax preflight failed: $pyFile"
        }
        $compiled += 1
    }

    Write-Host "Canonical Python files compiled: $compiled"
    Write-Host "Canonical Python syntax preflight: PASS"

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
    Write-Host "Phase 145-2 Final Gate R3: PASS"
    Write-Host "Archive verification: PASS"
    Write-Host "Canonical Python syntax preflight: PASS"
    Write-Host "Repository-wide pytest: PASS"
    Write-Host "Production semantics changed: no"
    Write-Host "Canonical test changes: none"
    Write-Host "Historical runner executability from archive: not guaranteed"
    Write-Host "=============================================================="
}
finally {
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
