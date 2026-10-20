$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    python -m phase166_r3w_transport_diagnostic.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3-W diagnostic failed' }
    python -m pytest -q .\phase166_r3v_existing_evidence_bridge\test_r3v.py .\phase166_r3v_gate_repair\test_gate.py
    if ($LASTEXITCODE -ne 0) { throw 'R3-W related targeted tests failed' }
    Write-Host 'R3-W read-only diagnosis finished; full pytest NOT run.'
} finally {
    Pop-Location
}
