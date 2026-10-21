$ErrorActionPreference = "Stop"
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoDir = Split-Path -Parent $PackageDir
Set-Location $RepoDir
python ".\phase166_close_collection_guard\close.py" --repo "."
$ExitCode = $LASTEXITCODE
if ($ExitCode -ne 0) {
    Write-Host "Phase 166 closure BLOCKED. Inspect the saved pytest_full.log."
}
exit $ExitCode
