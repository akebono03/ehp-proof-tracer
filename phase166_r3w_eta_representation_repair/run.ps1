$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    python ".\phase166_r3w_eta_representation_repair\install.py"
    if ($LASTEXITCODE -ne 0) { throw 'R3-W install failed' }
    python -m pytest -q ".\phase166_r3w_eta_representation_repair\test_r3w.py" ".\phase166_r3v_existing_evidence_bridge\test_r3v.py" ".\phase165_r57_r7_toda45_backward_connection\test_phase165_r57_r7_toda45_backward_connection.py"
    if ($LASTEXITCODE -ne 0) { throw 'R3-W targeted pytest failed' }
    Write-Host 'R3-W targeted PASS; full pytest NOT run.'
} finally { Pop-Location }
