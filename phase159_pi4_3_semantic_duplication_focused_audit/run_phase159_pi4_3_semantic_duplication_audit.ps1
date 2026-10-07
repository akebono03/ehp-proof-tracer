$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 159 pi4_3 semantic duplication focused audit"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

python "$ScriptDir\audit_phase159_pi4_3_semantic_duplication.py"

Write-Host ""
Write-Host "Audit output:"
Write-Host "$ScriptDir\phase159_pi4_3_semantic_duplication_audit.txt"
