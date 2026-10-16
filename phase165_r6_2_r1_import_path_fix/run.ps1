$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$RuleProvider = Join-Path $RepoRoot "phase165_r8_rule_provider.py"
if (-not (Test-Path $RuleProvider)) {
    throw "Required common rule provider is missing: $RuleProvider"
}
$PreviousPythonPath = $env:PYTHONPATH
try {
    if ($PreviousPythonPath) {
        $env:PYTHONPATH = "$RepoRoot$([IO.Path]::PathSeparator)$PSScriptRoot$([IO.Path]::PathSeparator)$PreviousPythonPath"
    } else {
        $env:PYTHONPATH = "$RepoRoot$([IO.Path]::PathSeparator)$PSScriptRoot"
    }
    Set-Location $RepoRoot
    python (Join-Path $PSScriptRoot "audit.py")
    if ($LASTEXITCODE -ne 0) { throw "R6-2 rule audit failed" }
    python -m pytest -q (Join-Path $PSScriptRoot "test_audit.py")
    if ($LASTEXITCODE -ne 0) { throw "R6-2 focused pytest failed" }
    Write-Host "R6-2 R1 rule audit passed. Full pytest NOT run."
} finally {
    $env:PYTHONPATH = $PreviousPythonPath
}
