$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
if (-not (Test-Path (Join-Path $root 'phase165_r55_nk_only_goal.py'))) {
    throw 'Expected ehp_proof repository root next to audit directory.'
}
Push-Location $root
try {
    python -m phase166_r3q_reference_audit_runner_fix.audit
    if ($LASTEXITCODE -ne 0) {
        throw 'R3-Q read-only audit failed.'
    }
    Write-Host 'Read-only R3-Q audit completed; full pytest NOT run.'
}
finally {
    Pop-Location
}
