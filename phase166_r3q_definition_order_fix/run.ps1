$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $root
try {
    python -m phase166_r3q_definition_order_fix.apply
    if ($LASTEXITCODE -ne 0) { throw "Patch application failed" }
    python -m pytest -q phase166_r3q_definition_order_fix/test_phase166_r3q_definition_order_fix.py phase166_r3d_pi32_regression/tests/test_phase166_r3d_pi32_regression.py
    if ($LASTEXITCODE -ne 0) {
        $backup = Get-Content (Join-Path $PSScriptRoot "latest_backup.txt") -Raw
        $backup = $backup.Trim()
        Copy-Item -LiteralPath (Join-Path $backup "phase165_r52_r16_web_citation_gate.py") -Destination (Join-Path $root "phase165_r52_r16_web_citation_gate.py") -Force
        throw "Targeted tests failed; original production module restored from backup."
    }
    Write-Host "R3-Q DEFINITION order check PASS; full pytest NOT run."
} finally {
    Pop-Location
}
