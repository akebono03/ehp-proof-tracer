param(
    [switch]$DryRun,
    [switch]$Apply,
    [string]$ReportDir = ""
)
$ErrorActionPreference = 'Stop'
if ($DryRun -eq $Apply) {
    throw 'Select exactly one of -DryRun or -Apply'
}
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $params = @()
    if ($DryRun) {
        $params += '--dry-run'
    } else {
        $params += '--apply'
    }
    if ($ReportDir -ne '') {
        $params += '--report-dir'
        $params += $ReportDir
    }
    & python -B -m phase172_r6r2_document_closeout.install @params
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 172 document closeout failed with exit code $LASTEXITCODE"
    }
} finally {
    Pop-Location
}
