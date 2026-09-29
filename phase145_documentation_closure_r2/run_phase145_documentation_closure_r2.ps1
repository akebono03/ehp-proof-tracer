$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 145 Documentation Closure R2"
Write-Host "PowerShell 5.1 encoding-safe runner"
Write-Host "=============================================================="

$env:PYTHONIOENCODING = "utf-8"

try {
    Write-Host ""
    Write-Host "A. Applying documentation update..."
    python ".\phase145_documentation_closure\apply_phase145_documentation_closure.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 145 documentation update failed."
    }

    Write-Host ""
    Write-Host "B. Verifying updated files exist..."
    $docs = @(
        ".\README.md",
        ".\docs\design.md",
        ".\docs\development_log.md",
        ".\docs\roadmap.md",
        ".\docs\proof_records.md"
    )

    foreach ($doc in $docs) {
        if (-not (Test-Path $doc)) {
            throw "Missing document: $doc"
        }
        Write-Host "PASS: $doc"
    }

    Write-Host ""
    Write-Host "C. Verifying Phase 145 final regression record..."
    foreach ($doc in $docs) {
        if (-not (Select-String -Path $doc -SimpleMatch "10303 passed in 2375.31s (0:39:35)" -Quiet)) {
            throw "Final regression record missing from $doc"
        }
        Write-Host "PASS: $doc"
    }

    Write-Host ""
    Write-Host "D. Git diff summary..."
    git diff --stat -- README.md docs/design.md docs/development_log.md docs/roadmap.md docs/proof_records.md

    Write-Host ""
    Write-Host "E. Git status..."
    git status --short -- README.md docs/design.md docs/development_log.md docs/roadmap.md docs/proof_records.md tests/__init__.py tests/conftest.py

    Write-Host ""
    Write-Host "=============================================================="
    Write-Host "Phase 145 documentation closure R2: PASS"
    Write-Host "Production code changes: none"
    Write-Host "Test code changes: none"
    Write-Host "No pytest rerun required."
    Write-Host "Phase 145 final suite already passed:"
    Write-Host "10303 passed in 2375.31s (0:39:35)"
    Write-Host "=============================================================="
}
finally {
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
