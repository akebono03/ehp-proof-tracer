$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
$originalPackage = Join-Path $root 'phase168_r3_41p10_generic_replay_audit'
$target = Join-Path $originalPackage 'run.ps1'
$replacement = Join-Path $package 'run_FIXED.ps1'
$output = Join-Path $originalPackage 'output'
$backups = Join-Path $output 'backups'

if (-not (Test-Path -LiteralPath $target)) {
    throw ('Original R3-41P10 runner not found: ' + $target)
}
if (-not (Test-Path -LiteralPath $replacement)) {
    throw ('Replacement runner is missing: ' + $replacement)
}

$oldSha = 'cc3c58931338c3d5d6de7deb6f3526ac314fa46cb2d98f3865e4e80d3448d288'
$newSha = '99235e51641fa7cac089e9849119652ecef7c330a49debad7523846c8c429d59'
$currentSha = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash.ToLowerInvariant()
$replacementSha = (Get-FileHash -LiteralPath $replacement -Algorithm SHA256).Hash.ToLowerInvariant()
if ($replacementSha -ne $newSha) {
    throw 'The replacement runner failed checksum validation.'
}
if ($currentSha -eq $newSha) {
    Write-Host 'R3-41P10A runner was already updated; no overwrite required.'
} elseif ($currentSha -eq $oldSha) {
    New-Item -ItemType Directory -Force -Path $backups | Out-Null
    $backup = Join-Path $backups ('run.ps1.before_p10a_' + [guid]::NewGuid().ToString('N'))
    Copy-Item -LiteralPath $target -Destination $backup -ErrorAction Stop
    Copy-Item -LiteralPath $replacement -Destination $target -Force -ErrorAction Stop
    Write-Host ('PATCHED_AUDIT_RUNNER ' + $target)
    Write-Host ('BACKUP ' + $backup)
} else {
    throw ('Unknown R3-41P10 runner checksum; not modified: ' + $currentSha)
}

Write-Host 'Recovering existing results without rerunning the audit or pytest.'
& powershell -ExecutionPolicy Bypass -File $target -BundleOnly
$recoveryExit = $LASTEXITCODE
if ($recoveryExit -ne 0) {
    throw ('Review bundle recovery failed with exit code ' + $recoveryExit)
}
Write-Host 'R3-41P10A_BUNDLE_RECOVERED'
Write-Host 'APPLICATION_SOURCE_UNCHANGED'
Write-Host 'FULL_PYTEST_NOT_RUN'
