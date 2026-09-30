$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 R5-43-10 Fixture Breakdown Audit"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "Documentation changes: none"
Write-Host "Full regression: NOT run"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = "$RepoRoot;$RepoRoot\tests"
$env:PYTHONIOENCODING = "utf-8"

try {
    Remove-Item `
      ".\phase150_r5_43_10_fixture_breakdown_audit.txt" `
      -ErrorAction SilentlyContinue

    Write-Host ""
    Write-Host "A. Syntax preflight..."
    python -m py_compile `
      "$ScriptRoot\diagnose_phase150_r5_43_10_fixture_breakdown.py"
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
    Write-Host "Syntax preflight: PASS"

    Write-Host ""
    Write-Host "B. Measuring six targets and four stages..."
    Write-Host "   Each START/END is flushed immediately."
    Write-Host "   If one stage takes several minutes, Ctrl+C is safe;"
    Write-Host "   the completed measurements remain in the output file."
    Write-Host ""

    python `
      "$ScriptRoot\diagnose_phase150_r5_43_10_fixture_breakdown.py"

    $ExitCode = $LASTEXITCODE

    Write-Host ""
    Write-Host "=============================================================="
    Write-Host "Audit exit code: $ExitCode"
    Write-Host "Output: .\phase150_r5_43_10_fixture_breakdown_audit.txt"
    Write-Host "Full regression: NOT run"
    Write-Host "=============================================================="

    exit $ExitCode
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
