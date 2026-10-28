param(
    [string]$Repository = ""
)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
if ([string]::IsNullOrWhiteSpace($Repository)) {
    $Repository = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
}
$stamp = Get-Date -Format "yyyyMMdd_HHmmss_fff"
$output = Join-Path ([System.IO.Path]::GetTempPath()) ("ehp_git_environment_audit_" + $stamp)
Write-Output "GIT_ENV_REPOSITORY=$Repository"
Write-Output "GIT_ENV_OUTPUT_OUTSIDE_REPOSITORY=$output"
& python (Join-Path $PSScriptRoot "audit.py") --root "$Repository" --output "$output"
if ($LASTEXITCODE -ne 0) {
    throw "Read-only audit failed with exit $LASTEXITCODE"
}
Write-Output "GIT_ENV_AUDIT_COMPLETE=PASS"
