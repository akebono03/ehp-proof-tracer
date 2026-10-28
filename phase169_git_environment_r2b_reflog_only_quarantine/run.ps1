param(
    [ValidateSet("Audit", "Quarantine")]
    [string]$Mode = "Audit",
    [switch]$DropboxPaused,
    [string]$Repository = ""
)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
if ([string]::IsNullOrWhiteSpace($Repository)) {
    $Repository = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
}
$outputRoot = Join-Path $env:LOCALAPPDATA "EHPProofTracerRecovery"
$arguments = @(
    (Join-Path $PSScriptRoot "recover.py"),
    "--root", $Repository,
    "--output-root", $outputRoot,
    "--mode", $Mode.ToLowerInvariant()
)
if ($DropboxPaused.IsPresent) {
    $arguments += "--dropbox-paused"
}
& python @arguments
if ($LASTEXITCODE -ne 0) {
    throw "Git recovery preconditions or checks failed; no blanket deletion performed. Exit=$LASTEXITCODE"
}
Write-Output "GIT_RECOVERY_SCRIPT_EXIT=0"
