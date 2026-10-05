$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "=============================================================="
Write-Host "Phase 158-R4 - 112-group prose formatting / continuity audit"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host "Production code changes: none"
Write-Host "Existing test changes: none"
Write-Host "Full pytest: not run"
Write-Host ""

Push-Location $RepoRoot
try {
    Write-Host "[1/3] Show current git HEAD"
    git rev-parse HEAD
    git log -1 --oneline
    Write-Host ""

    Write-Host "[2/3] Run 112-group audit"
    python "$PackageDir\audit_phase158_r4.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 158-R4 audit failed with exit code $LASTEXITCODE"
    }
    Write-Host ""

    Write-Host "[3/3] Show audit summary"
    Get-Content "$PackageDir\audit_output\summary.txt" -Encoding UTF8
    Write-Host ""
    Write-Host "Detailed findings:"
    Write-Host "  $PackageDir\audit_output\findings.csv"
    Write-Host "Rendered group outputs:"
    Write-Host "  $PackageDir\audit_output\group_outputs"
}
finally {
    Pop-Location
}
