$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 145 Documentation Closure"
Write-Host "README / design / development_log / roadmap / proof_records"
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
    Write-Host "B. Verifying Phase 145 markers..."
    $checks = @(
        @{ Path = ".\README.md"; Pattern = "## Phase 145 closure" },
        @{ Path = ".\docs\design.md"; Pattern = "# 29. Phase 145 完了境界" },
        @{ Path = ".\docs\development_log.md"; Pattern = "# Phase 145 — Narrative + depth 2 default / repository closure" },
        @{ Path = ".\docs\roadmap.md"; Pattern = "## Phase 145 — 完了" },
        @{ Path = ".\docs\proof_records.md"; Pattern = "# Phase 145 default presentation / regression provenance record" }
    )

    foreach ($check in $checks) {
        if (-not (Select-String -Path $check.Path -SimpleMatch $check.Pattern -Quiet)) {
            throw "Missing expected marker: $($check.Path) :: $($check.Pattern)"
        }
        Write-Host "PASS: $($check.Path)"
    }

    Write-Host ""
    Write-Host "C. Verifying final regression record..."
    $docs = @(
        ".\README.md",
        ".\docs\design.md",
        ".\docs\development_log.md",
        ".\docs\roadmap.md",
        ".\docs\proof_records.md"
    )
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
    Write-Host "Phase 145 documentation closure: PASS"
    Write-Host "Full updated documents are also copied to:"
    Write-Host "  .\phase145_documentation_closure\updated_full_documents\"
    Write-Host ""
    Write-Host "No pytest rerun is required for this documentation-only update."
    Write-Host "The Phase 145 final repository-wide regression already passed:"
    Write-Host "  10303 passed in 2375.31s (0:39:35)"
    Write-Host "=============================================================="
}
finally {
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
