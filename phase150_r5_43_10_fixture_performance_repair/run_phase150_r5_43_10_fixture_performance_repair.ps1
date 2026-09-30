$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 R5-43-10 Fixture Performance Repair"
Write-Host "Production changes: none"
Write-Host "Changed existing tests: R5-43-10 only"
Write-Host "Documentation changes: none"
Write-Host "Full regression: NOT run"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = "$RepoRoot;$RepoRoot\tests"
$env:PYTHONIOENCODING = "utf-8"

try {
    Write-Host ""
    Write-Host "A. Applying minimal test-fixture repair..."
    python "$ScriptRoot\apply_phase150_r5_43_10_fixture_performance_repair.py"
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host ""
    Write-Host "B. Syntax preflight..."
    python -m py_compile `
      ".\tests\test_phase144_6_r5_43_10_transport_chain_compression_production.py"
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
    Write-Host "Syntax preflight: PASS"

    Write-Host ""
    Write-Host "C. Focused R5-43-10 regression with durations..."
    $Started = Get-Date
    python -m pytest `
      tests/test_phase144_6_r5_43_10_transport_chain_compression_production.py `
      -q `
      --durations=20 `
      --durations-min=0.0
    $ExitCode = $LASTEXITCODE
    $Elapsed = ((Get-Date) - $Started).TotalSeconds

    Write-Host ""
    Write-Host "Focused elapsed: $([math]::Round($Elapsed, 2))s"
    Write-Host "=============================================================="
    Write-Host "Focused pytest exit code: $ExitCode"
    Write-Host "Full regression: NOT run"
    Write-Host "=============================================================="

    exit $ExitCode
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
