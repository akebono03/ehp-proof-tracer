$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 Stall Root-Cause Audit R5-43-10"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "Documentation changes: none"
Write-Host "Full regression: NOT run"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$TestFile = "tests/test_phase144_6_r5_43_10_transport_chain_compression_production.py"
$Target = "${TestFile}::test_phase144_6_r5_43_10_pi6_transport_connector_is_rendered_between_c2_and_c3"
$Output = Join-Path $RepoRoot "phase150_stall_root_cause_audit_r5_43_10.txt"

$env:PYTHONPATH = "$RepoRoot;$RepoRoot\tests"
$env:PYTHONIOENCODING = "utf-8"

function Run-Case {
    param(
        [string]$Label,
        [string[]]$PytestArgs
    )

    Write-Host ""
    Write-Host "--------------------------------------------------------------"
    Write-Host $Label
    Write-Host "--------------------------------------------------------------"

    $Started = Get-Date
    & python -m pytest @PytestArgs 2>&1 | Tee-Object -FilePath $Output -Append
    $ExitCode = $LASTEXITCODE
    $Elapsed = ((Get-Date) - $Started).TotalSeconds

    "CASE_RESULT label=$Label exit=$ExitCode elapsed=$([math]::Round($Elapsed, 2))s" |
        Tee-Object -FilePath $Output -Append |
        Write-Host

    if ($ExitCode -ne 0) {
        throw "Audit case failed: $Label"
    }
}

try {
    Remove-Item $Output -ErrorAction SilentlyContinue

    "Phase 150 Stall Root-Cause Audit R5-43-10" |
        Set-Content -Path $Output -Encoding UTF8

    Write-Host ""
    Write-Host "A. Target test alone (fresh pytest process)..."
    Run-Case `
        -Label "A_TARGET_ALONE" `
        -PytestArgs @(
            $Target,
            "-vv",
            "--setup-show",
            "--durations=10",
            "--durations-min=0.0"
        )

    Write-Host ""
    Write-Host "B. Whole R5-43-10 file (fresh pytest process)..."
    Run-Case `
        -Label "B_WHOLE_FILE" `
        -PytestArgs @(
            $TestFile,
            "-vv",
            "--setup-show",
            "--durations=20",
            "--durations-min=0.0"
        )

    Write-Host ""
    Write-Host "C. Immediate predecessor R5-42 plus R5-43-10 (same pytest process)..."
    Run-Case `
        -Label "C_R5_42_THROUGH_R5_43_10" `
        -PytestArgs @(
            "tests/test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py",
            $TestFile,
            "-vv",
            "--setup-show",
            "--durations=30",
            "--durations-min=0.0"
        )

    Write-Host ""
    Write-Host "D. Phase144-6 R5-43 prefix through R5-43-10 (same pytest process)..."
    Run-Case `
        -Label "D_R5_43_PREFIX" `
        -PytestArgs @(
            "tests/test_phase144_6_r5_43_1.py",
            "tests/test_phase144_6_r5_43_2.py",
            "tests/test_phase144_6_r5_43_3.py",
            "tests/test_phase144_6_r5_43_4.py",
            "tests/test_phase144_6_r5_43_5.py",
            "tests/test_phase144_6_r5_43_6.py",
            "tests/test_phase144_6_r5_43_7.py",
            "tests/test_phase144_6_r5_43_8.py",
            "tests/test_phase144_6_r5_43_9.py",
            $TestFile,
            "-vv",
            "--setup-show",
            "--durations=40",
            "--durations-min=0.0"
        )

    Write-Host ""
    Write-Host "=============================================================="
    Write-Host "Audit completed."
    Write-Host "Output: .\phase150_stall_root_cause_audit_r5_43_10.txt"
    Write-Host "Full regression: NOT run"
    Write-Host "=============================================================="
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
