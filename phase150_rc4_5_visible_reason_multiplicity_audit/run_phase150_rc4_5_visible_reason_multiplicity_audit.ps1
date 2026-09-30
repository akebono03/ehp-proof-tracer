$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 RC4-5 Visible Reason Multiplicity Audit"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "Documentation changes: none"
Write-Host "Full regression: NOT run"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Output = Join-Path $ScriptRoot "phase150_rc4_5_visible_reason_multiplicity_output.txt"

$env:PYTHONPATH = "$RepoRoot;$RepoRoot\tests"
$env:PYTHONIOENCODING = "utf-8"

try {
    Write-Host ""
    Write-Host "A. Running multiplicity audit for all six RC4-5 targets..."
    python "$ScriptRoot\audit_phase150_rc4_5_visible_reason_multiplicity.py" |
      Tee-Object -FilePath $Output
    $ExitCode = $LASTEXITCODE

    Write-Host ""
    Write-Host "=============================================================="
    Write-Host "Audit exit code: $ExitCode"
    Write-Host "Output: $Output"
    Write-Host "Repository changes: none"
    Write-Host "Full regression: NOT run"
    Write-Host "=============================================================="
    exit $ExitCode
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
