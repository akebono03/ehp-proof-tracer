param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
if (-not (Test-Path (Join-Path $repo '.git'))) { throw 'Run from ehp_proof repository root' }
$source = Join-Path $PSScriptRoot 'audit.py'
$targetDir = Join-Path $repo 'phase175_r4r14r3_binary_composition_audit'
$target = Join-Path $targetDir 'audit.py'
if (-not (Test-Path $target)) { throw 'Extract R4R14R3_binary_composition_audit.zip first' }
$old = 'd98a7b45e08cd3b07c16e3f38e0a558ccebfc9b67a'
$new = 'd98a7b45e08cd3b07c16e3f38e0a558ccebfc9b6'
$existing = [System.IO.File]::ReadAllText($target)
$expected = [System.IO.File]::ReadAllText($source)
if ($existing -ne $expected) {
    if (-not $existing.Contains($old)) { throw 'Unexpected audit script; refusing replacement' }
    if ($existing.Replace($old, $new) -ne $expected) { throw 'Changes beyond reviewed SHA correction; refusing replacement' }
    [System.IO.File]::WriteAllText($target, $expected, (New-Object System.Text.UTF8Encoding($false)))
}
$script = Join-Path $targetDir 'run.ps1'
if ($DryRun) {
    & powershell -NoProfile -ExecutionPolicy Bypass -File $script -DryRun
} else {
    & powershell -NoProfile -ExecutionPolicy Bypass -File $script
}
if ($LASTEXITCODE -ne 0) { throw 'R4R14R3R1 delegated audit failed' }
if ($DryRun) { Write-Output 'PHASE175_R4R14R3R1_GATE=PASS_DRYRUN_PIN_CORRECTED' }
else { Write-Output 'PHASE175_R4R14R3R1_GATE=PASS_FOCUSED_AUDIT_PIN_CORRECTED' }
