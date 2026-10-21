$ErrorActionPreference = 'Stop'
$RepoRoot = (Get-Location).Path
$AuditDir = $PSScriptRoot
if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 "$AuditDir\audit.py" "$RepoRoot"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    & python "$AuditDir\audit.py" "$RepoRoot"
} else {
    throw 'Python 3 is required. Install Python or run on a machine with Python 3.'
}
if ($LASTEXITCODE -ne 0) { throw "Audit failed (exit $LASTEXITCODE)" }
